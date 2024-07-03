from project_data_load import load_data, preprocess_data, process_outliers, process_data
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from sklearn.preprocessing import StandardScaler

df_cleaned, df_replaced, df_pivot = process_data()
col_list = ['totalMinutes', 'videoDays', 'videoLikeCnt', 'videoCommentCnt', 'videoViewCnt']


## 정규성 검정 (shapiro-wilk, Q-Q plot)
def sharpiro_wilk(df, column_list):
    for col in column_list:
        # 샤피로-윌크 검정
        shapiro_test = stats.shapiro(df[col])
        print(f"Test for {col}: \n Statistic: {shapiro_test.statistic}, p-value: {shapiro_test.pvalue}")

        # 귀무가설: 정규분포이다, 대립가설: 정규분포가 아니다.
        print(f"\n결과 해석: ")
        if shapiro_test.pvalue > 0.05:
            print(f"p-value가 0.05보다 크므로 {col} 데이터는 정규분포를 따른다.\n")
            print('=========================================================================')

        else:
            print(f"p-value가 0.05보다 작으므로 {col} 데이터는 정규분포를 따르지 않는다.\n")
            print('=========================================================================')


sharpiro_wilk(df_replaced, col_list)

## Q-Q plot (표준화)
# 데이터 표준화
scaler = StandardScaler()
x_data_scaled = scaler.fit_transform(df_replaced[col_list])
x_data_scaled = pd.DataFrame(x_data_scaled, columns=col_list)

def make_qqplot(df, column_list):
    for col in column_list:
        plt.figure(figsize=(12, 8))
        plt.grid(True, linestyle='--', alpha=0.5)
        stats.probplot(df[col], dist=stats.norm, plot=plt)
        plt.title(f'Q-Q plot of {col}')
        plt.ylim(-3, 6)
        plt.savefig(f'Q-Q_{col}.png')
        plt.show()

make_qqplot(x_data_scaled, col_list)


## 상관분석: 회귀분석을 위한 전초전, 선형성 확인 후 실시
# 연속변수로 측정된 두 변수간의 선형관계를 분석하는 기법
# 두 변수 모두 정규성을 만족하지 못할 때, 비모수 검정 (스피어만 서열상관분석)
def calculate_spearman_corr(df, column_list, target):
    # 귀무가설: 상관계수가 0이다 (상관관계가 없다), 대립가설: 상관계수가 0이 아니다 (상관관계가 있다)
    for col in column_list:
        if col != target:
            spearman_corr, spearman_pvalue = stats.spearmanr(df[col], df[target])

            print(f"\n결과 해석: {col}과 {target}")
            print(f'스피어만 상관계수: {spearman_corr}')
            print(f'p-value: {spearman_pvalue}')
            if spearman_pvalue > 0.05:
                print(f"{col}, {target}의 p-value가 0.05보다 크므로 두 변수 간에 유의미한 상관 관계가 없다.")
            else:
                print(f"{col}와 {target}의 p-value가 0.05보다 작으므로 두 변수 간에 유의미한 상관 관계가 있다.")

calculate_spearman_corr(df_replaced, col_list, 'videoViewCnt')

##

