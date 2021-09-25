#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import traceback

import yagmail
import os

def format_address(s):
    addr = parseaddr(s)
    return formataddr(addr)

def demo_smtplib():
    # 发送人和收件人地址
    sender = "daqi@mrzcode.com"
    receivers = ['zyueqi@qq.com']

    # 带有样式的模版内容,否则默认就是字符串
    mail_msg = """
        <p>HTML格式的内容发送.</p>
        <p><a href="https://github.com/mrzcode/TestProjectManagement">提测平台项目代码</a></p>"""
    message = MIMEText(mail_msg, 'html', 'utf-8')
    # message = MIMEText('字符串无样式邮件发送测试...', 'plain', 'utf-8')

    # # 自定义发件人名称
    # message['From'] = Header("大奇测试开发<daqi@mrzcode.com>", 'utf-8')
    # message['To'] = Header("Python自动化发送测试邮件", 'utf-8')

    # 格式化邮件显示
    message['From'] = format_address(u'DaQi <%s>' % sender)

    for receiver in receivers:
        message['To'] = format_address(receiver)

    # 定义邮件主题
    subject = '格式化后的微信企业邮箱发送邮件测试'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        # 发件人邮箱中发送服务器地和端口（企业邮箱是用的SSL)
        mail_server = smtplib.SMTP_SSL('smtp.exmail.qq.com', 465)
        mail_server.login('daqi@mrzcode.com', 'Test@2021')  # 登录邮箱和密码

        # 发送内容
        mail_server.sendmail(sender, receivers, message.as_string())
        print('没有任何异常邮件发送成功！')
        # 关闭邮件服务
        mail_server.quit()

    except Exception:
        print('traceback.format_exc(): {}'.format(traceback.format_exc()))


def demo_yagmail():
    # 设置收件人（不需要再设置发件人）
    receivers = ['zyueqi@qq.com', 'daqigroup@mrzcode.com']
    # 邮件主题
    subject = 'Yagmail测试主题'
    # 内容，可以单独定义，然后组成一个内容体
    body = 'Body描述'
    html = '<a href="https://github.com/mrzcode/TestProjectManagement">项目代码点我!</a>'

    # 附件文件绝对路径， 或者 通过open打开直接给io流文件
    path_file = os.path.dirname(os.path.abspath(__file__))+'/source/result.txt'
    attachments =[path_file]

    # 初始化服务对象直接根据参数给定，更多参考SMTP(）内部
    server = yagmail.SMTP(host='smtp.exmail.qq.com', port=465, user='daqi@mrzcode.com', password='Test@2021')
    # 发送内容，设置接受人等信息，更多参考SMTP.send()内部
    server.send(to=receivers,
                subject=subject,
                contents=[body, html],
                attachments=attachments)

    server.close()
    print("邮件发送的如此简单！")


if __name__ == "__main__":
    # demo_smtplib()
    demo_yagmail()