#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/24 上午10:26
# @Author  : Leon
# @Site    :
# @File    : api_code.py
# @Software: PyCharm
# @Description:


class Code(object):
    def __init__(self, code, note):
        if not isinstance(code, int):
            raise TypeError('\'code\' must be int')
        if not isinstance(note, str):
            raise TypeError('\'note\' must be str')
        self.__code__ = code
        self.__note__ = note

    @property
    def code(self):
        return self.__code__

    @property
    def note(self):
        return self.__note__

    def __str__(self):
        return '{"code": "%d", "note": "%s"}' % (self.__code__, self.__note__)


SUCCESS = Code(200, '')
PARAMETERS_INCORRECT = Code(400, '参数不正确')
PARAMETERS_INVALID = Code(401, '特定参数不符合条件(eg:没有这个用户)')
SAVE_FAIL = Code(402, '保存失败')
CHECK_FAIL = Code(403, '检验不通过')
NOT_EXIST = Code(404, '该资源不存在')
RESOURCE_USED = Code(405, '资源已经使用过')
RESOURCE_EXPIRE = Code(406, '资源已经过期')
SERVER_NOT_EXIST = Code(407, '该服务不存在')
SERVER_OVERLOAD = Code(408, '该服务使用达到上限')

ERROR = Code(500, '执行错误')
AUTHENTICATION_FAIL = Code(501, '认证失败')
ROLES_FAIL = Code(502, '授权失败')
SESSION_EXPIRATION = Code(503, 'Session 过期')
SESSION_LOSE = Code(504, 'Session 丢失')
