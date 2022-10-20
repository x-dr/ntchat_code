import requests
import json
import time
import re
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv('.env'))
import os
JD_COOKIE = os.environ.get('JD_COOKIE') #抓取你自己的京东cookie
UNION_ID = os.environ.get('UNION_ID')  #你自己的京东联盟ID


def get_time_stamp():
    return int(time.time())




def get_url(raw_url):
    body={
    "funName":"getSuperClickUrl",
    "param":{
        "materialInfo":raw_url,
        "ext1":"200|100_3|"},
    "unionId":UNION_ID
    }
    url = f'https://api.m.jd.com/api?functionId=ConvertSuperLink&appid=u&_={get_time_stamp()}&body={body}&loginType=2' 
    return url


def get_headers():
    headers = {
        'Host': 'api.m.jd.com',
        'Cookie': JD_COOKIE,
        'content-type': 'application/json',
        'Accept-Encoding': 'gzip,compress,br,deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.29(0x18001d30) NetType/4G Language/zh_CN',
        'Referer': 'https://servicewechat.com/wxf463e50cd384beda/144/page-frame.html'
    }
    return headers

def get_data(raw_url):
    headers = get_headers()
    payload={}
    url = get_url(raw_url)
    # print(url)
    data = requests.request("GET", url, headers=headers, data=payload)
    return data.json()

#QRURL
# 获取链接二维码图片
def get_pic_url(raw_url):
    # raw_url = 'https://u.jd.com/kIKWvlS'

# https://api.m.jd.com/api?functionId=unionSearch&appid=u&_=1666099241716&
# body={"funName":"getCode","
# param":{"materialId":"https://u.jd.com/kMtgw9Q","needDlinkQRurl":1,"ext1":"200|100_3|","command":1},
# "unionId":1001138515}&loginType=2
    payload = {}
    body = {
        "funName": "getCode",
        "param": {
            "materialId": raw_url,
            "needDlinkQRurl": 1,
            "ext1": "200|100_3|",
            "command": 1},
        "unionId": UNION_ID
    }
    url = f'https://api.m.jd.com/api?functionId=unionSearch&appid=u&_={get_time_stamp()}&body={body}&loginType=2'
    dlinkQRUrl = requests.request("GET", url, headers=get_headers(), data=payload)
    
    return dlinkQRUrl.json()['data']['dlinkQRUrl']

def get_msg(raw_url):

    data = get_data(raw_url)
    if data['code'] == 200:
        # print(data)
        if 'wlCommission' in data['data']:

            originalContext = data['data']['originalContext']
            wlCommission=data['data']['wlCommission']
            wlCommissionShare=data['data']['wlCommissionShare']

            linkQRUrl = get_pic_url(data['data']['promotionUrl'])
            # originalContext
            msg = f'【京东联盟】\n{originalContext}\n\n【预计佣金:¥】{wlCommission}\n【佣金比例:】{wlCommissionShare}%'
            # print(msg)
            return '200',msg, linkQRUrl
        else:
            msg=data['data']['originalContext']
            return msg

    else:
        msg = data['message']
    
    return msg   

# print(get_msg())