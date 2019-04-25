#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/24 上午10:26
# @Author  : Leon
# @Site    : 
# @File    : flask_config.py
# @Software: PyCharm
# @Description:
from flask import Flask

flask_app = Flask(__name__)

flask_app.config.update(dict(
    CSRF_ENABLED=True,
    SECRET_KEY='41551b9b2bf84bf099318f44d9ae5f0d'
))
