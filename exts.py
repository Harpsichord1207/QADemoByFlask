#!/usr/bin/env python  
# -*- coding:utf-8 -*- 

""" 
@version: v1.0 
@author: Harp
@contact: liutao25@baidu.com 
@software: PyCharm 
@file: exts.py 
@time: 2018/1/15 0015 21:10 
"""

from models import Users
from werkzeug.security import check_password_hash


def validate_login_register(username, password1, password2=None):
    user = Users.query.filter(Users.username == username).first()
    if password2:
        if user:
            return '用户名已经存在'
        else:
            if len(username) < 4:
                return '用户名长度至少4个字符'
            elif password1 != password2:
                return '两次密码不一致'
            elif len(password1) < 6:
                return '密码长度至少6个字符'
            else:
                return '注册成功，请登录'
    else:
        if user:
            if check_password_hash(user.password, password1):
                return '登录成功'
            else:
                return '密码错误'
        else:
            return '用户名不存在'


def validate_change_password(user, o_password, password1, password2):
    if check_password_hash(user.password, o_password):
        if password1 != password2:
            return '两次密码不一致'
        elif len(password1) < 6:
            return '密码长度至少6个字符'
        else:
            return '密码修改成功，请重新登录'
    else:
        return '原始密码错误'


if __name__ == "__main__":
    pass
