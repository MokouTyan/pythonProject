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

base_url = JsonFile['url']
notice_title_href_xpath = JsonFile['notice_title_href_xpath']
notice_title_xpath = JsonFile['notice_title_xpath']
notice_content_xpath = JsonFile['notice_content_xpath']
search = JsonFile['search']
notice_content_xpath = notice_content_xpath.replace("替换", search)


# 返回下一页的链接，这部分还没写完
def get_next_page_url(current_url):
    current_html = requests.get(current_url)
    current_html.encoding = "utf-8"
    selecter = etree.HTML(current_html.text)
    next_page_url = selecter.xpath("""//*[contains(text(),'下一页') or contains(text(),'下页') or contains(text(),'next') or contains(text(),'Next')]/@href""")
    print("下一页链接", next_page_url)
    return next_page_url

if __name__ == '__main__':
    current_url = base_url

    current_html = requests.get(current_url)
    current_html.encoding = "utf-8"
    selecter = etree.HTML(current_html.text)
    notice = selecter.xpath(notice_title_href_xpath)
    print(notice)

    # print(current_html)
    # next_page_url_xpath = """//*[@href = 'tj-sgsj_2.shtml']/@href"""
    # next_page_url = selecter.xpath(next_page_url_xpath)
    # print("下一页链接", next_page_url)

    # 获取当前页面的所有公告
    for result in notice:
        # 获得网址
        result_url = urljoin(current_url, result)
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