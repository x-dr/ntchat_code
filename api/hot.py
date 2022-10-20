# -*- coding: utf-8 -*-

import re
from lxml import etree
Headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}

import requests

def validate_title(title):
    new_title=re.sub("#","", title)
    return new_title

def get_weibo_hot():
    """
    爬取微博热搜
    :return:
    """
    url = 'https://weibo.com/ajax/statuses/hot_band'
    response_html = requests.get(url=url,headers=Headers)
    RawData = response_html.json()
    Result = RawData["data"]["band_list"]
    Top = f'[置顶]{RawData["data"]["hotgov"]["name"]}'
    Data = [Top]
    for i in range(0, 10):
        Data.append(f'{i+1}.{Result[i]["note"]}')
    return "\n".join(Data)


def get_zhihu():
    """
    爬取知乎热榜
    :return:
    """
    url = 'https://api.zhihu.com/topstory/hot-list'
    response_html = requests.get(url=url,headers=Headers)
    RawData = response_html.json()

    Result = RawData["data"]
    Data = []
    for i in range(0, 9):
        Data.append(f'{i+1}.{Result[i]["target"]["title"]}')
    return "\n".join(Data)