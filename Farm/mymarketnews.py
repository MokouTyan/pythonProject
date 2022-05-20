import requests
from lxml import etree
import lxml

if __name__ == '__main__':
    url = "http://www.dce.com.cn/dalianshangpin/ywfw/jystz/ywtz/index.html"
    fronturl = "http://www.dce.com.cn"
    html = requests.get(url)
    html.encoding = "utf-8"
    selecter = etree.HTML(html.text)
    notice = selecter.xpath("""//a[contains(text(),'玉米') and contains(@istitle,'true')]/@href""")
    # print(notice)
    for result in notice:
        result_url = fronturl + result
        # 获得网址
        print("网址： ", result_url)
        result_html = requests.get(result_url)
        result_html.encoding = "utf-8"
        result_detail = etree.HTML(result_html.text)
        result_content = result_detail.xpath("""//*[contains(@class,'detail_content')]/p/text()""")
        result_title = result_detail.xpath("""//*[@id="13377"]/div[2]/div[2]/div[1]/h2/text()""")
        print("标题: ", result_title)
        print("内容： ")
        for result_print in result_content:
            print(result_print)
        print("\n\n\n")