#!/usr/bin/env python  
# -*- coding:utf-8 -*- 

""" 
@version: v1.0 
@author: Harp
@contact: liutao25@baidu.com 
@software: PyCharm 
@file: models.py 
@time: 2018/1/13 0013 22:30 
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    register_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    avatar_path = db.Column(db.String(256), nullable=False, default='images/doraemon.jpg')


class Questions(db.Model):
    __tablename__ = 'questions_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.TEXT, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users_info.id'))
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    author = db.relationship('Users', backref=db.backref('questions', order_by=create_time.desc()))


# TODO: create_time does not change
# https://www.jianshu.com/p/20f5e4812477
class Comments(db.Model):
    __tablename__ = 'comments_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.TEXT, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions_info.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users_info.id'))
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    author = db.relationship('Users', backref=db.backref('comments'))
    question = db.relationship('Questions', backref=db.backref('comments', order_by=create_time.desc()))
