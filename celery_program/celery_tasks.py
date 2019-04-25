#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/25 上午11:40
# @Author  : Leon
# @Site    : 
# @File    : celery_tasks.py
# @Software: PyCharm
# @Description:
import sys
sys.path.append("./")
import time
from config.log import LOG
from launcher.launcher_celery import celery_app
from utils.decorator_tools import celery_task_cancel_check
from utils.celery_util import gw_delay, async_update_task_progress, task_is_interrupt


@celery_app.task(name="celery_beat_submit_task", bind=True)
def celery_beat_submit_task(self, task_name, *args, **kwargs):
    """
    给 celery beat 使用，所以不加 @celery_task_cancel_check。该任务负责用任务封装函数来提交任务函数
    :param self:
    :param task_name:
    :param args:
    :param kwargs:
    :return:
    """
    if task_name is None or task_name == '':
        raise TypeError('task name must be a str')
    if not task_name in celery_task_function_name_function_map:
        raise TypeError('task[%s] not exit' % task_name)
    gw_delay(celery_task_function_name_function_map[task_name], *args, **kwargs)
    # print('celery beat 提交任务：%s' % task_name
    LOG.info('celery beat submit task: %s' % task_name)


@celery_app.task(name="hello_test", bind=True)
@celery_task_cancel_check
def celery_say_hello(self, name, sum):
    """
    hello 测试
    :param self:
    :param name:
    :param sum: 迭代次数
    :return:
    """
    task_id = str(self.request.id)
    i = 0
    while i < sum and not task_is_interrupt(task_id):
        if name is None or name == '':
            print('Hello 佚名 - %d' % i)
        else:
            print('Hello %s - %d' % (name, i))

        i += 1
        async_update_task_progress(task_id, i * 100 / sum)
        time.sleep(1)


# 函数名和函数的对应关系，给 celery beat 任务调用
celery_task_function_name_function_map = {
    'celery_say_hello': celery_say_hello
}

