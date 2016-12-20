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


def send_email(email_message, attach_file_path_list):
    server = 'smtp.exmail.qq.com'
    sender = 'dqi@mingshiim.com'
    #sender = 'guangy@mingshiim.com'
    print("type in psw: ")
    psw = input()

    ############### info 1 ################
    receiver_0 = 'xhwang@mingshiim.com'
    receiver_1 = 'whxun@mingshiim.com'
    receiver_2 = 'guangy@mingshiim.com'
    receiver_3 = 'dqi@mingshiim.com'
    receivers = [receiver_0, receiver_1, receiver_2 , receiver_3]

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = ','.join(receivers)
    subject = 'Trading Monitor (alpha) ' + datetime.datetime.now().strftime("%Y-%m-%d")
    message['Subject'] = Header(subject, 'utf-8')

    email_text = 'Dear all,\n\nPlease see the attached files for trading summary.\n\n' + email_message + 'Best,\nDing'
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

