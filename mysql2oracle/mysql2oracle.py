# encoding: utf-8
import pymysql
import json
import cx_Oracle
from datetime import date, timedelta
import sys



with open('config.json', 'r', encoding='utf-8') as f:
    JsonFile = json.load(f)
mysql_host = JsonFile['mysql_host']
mysql_user = JsonFile['mysql_user']
mysql_password = JsonFile['mysql_password']
mysql_port = JsonFile['mysql_port']
mysql_database = JsonFile['mysql_database']
mysql_tables = JsonFile['mysql_tables']
oracle_user = JsonFile['oracle_user']
oracle_password = JsonFile['oracle_password']
oracle_host = JsonFile['oracle_host']
oracle_tables = JsonFile['oracle_tables']
yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")

class Logger(object):
    def __init__(self, filename='logs\\'+yesterday+'.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

def sql_generate(datebase_name, data_list, data_tuple):
    index = oracle_tables.index(datebase_name)
    insert_sql = 'INSERT INTO ' + oracle_tables[index] + ' ('
    count = 0
    all = len(data_list[0].keys())
    for j in data_list[0].keys():
        insert_sql = insert_sql + '"' + j + '"'
        count = count + 1
        if count<all:
            insert_sql = insert_sql + ', '
    insert_sql = insert_sql + ', "ID") values ('

    count = 0
    for j in range(all):
        insert_sql = insert_sql + ':' + str(j+1)
        count = count + 1
        if count < all:
            insert_sql = insert_sql + ', '
    insert_sql = insert_sql + ', func_nextid(\''+ datebase_name +'\'))'
    print('插入语句为', insert_sql)
    # send_to_db(insert_sql, data_list, data_tuple)
    return insert_sql

def send_to_db(sql,data_list,data_tuple):
    oracle_connection = cx_Oracle.connect(oracle_user, oracle_password, oracle_host, encoding="UTF-8")
    oracle_cursor = oracle_connection.cursor()
    try:
        oracle_cursor.executemany(sql, data_tuple)
        oracle_connection.commit()
    except:
        return
    oracle_cursor.close()
    oracle_connection.close()


if __name__ == '__main__':
    sys.stdout = Logger(stream=sys.stdout)
    mysql_conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, port=mysql_port,
                           database=mysql_database, autocommit=True)
    mysql_cursor = mysql_conn.cursor(cursor=pymysql.cursors.DictCursor)
    print('正在获取昨日数据', yesterday, '的数据\n')
    for i in mysql_tables:
        print('正在提取mysql数据库中的', i, '表的数据')
        sql = 'SELECT * FROM ' + i + ' WHERE DATE like \'' + yesterday + '%\''
        print('查询语句为', sql)
        result_tuple = []
        mysql_cursor.execute(sql)
        result_dict = mysql_cursor.fetchall()
        if len(result_dict) == 0:
            print('无结果，进行下个表的查询')
            continue
        print(result_dict)
        for j in result_dict:
            result_tuple.append(tuple(j.values()))
        # print(result_tuple)
        sql_generate(i, result_dict, result_tuple)
        print()


    mysql_cursor.close()
    mysql_conn.close()
