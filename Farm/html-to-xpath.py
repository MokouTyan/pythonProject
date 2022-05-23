import requests
from lxml import html

page = requests.get("https://yjsy.fzu.edu.cn/zsgz/bsyjszs.htm")
page.encoding = 'utf-8'
# print(page.text)
root = html.fromstring(page.text)
tree = root.getroottree()
# result = root.xpath('''//*[@class='lists diylist']''')
temp_xpath = """//a[contains(text(),\"""" + "福州大学2022年工程类专业学位博士研究生招生简章" + """\")]"""
print(temp_xpath)
result = root.xpath(temp_xpath)
print(result)
print(tree.getpath(result[0]))
# 如果有多项才使用for循环
# for r in result:
#     print(tree.getpath(r))
