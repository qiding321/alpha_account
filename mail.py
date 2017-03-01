# -*- coding: utf-8 -*-
"""
Created on 2016/12/14 15:05

@version: python3.5
@author: qiding
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header

import datetime
import os
import time

import log

my_log = log.my_log


def send_email(email_message, attach_file_path_list, today_str):
    server = 'smtp.exmail.qq.com'

    # print("type label of sender, q or y: ")
    # s_label = input()
    s_label = 'q'
    if s_label == 'q':
        sender = 'dqi@mingshiim.com'
    elif s_label =='y':
        sender = 'guangy@mingshiim.com'
    else:
        print ("Wring input!!!")
        raise
    print("type in psw: ")
    psw = input()

    ############### info 1 ################
    receiver_4 = 'yuanyu@mingshiim.com'
    receiver_0 = 'xhwang@mingshiim.com'
    receiver_1 = 'whxun@mingshiim.com'
    receiver_2 = 'guangy@mingshiim.com'
    receiver_3 = 'dqi@mingshiim.com'
    receivers = [receiver_4, receiver_0, receiver_1, receiver_2 , receiver_3]

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = ','.join(receivers)
    subject = 'Trading Monitor (alpha) ' + today_str
    message['Subject'] = Header(subject, 'utf-8')

    description_str = '''
long_trading_diff: long target value - long trading value
short_trading_diff: short target value - short trading value
trading_cost: trading cost rate, positive means loss
long_cost_rate: long trading cost rate
short_cost_rate: short trading cost rate
long_trading_value: long trading value
long_target_value: long target value
short_trading_value: short trading value
short_target_value: short target value
long_cost: long cost value
short_cost: short cost value
na_volume_long: stocks not available to get price, long side
na_volume_short: stocks not available to get price, short side
    '''
    email_text = 'Dear all,\n\nPlease see the attached files for trading summary.\n' + email_message + '\n\n' + description_str + '\n\nBest,\nDing'

    message.attach(MIMEText(email_text, 'plain', 'utf-8'))

    for file_path in attach_file_path_list:
        att1 = MIMEApplication(open(file_path, 'r').read())
        att1.add_header('Content-Disposition', 'attachment', filename=os.path.split(file_path)[1])
        message.attach(att1)

    log_info = 'Subject: {}\nSender: {}\nReceiver: {}\nMessage: {}\nAttachment: {}\n'.format(
        subject,
        sender,
        receivers,
        email_text,
        attach_file_path_list,
    )
    my_log.info(log_info)

    my_log.info('sure to send email? (y/n)')
    confirm = input()
    if confirm == 'y':
        time.sleep(60)
        pass
    else:
        exit()

    try:
        smtpObj = smtplib.SMTP(server)
        smtpObj.login(sender, psw)
        smtpObj.sendmail(sender, receivers, message.as_string())

        my_log.info("emails sent!")
        smtpObj.close()
    except smtplib.SMTPException:
        my_log.info("Error: cannot send emails")

