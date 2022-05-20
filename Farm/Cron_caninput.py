import requests
from lxml import etree
import lxml
import json
import time
import string
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 全局变量
with open('config.json', 'r', encoding='utf-8') as f:
    JsonFile = json.load(f)

# url = JsonFile['url']
notice_title_href_xpath = JsonFile['notice_title_href_xpath']
notice_title_xpath = JsonFile['notice_title_xpath']
notice_content_xpath = JsonFile['notice_content_xpath']
search = JsonFile['search']
notice_content_xpath = notice_content_xpath.replace("替换", search)
print(notice_content_xpath)


if __name__ == '__main__':
    try:
        print("请输入要爬取的网站的公告首页（默认为国家粮食和物资储备局）")
        url = input()
        print("请输入要爬取的网站的公告首页（默认为国家粮食和物资储备局）")
        search = input()
    except:
        print("输入有误")
    html = requests.get(url)
    html.encoding = "utf-8"
    selecter = etree.HTML(html.text)
    notice = selecter.xpath(notice_title_href_xpath)
    print(notice)
    for result in notice:
        # 获得网址
        result_url = urljoin(url, result)
        print("网址： ", result_url)
        result_html = requests.get(result_url)
        result_html.encoding = "utf-8"
        result_detail = etree.HTML(result_html.text)
        result_title = result_detail.xpath(notice_title_xpath)
        print("标题: ", result_title)

        result_content = result_detail.xpath(notice_content_xpath)
        print("内容： ")
        for result_print in result_content:
            print(result_print)
        print("\n")
        time.sleep(1)