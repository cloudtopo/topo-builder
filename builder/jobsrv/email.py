#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
进程相关函数封装
Copyright 2009 Cloudtopo
"""

import smtplib
from builder.jobsrv.util import StrUtil,FileUtil

def send_email(fromaddr, toaddrs, server, port, login, password, subject, text, attachment=None, tls=False):
    if StrUtil.empty_str(server):
        return
    
    #支持多种邮件列表格式
    if not isinstance(toaddrs, list):
        if toaddrs.find(";") != -1:
            toaddrs = toaddrs.split(";")
        elif toaddrs.find(",") != -1:
            toaddrs = toaddrs.split(",")
        else:
            toaddrs = toaddrs.split(" ")
                     
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
           % (fromaddr, ", ".join(toaddrs), subject) )
    msg += text

    server = smtplib.SMTP(server, port)
    #server.set_debuglevel(1)
    server.ehlo()
    if tls:
        server.starttls()
    if login != "":
        server.login(login, password)
    
    server.sendmail(fromaddr, toaddrs, msg.encode("utf-8"))
    server.quit()
        