from project_data_load import load_data, preprocess_data, process_outliers, process_data
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
import pandas as pd
import datetime

df_cleaned, df_replaced, df_pivot = process_data()
col_list = ['totalMinutes', 'videoDays', 'videoLikeCnt', 'videoCommentCnt', 'videoViewCnt']

## 기술통계
df_filter = df_pivot.loc[df_pivot['type'] == 'replaced'].reset_index(drop=True)
# view = df_filter.loc[df_filter['column'] == 'videoCommentCnt']
# view['75%']-view['25%']

## 박스 플롯 (변수 1개)
def make_boxplot(df, column_list):
    for col in column_list:
        sns.set_style("whitegrid", {"grid.linestyle": "--"})
        plt.figure(figsize=(8, 6))
        if (col == 'totalMinutes') | (col == 'videoDays') | (col == 'videoCommentCnt'):
            formatter = ticker.FuncFormatter(lambda y, _: f'{int(y):,.0f}')
        elif col == 'videoViewCnt':
            formatter = ticker.FuncFormatter(lambda y, _: f'{int(y/1000000):,.0f}M')
        else:
            formatter = ticker.FuncFormatter(lambda y, _: f'{int(y/1000):,.0f}K')

        plt.gca().yaxis.set_major_formatter(formatter)
        sns.boxplot(df[col], color="skyblue")
        plt.title(f'Boxplot of {col}')
        plt.ylim(min(df[col]), max(df[col]))
        plt.ylabel(f'{col}')
        plt.savefig(f'{col}_boxplot.png')
        plt.show()


make_boxplot(df_replaced, col_list)


## 히스토그램 (수치형 변수, 변수 1개)
def make_hist(df, column_list):
    for col in column_list:
        n = len(df[col])
        bins = int(np.ceil(np.log2(n)+1))

        plt.figure(figsize=(12, 6))
        sns.histplot(df[col], bins=bins, kde=False, color='skyblue', edgecolor='whitesmoke', linewidth=1.4)
        if (col == 'totalMinutes') | (col == 'videoDays') | (col == 'videoCommentCnt'):
            formatter = ticker.FuncFormatter(lambda x, _: f'{int(x):,.0f}')
        elif col == 'videoViewCnt':
            formatter = ticker.FuncFormatter(lambda x, _: f'{int(x/1000000):,.0f}M')
        else:
            formatter = ticker.FuncFormatter(lambda x, _: f'{int(x/1000):,.0f}K')

        # x축 단위 설정
        plt.gca().xaxis.set_major_formatter(formatter)

        # 그리드 추가
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.title(f'Histogram of {col}')
        plt.xlim(min(df[col]), max(df[col]))
        plt.ylim(0, 50)
        plt.xlabel(f'{col}')
        plt.ylabel('Frequency')
        plt.savefig(f'{col}_hist.png')
        plt.show()


make_hist(df_replaced, col_list)


## 히트맵_상관분석 (수치형 변수, 변수 2개)
def make_heatmap(df, column_list):
    correlation_matrix = df[column_list].corr()

    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True,
                linewidths=1.4, cbar=True,
                cmap='Blues', fmt='.1f')
    plt.title('Correlation Heatmap')
    plt.savefig(f'Correlation_Heatmap.png')
    plt.show()


make_heatmap(df_replaced, col_list)


## 산점도 (연속형+연속형 선호, 변수 2개)
def make_scatter(df, column_list):
    target = 'videoViewCnt'
    for col in column_list:
        if col != target:
            plt.figure(figsize=(12, 6))
            sns.scatterplot(x=df[col], y=df[target], color='skyblue')

            # 기본
            # x축 단위 설정
            # ticker.FuncFormatter(형식 지정, 눈금 위치), 소수점 이하 0자리까지 표시(=정수)
            plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):.0f}'))
            # y축 단위 설정
            plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{int(y):,.0f}'))
            plt.title(f'Scatter of {col} and {target}')
            plt.xlabel(f'{col}')
            plt.ylabel(f'{target}')
            plt.savefig(f'{target}_{col}_scatter.png')
            plt.show()


make_scatter(df_replaced, col_list)


## 영상 생성 일자(barplot)
df_replaced['videoPublishTime'] = pd.to_datetime(df_replaced['videoPublishTime'])
def make_bar(df, column):
    if column == 'videoPublishYear':
        df[column] = df['videoPublishTime'].dt.year
    elif column == 'videoPublishMonth':
        df[column] = df['videoPublishTime'].dt.month

    uploads = df.groupby(column).size().reset_index(name='count')

    # barplot
    plt.figure(figsize=(12, 6))
    sns.barplot(x=column, y='count', data=uploads, hue=column, palette='PuBuGn', legend=False)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.title(f'{column.replace("videoPublish", "").capitalize()}ly Uploads of Lofi Videos')
    plt.xlabel(f'{column.replace("videoPublish", "").capitalize()}')
    plt.ylabel('Number of Videos')
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f'{int(y)}'))
    plt.savefig(f'video{column.replace("videoPublish", "").capitalize()}_bar.png')
    plt.show()


# 연도별 그래프
make_bar(df_replaced, "videoPublishYear")

# 월별 그래프
make_bar(df_replaced, "videoPublishMonth")


##

