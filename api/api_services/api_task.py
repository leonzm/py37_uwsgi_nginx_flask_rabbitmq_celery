#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/20 上午9:56
# @Author  : Leon
# @Site    :
# @File    : api_task.py
# @Software: PyCharm
# @Description:
import re
import json
import time
import pymongo
from config.log import LOG
from model import celery_task_po
from model.collect import COLLECT_TYPE_API_CALL
from utils.collect_util import COLLECT_LOG
from config.flask_config import flask_app
from config import config
from utils.mongodb_util import MongodbUtils
from api.api_suppert.api_template import response_json, success, fail
from api.api_suppert.api_code import PARAMETERS_INCORRECT, NOT_EXIST, RESOURCE_EXPIRE
from flask import request
from utils.celery_util import gw_delay, gw_apply_async
from celery_program.celery_tasks import celery_say_hello, celery_task_function_name_function_map


@flask_app.route('/task/celery_task/<start_time>/<end_time>/<page_index>/<page_size>', methods=['GET'])
@response_json
def get_celery_task(start_time, end_time, page_index, page_size):
    """
    抽任务信息查询，必选参数：start_time、end_time、page_index、page_size，可选参数：task_id、sample_id、task_status
    :param start_time:
    :param end_time:
    :param page_index: 当前页码
    :param page_size: 每页条数
    :return:
    """
    if not re.match(r'\d{13}', start_time):
        return fail(code_obj=None, code=PARAMETERS_INCORRECT.code, note='start_time %s，必须是13位的时间戳' %
                                                                        PARAMETERS_INCORRECT.note)
    if not re.match(r'\d{13}', end_time):
        return fail(code_obj=None, code=PARAMETERS_INCORRECT.code, note='end_time %s，必须是13位的时间戳' %
                                                                        PARAMETERS_INCORRECT.note)
    if not re.match(r'\d+', page_index):
        return fail(code_obj=None, code=PARAMETERS_INCORRECT.code, note='page_index %s，必须是整数' %
                                                                        PARAMETERS_INCORRECT.note)
    if not re.match(r'\d+', page_size):
        return fail(code_obj=None, code=PARAMETERS_INCORRECT.code, note='page_size %s，必须是整数' %
                                                                        PARAMETERS_INCORRECT.note)
    task_id = request.args.get('task_id', '')
    sample_id = request.args.get('sample_id', '')
    task_status = request.args.get('task_status', '')
    order_by = request.args.get('orderBy', '')
    sortor = pymongo.DESCENDING
    if order_by == 'asc':
        sortor = pymongo.ASCENDING

    if task_status != '' and not re.match(r'\d+', task_status):
        return fail(code_obj=None, code=PARAMETERS_INCORRECT.code, note='task_status %s，必须是整数' %
                                                                        PARAMETERS_INCORRECT.note)

    with MongodbUtils(ip=config.DB_REPLICA_IP, database=config.DB_REPLICA_DATABASE,
                      collection=config.DB_TASK_COLLECTION) as conn_task:
        selector = {'create_time': {'$gte': int(start_time), '$lte': int(end_time)}}
        if task_id != '':
            selector['task_id'] = task_id
        if sample_id != '':
            selector['sample_id'] = sample_id
        if task_status != '':
            selector['task_status'] = int(task_status)

        cursor_task = conn_task.find(selector).sort('create_time', sortor)
        count = cursor_task.count()
        cursor_task.skip((int(page_index) - 1) * int(page_size))
        result = []
        for sample_info in cursor_task:
            result.append(sample_info)
            if len(result) >= int(page_size):
                break
        cursor_task.close()

        if len(result) == 0:
            return fail(NOT_EXIST)

        return success().put('result', result).put('count', count) \
            .put('total_pages', count / int(page_size) + (count % int(page_size) > 0 and 1 or 0)) \
            .put('page_index', int(page_index)) \
            .put('page_size', int(page_size))


@flask_app.route('/task/celery_task', methods=['GET'])
@response_json
def get_celery_task_by_task_ids():
    """
    根据任务 ID 集合，查询任务信息
    :return:
    """
    task_ids = request.args.get('task_ids', '')
    if task_ids == '':
        return fail(code_obj=None, code=PARAMETERS_INCORRECT.code, note='task_ids' % PARAMETERS_INCORRECT.note)

    task_id_list = []
    for s in task_ids.split(','):
        if s.strip() != '':
            task_id_list.append(s.strip())

    with MongodbUtils(ip=config.DB_REPLICA_IP, database=config.DB_REPLICA_DATABASE,
                      collection=config.DB_TASK_COLLECTION) as conn_task:
        selector = {'task_id': {'$in': task_id_list}}
        cursor_task = conn_task.find(selector).sort('create_time', pymongo.ASCENDING)
        result = []
        for task_info in cursor_task:
            result.append(task_info)

        if len(result) == 0:
            return fail(NOT_EXIST)

        return success().put('result', result).put('count', len(result))


