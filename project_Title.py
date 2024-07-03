## csv 불러들이기
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords, words
from nltk.tokenize import word_tokenize
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import random
from nltk.util import ngrams
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('words')

df_pre = pd.read_csv('lofi_data.csv', encoding='utf-8', index_col=0)

###### 텍스트 분석 ######
# [동영상 제목]
# videoTitle 전처리
# 영어만 추출(이모티콘, 숫자 및 부호 삭제)
# 영어 한글자인 단어 삭제
# 소문자
df_pre['pre_videoTitle'] = df_pre['videoTitle'].str.lower()

## / 대체
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('/', ' ')
#  ^: not, \s: 공백문자, \b: 문자 경계 (한글 제거)
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('[^a-z\s]', ' ', regex=True)

##
# 빈도수가 많은 word로 변경
# hip hop, lo fi -> 공백제거,
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('hip hop', 'hiphop')
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('lo fi', 'lofi')

# amp삭제
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace(r'\bamp\b', '', regex=True)


# slow->slowed,
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('slowed', 'slow')
# df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('sloweded', 'slow')

# beats, beatss->beat,
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('beats', 'beat')
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('beatss', 'beat')

# songs->song,
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('songs', 'song')
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('sang', 'song')

# ver, versionsion ->version,
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('ver', 'version')
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('versionsion', 'version')

# relaxing, relaxation->relax,
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('relaxing', 'relax')
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('relaxation', 'relax')

# raining, rain->rainy
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('raining', 'rainy')
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('rain', 'rainy')
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('rainyy', 'rainy')

# lofimusic-> lofi, music분리, (그룹화), r'\1: 1그룹 참조, \2: 2그룹 참조'
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace(r'(lofi)(music)', r'\1, \2', regex=True)

# jazzhop, jazzy -> jazz,
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('jazzhop', 'jazz')
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('jazzy', 'jazz')


# hours->hour
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('hours', 'hour')

# reverbed, reversionb ->reverb
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('reverbed', 'reverb')
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('reversionb', 'reverb')

# lyric, lyrical, lyricsal, audiolyric->lyrics,
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('lyrics', 'lyric')
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('lyrical', 'lyric')
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('lyricsal', 'lyric')
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('audiolyric', 'lyric')

# ft->feat
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('ft', 'feat')

# chillout, chilllhop->chill
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('chillout', 'chill')
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('chillhop', 'chill')

# asthetic-> aesthetic
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('asthetic', 'aesthetic')

# synthwave
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('synthwave', 'synthesizer')


# mash, mashupup-> mashup
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('mash', 'mashup')
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('mashupup', 'mashup')

# sounds  -> sound
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('sounds', 'sound')

# dreams -> dream
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('dreams', 'dream')

# oceans-> ocean
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('oceans', 'ocean')

# headphones -> headphone
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('headphones', 'headphone')

# instra->instagram
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('insta', 'instagram')
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('instagramgram', 'instagram')

# slowandreverb
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace(r'(slow)(and)(reverb)', r'\1, \2, \3', regex=True)

# peace, peacefulful -> peaceful
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('peace', 'peaceful')
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('peacefulful', 'peaceful')

# trending-> trend
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('trending', 'trend')

# sleeping -> sleep
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace('sleeping', 'sleep')

# altamashup-> mashup
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace(r'(alta)(mashup)', r'\1, \2', regex=True)

# lofibhajans-> lofi
df_pre['pre_videoTitle'] = df_pre['pre_videoTitle'].str.replace(r'(lofi)(bhajans)', r'\1, \2', regex=True)


## 모든 제목 결합
titles = ' '.join(df_pre['pre_videoTitle'])

eng_titles = ' '.join(re.findall(r'[a-zA-Z]+', titles))

# 영어 토큰화, 불용어 제거
# word_tokenize : 문자열을 단어 단위로 구분
eng_tokens = word_tokenize(eng_titles.lower())
# word.isalnum() : 알파벳, 숫자만 포함 (특수문자, 기호 제외)
# 영어는 nltk 라이브러리가 기본적으로 제공하는 불용어 리스트 존재
# stopwords.words('english') : 분석에 의미 없는 관사 등을 의미
eng_filtered_tokens = [word for word in eng_tokens if word.isalnum() and word not in stopwords.words('english')]

