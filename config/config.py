#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/24 上午10:26
# @Author  : Leon
# @Site    : 
# @File    : config.py
# @Software: PyCharm
# @Description:
# from celery.schedules import crontab, timedelta

flask_port = 5004
environment = 'default'
environment_name = u'本地'

# 定时任务
CELERYBEAT_SCHEDULE = {
    # 'test_celery_beat_submit_task': {
    #     'task': 'celery_beat_submit_task',
    #     'schedule': crontab(hour=19, minute=30),
    #     'args': ['celery_say_hello', 'AutoHelloName', 100]
    # }
}
