#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 调用SMTP服务器
import smtplib
from email.mime.text import MIMEText
from email.header import Header
# 正则表达式
import re
# 用于读取目录下的所有文件
import os
# 用于读取颜色
import openpyxl
import datetime
import time
import json

with open('config.json', 'r', encoding='utf-8') as f:
    JsonFile = json.load(f)


ColorSheetName = JsonFile['ColorSheetName']
ColorRow = JsonFile['ColorRow']
ColorColumn = JsonFile['ColorColumn']
Delay = JsonFile['Delay']
# SMTP 服务
mail_host = JsonFile['mail_host']  # 设置服务器
mail_user = JsonFile['mail_user']  # 用户名
mail_pass = JsonFile['mail_pass']  # 口令
sender = JsonFile['sender']
# 收件邮箱列表
receivers = JsonFile['receivers']  # 接收邮件列表，可设置为你的QQ邮箱或者其他邮箱
# 邮件主题
SendSubject = JsonFile['SendSubject']
# 发送内容
SendContext = JsonFile['SendContext']
# 发件人名称
SendHeaderSender = JsonFile['SendHeaderSender']
# 收件人名称
SendHeaderReceiver = JsonFile['SendHeaderReceiver']


# 邮箱服务
def send_email():
    SendCon = SendContext + '\n' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    message = MIMEText(SendCon, 'plain', 'utf-8')
    message['From'] = Header(SendHeaderSender, 'utf-8')
    message['To'] = Header(SendHeaderReceiver, 'utf-8')
    message['Subject'] = Header(SendSubject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

# 获取当前工作路径和文件名
def get_filename():
    path = os.getcwd()  # 文件夹目录
    print("当前工作目录为", path)
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    print("当前目录下文件有", files)  # 打印结果

    # 筛选出不带~的文件
    list1 = ['~']
    newlist = [x for x in files if all(y not in x for y in list1)]
    print(newlist)

    # 筛选出剩余文件中的xlsx文件
    r = re.compile(".*xlsx")
    newlist = list(filter(r.match, newlist))
    file = newlist[0]

    file = path + '\\' + file
    print("当前读取的文件是 ", file)
    return file

if __name__ == '__main__':

    file = get_filename()

    while True:

        workbook = openpyxl.load_workbook(file)
        worksheet = workbook[ColorSheetName]
        color = str(worksheet.cell(row=ColorRow, column=ColorColumn).fill.fgColor.rgb)
        if color != "00000000":
            print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + "监测到变色，发送邮件")
            send_email()
            break
        else:
            print(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + " 无变化")

        time.sleep(Delay)

    os.system("Pause")