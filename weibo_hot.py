# coding=utf-8
"""
weibo
"""
import json
import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) " \
        "AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
}


def get_weibo_hot():
    """
    """
    url = "http://s.weibo.com/top/summary?cate=realtimehot"
    
    res = requests.get(url, headers=headers)
    if not res:
        return None

    content = res.content

    soup = BeautifulSoup(content)
    list_ul = soup.find("ul", attrs={"class": "list_a"})
    if not list_ul:
        return None

    data = []
    list_lis = list_ul.find_all("li")
    for li_item in list_lis:
        a = li_item.find("a")
        if not a:
            continue

        a_text = a.get_text("$&$")
        a_text_info = a_text.split("$&$")
        a_text_info_new = []

        for aa in a_text_info:
            if aa.strip():
                a_text_info_new.append(aa.strip())

        if len(a_text_info_new) == 3:
            item_data = {}
            item_data["link"] = a.get("href")
            item_data["seq"] = int(a_text_info_new[0])
            item_data["content"] = a_text_info_new[1]
            item_data["hot"] = a_text_info_new[2]

            data.append(item_data)

        #print(a_text)
    print(json.dumps(data))


if __name__ == '__main__':
    get_weibo_hot()