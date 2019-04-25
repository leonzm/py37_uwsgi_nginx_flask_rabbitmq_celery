#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/25 上午11:40
# @Author  : Leon
# @Site    :
# @File    : collect.py
# @Software: PyCharm
# @Description:
import time

# 日志级别
LEVEL_ID_DEBUG = 1
LEVEL_ID_INFO = 2
LEVEL_ID_WARN = 3
LEVEL_ID_ERROR = 4

COLLECT_TYPE_INFO = 1  # 普通
COLLECT_TYPE_FORMAT_COUNT = 2  # 格式化统计
COLLECT_TYPE_API_CALL = 3  # 接口调用
COLLECT_TYPE_SAMPLE_PACKAGE = 4  # 打抽样包
COLLECT_TYPE_SAMPLE = 5  # 抽样记录


class Collect(object):

    def __init__(self, user, sender, level_id, task_id, collect_type, ip, message):
        if not isinstance(user, str):
            raise TypeError('user must be a str')
        if not isinstance(level_id, int):
            raise TypeError('level id must be a int')
        if task_id is not None and not isinstance(task_id, str):  # task_id 可为空
            raise TypeError('task id must be a str')
        if not isinstance(collect_type, int):
            raise TypeError('collect type must be a int')
        if not isinstance(ip, str):
            raise TypeError('ip must be a str')
        if not isinstance(message, str):
            raise TypeError('message must be str')

        self._user = user
        self._sender = sender
        self._level_id = level_id
        self._task_id = task_id
        self._collect_type = collect_type
        self._ip = ip
        self._message = message
        self._create_time = int(time.time() * 1000)

    def to_dict(self):
        return {
            'user': self._user,
            'sender': self._sender,
            'level_id': self._level_id,
            'task_id': self._task_id,
            'collect_type': self._collect_type,
            'ip': self._ip,
            'message': self._message,
            'create_time': self._create_time
        }


class SampleLog(object):
    def __init__(self, day, total_num, channel_id, subtask, send_day, package_num, remarks=''):
        if not isinstance(day, str):
            raise TypeError('day must be a str')
        if not isinstance(total_num, int):
            raise TypeError('total_num must be a int')
        if not isinstance(channel_id, str):
            raise TypeError('channel_id must be a str')
        if not isinstance(subtask, list):
            raise TypeError('subtask must be list')
        if not isinstance(package_num, int):
            raise TypeError('package_num must be int')

        self.day = day
        self.total_num = total_num
        self.channel_id = channel_id
        self.subtask = subtask
        self.send_day = send_day
        self.package_num = package_num
        self.remarks = remarks

    def to_dict(self):
        return {
            'day': self.day,
            'total_num': self.total_num,
            'channel_id': self.channel_id,
            'subtask': self.subtask,
            'send_day': self.send_day,
            'package_num': self.package_num,
            'remarks': self.remarks
        }


if __name__ == '__main__':
    c = Collect(user='sys', sender='model.collect.main', level_id=LEVEL_ID_INFO, task_id='',
                collect_type=COLLECT_TYPE_INFO,
                ip='127.0.0.1', message='日志测试')
    print(c.to_dict())
    pass
