import requests
from utils.weather import weather_dict
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv('.env'))
import os
# https://console.amap.com/dev/index
# 高德地图key
amap_key = os.environ.get('amap_key')

# APIKey
#https://dashboard.caiyunapp.com/v1/token/
#彩云天气key
weather_key = os.environ.get('weather_key')

# 地理编码
def geo(add:str)-> dict:
    """获取地理编码"""
    url = 'https://restapi.amap.com/v3/geocode/geo?parameters'
    param ={
        'key':amap_key,
        'address':add,
        'output':'json'
    }
    response = requests.get(url,params=param)
    data = response.json()['geocodes'][0]['location']
    return data


def get_city_weather(city_name: str = '广州'):
    """获取城市天气"""
    location=geo(city_name)
    url = f'https://api.caiyunapp.com/v2.6/{weather_key}/{location}/weather.json?dailysteps=1&alert=true'
    response = requests.get(url)
    data = response.json()
    res=get_data(data,city_name)
    # print(res)
    return res

def get_location_weather(location,city_name):
    url = f'https://api.caiyunapp.com/v2.6/{weather_key}/{location}/weather.json?dailysteps=1&alert=true'
    response = requests.get(url)
    data = response.json()
    res=get_data(data,city_name)
    # print(res)
    return res



def get_data(data,city_name):
    res = "{}\n\n当前温度: {} ℃\n体感温度: {} ℃ \n天气: {}\n空气质量: {}\n紫外线: {}\n舒适度指数: {}\n相对湿度: {} % \n未来24小时天气： {} \npm2.5: {} μg/m3\n \n\n{}".format(
                        city_name,
                        data['result']['realtime']['temperature'],  #当前温度
                        data['result']['realtime']['apparent_temperature'], #体感温度
                        weather_dict[data['result']['realtime']['skycon']], #天气
                        # 
                        
                        data['result']['realtime']['air_quality']['description']['chn'], #国标 AQI
                        data['result']['realtime']['life_index']['ultraviolet']['desc'], #紫外线
                        data['result']['realtime']['life_index']['comfort']['desc'], #舒适度指数
                        data['result']['realtime']['humidity'], #相对湿度
                        data['result']['hourly']['description'], #天气描述
                        data['result']['realtime']['air_quality']['pm25'], #pm2.5

                        data['result']['minutely']['description']) # 提示
    return res