#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/25 上午11:40
# @Author  : Leon
# @Site    :
# @File    : launcher_celery.py
# @Software: PyCharm
# @Description:
from celery import Celery

celery_app = Celery(include=["celery_program.celery_tasks"])

celery_app.config_from_object("celery_program.celery_config")

if __name__ == '__main__':
    celery_app.start()