# 단어 빈도
eng_freq =Counter(eng_filtered_tokens)

# most_common() : Counter클래스 제공, 내림차순 정렬
eng_rank = eng_freq.most_common()

# list to df
eng_df = pd.DataFrame(eng_rank).rename(columns={0:'word', 1:'count'})


## word 값이 영문 2개 이하 제거(영어 스펠링 1개인 것 제거)
eng_df = eng_df.loc[eng_df['word'].str.len() > 2]

# 영어 단어만 식별
eng_words = set(words.words())
eng_df['is_meaningful'] = eng_df['word'].apply(lambda x: x in eng_words)

eng_df = eng_df.reset_index(drop=True)

# false 포함
eng_false = eng_df.loc[eng_df['is_meaningful'] == False].reset_index(drop=True)
false_index = [0, 1, 2, 7, 9, 34, 39, 55]
eng_false = eng_false.iloc[false_index].reset_index(drop=True)


# true 제외
eng_true = eng_df.loc[eng_df['is_meaningful'] == True].reset_index(drop=True)
true_index = [15, 38, 44, 45, 47, 48, 53, 55, 63, 82, 87, 89, 91, 92, 96]
eng_true = eng_true.iloc[~eng_true.index.isin(true_index)].reset_index(drop=True)


# 결합(빈도)_정리 완료
df_frequency = pd.concat([eng_true, eng_false]).reset_index(drop=True)
df_frequency = df_frequency.sort_values('count', ascending=False).reset_index(drop=True)


## total count
df_frequency['count'].sum()


## 워드클라우드
# df to dict
df = df_frequency.iloc[:, :2]

word_count_dict = {}
for index, row in df_frequency.iterrows():
    word_count_dict[row['word']] = row['count']

text = ' '.join([(word+' ')*count for word, count in word_count_dict.items()])
text_list = text.split()
random.shuffle(text_list)
shuffle_text = ' '.join(text_list)

wc = WordCloud(width=800, height=400, background_color='white').generate(shuffle_text)

plt.figure(figsize=(15, 10))
# 이미지 화면에 표시
plt.imshow(wc)
plt.axis('off')
plt.savefig('Wordcloud.png')
plt.show()


## N-그램 분석
def filter_title(title, words):
    pattern = r'\b(' + '|'.join(words) + r')\b'
    matches = re.findall(pattern, title, flags=re.IGNORECASE)
    return ' '.join(matches)

words = df['word'].tolist()
df_pre['pre_keywords'] = df_pre['pre_videoTitle'].apply(lambda x: filter_title(x, words))

all_words = ' '.join(df_pre['pre_keywords'])
words_tokens = nltk.word_tokenize(all_words)

# 2, 3그램 생성
bigrams = list(ngrams(words_tokens, 2))
trigrams = list(ngrams(words_tokens, 3))

# 빈도
fre_bigrams = Counter(bigrams)
fre_trigrams = Counter(trigrams)

# 상위 그램 추출
top_bigrams = fre_bigrams.most_common(20)
top_trigrams = fre_trigrams.most_common(20)


# 시각화
def draw_barplots(bigrams, trigrams):
    plt.figure(figsize=(20, 10))
    plt.subplot(1, 2, 1)
    labels, values = zip(*bigrams)
    labels = [' '.join(label) for label in labels]
    sns.barplot(x=values, y=labels, color='skyblue')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.title('Top 20 of Bigrams')
    plt.xlim(0, 19)
    plt.xlabel('Count')

    plt.subplot(1, 2, 2)
    labels, values = zip(*trigrams)
    labels = [' '.join(label) for label in labels]
    sns.barplot(x=values, y=labels, color='skyblue')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.title('Top 20 of Trigrams')
    plt.xlim(0, 9)
    plt.xlabel('Count')

    plt.tight_layout()
    plt.savefig('grams_barplot.png')
    plt.show()


draw_barplots(top_bigrams, top_trigrams)


##

