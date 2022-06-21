import time
import datetime
import json

# a = datetime.datetime.now()
# b = a.strftime("%Y%m%d")
# c = a + datetime.timedelta(days=4)
# d = c.strftime("%Y%m%d")
# e = '2013/10/10'
# f = datetime.datetime.strptime(e, '%Y/%m/%d')
# print(a)
# print(b)
# print(c)
# print(d)
# print(e)
# print(f)

with open('config.json', 'r', encoding='utf-8') as f:
    JsonFile = json.load(f)
base_url = JsonFile['base_url']
begin_date = JsonFile['begin_date']


begin_date = datetime.datetime.strptime(begin_date, '%Y-%m-%d')
date = begin_date

now = datetime.datetime.now()


while date < now:
    date = date + datetime.timedelta(days=1)
    # print(date.strftime("%Y%m%d"))
    url = base_url + date.strftime("%Y%m%d") + '.dat'
    print(url)