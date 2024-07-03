from project_data_load import load_data, preprocess_data, process_outliers, process_data
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np
import pandas as pd


df_cleaned, df_replaced, df_pivot = process_data()
col_list = ['totalMinutes', 'videoDays', 'videoLikeCnt', 'videoCommentCnt', 'videoViewCnt']


## 랜덤 포레스트

df = df_replaced[col_list]

# 데이터 스케일링: 전체 데이터 변환 후 학습, 테스트 데이터로 분리
scaler = StandardScaler()
scaled = scaler.fit_transform(df)
scaled_df = pd.DataFrame(data=scaled, columns=df.columns)

# 독립, 종속 변수 분리
X = scaled_df.iloc[:, :4]
y = scaled_df['videoViewCnt']

# 학습, 테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 랜덤 포레스트 모델
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# 예측
y_pred = model.predict(X_test)

# 모델 평가
# 결정계수: 모델이 데이터를 얼마나 예측하는지에 대한 지표, 1에 가까울수록 좋음
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

print(f"R-squared : {r2}")
print(f"Mean Squared Error: {mse}")
print(f"Root Mean Squared Error: {rmse}")


## Grid Search
params = {'n_estimators': [10, 50, 100, 200], # 결정 트리 갯수
          'max_depth': [8, 16, 24], # 트리 최대 깊이
          'min_samples_leaf': [1, 6, 12], # 리프 노드에 필요한 최소 샘플 수
          'min_samples_split': [2, 8, 16] # 내부 노드 분할에 필요한 최소 샘플 수
          }

grid_search = GridSearchCV(estimator=model, param_grid=params,
                           scoring='neg_mean_squared_error', cv=10, verbose=1, n_jobs=-1)
grid_search.fit(X_train, y_train)

# print('Best parameters: ', grid_search.best_params_)
# print('Best Scroe: ', -grid_search.best_score_)

# 최적의 모델 선택 및 평가
best_model = grid_search.best_estimator_
best_y_pred = best_model.predict(X_test)

# 모델 평가
best_r2 = r2_score(y_test, best_y_pred)
best_mse = mean_squared_error(y_test, best_y_pred)
best_rmse = np.sqrt(best_mse)

print(f"Best model R-squared : {best_r2}")
print(f"Best model Mean Squared Error: {best_mse}")
print(f"Best model Root Mean Squared Error: {best_rmse}")

# 피처 중요도
ftr_importances_values = model.feature_importances_
ftr_importances = pd.Series(ftr_importances_values, index=X.columns)


### 시각화
plt.figure(figsize=(13, 8))
plt.grid(True, linestyle='--', alpha=0.5)
sns.barplot(x=ftr_importances, y=ftr_importances.index, palette='PuBuGn', hue=ftr_importances.index)
plt.title(f'Feature Importances')
plt.xlabel('Importance')
plt.ylabel('')
plt.xlim(0, 1)
plt.savefig('ftr_importances')
plt.show()


##

