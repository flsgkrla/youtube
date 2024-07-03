import pandas as pd
from PIL import Image
from io import BytesIO
import requests
import os
import json
import glob
import matplotlib.pyplot as plt
import seaborn as sns

df_pre = pd.read_csv('lofi_data.csv', encoding='utf-8', index_col=0)

# 원본
df_obj = df_raw.copy()

df_obj_cnt = df_obj['class'].value_counts().reset_index(name='count')
df_obj_gb = df_obj.groupby('name')['class'].count().sort_values(ascending=False).reset_index(name='count')

# 개별 이미지에서 탐지된 객체 평균 개수
df_obj_gb['count'].mean()

# 전체 confidence 평균
df_obj['confidence'].mean()

# 개별 이미지 confidence 평균
df_obj.groupby('name')['confidence'].mean().sort_values(ascending=False).reset_index(name='mean')


# 필터링
# confidence 0.7 이상
df_conf = df_obj.loc[df_obj['confidence'] >= 0.7].reset_index(drop=True)
df_conf_cnt = df_conf['class'].value_counts().reset_index(name='count')
df_conf_gb = df_conf.groupby('name')['class'].count().sort_values(ascending=False).reset_index(name='count')


#
df_conf_gb['count'].mean()
df_conf['confidence'].mean()
df_conf.groupby('name')['confidence'].mean().sort_values(ascending=False).reset_index(name='mean')



## class별 개수 시각화
def class_barplot(df, filename):
    plt.figure(figsize=(15, 10))
    sns.barplot(x='class', y='count', data=df, hue='class', palette='PuBuGn', legend=False)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.title('Number of Object Detections')
    plt.xlabel('')
    plt.xticks(rotation=45)
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig(f'detected_{filename}.png')
    plt.show()

class_barplot(df_obj_cnt, 'raw')
class_barplot(df_conf_cnt, 'filtered')
