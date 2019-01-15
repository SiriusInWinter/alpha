# coding=utf-8
"""
one piece
"""
import re
import os
import json
import requests
from bs4 import BeautifulSoup


headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) " \
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 " \
                "Safari/537.36"
}


def get_op_newest_update():
    """
    get_op_newest_update
    """
    page_url = "http://ac.qq.com/Comic/comicInfo/id/505430"
    res = requests.get(page_url, headers=headers)
    if not res or res.status_code != 200:
        return None

    soup = BeautifulSoup(res.content)
    chapter_log_ul = soup.find("ul", attrs={"class": "works-chapter-log"})
    if not chapter_log_ul:
        return None

    chapter_log_lis = chapter_log_ul.find_all("li")
    if not chapter_log_lis or len(chapter_log_lis) < 2:
        return None

    newest_li = chapter_log_lis[-1]
    newest_li_spans = newest_li.find_all("span")
    newest_li_a = newest_li.find("a", attrs={"class": "works-ft-new"})
    if not newest_li_spans or not newest_li_a:
        return None
    result = {}
    # chapter update time
    update_time = newest_li_spans[-1].text
    # chapter num & name
    a_content = newest_li_a.text
    a_url = "http://ac.qq.com" + newest_li_a.get("href")
    p_newest = re.compile(u".*第\s*(\d+)\s*话.*")
    m_newest = p_newest.match(a_content)
    if m_newest:
        newest_page = m_newest.group(1)
        result["num"] = int(newest_page)
    else:
        return None
    # result
    result["update_time"] = update_time
    result["title"] = a_content
    result["url"] = a_url
    return result


def check_update():
    """
    check_update
    """
    newest_update = get_op_newest_update()
    if not newest_update:
        return False, None

    file_path = "./one_piece_newest.txt"
    if not os.path.exists(file_path):
        f = open(file_path, "w+")
        f.write(json.dumps(newest_update, ensure_ascii=False))
        f.close()
        return True, newest_update

    update_flag = False
    f = open(file_path, "r+")
    line = f.readline().strip()
    if line:
        line_info = json.loads(line)
        if newest_update.get("num", 0) > line_info.get("num", 0):
            update_flag = True
    # update
    f.truncate()
    f.write(json.dumps(newest_update, ensure_ascii=False).encode("utf-8"))
    f.close()

    return update_flag, newest_update


if __name__ == '__main__':
    print(get_op_newest_update())
    #print check_update()