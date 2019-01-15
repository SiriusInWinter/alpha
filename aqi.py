# coding=utf-8
"""
Air Quality Index

Data collected from aqicn.org
Api instructions: https://aqicn.org/api/cn/
"""
import json
import requests
from functools import partial



AQI_DATA_PLATFORM_TOKEN = "877232d674043e76c5ea9037b8772e1aa4dbd702"
AQI_CITY_DATA_URL = "http://api.waqi.info/feed/{0}/?token={1}"


def get_aqi_by_city(city_name):
    """
    get aqi by city name, eg: beijing
    """
    url = AQI_CITY_DATA_URL.format(city_name, AQI_DATA_PLATFORM_TOKEN)

    res = requests.get(url)
    if not res or res.status_code != 200:
        return None

    content = res.content
    print(content)
    return json.loads(content)


# map city

aqi_beijing = partial(get_aqi_by_city, "beijing")
aqi_shanghai = partial(get_aqi_by_city, "shanghai")
api_hangzhou = partial(get_aqi_by_city, "hangzhou")


if __name__ == '__main__':
    print(api_hangzhou())