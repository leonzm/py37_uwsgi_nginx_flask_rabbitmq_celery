#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/25 上午11:40
# @Author  : Leon
# @Site    :
# @File    : common_util.py
# @Software: PyCharm
# @Description:
import re
import socket
import time
import hashlib
import datetime
import pandas as pd
from decimal import Decimal
from threading import Thread


def in_async(func):
    """
    异步开线程调用

    :param func: 被修饰的函数
    :return:
    """
    def wrapper(*args, **kwargs):
        thr = Thread(target=func, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


def get_localhost_ip():
    """
    获取本地 ip (host 的方式)
    :return:
    """
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception as e:
        pass
    return 'Unknown'


def get_diff_today_for_day(diff_days=0):
    """
    取距今多数天的日期
    diff_days = 0，今天
    diff_days = -1，昨天
    diff_days = 1，明天
    :param diff_days:
    :return: yyyy-MM-dd
    """
    return time.strftime("%Y-%m-%d", time.localtime(time.time() + diff_days * 60 * 60 * 24))


def md5(string):
    """
    对字符串进行 md5
    :param string:
    :return:
    """
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()


def invert_dict(d):
    """
    字典反转
    :param d:
    :return:
    """
    return dict((v, k) for k, v in d.iteritems())


def keep_decimal(float_value, decimal_num):
    """
    保留2位小数
    :param float_value:
    :param decimal_num:
    :return:
    """
    if not isinstance(float_value, float) and not isinstance(float_value, int):
        raise TypeError('float_value must be a float or int')
    if not isinstance(decimal_num, int):
        raise TypeError('decimal_num must be a int')
    return float(('%.' + str(decimal_num) + 'f') % float_value)


def save_data_frames_to_excel(sheets, data_frames, file_path):
    """
    保存多个 DataFrame 到 excel
    :param sheets: list/tulp
    :param data_frames: list/tulp
    :param file_path: str，文件路径（xls/xlsx）
    :return:
    """
    if len(sheets) == len(data_frames) and len(sheets) > 0:
        writer = pd.ExcelWriter(file_path)
        for i in range(len(sheets)):
            data_frames[i].to_excel(writer, sheets[i], index=False)
            pass
        writer.save()
        pass
    pass


def percent_to_float(str_percent):
    """
    百分数转换为小数
    :params str_percent: str，字符串形式的百分数表示
    :return: float，对应的小数
    """
    return float(str_percent.replace('%', '')) / 100.0


def decimal_to_percent(decimal_value, max_decimal_number=2):
    """
    小数转百分数
    :param decimal_value: Decimal
    :param max_decimal_number int，小数个数，默认2
    :return:
    """
    if isinstance(decimal_value, int):
        decimal_value = Decimal(decimal_value)
    if isinstance(decimal_value, float):
        decimal_value = Decimal(decimal_value)
    if isinstance(decimal_value, Decimal) and not Decimal.is_nan(decimal_value):
        format_str = '%%.%df%%%%' % max_decimal_number
        return format_str % (100 * decimal_value)
    return None


def str_parameter_check(param_name, param_value, can_null=True, can_empty=True):
    """
    字符串类型的参数检查
    :param param_name: str，参数名
    :param param_value: str，参数值
    :param can_null: bool，是否可以为 None
    :param can_empty: bool，是否可以为 空字符串
    :return:
    """
    if param_value is not None:
        if not isinstance(param_value, str):
            raise TypeError('Parameter of {} must be a str'.format(param_name))
        else:  # str
            if param_value == '' and not can_empty:
                raise TypeError('Parameter of {} must be not empty'.format(param_name))
    else:  # None
        if not can_null:
            raise TypeError('Parameter of {} must be not None'.format(param_name))
    pass


def int_parameter_check(param_name, param_value, can_null=True):
    """
    整形类型的参数检查
    :param param_name: str，参数名
    :param param_value: int，参数值
    :param can_null: bool，是否可以为 None
    :return:
    """
    if param_value is not None:
        if not isinstance(param_value, int):
            raise TypeError('Parameter of {} must be a int'.format(param_name))
    else:  # None
        if not can_null:
            raise TypeError('Parameter of {} must be not None'.format(param_name))
    pass


def decimal_parameter_check(param_name, param_value, can_null=True):
    """
    Decimal 类型的参数检查
    :param param_name: str，参数名
    :param param_value: Decimal，参数值
    :param can_null: bool，是否可以为 None
    :return:
    """
    if param_value is not None:
        if not isinstance(param_value, Decimal):
            raise TypeError('Parameter of {} must be a Decimal'.format(param_name))
    else:  # None
        if not can_null:
            raise TypeError('Parameter of {} must be not None'.format(param_name))
    pass


def date_of_str_parameter_check(param_name, param_value, can_null=True,
                                date_format=r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'):
    """
    字符串类型表达的时间参数检查
    :param param_name: str，参数名
    :param param_value: str，参数值
    :param can_null: bool，是否可以为 None
    :param date_format: str，时间格式的正则要求
    :return:
    """
    if param_value is not None:
        if not isinstance(param_value, str):
            raise TypeError('Parameter of {} must be a str by date'.format(param_name))
        else:
            if not re.match(date_format, param_value):
                raise TypeError('Parameter of {} format error'.format(param_name))
        pass
    else:  # None
        if not can_null:
            raise TypeError('Parameter of {} must be not None'.format(param_name))
    pass


def sql_value_insert_process(record_dict, key, default=None):
    """
    根据字典中的值，转化为数据库插入的 sql 表示
    :param record_dict: dict，表的一条记录
    :param key: str，要处理的字段名
    :param default: 字段的默认值
    :return:
    """
    value = record_dict.get(key, default)
    if value is None:
        return 'NULL'
    elif isinstance(value, str):
        return '\'%s\'' % value.replace('\'', '')
    elif isinstance(value, datetime.datetime):
        return '\'%s\'' % value.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(value, Decimal):
        return '{}'.format(value)
    elif isinstance(value, int):
        return '{}'.format(value)
    else:
        return '{}'.format(value)


def gen_replace_into_sql(table_name, attr_dict={}):
    """
    转换插入或更新的 sql 语句
    :param table_name: str，表名
    :param attr_dict: dict，属性字典
    :return:
    """
    columns = attr_dict.keys()
    sql = """
replace into {} ({})
values({})
          """.format(table_name, ','.join(columns),
                     ','.join([sql_value_insert_process(attr_dict, column) for column in columns]))
    return sql


def gen_insert_on_duplicate(table_name, attr_dict, primary_key=None, ignore_columns=None):
    """
    转换插入主键存在更新sql 语句
    :param table_name: str 表名
    :param attr_dict: dict {表列名:值}
    :param primary_key: str 主键列名
    :param ignore_columns: list: [str] 需要忽略更新的列
    :return: str
    """
    ignore_columns = ignore_columns if ignore_columns else []

    sql = "INSERT INTO {table_name} {columns} VALUES {values} ON DUPLICATE KEY UPDATE {update_sql}"

    columns = attr_dict.keys()
    values = [attr_dict[col] for col in columns]
    update_sql_list = []
    # 生成需要更新的字段sql
    for col in columns:
        if primary_key and col == primary_key:
            # 忽略主键
            continue
        if col in ignore_columns:
            # 忽略给的的列
            continue
        key = "'{}'".format(attr_dict[col]) if isinstance(attr_dict[col], str) else attr_dict[col]
        if key is None:
            key = 'NULL'
        update_sql_list.append("`{}`={}".format(col, key))
    update_sql = ','.join(update_sql_list)
    res_sql = sql.format(table_name=table_name,
                         columns='{}'.format(tuple(['`{}`'.format(col) for col in columns])).replace("'", ''),
                         values=tuple(values), update_sql=update_sql)
    return res_sql.replace('None', 'NULL')


def calc_diff(start_day, end_day):
    """
    计算两个日期相差多少天
    :param start_day: str，yyyy-MM-dd
    :param end_day: str，yyyy-MM-dd
    :return:
    """
    start = int(time.mktime(datetime.datetime.strptime('%s 00:00:00' % start_day, "%Y-%m-%d %H:%M:%S").timetuple()))
    end = int(time.mktime(datetime.datetime.strptime('%s 00:00:00' % end_day, "%Y-%m-%d %H:%M:%S").timetuple()))
    return (end - start) / (24 * 60 * 60)


def calc_add(start_day, add_day_num):
    """
    起始日期加上指定天数
    :param start_day: str，yyyy-MM-dd
    :param add_day_num: int
    :return:
    """
    start = int(time.mktime(datetime.datetime.strptime('%s 00:00:00' % start_day, "%Y-%m-%d %H:%M:%S").timetuple()))
    end = start + add_day_num * (24 * 60 * 60)
    return time.strftime("%Y-%m-%d", time.localtime(end))
