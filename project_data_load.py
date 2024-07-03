import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
import re
from scipy import stats
from scipy.stats import skew, kurtosis

def load_data():
    df = pd.read_csv('lofi_data.csv', encoding='utf-8', index_col=0)
    return df

def preprocess_data(df):
    df_none = df.loc[df['videoDuration'] != 'live']

    # 동영상 재생 시간을 분 단위로 변경
    pattern = re.compile(r'((\d+H)?(\d+M)?(\d+S)?)')

    def get_total_minutes(series):
        match = pattern.match(series)

        if match:
            hours = int(match.group(2)[:-1] if match.group(2) else 0)
            minutes = int(match.group(3)[:-1] if match.group(3) else 0)
            seconds = int(match.group(4)[:-1] if match.group(4) else 0)
            total_minutes = round((hours * 60) + minutes + (seconds / 60), 1)
            return total_minutes
        else:
            return None

    df['totalMinutes'] = df_none['videoDuration'].astype(str).apply(get_total_minutes)

    # 영상 생성 일자
    specific_date = datetime(2024, 6, 12, 0, 0, tzinfo=ZoneInfo('Asia/Seoul'))
    df['videoPublishTime'] = pd.to_datetime(df['videoPublishTime'])
    df['videoDays'] = (specific_date - df['videoPublishTime']).dt.days

    # 라이브, 좋아요 0 데이터 제거
    df_cleaned = df.loc[(df['videoLikeCnt'] != 0) & (df['videoDuration'] != 'live')].reset_index(drop=True)

    return df_cleaned

def process_outliers(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - IQR * 1.5
    upper_bound = Q3 + IQR * 1.5

    outliers = (df[col] < lower_bound) | (df[col] > upper_bound)

    # original data
    original_stats = df[col].describe().to_dict()
    original_stats.update({
        'skew': skew(df[col]),
        'kurtosis': kurtosis(df[col]),
        'outliers_count': outliers.sum()
    })

    # removed data
    df_removed = df.loc[~outliers]
    removed_stats = df_removed[col].describe().to_dict()
    removed_stats.update({
        'skew': skew(df_removed[col]),
        'kurtosis': kurtosis(df_removed[col]),
        'outliers_count': len(df) - len(df_removed)
    })

    # replaced data
    df_replaced = df.copy()
    df_replaced[col] = df_replaced[col].astype(float)
    df_replaced.loc[df_replaced[col] < lower_bound, col] = lower_bound
    df_replaced.loc[df_replaced[col] > upper_bound, col] = upper_bound
    replaced_stats = df_replaced[col].describe().to_dict()
    replaced_stats.update({
        'skew': skew(df_replaced[col]),
        'kurtosis': kurtosis(df_replaced[col]),
        'outliers_count': outliers.sum()
    })

    # 평균, 중앙값, 표준편차 변화율
    original_mean = original_stats['mean']
    original_median = original_stats['50%']
    original_std = original_stats['std']

    removed_mean = removed_stats['mean']
    removed_median = removed_stats['50%']
    removed_std = removed_stats['std']

    replaced_mean = replaced_stats['mean']
    replaced_median = replaced_stats['50%']
    replaced_std = replaced_stats['std']

    removed_stats['mean_change_rate'] = ((removed_mean - original_mean) / original_mean) * 100
    removed_stats['median_change_rate'] = ((removed_median - original_median) / original_median) * 100
    removed_stats['std_change_rate'] = ((removed_std - original_std) / original_std) * 100

    replaced_stats['mean_change_rate'] = ((replaced_mean - original_mean) / original_mean) * 100
    replaced_stats['median_change_rate'] = ((replaced_median - original_median) / original_median) * 100
    replaced_stats['std_change_rate'] = ((replaced_std - original_std) / original_std) * 100

    return original_stats, removed_stats, replaced_stats, df_replaced


def process_data():
    df_pre = load_data()
    df_cleaned = preprocess_data(df_pre)

    col_list = ['totalMinutes', 'videoDays', 'videoLikeCnt', 'videoCommentCnt', 'videoViewCnt']

    # 최종 df_replaced 생성
    df_replaced = df_cleaned.copy()
    results = []

    for col in col_list:
        original_stats, removed_stats, replaced_stats, df_replaced_col = process_outliers(df_cleaned, col)

        # 결과값 df_replaced 반영
        df_replaced[col] = df_replaced_col[col]

        for key in original_stats.keys():
            results.append({
                'column': col,
                'type': 'original',
                'key': key,
                'value': original_stats[key]
            })
        for key in removed_stats.keys():
            results.append({
                'column': col,
                'type': 'removed',
                'key': key,
                'value': removed_stats[key]
            })
        for key in replaced_stats.keys():
            results.append({
                'column': col,
                'type': 'replaced',
                'key': key,
                'value': replaced_stats[key]
            })

    # list to dataframe
    df_result = pd.DataFrame(results)

    df_pivot = df_result.pivot_table(index=['column', 'type'], columns='key', values='value')
    df_pivot = df_pivot.reset_index()
    df_pivot = df_pivot[['column', 'type', 'count', '25%', '50%', '75%', 'std',
                         'mean', 'max', 'min', 'outliers_count', 'kurtosis', 'skew',
                         'mean_change_rate', 'median_change_rate', 'std_change_rate']]

    return df_cleaned, df_replaced, df_pivot
