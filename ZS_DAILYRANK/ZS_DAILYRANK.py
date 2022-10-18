import requests
import json
import datetime
import string
from lxml import etree
import pymysql
from datetime import date, timedelta
import sys

todaylog = (date.today() + timedelta(days=0)).strftime("%Y-%m-%d")
class Logger(object):
    """
    用来写日志用的
    """
    def __init__(self, filename='logs/' + todaylog+'.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

def sql_generate(datebase_name, data_list):
    """
    用来生成SQL语言用的
    :param datebase_name: 表名
    :param data_list: 一个数组，每个元素为一个字典
    :return:
    """
    insert_sql = 'INSERT INTO `' + datebase_name + '`('
    count = 0
    all = len(data_list[0].keys())
    for j in data_list[0].keys():
        insert_sql = insert_sql + j
        count = count + 1
        if count<all:
            insert_sql = insert_sql + ','
    insert_sql = insert_sql + ') select '
    count = 0
    for j in data_list[0].keys():
        insert_sql = insert_sql + '%(' + j + ')s'
        count = count + 1
        if count < all:
            insert_sql = insert_sql + ','
    insert_sql = insert_sql + '\nFROM DUAL WHERE NOT EXISTS(SELECT * FROM ' + datebase_name +' WHERE '
    count = 0
    for j in data_list[0].keys():
        insert_sql = insert_sql + j +' = %(' + j + ')s'
        count = count + 1
        if count<all:
            insert_sql = insert_sql + ' and '
    insert_sql = insert_sql + ');'
    print(insert_sql)
    # send_to_db(insert_sql, data_list)
    return insert_sql

def send_to_db(sql,data):
    """
    用来发送到数据库用的
    :param sql: SQL语句
    :param data: 数组，元素为字典
    :return:
    """
    conn = pymysql.connect(host='192.168.141.14',
                           user='root',
                           password='123456',
                           port=3306,
                           database='Data',
                           autocommit=True
                           )
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    affect_rows = cursor.executemany(sql, data)
    print('插入行数', affect_rows)
    cursor.close()
    conn.close()

if __name__ == '__main__':
    sys.stdout = Logger(stream=sys.stdout)
    today_year = (date.today() + timedelta(days=0)).strftime("%Y")
    today = (date.today() + timedelta(days=0)).strftime("%Y%m%d")
    base_url = 'http://www.czce.com.cn/cn/DFSStaticFiles/Future/' + today_year + '/' + '20220817' + '/FutureDataHolding.htm'
    print(base_url)
    packet = requests.get(base_url)
    result_all = []
    result_buy = []
    result_sell = []
    if packet.status_code == 404:
        print('fail\n\n\n')
    elif packet.status_code == 200:
        result = packet.content.decode('UTF-8', 'strict').replace('&nbsp;', ' ')
        # with open("./logs/test.txt", "w") as f:
        #     f.write(result)
        html = etree.HTML(result)
        html_title = html.xpath('//*[@colspan]/..')
        html_table = html.xpath('//tr')

        j = 0
        INSTRUMENT = ''
        DATE = datetime.datetime.now()


        for i in html_table:
            temp_dict = {}
            if i[0].text == '名次':
                continue
            elif i[0].text == '合计':
                continue
            elif i == html_title[j]:
                title = html.xpath('//*[@colspan]/b/text()')[j]
                INSTRUMENT = title.split()[0][3:]
                DATE = datetime.datetime.strptime(title.split()[1][3:], '%Y-%m-%d')
                print(INSTRUMENT)
                print(DATE)
                j = j + 1
                # 这一步是防止j超过了title的数量
                if j == len(html_title):
                    j = 0
            else:
                temp_dict['DATE'] = DATE
                temp_dict['INSTRUMENT'] = INSTRUMENT
                temp_dict['RANK_'] = i[0].text
                temp_dict['NAME'] = i[1].text
                temp_dict['DATA'] = i[2].text.replace(',', '').replace('-', '0')
                temp_dict['DATA_CHG'] = i[3].text.replace(',', '').replace('-', '0')
                result_all.append(temp_dict)
                print(temp_dict)
                temp_dict = {}
                temp_dict['DATE'] = DATE
                temp_dict['INSTRUMENT'] = INSTRUMENT
                temp_dict['RANK_'] = i[0].text
                temp_dict['NAME'] = i[4].text
                temp_dict['DATA'] = i[5].text.replace(',', '').replace('-', '0')
                temp_dict['DATA_CHG'] = i[6].text.replace(',', '').replace('-', '0')
                result_buy.append(temp_dict)
                print(temp_dict)
                temp_dict = {}
                temp_dict['DATE'] = DATE
                temp_dict['INSTRUMENT'] = INSTRUMENT
                temp_dict['RANK_'] = i[0].text
                temp_dict['NAME'] = i[7].text
                temp_dict['DATA'] = i[8].text.replace(',', '').replace('-', '0')
                temp_dict['DATA_CHG'] = i[9].text.replace(',', '').replace('-', '0')
                result_sell.append(temp_dict)
                print(temp_dict)

    sql_generate('ZS_DAILYRANK_ALL', result_all)
    sql_generate('ZS_DAILYRANK_BUY', result_buy)
    sql_generate('ZS_DAILYRANK_SELL', result_sell)