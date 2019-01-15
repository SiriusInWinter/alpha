# coding=utf-8
"""
weather
"""
import json
import requests
from bs4 import BeautifulSoup


city_weather_code = {
    "北京": "101010100",
}


headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) " \
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 " \
                "Safari/537.36"
}


def get_week_weather(city_name):
    """
    week weather
    """
    if city_name not in city_weather_code:
        return None

    weather_code = city_weather_code[city_name]
    url = "http://www.weather.com.cn/weather/{}.shtml".format(weather_code)
    res = requests.get(url, headers=headers)
    print(url, res)
    if not res:
        return None

    content = res.content
    soup = BeautifulSoup(content)
    ul = soup.find("ul", attrs={"class": "t"})
    if not ul:
        return None
    lis = ul.find_all("li")
    if not lis:
        return None

    data = []
    for li in lis:
        weather_info = {}
        date_h1 = li.find("h1")
        if date_h1:
            weather_info["date"] = date_h1.text.strip()
        else:
            continue
        p_s = li.find_all("p")
        for p_item in p_s:
            p_class = p_item.get("class")
            if "wea" in p_class:
                weather_info["weather"] = p_item.text.strip()
            if "win" in p_class:
                weather_info["wind"] = p_item.text.strip()
            if "tem" in p_class:
                weather_info["temp"] = p_item.text.strip().replace("\n", "")
        data.append(weather_info)
    return data


if __name__ == '__main__':
    print(get_week_weather(u"北京"))
