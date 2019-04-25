#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/25 上午11:40
# @Author  : Leon
# @Site    :
# @File    : celery_config.py
# @Software: PyCharm
# @Description:
import config.config as config
# from celery.schedules import crontab, timedelta


BROKER_URL = 'amqp://%s:%s@%s:%s/%s' % (config.RMQ_BROKER_USER,
                                        config.RMQ_BROKER_PASS,
                                        config.RMQ_BROKER_IP,
                                        config.RMQ_BROKER_PORT,
                                        config.RMQ_BROKER_VHOST)


CELERY_QUEUE_HA_POLICY = 'all'
CELERY_ACKS_LATE = True
CELERY_RESULT_PERSISTENT = True
CELERYD_PREFETCH_MULTIPLIER = 1

CELERYD_CONCURRENCY = 12
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True

#CELERYBEAT_SCHEDULE = {
    # 'auto_hello_test': {
    #     'task': 'hello_test',
    #     'schedule': timedelta(seconds=10000),
    #     'args': ['AutoHelloName']
    # }
    # 'test_celery_beat_submit_task': {
    #      'task': 'celery_beat_submit_task',
    #      'schedule': timedelta(seconds=4),
    #      'args': ['celery_say_hello', 'AutoHelloName']
    # }
#}

CELERYBEAT_SCHEDULE = config.CELERYBEAT_SCHEDULE
