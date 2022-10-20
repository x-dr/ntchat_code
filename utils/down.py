import os.path
import requests
from ntchat.utils import generate_guid
import os
import sys
import re

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3877.400 QQBrowser/10.8.4506.400'
    
}


def get_exec_dir():
    return os.path.dirname(sys.argv[0])


def get_download_dir():
    user_dir = os.path.join(get_exec_dir(), 'download')
    user_dir = os.path.abspath(user_dir)
    if not os.path.isdir(user_dir):
        os.makedirs(user_dir)
    return user_dir



def new_download_file():
    while True:
        path = os.path.join(get_download_dir(), generate_guid("temp"))
        # print(path)
        if not os.path.isfile(path):
            return path





#下载抖音视频
def new_download_video(title):
    while True:
        path = os.path.join(get_download_dir(), title)
        # print(path)
        if not os.path.isfile(path):
            return path

def get_local_video(url, title):
    # print(title)
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 过滤不能作为文件名的字符，替换为下划线   
    if os.path.isfile(url):
        return url
    if not url:
        return None
    video_response = requests.get(url=url, headers=headers)
    data = video_response.content
    temp_file = new_download_video(new_title)+'.mp4'
    with open(temp_file, 'wb') as fp:
        fp.write(data)
        fp.close()
    return temp_file



#下载图片
def get_local_pic(url):
    if os.path.isfile(url):
        return url
    if not url:
        return None
    # json_data = requests.get(url=url, headers=headers).json()
    pic = requests.get(url, headers=headers)
    # print(pic.status_code)
    temp_file = new_download_file()+'.jpg'
    if (pic.status_code == 200):     
        # open('./download/1.jpg', 'wb').write(pic.content)
        with open(temp_file, 'wb') as f:
            f.write(pic.content)
            f.close()
    return temp_file