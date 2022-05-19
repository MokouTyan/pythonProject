#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.163.com"  # 设置服务器
mail_user = "a502337328@163.com"  # 用户名
mail_pass = "VVSRGCETMIATYQEN"  # 口令

#sender = 'from@runoob.com'
sender = 'a502337328@163.com'
receivers = ['502337328@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

SendContext = "这里是发送内容" + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

message = MIMEText(SendContext, 'plain', 'utf-8')
message['From'] = Header("邮件提醒", 'utf-8')
message['To'] = Header("收件人", 'utf-8')

subject = '监测到颜色发生变化'
message['Subject'] = Header(subject, 'utf-8')

def Send_Email():
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")