@flask_app.route('/task/celery_task/cancel/<user_id>', methods=['POST'])
@response_json
def cancel_celery_task(user_id):
    """
    根据任务 ID 取消任务，只能取消状态为"创建"的任务
    :return:
    """
    task_id = request.form['task_id']
    if task_id is None or task_id == '':
        return fail(code_obj=None, code=PARAMETERS_INCORRECT.code, note='task_id' % PARAMETERS_INCORRECT.note)

    task_id = task_id.encode('utf-8')
    with MongodbUtils(ip=config.DB_REPLICA_IP, database=config.DB_REPLICA_DATABASE,
                      collection=config.DB_TASK_COLLECTION) as conn_task:
        selector = {'task_id': task_id}
        task_info = conn_task.find_one(selector)

        if task_info is None:
            return fail(NOT_EXIST)

        if task_info['task_status'] != celery_task_po.TASK_STATUS_CREATE:
            return fail(code_obj=None, code=RESOURCE_EXPIRE.code, note='该任务不是"创建"状态，不能被取消')

        conn_task.update({'task_id': task_id}, {
            '$set': {'task_status': celery_task_po.TASK_STATUS_CANCEL, 'update_time': int(time.time() * 1000)}})
        # 记录日志
        message = json.dumps({'task_id': task_id})
        COLLECT_LOG.info(user=user_id, sender='api.api_services.api_task.cancel_celery_task', task_id=task_id,
                         collect_type=COLLECT_TYPE_API_CALL, message=message)

        return success()


@flask_app.route('/task/celery_task/interrupt/<user_id>', methods=['POST'])
@response_json
def interrupt_celery_task(user_id):
    """
    根据任务 ID 中断任务，只能中断状态为"运行"的任务
    :return:
    """
    task_id = request.form['task_id']
    if task_id is None or task_id == '':
        return fail(code_obj=None, code=PARAMETERS_INCORRECT.code, note='task_id' % PARAMETERS_INCORRECT.note)

    task_id = task_id.encode('utf-8')
    with MongodbUtils(ip=config.DB_REPLICA_IP, database=config.DB_REPLICA_DATABASE,
                      collection=config.DB_TASK_COLLECTION) as conn_task:
        selector = {'task_id': task_id}
        task_info = conn_task.find_one(selector)

        if task_info is None:
            return fail(NOT_EXIST)

        if task_info['task_status'] != celery_task_po.TASK_STATUS_RUN:
            return fail(code_obj=None, code=RESOURCE_EXPIRE.code, note='该任务不是"运行"状态，不能被中断')

        conn_task.update({'task_id': task_id}, {
            '$set': {'task_status': celery_task_po.TASK_STATUS_INTERRUPT, 'update_time': int(time.time() * 1000)}})
        # 记录日志
        message = json.dumps({'task_id': task_id})
        COLLECT_LOG.info(user=user_id, sender='api.api_services.api_task.interrupt_celery_task', task_id=task_id,
                         collect_type=COLLECT_TYPE_API_CALL, message=message)

        return success()


@flask_app.route('/task/add/say_hello/<user_id>', methods=['GET'])
@response_json
def add_say_hello(user_id):
    name = request.args.get('name', 'default')
    str_sum = request.args.get('sum', '10')
    countdown = int(request.args.get('countdown', '0'))
    if not re.match(r'\d+', str_sum):
        return fail(code_obj=None, code=PARAMETERS_INCORRECT.code, note='sum %s，必须是正整数' % PARAMETERS_INCORRECT.note)
    _sum = int(str_sum)
    # task_id = gw_delay(celery_say_hello, name=name)
    task_id = gw_apply_async(celery_say_hello, countdown=countdown, kwargs={'name': name, 'sum': _sum})
    LOG.info('Add say_hello task')

    # 记录日志
    message = json.dumps({'name': name, 'countdown': countdown})
    COLLECT_LOG.info(user=user_id, sender='api.api_services.api_task.add_hello_test', task_id=task_id,
                     collect_type=COLLECT_TYPE_API_CALL, message=message)
    return success().put('result', task_id)


@flask_app.route('/task/add/<task_name>/<user_id>', methods=['GET'])
@response_json
def add_celery_common(task_name, user_id):
    """
    通用 celery 任务提交服务

    :param task_name:
    :param user_id:
    :return:
    """
    args = dict(request.args)
    countdown = int(request.args.get('countdown', '0'))
    kwargs = args.copy()
    if 'countdown' in args:
        args.pop('countdown')

    if task_name not in celery_task_function_name_function_map:
        return fail(NOT_EXIST)

    task_id = gw_apply_async(celery_task_function_name_function_map.get(task_name), countdown=countdown, kwargs=args)
    LOG.info('Add {} task'.format(task_name))

    # 记录日志
    COLLECT_LOG.info(user=user_id, sender='api.api_services.api_task.add_celery_common', task_id=task_id,
                     collect_type=COLLECT_TYPE_API_CALL, message=json.dumps(kwargs))
    return success().put('result', task_id)
