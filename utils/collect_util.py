#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config import config
from model.collect import Collect, LEVEL_ID_DEBUG, LEVEL_ID_INFO, LEVEL_ID_WARN, LEVEL_ID_ERROR, COLLECT_TYPE_INFO, \
    COLLECT_TYPE_FORMAT_COUNT
from utils.mongodb_util import MongodbUtils
from utils.commont_util import get_localhost_ip


class CollectUtil(object):

    def __init__(self):
        self._collect_conn = MongodbUtils(ip=config.DB_REPLICA_IP, database=config.DB_REPLICA_DATABASE,
                                          collection=config.DB_COLLECT_COLLECTION,
                                          read_preference=config.DB_REPLICA_READ_PREFERENCE).db_table_connect()

    def _save_collect(self, user, sender, level_id, task_id, collect_type, message):
        if task_id is None:
            task_id = ''
        collect = Collect(user=user, sender=sender, level_id=level_id, task_id=task_id, collect_type=collect_type,
                          ip=get_localhost_ip(), message=message)
        self._collect_conn.insert(collect.to_dict())

    def debug(self, user, sender, task_id, collect_type, message):
        self._save_collect(user=user, sender=sender, level_id=LEVEL_ID_DEBUG, task_id=task_id,
                           collect_type=collect_type, message=message)

    def info(self, user, sender, task_id, collect_type, message):
        self._save_collect(user=user, sender=sender, level_id=LEVEL_ID_INFO, task_id=task_id,
                           collect_type=collect_type, message=message)

    def warn(self, user, sender, task_id, collect_type, message):
        self._save_collect(user=user, sender=sender, level_id=LEVEL_ID_WARN, task_id=task_id,
                           collect_type=collect_type, message=message)

    def error(self, user, sender, task_id, collect_type, message):
        self._save_collect(user=user, sender=sender, level_id=LEVEL_ID_ERROR, task_id=task_id,
                           collect_type=collect_type, message=message)

COLLECT_LOG = CollectUtil()

if __name__ == '__main__':
    COLLECT_LOG.debug('sys', 'util.collect_util.main', '', COLLECT_TYPE_INFO, '普通 debug 日志.')
    COLLECT_LOG.info('sys', 'util.collect_util.main', '', COLLECT_TYPE_INFO, '普通 info 日志.')
