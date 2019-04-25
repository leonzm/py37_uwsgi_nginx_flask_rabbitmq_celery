#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/25 上午11:40
# @Author  : Leon
# @Site    :
# @File    : celery_task_po.py
# @Software: PyCharm
# @Description:
import time
from utils.commont_util import get_localhost_ip


# 任务状态，依次为：创建、运行、运行结束、运行异常、取消、中断
TASK_STATUS_CREATE = 1
TASK_STATUS_RUN = 2
TASK_STATUS_FISH = 3
TASK_STATUS_EXCEPTION = 4
TASK_STATUS_CANCEL = 5
TASK_STATUS_INTERRUPT = 6


class CeleryTaskPO:

    def __init__(self, task_id=None, task_name=None, task_params_args=None, task_params_kwargs=None, task_error='', task_status=TASK_STATUS_CREATE,
                 task_countdown=0):
        if not isinstance(task_id, str):
            raise TypeError('task id must be a str')
        if not isinstance(task_name, str):
            raise TypeError('task name must be a str')
        if task_params_args is not None and not isinstance(task_params_args, tuple):
            raise TypeError('task params must be a tuple')
        if task_params_kwargs is not None and not isinstance(task_params_kwargs, dict):
            raise TypeError('task params kwargs must be a dict')
        if not isinstance(task_status, int):
            raise TypeError('task status must be an int')
        if not isinstance(task_error, str):
            raise TypeError('task error must be a str')
        if not isinstance(task_countdown, int):
            raise TypeError('task countdown must be an int')

        self._task_id = task_id
        self._task_name = task_name
        self._task_params_args = task_params_args
        self._task_params_kwargs = task_params_kwargs
        self._task_status = task_status
        self._task_error = task_error
        self._task_countdown = task_countdown
        self._task_progress = 0
        self._ip = get_localhost_ip()
        self._create_time = int(time.time() * 1000)
        self._update_time = self._create_time

    @property
    def task_id(self):
        return self._task_id

    @task_id.setter
    def task_id(self, value):
        if not isinstance(value, str):
            raise TypeError('task id must be a str')
        self._task_id = value

    @property
    def task_name(self):
        return self._task_name

    @task_name.setter
    def task_name(self, value):
        if not isinstance(value, str):
            raise TypeError('task name must be a str')
        self._task_name = value

    @property
    def task_params_args(self):
        return self._task_params_args

    @task_params_args.setter
    def task_params_args(self, value):
        if value is not None and not isinstance(value, tuple):
            raise TypeError('task params args must be a tuple')
        self._task_params_args = value

    @property
    def task_params_kwargs(self):
        return self._task_params_kwargs

    @task_params_kwargs.setter
    def task_params_kwargs(self, value):
        if value is not None and not isinstance(value, tuple):
            raise TypeError('task params kwargs must be a dict')
        self._task_params_kwargs = value

    @property
    def task_status(self):
        return self._task_status

    @task_status.setter
    def task_status(self, value):
        if not isinstance(value, int):
            raise TypeError('task status must be a int')
        self._task_status = value

    @property
    def task_error(self):
        return self._task_error

    @task_error.setter
    def task_error(self, value):
        if not isinstance(value, str):
            raise TypeError('task error must be a str')
        self._task_error = value

    @property
    def task_countdown(self):
        return self._task_countdown

    @property
    def task_progress(self):
        return self._task_progress

    @task_progress.setter
    def task_progress(self, value):
        if not isinstance(value, int):
            raise TypeError('task progress must be a int')
        if value < 0 or value > 100:
            raise TypeError('task progress must >= 0 and <= 100')
        self._task_progress = value

    @property
    def update_time(self):
        return self._update_time

    @update_time.setter
    def update_time(self, value):
        if not isinstance(value, int):
            raise TypeError('update time  must be a int')
        self._update_time = value

    @property
    def ip(self):
        return self._ip

    @property
    def create_time(self):
        return self._create_time


def to_dict(task_obj):
    return {
        'task_id': task_obj.task_id,
        'task_name': task_obj.task_name,
        'task_params_args': task_obj.task_params_args,
        'task_params_kwargs': task_obj.task_params_kwargs,
        'task_status': task_obj.task_status,
        'task_error': task_obj.task_error,
        'task_countdown': task_obj.task_countdown,
        'task_progress': task_obj.task_progress,
        'ip': task_obj.ip,
        'create_time': task_obj.create_time,
        'update_time': task_obj.update_time
    }

if __name__ == '__main__':
    pass
