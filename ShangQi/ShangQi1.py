
import re
import json
import datetime
import time

import requests
import string

with open('config.json', 'r', encoding='utf-8') as f:
    JsonFile = json.load(f)
base_url = JsonFile['base_url']
begin_date = JsonFile['begin_date']
begin_date = datetime.datetime.strptime(begin_date, '%Y-%m-%d')

def send_to_db_futures(date, dict):
    # print(date)
    print('交易所', i['INSTRUMENTID'].strip(), i['CJ1'])

def send_to_db_nofutures(date, dict):
    pass

def send_to_db_volume(date, dict):
    pass

def send_to_db_buy(date, dict):
    pass

def send_to_db_sell(date, dict):
    pass

def send_to_db_count(date, dict):
    pass







date = begin_date
now = datetime.datetime.now()


while date < now:
    date = date + datetime.timedelta(days=1)
    # print(date.strftime("%Y%m%d"))
    url = base_url + date.strftime("%Y%m%d") + '.dat'
    print(url)

    content = requests.get(url)
    if content.status_code==404:
        print('fail\n\n\n')
    elif content.status_code==200:
        result = content.json()
        # print(result['o_cursor'])
        current_date = datetime.datetime.strptime(result['report_date'], '%Y%m%d')
        print(current_date)
        for i in result['o_cursor']:
            if i['RANK'] == -1:
                send_to_db_futures(current_date, i)
            elif i['RANK'] == 0:
                send_to_db_nofutures(current_date, i)
            elif i['RANK'] == 999:
                # 发送合计量（没有参与者）
                send_to_db_count(current_date, i)
            else:
                # 发送总成交量
                send_to_db_volume(current_date, i)
                # 发送持买单量
                send_to_db_buy(current_date, i)
                # 发送持卖单量
                send_to_db_sell(current_date, i)
        print(len(result['o_cursor']))
        time.sleep(3)