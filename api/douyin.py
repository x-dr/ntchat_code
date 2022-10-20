import datetime
import json
import re

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 "
}

#提取视频id
def get_video_url(share_text):
    video_url = re.search(r"(https?.*?)(?=http|$|<|>|\s|,)", share_text).group(1)
    resp = requests.get(video_url, headers=headers)
    video_id = re.search(r"video/(\d+)/", resp.url)
    return video_id.group(1)


#获取视频信息
def get_video_info(share_text):

    video_id=get_video_url(share_text)
    url = f"https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={video_id}"
    resp = requests.get(url, headers=headers).json()

    # resp = json.loads(resp)
    # print(resp)
    # # 作者
    author = resp['item_list'][0]['author']['nickname']
    # print(author)
    # 视频描述，标题
    desc = resp['item_list'][0]['desc']
    # print(desc)
    # 发布时间
    create_time = resp['item_list'][0]['create_time']
    date = datetime.datetime.utcfromtimestamp(create_time).strftime("%Y-%m-%d %H:%M:%S")
    # print(date)
    # 视频封面url
    cover_url = resp['item_list'][0]['video']['origin_cover']['url_list'][0]
    # 视频地址url
    video_url = resp['item_list'][0]['video']['play_addr']['url_list'][0].replace('playwm', 'play').replace('720p', '9999')
    # print(video_url)
    # 视频时长
    duration1 = resp['item_list'][0]['video']['duration']   
    # print(str(datetime.timedelta(seconds=int(duration/1000))))
    duration=str(datetime.timedelta(seconds=int(duration1/1000)))
    re_url = requests.get(video_url, headers=headers).url
    # print(re_url)
    # 评论数
    comment_count = resp['item_list'][0]['statistics']['comment_count']
    # 赞
    digg_count = resp['item_list'][0]['statistics']['digg_count']
    video_info = f"视频标题：{desc}\n发布时间：{date}\n视频时长:{duration}\n抖  主：{author}\n评  论：{comment_count}\n点  赞：{digg_count}\n\n视频链接：{video_url}"

    return cover_url, re_url, video_info,video_url,desc

