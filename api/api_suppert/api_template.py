#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/24 上午10:26
# @Author  : Leon
# @Site    :
# @File    : api_template.py
# @Software: PyCharm
# @Description:
import json
import functools
from utils.json_format import CJsonEncoder
from flask import make_response
from api.api_suppert.api_code import SUCCESS


class JsonReturn(dict):
    def __init__(self, is_success, code, note):
        if not isinstance(is_success, bool):
            raise TypeError('\'is_success\' must be bool')
        if not isinstance(code, int):
            raise TypeError('\'code\' must be int')
        if not isinstance(note, str):
            raise TypeError('\'note\' must be str')
        self['success'] = is_success
        self['code'] = code
        self['note'] = note

    def __str__(self):
        return json.dumps(self, cls=CJsonEncoder)

    def add(self, key, value):
        self[key] = value
        return self

    def put(self, key, value):
        self[key] = value
        return self

    def to_json(self):
        return json.dumps(self, cls=CJsonEncoder)

    @property
    def success(self):
        return self['success']

    @success.setter
    def success(self, value):
        if not isinstance(value, bool):
            raise TypeError('\'success\' must be bool')
        self['success'] = value

    @property
    def code(self):
        return self['code']

    @code.setter
    def code(self, value):
        if not isinstance(value, int):
            raise TypeError('\'code\' must be int')
        self['code'] = value

    @property
    def note(self):
        return self['note']

    @note.setter
    def note(self, value):
        if not isinstance(value, str):
            raise TypeError('\'note\' must be str')
        self['note'] = value


def __create__(is_success, code, note):
    return JsonReturn(is_success, code, note)


def success(code_obj=SUCCESS, code=SUCCESS.code, note=SUCCESS.note):
    if code_obj is not None:
        return __create__(True, code_obj.code, code_obj.note)
    return __create__(True, code, note)


def fail(code_obj=None, code=None, note=None, exception=None):
    if code_obj is not None:
        json_return = __create__(False, code_obj.code, code_obj.note)
    else:
        json_return = __create__(False, code, note)
    if exception is not None and isinstance(exception, BaseException):
        json_return['stack'] = repr(exception)
    return json_return


def response_json(func):
    """
    Rest 返回封装
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        # 跨域设置
        headers = {'Access-Control-Allow-Origin': '*',
                   'Access-Control-Allow-Methods': 'HEAD, OPTIONS, GET, POST, DELETE, PUT',
                   'Access-Control-Allow-Headers': 'Content-Type'}
        if isinstance(res, JsonReturn):
            return make_response(res.to_json(), 200, headers)
        elif isinstance(res, dict):
            return make_response(json.dumps(res, cls=CJsonEncoder), 200, headers)
        else:
            return res
    return wrapper


if __name__ == '__main__':
    pass
