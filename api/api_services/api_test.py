#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/24 上午10:35
# @Author  : Leon
# @Site    : 
# @File    : api_test.py
# @Software: PyCharm
# @Description:
from config.flask_config import flask_app
from api.api_suppert.api_template import response_json, success
# from api.api_suppert.api_code import PARAMETERS_INCORRECT, NOT_EXIST, RESOURCE_EXPIRE


@flask_app.route('/test/hello/<name>', methods=['GET'])
@response_json
def hello(name):
    return success().put('result', 'Hello {}'.format(name))
