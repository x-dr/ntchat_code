# -*- coding: utf-8 -*-
import os
import sys
import time
os.environ['NTCHAT_LOG'] = "ERROR"

import ntchat
import datetime
from api.douyin import get_video_info, get_video_id, get_video_url
from api.caiyun import get_city_weather,get_location_weather
from api.hot import get_weibo_hot,get_zhihu
from api.jd import get_msg as jd_msg
from utils.down import get_local_video,get_local_pic
from utils.urltoqr import create_qr_code
import schedule
import xmltodict
import pprint
import xml.dom.minidom

wechat = ntchat.WeChat()

wechat.open(smart=True)
# 等待登录
# wechat.wait_login()
menu="""注意：目前所有带+的查询，中间必须是一个空格

        
--------------生活-------------
1、天气+地点(天气 北京)
2、微博热搜
3、知乎热榜

--------------工具-------------
1、qr+内容(转二维码)
2、京东转链+链接


--------------娱乐-------------
1、解析抖音视频(抖音-分享-复制链接-在微信群粘贴)
"""


# 注册消息回调
@wechat.msg_register(ntchat.MT_RECV_FRIEND_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    xml_content = message["data"]["raw_msg"]
    # print(xml_content)
    dom = xml.dom.minidom.parseString(xml_content)

    # 从xml取相关参数
    encryptusername = dom.documentElement.getAttribute("encryptusername")
    ticket = dom.documentElement.getAttribute("ticket")
    scene = dom.documentElement.getAttribute("scene")

    # 自动同意好友申请
    ret = wechat_instance.accept_friend_request(encryptusername, ticket, int(scene))

    if ret:
        # 通过后向他发条消息
        wechat_instance.send_text(to_wxid=ret["userName"], content=menu)




# 消息回调
@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat: ntchat.WeChat, message):
    data = message["data"]
    msg = data["msg"]
    # print("======================\n","======================\n",message,"======================\n","======================\n")
    from_wxid = data["from_wxid"]
    room_wxid = data["room_wxid"]
    self_wxid = wechat.get_login_info()["wxid"]

    if from_wxid == self_wxid:
        return

    if msg[0:2] == "功能":
        res =menu
        if room_wxid != "":
            wechat.send_text(to_wxid=room_wxid, content=res)
        else:
            wechat.send_text(to_wxid=from_wxid, content=res)

    if msg[0:3] == "天气 " or msg == "天气":
                city_name=msg[3:] if msg[3:] else "广州"
                res = get_city_weather(city_name)
                if res:
                    if room_wxid != "":
                        wechat.send_text(to_wxid=room_wxid, content=res)

                    else:
                        wechat.send_text(to_wxid=from_wxid, content=res)
                else:
                    if room_wxid != "":
                        wechat.send_text(to_wxid=room_wxid, content="查询失败，请输入正确的城市名")
                    else:
                        wechat.send_text(to_wxid=from_wxid, content="查询失败，请输入正确的城市名")




    if 'https://v.douyin.com' in msg:
        douyin_result = get_video_info(msg)
        if room_wxid != "":
            wechat.send_text(to_wxid=room_wxid, content=douyin_result[2])
            file_path = get_local_video(douyin_result[1], douyin_result[4])
            wechat.send_video(to_wxid=room_wxid, file_path=file_path)
        else:
            wechat.send_text(to_wxid=from_wxid, content=douyin_result[2])
            file_path = get_local_video(douyin_result[1], douyin_result[4])
            wechat.send_video(to_wxid=from_wxid, file_path=file_path)
    

    if msg[0:4] == "微博热搜":
        res = get_weibo_hot()
        if room_wxid != "":
            wechat.send_text(to_wxid=room_wxid, content=res)
        else:
            wechat.send_text(to_wxid=from_wxid, content=res)
    if msg[0:4] == "知乎热榜":
        res = get_zhihu()
        if room_wxid != "":
            wechat.send_text(to_wxid=room_wxid, content=res)
        else:
            wechat.send_text(to_wxid=from_wxid, content=res)

    if msg[0:4] == "京东转链":
        raw_url=msg[5:]
        data=jd_msg(raw_url)
        code=data[0]
        if code=='200':  
            linkQRUrl=f'https://img14.360buyimg.com/n1/{data[2]}'
            # print(linkQRUrl)

            if room_wxid != "":
                wechat.send_text(to_wxid=room_wxid, content=data[1])
                file_path = get_local_pic(linkQRUrl)
                wechat.send_image(to_wxid=room_wxid, file_path=file_path)
            else:
                wechat.send_text(to_wxid=from_wxid, content=data[1])
                file_path = get_local_pic(linkQRUrl)
                wechat.send_image(to_wxid=from_wxid, file_path=file_path)
        else:
            
            if room_wxid != "":
                wechat.send_text(to_wxid=room_wxid, content=data)
            else:
                wechat.send_text(to_wxid=from_wxid, content=data)

    if msg[0:2] == "qr":
        raw_url=msg[3:]
        # print(raw_url)
        data=create_qr_code(raw_url)
        if room_wxid != "":
            file_path = get_local_pic(data)
            wechat.send_image(to_wxid=room_wxid, file_path=file_path)
        else:   
            file_path = get_local_pic(data)
            wechat.send_image(to_wxid=from_wxid, file_path=file_path)







#监听位置信息
@wechat.msg_register(ntchat.MT_RECV_LOCATION_MSG)
def on_recv_text_msg(wechat: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    room_wxid = data["room_wxid"]
    self_wxid = wechat.get_login_info()["wxid"]
    msg = data["raw_msg"]



    if from_wxid == self_wxid:
        return
    d=xmltodict.parse(msg)
    # print(d['msg']['location']['@x'],d['msg']['location']['@y'])
    location=d['msg']['location']['@y']+","+d['msg']['location']['@x']
    city_name=d['msg']['location']['@label']
    res = get_location_weather(location,city_name)
    if res:
        # print(res)
        if room_wxid != "":
            wechat.send_text(to_wxid=room_wxid, content=res)
        else:
            wechat.send_text(to_wxid=from_wxid, content=res)    
    else:
        if room_wxid != "":
            wechat.send_text(to_wxid=room_wxid, content="查询失败，请输入正确的城市名")
        else:
            wechat.send_text(to_wxid=from_wxid, content="查询失败，请输入正确的城市名")



try:
    while True:
        # schedule.run_pending()
        pass
except KeyboardInterrupt:
    ntchat.exit_()
    sys.exit()
