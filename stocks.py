# coding=utf-8
"""
stocks
"""
import re
import os
import json
import requests
from bs4 import BeautifulSoup


stock_map = {
    "baidu": "https://www.laohu8.com/hq/s/BIDU",
    "alibaba": "https://www.laohu8.com/hq/s/BABA",
}


headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) " \
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 " \
                "Safari/537.36"
}


def get_stock_from_laohu(url):
    """
    laohu
    """
    res = requests.get(url, headers=headers)
    if not res or res.status_code != 200:
        return None
 
    stock_info = {}
    soup = BeautifulSoup(res.content)
    stock_div = soup.find("div", attrs={"class": "stock-quote-wrap"})
    if not stock_div:
        return None

    title_p = stock_div.find("p", attrs={"class": "title"})
    stock_info["title"] = title_p.text.replace("\n", " ")

    current_quote_div = stock_div.find("div", attrs={"class": "current-quote"})
    if not current_quote_div:
        return None

    current_num_strong = current_quote_div.find("strong", attrs={"class": "num price"})
    if not current_num_strong:
        return None
    stock_info["current_quote"] = current_num_strong.text

    change_p = current_quote_div.find("p", attrs={"class": "change"})
    if not change_p:
        return stock_info
    change_info = change_p.find_all("span")
    if change_info:
        changes = []
        for change_item in change_info:
            changes.append(change_item.text)
        stock_info["change"] = changes

    # detail
    detail_tb = stock_div.find("table", attrs={"class": "detail"})
    if detail_tb:
        tds = detail_tb.find_all("td")
        detail_info = {}
        for td_item in tds:
            if td_item.text and ":" in td_item.text:
                td_text_info = td_item.text.split(":")
                if len(td_text_info) == 2:
                    detail_info[td_text_info[0]] = td_text_info[1]
        if detail_info:
            stock_info["detail"] = detail_info

    return stock_info


def get_all_stocks():
    """
    get all
    """
    data = {}
    for stock_name in stock_map:
        res = get_stock_from_laohu(stock_map[stock_name])
        if res:
            data[stock_name] = res

    return data


if __name__ == '__main__':
    get_all_stocks()