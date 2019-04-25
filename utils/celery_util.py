#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/25 上午11:40
# @Author  : Leon
# @Site    :
# @File    : celery_util.py
# @Software: PyCharm
# @Description:
import time
import threading
from config.log import LOG
from config import config
from pymongo import ReadPreference
from utils.commont_util import in_async
from utils.mongodb_util import MongodbUtils
from model.celery_task_po import CeleryTaskPO, to_dict, TASK_STATUS_CREATE, TASK_STATUS_RUN, TASK_STATUS_INTERRUPT


# 维护当前机器发起的任务状态信息
CURRENT_TASK_STATUS_DICT = {}  # <task_id, task_status>
TASK_STATUS_MONITOR = False  # 是否已经启动监控

# 任务进度缓存，用于和上一次进度比较，如果小于最小步长，就不更新，避免频繁更新数据库
CURRENT_TASK_PROGRESS_DICT = {}  # <task_id, task_progress>
TASK_PROGRESS_UPDATE_MIN = 2


def update_current_task_status_dict():
    """
    每10秒更新一次任务状态信息，超过3天的移除
    :return:
    """
    while True:
        task_id_list = []
        for task_id in CURRENT_TASK_STATUS_DICT.keys():
            task_id_list.append(task_id)
        # LOG.info('任务状态缓存队列大小：%d' % len(task_id_list))
        if len(task_id_list) > 0:
            try:
                with MongodbUtils(ip=config.DB_REPLICA_IP, database=config.DB_REPLICA_DATABASE,
                                  collection=config.DB_TASK_COLLECTION,
                                  read_preference=ReadPreference.PRIMARY) as conn_task:
                    cursor_task = conn_task.find({'task_id': {'$in': task_id_list}})
                    for task_info in cursor_task:
                        if task_info['create_time'] + 3 * 24 * 60 * 60 * 1000 < int(time.time() * 1000):
                            CURRENT_TASK_STATUS_DICT.pop(task_info['task_id'].encode('utf-8'))
                            # LOG.info('任务[%s]状态缓存移除' % task_info['task_id'].encode('utf-8'))
                            continue
                        CURRENT_TASK_STATUS_DICT[task_info['task_id']] = task_info['task_status']
                        # LOG.info('任务[%s]的状态更新为：%d' % (task_info['task_id'].encode('utf-8'), task_info['task_status']))
                    cursor_task.close()
            except Exception:
                pass

        time.sleep(10)


def start_update_current_task_status_dict():
    """
    启动每10秒更新一次任务状态信息的线程
    :return:
    """
    t = threading.Thread(target=update_current_task_status_dict, name='update_current_task_status_dict')
    t.setDaemon(True)
    t.start()


def task_is_interrupt(task_id):
    """
    读取任务缓存，判断该任务有无被中断
    :param task_id:
    :return:
    """
    global TASK_STATUS_MONITOR
    if not TASK_STATUS_MONITOR:
        TASK_STATUS_MONITOR = True
        start_update_current_task_status_dict()

    str_task_id = task_id

    if str_task_id in CURRENT_TASK_STATUS_DICT:
        if CURRENT_TASK_STATUS_DICT[str_task_id] == TASK_STATUS_INTERRUPT:
            LOG.info('Find task [%s] interrupt' % str_task_id)
            return True
    else:
        # LOG.info('任务[%s]加入任务缓存监控' % str_task_id)
        CURRENT_TASK_STATUS_DICT[str_task_id] = TASK_STATUS_RUN  # 加入缓存，过一会可以查到

    return False


def gw_delay(task, *args, **kwargs):
    """
    提交任务
    :param task:函数名
    :param args:
    :param kwargs:
    :return: 任务 id
    """
    res = task.delay(*args, **kwargs)
    task_id = res.id
    task_name = task.name
    task_params_args = args
    task_params_kwargs = kwargs
    # print '提交任务[id=%s, name=%s]' % (task_id, task_name)
    LOG.info('Add task[id=%s, name=%s]' % (task_id, task_name))
    task_obj = CeleryTaskPO(task_id=task_id, task_name=task_name, task_params_args=task_params_args,
                            task_params_kwargs=task_params_kwargs)
    save_task_obj(task_obj)
    return task_id


def gw_apply_async(task, countdown=0, args=(), kwargs={}, route_name=None, **options):
    """
    提交任务
    :param task:函数名
    :param countdown:指定多少秒后执行任务
    :param args:
    :param kwargs:
    :param route_name:
    :param options:
    :return: 任务 id
    """
    res = task.apply_async(args, kwargs, route_name, countdown=countdown, **options)
    task_id = res.id
    task_name = task.name
    task_params_args = args
    task_params_kwargs = kwargs
    # print '提交任务[id=%s, name=%s]' % (task_id, task_name)
    LOG.info('Add task[id=%s, name=%s]' % (task_id, task_name))
    task_obj = CeleryTaskPO(task_id=task_id, task_name=task_name, task_params_args=task_params_args,
                            task_params_kwargs=task_params_kwargs, task_countdown=countdown)
    save_task_obj(task_obj)
    return task_id


def save_task_obj(task_obj):
    with MongodbUtils(ip=config.DB_REPLICA_IP, database=config.DB_REPLICA_DATABASE,
                      collection=config.DB_TASK_COLLECTION,
                      read_preference=config.DB_REPLICA_READ_PREFERENCE) as task_conn:
        task_conn.insert(to_dict(task_obj))


@in_async
def async_update_task_progress(task_id, task_progress):
    """
    异步更新任务的进度
    :param task_progress:
    :return:
    """
    if isinstance(task_id, str) and task_id != '' and isinstance(task_progress, int) and 0 < task_progress <= 100:
        if task_id not in CURRENT_TASK_PROGRESS_DICT:
            CURRENT_TASK_PROGRESS_DICT[task_id] = task_progress
        elif task_progress - CURRENT_TASK_PROGRESS_DICT[task_id] < TASK_PROGRESS_UPDATE_MIN:  # 低于最小步长不予更新
            return

        with MongodbUtils(ip=config.DB_REPLICA_IP, database=config.DB_REPLICA_DATABASE,
                          collection=config.DB_TASK_COLLECTION) as conn_task:
            selector = {'task_id': task_id}
            task_info = conn_task.find_one(selector)

            if task_info is not None and task_info['task_status'] == TASK_STATUS_RUN and task_info['task_progress'] < task_progress:
                conn_task.update({'task_id': task_id}, {'$set': {'task_progress': task_progress, 'update_time': int(time.time() * 1000)}})
                # LOG.info('任务[%s]进度改为：%d' % (task_id, task_progress))
                CURRENT_TASK_PROGRESS_DICT[task_id] = task_progress
