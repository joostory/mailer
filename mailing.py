#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from optparse import OptionParser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.headerregistry import Address
from email.utils import formatdate
import os
import traceback

def make_message(from_user, to_user, subject, text):
    msg = MIMEText(text, "html", _charset="utf-8")
    msg["From"] = from_user
    msg["To"] = to_user
    msg["Subject"] = Header(s=subject, charset="utf-8")
    msg["Date"] = formatdate(localtime = 1)
    return msg


def send_mail(from_user, to_users, subject, text):
    smtp = smtplib.SMTP_SSL("smtp.daum.net", 465)
    smtp.login("", "")

    for to_user in to_users:
        try:
            msg = make_message(from_user, to_user, subject, text)
            smtp.sendmail(from_user, [to_user], msg.as_string())
            print('OK: {}'.format(to_user))
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            print(e)
            print('FAIL: {}'.format(to_user))
    
    smtp.close()


def read_msg(msgfile):
    msg = ''
    with open(msgfile, 'r') as f:
        msg = f.read()
    
    return msg


def read_to(tofile):
    to_users = []
    with open(tofile, 'r') as f:
        for line in f:
            to_users.append(line.strip())
    return to_users


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-m', '--msgfile', help='Message file', dest='msgfile')
    parser.add_option('-t', '--to', help='To email list', dest='tofile')
    parser.add_option('-f', '--from', help='From', dest='from_user')
    parser.add_option('-n', '--from-name', help='From name', dest='from_name')
    parser.add_option('-s', '--subject', help='Subject', dest='subject')
    (options, args) = parser.parse_args()
    
    if options.msgfile is None or options.tofile is None:
        parser.print_help()
        exit(1)

    msg = read_msg(options.msgfile)
    to_users = read_to(options.tofile)

    send_mail(
        options.from_user,
        to_users,
        options.subject,
        msg
    )
