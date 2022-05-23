import requests
from lxml import etree
from lxml import html
import json
import time
import string
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 全局变量
with open('config.json', 'r', encoding='utf-8') as f:
    JsonFile = json.load(f)
# 全局变量可修改
base_url = JsonFile['url']
notice_title_href_xpath = JsonFile['notice_title_href_xpath']
notice_title_xpath = JsonFile['notice_title_xpath']
notice_content_xpath = JsonFile['notice_content_xpath']
notice_pages = JsonFile['notice_pages']
search = JsonFile['search']
notice_content_xpath = notice_content_xpath.replace("替换", search)
# 全局变量不修改，调试用的
chrome_driver = r'.\chromedriver.exe'  # chromedriver的文件位置
next_page_keywords = JsonFile['next_page_keywords']
delay = JsonFile['delay']
notice_list_number = JsonFile['notice_list_number']

# 返回下一页的链接，因为是动态js加载的，所以我要使用selenium
def get_next_page_url(current_url, notice_pages):
    s = Service(executable_path=chrome_driver)
    driver = webdriver.Chrome(service=s)
    driver.get(current_url)
    time.sleep(3)
    result = []
    result.append(driver.current_url)
    i = 1
    print(driver.current_url)
    print("开始寻找所有的公告页面")
    while True:
        try:
            pre_url = driver.current_url
            driver.find_element(by=By.XPATH, value=next_page_keywords).click()
            if driver.current_url==pre_url:
                break
            i = i + 1
            result.append(driver.current_url)
            if i>=notice_pages:
                break
            time.sleep(delay)
        except:
            print("到达页数上限")
            break
    print("已找到所有页面，一共有", i, "页")
    time.sleep(3)
    driver.quit()
    print(result)
    return result

# 自适应寻找公告列表的xpath
def get_notice_page_title(base_url):
    s = Service(executable_path=chrome_driver)
    driver = webdriver.Chrome(service=s)
    driver.get(base_url)
    time.sleep(1)
    # print(driver.execute_script("return document.documentElement.innerHTML"))
    ul_list = driver.find_elements(By.XPATH, value="//ul")
    # 找出最长ul
    temp = 0

    for ul in ul_list:
        # 没有字数的列表块跳过不输出
        if len(ul.text)==0:
            continue
        print("————————————————————————————————————————————")
        print("【当前最大列表块】\n字数：", len(ul.text), "\n内容：\n", ul.text)
        print("————————————————————————————————————————————")
        if len(ul.text)>temp:
            temp = len(ul.text)
            print(temp)
            # li_list记录的是最长板块的列表集合
            li_list = ul.find_elements(By.XPATH, value="li")
            # 将列表中的第二个公告赋予xpath，防止置顶贴

        print("\n")
    print("最后得到的公告标题为：\n", li_list[notice_list_number].find_element(By.XPATH, value="a").text)
    return li_list[notice_list_number].find_element(By.XPATH, value="a").text
    driver.quit()

# 将标题去获取页面的标题xpath
def get_notice_page_xpath(title):
    page = requests.get(base_url)
    page.encoding = 'utf-8'
    # print(page.text)
    root = html.fromstring(page.text)
    tree = root.getroottree()
    temp_xpath = """//a[contains(text(),\"""" + title + """\")]"""
    result = root.xpath(temp_xpath)
    result_xpath = tree.getpath(result[0])
    print("返回的xpath是：\n", result_xpath)
    # 如果有多项才使用for循环
    # for r in result:
    #     print(tree.getpath(r))
    return result_xpath

# 将取得的单项xpath处理成多项，将最后的li后面中括号去掉
def handle_suffix_of_xpath(pre_xpath):
    # print(pre_xpath.rfind('[', beg=0, end=len(title_xpath)))
    print(str.rfind(pre_xpath, '[', 0, len(pre_xpath)))
    x = str.rfind(pre_xpath, '[', 0, len(pre_xpath))
    # print(pre_xpath)
    string_list = list(pre_xpath)
    # print(len(string_list))
    # print(string_list)
    del string_list[x:x+3]
    # print(len(string_list))
    # print(string_list)
    after_xpath = ''.join(string_list)
    # print(len(pre_xpath))
    # print(pre_xpath)
    # print(len(after_xpath))
    print("处理后的xpath为", after_xpath)
    return after_xpath

if __name__ == '__main__':
    current_url = base_url

    # 自适应获取当前后续的所有页面List
    notice_pages_list = get_next_page_url(current_url, notice_pages)
    # 自适应获取通知列表的标题
    title = get_notice_page_title(base_url)
    # 将上面函数获取的标题去获取页面的标题xpath
    title_xpath = get_notice_page_xpath(title)
    # 将取得的单项xpath处理成多项
    after_xpath = handle_suffix_of_xpath(title_xpath)
    # current_html = requests.get(current_url)
    # current_html.encoding = "utf-8"
    # selector = etree.HTML(current_html.text)
    # notice = selector.xpath(notice_title_href_xpath)
    # print(notice)
    # 获取当前页面的所有公告
    # for result in notice:
    #     # 获得网址
    #     result_url = urljoin(current_url, result)
    #     print("网址： ", result_url)
    #     result_html = requests.get(result_url)
    #     result_html.encoding = "utf-8"
    #     result_detail = etree.HTML(result_html.text)
    #     result_title = result_detail.xpath(notice_title_xpath)
    #     print("标题: ", result_title)
    #
    #     result_content = result_detail.xpath(notice_content_xpath)
    #     print("内容： ")
    #     for result_print in result_content:
    #         print(result_print)
    #     print("\n")
    #     time.sleep(delay)
