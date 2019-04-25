#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/25 上午11:40
# @Author  : Leon
# @Site    :
# @File    : decorator_tools.py
# @Software: PyCharm
# @Description:
from config import config
from utils.mongodb_util import MongodbUtils
import functools
from pymongo import DESCENDING
from config.log import LOG
from model.celery_task_po import CeleryTaskPO, TASK_STATUS_CREATE, TASK_STATUS_RUN, TASK_STATUS_FISH, \
    TASK_STATUS_INTERRUPT, TASK_STATUS_CANCEL, TASK_STATUS_EXCEPTION
import traceback
import time
from utils.celery_util import task_is_interrupt


def celery_task_cancel_check(func):
    """
    celery task 装饰器
    1.判断当前任务是否合法
    2.判断当前任务是否被取消，如果已经被取消，就不执行
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kw):
        task_id = args[0].request.id
        task_name = args[0].request.task

        time.sleep(0.1)  # 等待 task 信息更新到库
        # 判断任务是否被取消
        with MongodbUtils(ip=config.DB_REPLICA_IP, database=config.DB_REPLICA_DATABASE,
                          collection=config.DB_TASK_COLLECTION,
                          read_preference=config.DB_REPLICA_READ_PREFERENCE) as task_connection:
            task_cursor = task_connection.find({'task_id': task_id}).sort('update_time', DESCENDING)
            task_obj = None
            if task_cursor.count() > 0:
                task_obj = task_cursor[0]
            task_cursor.close()

            if task_obj is None:
                LOG.info('Task[id=%s, name=%s] not exist, so not run' % (task_id, task_name))
                return None
            if task_obj['task_status'] != TASK_STATUS_CREATE:
                LOG.info('Task[id=%s, name=%s] status is %d，not create of status, so not run' % (task_id, task_name, task_obj['task_status']))
                return None
        LOG.info('Task[id=%s, name=%s] start run' % (task_id, task_name))
        update_task_status(task_connection, task_obj, TASK_STATUS_RUN)
        res = None
        try:
            if (args is None or len(args) == 0) and kw:
                res = func()
            else:
                res = func(*args, **kw)
        except Exception as e:
            # task_obj['task_error'] = e.message
            _error_msg = traceback.format_exc()
            task_obj['task_error'] = _error_msg
            update_task_status(task_connection, task_obj, TASK_STATUS_EXCEPTION)

            raise Exception('调用 task 异常：%s' % _error_msg)
        else:
            update_task_status(task_connection, task_obj, TASK_STATUS_FISH)
        return res

    return wrapper


def update_task_status(task_connection, task_obj, task_status):
    """
    更新任务状态
    :param task_connection:
    :param task_obj:
    :param task_status:
    :return:
    """
    if not task_is_interrupt(task_obj['task_id']):  # 必须该任务没有被中断才可以更新
        task_obj['task_status'] = task_status
        if task_status == TASK_STATUS_FISH:  # 如果任务完成，进度改为100
            task_obj['task_progress'] = 100
        task_obj['update_time'] = int(time.time() * 1000)
        task_connection.update({'_id': task_obj['_id']}, task_obj)
        LOG.info('Task[id=%s, name=%s] status update to %d' % (task_obj['task_id'], task_obj['task_name'], task_status))


if __name__ == '__main__':
   pass
