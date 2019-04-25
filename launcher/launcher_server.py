#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/24 上午10:26
# @Author  : Leon
# @Site    :
# @File    : launcher_server.py
# @Software: PyCharm
# @Description:
import time
from config import config
from api.api_suppert import api_code
from config.flask_config import flask_app
from api.api_suppert.api_template import response_json, success, fail
from api.api_services import api_test, api_task

# 项目信息
PROJECT_NAME = 'py37_uwsgi_nginx_flask_rabbitmq_celery'
PROJECT_VERSION = 'V1.00.00R1900424'
PROJECT_START_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


@flask_app.route("/")
@response_json
def server_index():
    return success().put('project_name', PROJECT_NAME).put('project_version', PROJECT_VERSION) \
        .put('project_envi', config.environment).put('start_time', PROJECT_START_TIME) \
        .put('now', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


@flask_app.errorhandler(404)
@response_json
def server_not_found(error):
    return fail(api_code.SERVER_NOT_EXIST)


@flask_app.errorhandler(500)
@response_json
def server_error(error):
    return fail(api_code.ERROR)


if __name__ == '__main__':
    flask_app.run(host="0.0.0.0", port=config.flask_port)
