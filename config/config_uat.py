#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/24 上午10:26
# @Author  : Leon
# @Site    : 
# @File    : config.py
# @Software: PyCharm
# @Description:
from pymongo import ReadPreference
# from celery.schedules import crontab, timedelta

flask_port = 5004
environment = 'UAT'
environment_name = 'UAT'

# Rabbitmq 配置
RMQ_BROKER_IP = "127.0.0.1"
RMQ_BROKER_PORT = "5672"
RMQ_BROKER_VHOST = "leon"
RMQ_BROKER_USER = "leon"
RMQ_BROKER_PASS = "123456"

# mongo 库
DB_REPLICA_IP = "127.0.0.1"
DB_REPLICA_DATABASE = "db_test"
DB_TASK_COLLECTION = "celery_task"
DB_COLLECT_COLLECTION = 'collect'
DB_COLLECT_DB_CONFIG = 'db_config'
DB_REPLICA_READ_PREFERENCE = ReadPreference.PRIMARY

# 定时任务
CELERYBEAT_SCHEDULE = {
    # 'test_celery_beat_submit_task': {
    #     'task': 'celery_beat_submit_task',
    #     'schedule': crontab(hour=19, minute=30),
    #     'args': ['celery_say_hello', 'AutoHelloName', 100]
    # }
}
