#!/usr/bin/env python
#-*- coding:utf-8 _*-

"""
@File       : app_config.py
@version    : 0.1
@Author     : kelvin
@Time       : 2020-04-19

--------------------------------------------------------------------
@Changes log:
    2020-04-19 : 0.1 Create
"""

__args_opts__ = None

__excel_files__ = {}

__start_date__ = None

__end_date__ = None

__output__ = None

import json
import logging
import os
import time

from pandas._libs.tslibs.timestamps import Timestamp

__config_file__ = os.path.join(os.getcwd(),'kpi.config')

__kpi_path__ = os.getcwd()

__excel_files__ = {}

__my_name__ = ''


def parse_opts(opts):
    global __excel_files__, __output__, __start_date__, __end_date__, __args_opts__, __my_name__, __config_file__
    __args_opts__ = opts

    args = {arg[2:]: opt for arg, opt in opts}

    logging.debug('args: {0}'.format(args))

    if args.get('excel', None):
        __my_name__ = 'AAA'
        __excel_files__[__my_name__] = args['excel']
    else:
        read_config()
        __excel_files__ = {k: os.path.join(__kpi_path__, v) for k, v in __excel_files__.items()}

    __output__ = args.get('output', os.getcwd())

    args_date = args.get('date', '')

    if args_date:
        dates = args_date.split(',')
        if len(dates) > 1:
            __start_date__ = dates[0]
            __end_date__ = dates[1]
        else:
            __start_date__ = dates[0]
            __end_date__ = time.strftime('%Y-%m-%d', time.localtime())

        try:
            Timestamp(__start_date__)
            Timestamp(__end_date__)
        except ValueError as e:
            raise ValueError('参数: --date 格式错误,不是有效的日期格式, 格式:yyyy-mm-dd , {0} {1}'.format(
                __start_date__, __end_date__
            ))

    else:
        __start_date__ = __end_date__ = time.strftime('%Y-%m-01', time.localtime())
        __end_date__ = __end_date__ = time.strftime('%Y-%m-%d', time.localtime())


def read_config():
    global __kpi_path__, __excel_files__
    try:
        with open(__config_file__, encoding='utf-8') as f:
            data = json.load(f)
            __kpi_path__ = data['kpi_path']
            __excel_files__ = data['excel_files']
    except Exception as e:
        logging.error('json decode error')
        import traceback
        traceback.print_exc()