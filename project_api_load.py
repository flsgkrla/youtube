###### 데이터 수집 ######
import pandas as pd
from googleapiclient.discovery import build

API_KEY = 'AIzaSyDV5sK3M8AQk7b3yBiw255akoktPPm84Xs'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_SERVICE_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_SERVICE_VERSION, developerKey=API_KEY)

# searchList (영상 조회)
def search_list(query, order, max_results):
    search_videoId = []
    search_channelId = []
    search_title = []
    search_description = []
    search_imageUrl = []
    search_channelTitle = []
    search_liveBroadcastContent = []
    search_publishTime = []
    orders = []
    queries = []

    search_request = youtube.search().list(
        part="snippet",
        order=order,
        q=query,
        maxResults=max_results
    )
    response = search_request.execute()

    for item in response.get('items', []):
        videoId = item.get('id', {}).get('videoId')
        if not videoId:
            continue
        channelId = item.get('snippet', {}).get('channelId', "0")
        title = item.get('snippet', {}).get('title', "0")
        description = item.get('snippet', {}).get('description', "0")
        imageUrl = item.get('snippet', {}).get('thumbnails', {}).get('high', {}).get('url', "0")
        channelTitle = item.get('snippet', {}).get('channelTitle', "0")
        liveBroadcastContent = item.get('snippet', {}).get('liveBroadcastContent', "0")
        publishTime = item.get('snippet', {}).get('publishTime', "0")

        # videoId = item['id']['videoId']
        # channelId = item['snippet']['channelId']
        # title = item['snippet']['title']
        # description = item['snippet']['description']
        # imageUrl = item['snippet']['thumbnails']['high']['url']
        # channelTitle = item['snippet']['channelTitle']
        # liveBroadcastContent = item['snippet']['liveBroadcastContent']
        # publishTime = item['snippet']['publishTime']


        search_videoId.append(videoId)
        search_channelId.append(channelId)
        search_title.append(title)
        search_description.append(description)
        search_imageUrl.append(imageUrl)
        search_channelTitle.append(channelTitle)
        search_liveBroadcastContent.append(liveBroadcastContent)
        search_publishTime.append(publishTime)
        orders.append(order)
        queries.append(query)



    df = pd.DataFrame({
        'videoId': search_videoId,
        'channelId': search_channelId,
        'videoTitle': search_title,
        'videoDescription': search_description,
        'imageUrl': search_imageUrl,
        'channelTitle': search_channelTitle,
        'liveBroadcastContent': search_liveBroadcastContent,
        'videoPublishTime': search_publishTime,
        'order': orders,
        'query': queries
    })


    # object to datetime
    df['videoPublishTime'] = pd.to_datetime(df['videoPublishTime'])
    # timezone
    df['videoPublishTime'] = df['videoPublishTime'].dt.tz_convert('Asia/Seoul')

    return df


queries = ["lofi", "LOFI", "Lofi", "LoFi", "lo-fi", "LO-FI", "Lo-fi", "Lo-Fi"]
df_search = pd.concat(
    [search_list(query, "viewCount", 50) for query in queries],
    ignore_index=True
)


## videoList (영상 추가 정보)
def videos_list(max_results):
    videos_videoId = []
    videos_viewCount = []
    videos_likeCount = []
    videos_commentCount = []
    videos_duration = []

    id_lists = df_search['videoId']
    for id in id_lists:

        videos_request = youtube.videos().list(
            part="statistics, contentDetails",
            id=id,
            maxResults=max_results
        )
        response = videos_request.execute()

        for item in response.get('items', []):
            videoId = item.get('id', "0")
            viewCount = item.get('statistics', {}).get('viewCount', "0")
            likeCount = item.get('statistics', {}).get('likeCount', "0")
            commentCount = item.get('statistics', {}).get('commentCount', "0")
            duration = item.get('contentDetails', {}).get('duration', "0")

            # videoId = item['id']
            # viewCount = item['statistics']['viewCount']
            # likeCount = item['statistics'].get('likeCount', "0")
            # commentCount = item['statistics']['commentCount']
            # duration = item['contentDetails']['duration']


            videos_videoId.append(videoId)
            videos_viewCount.append(viewCount)
            videos_likeCount.append(likeCount)
            videos_commentCount.append(commentCount)
            videos_duration.append(duration)

    df_videos = pd.DataFrame({
        'videoId': videos_videoId,
        'videoViewCnt': videos_viewCount,
        'videoLikeCnt': videos_likeCount,
        'videoCommentCnt': videos_commentCount,
        'videoDuration': videos_duration
    })

    return df_videos

