#!/usr/bin/env python  
# -*- coding:utf-8 -*- 

""" 
@version: v1.0 
@author: Harp
@contact: liutao25@baidu.com 
@software: PyCharm 
@file: config.py 
@time: 2018/1/11 0011 11:34 
"""

DEBUG = True

HOST = "127.0.0.1"
PORT = "3306"
DB = "harp"
USER = "root"
PASS = "123456"
CHARSET = "utf8"
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset={}".format(USER, PASS, HOST, PORT, DB, CHARSET)
SQLALCHEMY_DATABASE_URI = DB_URI

SECRET_KEY = "THIS-A-SECRET-KEY"

MAX_CONTENT_LENGTH = 1 * 1024 * 1024
