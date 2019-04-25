#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
from config.log import LOG
from pymongo import MongoClient
from pymongo import ReadPreference

db_pool = {}


class MongodbUtils(object):
    def __init__(self, collection="", ip="", port=None, database="",
                 replicaset_name="", read_preference=ReadPreference.SECONDARY_PREFERRED):

        self.collection = collection
        self.ip = ip
        self.port = port
        self.database = database
        self.replicaset_name = replicaset_name
        self.read_preference = read_preference

        if (ip, port) not in db_pool:
            db_pool[(ip, port)] = self.db_connection()
        elif not db_pool[(ip, port)]:
            db_pool[(ip, port)] = self.db_connection()

        self.db = db_pool[(ip, port)]
        self.db_table = self.db_table_connect()

    def __enter__(self):
        return self.db_table

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def db_connection(self):
        db = None
        try:
            if self.replicaset_name:
                # 当pymongo更新到3.x版本, 连接副本集的方法得用MongoClient, 如果版本<=2.8.1的, 得用MongoReplicaSetClient
                db = MongoClient(self.ip, read_preference=self.read_preference, replicaset=self.replicaset_name, connect=False)
            else:
                db = MongoClient(self.ip, self.port, connect=False)

        except Exception as e:
            LOG.error(traceback.format_exc())
        return db

    def db_table_connect(self):
        table_db = self.db[self.database][self.collection]
        return table_db


if __name__ == "__main__":
    pass