# df_search_video = pd.merge(df_search, videos_list(50), on='videoId', how='inner')
df_search_video = pd.concat([df_search, videos_list(50)], axis=1)



## channel_list (채널 정보)

def channels_list(max_results):
    channels_description = []
    channels_publishedAt = []
    channels_viewCount = []
    channels_subscriberCount = []
    channels_videoCount = []


    id_lists = df_search_video['channelId']
    for id in id_lists:
        videos_request = youtube.channels().list(
            part="snippet, statistics",
            id=id,
            maxResults=max_results
        )
        response = videos_request.execute()

        for item in response.get('items', []):
            channelDesc = item.get('snippet', {}).get('description', "0")
            channelPub = item.get('snippet', {}).get('publishedAt', "0")
            channelViewCnt = item.get('statistics', {}).get('viewCount', "0")
            channelSubscriberCnt = item.get('statistics', {}).get('subscriberCount', "0")
            channelVideoCnt = item.get('statistics', {}).get('videoCount', "0")


            # channelDesc = item['snippet']['description']
            # channelPub = item['snippet']['publishedAt']
            # channelViewCnt = item['statistics']['viewCount']
            # channelSubscriberCnt = item['statistics']['subscriberCount']
            # channelVideoCnt = item['statistics']['videoCount']

            channels_description.append(channelDesc)
            channels_publishedAt.append(channelPub)
            channels_viewCount.append(channelViewCnt)
            channels_subscriberCount.append(channelSubscriberCnt)
            channels_videoCount.append(channelVideoCnt)

    df = pd.DataFrame({
        'channelDescription': channels_description, # 채널 설명
        'channelPublishedAt': channels_publishedAt, # 채널 만든 날짜
        'channelViewCount': channels_viewCount, # 채널 조회수
        'subscriberCount': channels_subscriberCount, # 구독자수
        'totalVideoCount': channels_videoCount # 업로드된 공개 동영상 수
    })


    # publishedAt to datetime, timezone change
    df['channelPublishedAt'] = pd.to_datetime(df['channelPublishedAt'], format='ISO8601')
    df['channelPublishedAt'] = df['channelPublishedAt'].dt.tz_convert('Asia/Seoul')

    return df

df_channels = channels_list(50)

# 최종 df
df_raw = pd.concat([df_search_video, df_channels], axis=1)



##

df_final = df_search_video.copy()
df_final.info()

## 영상 길이 변환
# loc[cond, update col] = 'new value'
df_final.loc[df_final['videoDuration'] == "P0D", 'videoDuration'] = "live"
# Remove PT from the duration strings except for 'live', where(조건(만족하면 그대로), 대체값)
df_final['videoDuration'] = df_final['videoDuration'].where(df_final['videoDuration'] == 'live', df_final['videoDuration'].str[2:])


## 데이터 수집 확인
# 비디오 값 확인 (api 코드 수정)
# videoId 값 동일 여부 판단
videoId = df_final['videoId']
# 동일 컬럼명 변경
videoId.columns = ['videoId.1', 'videoId.2']
# 다른 비디오값 존재 여부 확인 (null 나와야 함)
videoId.loc[videoId['videoId.1'] != videoId['videoId.2']]


## 비디오 중복 확인
video_unique = videoId.drop_duplicates(['videoId.1'])

# 비디오 중복 제거
df_unique = df_final.drop_duplicates(['videoId']).reset_index(drop=True)

## 영상 길이 초 단위 제거
# str : Series 객체에 접근하기 위함, 최종 조건 = (조건) | (조건)
cond = ((df_unique['videoDuration'].str.contains('M')) | (df_unique['videoDuration'] == 'live'))
df_unique = df_unique[cond].reset_index(drop=True)

## lofi 음악 아닌 것 제거
# df_pre = df_unique.loc[(df_unique['channelId'] != 'UC06cxbuQh-VGSQwh3All8kQ') & (df_unique['channelId'] != 'UCrCEi8td15_1DBnrU6h0TRA')].reset_index(drop=True)


## csv 생성
df_unique.to_csv('lofi_data.csv', encoding='utf-8')