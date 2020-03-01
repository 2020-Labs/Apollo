#!/usr/bin/env python
#-*- coding:utf-8 _*-

"""
@File       : report.py
@version    : 0.1
@Author     : Kelvin
@Time       : 2020-03-01

--------------------------------------------------------------------
@Changes log:
    2020-03-01 : 0.1 Create

"""

'''
Rport Text Template
--------------------------------------------------------------------
URL: 710q.html
标题:710Q Network团队 修复问题汇总
数据采集时间：
报告生成时间：
--------------------------------------------------------------------

明细：
姓名    修复    分析转出    小计
A       87         3       90

.....

==============================

2020-1-15 ~ 2020-1-23 新增数据
姓名    修复    分析转出    小计
A        3         1        4

......

'''
import logging
import os
import time

from config import AppConfig
from db import DbHelper
import db

class ReportText:

    __ReportFile = ''

    def __init__(self):
        self.__ReportFile = os.path.join(AppConfig.BASE_PATH, AppConfig.REPORT_FILE)

    def output_report(self):
        output = []
        output.append('-' * 100)
        output.append('标题：{0}'.format(AppConfig.REPORT_TITLE))
        output.append('数据采集时间：{0}'.format(AppConfig.DATE))
        output.append('报告生成时间: {0}'.format(time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime())))
        output.append('-' * 100)

        thead = "{0:<10}\t{1:<10}\t{2:<10}\t{3:<10}"
        tbody = "{0:<10}\t{1:<10}\t{2:<15}\t{3:<15}"
        dbhelper = DbHelper.getInstance()
        for url, ds in dbhelper.calc_data_by_file():
            # logging.debug('{0} , {1}'.format(url, ds))
            output.append('')
            output.append('=' * 100)
            output.append('File: {0}'.format(url))
            output.append(thead.format('姓名', '修复', '分析转出', '小计'))

            for v in ds:
                output.append(tbody.format(v['name'], v[db.COLUMNS_FIX], v[db.COLUMNS_OUT], v[db.COLUMNS_TOTAL]))
            output.append('=' * 100)

        data = dbhelper.calc_new()
        if data:
            output.append('')
            output.append('=' * 100)
            output.append('{0} ~ {1} 的新增Bug'.format(dbhelper.get_initial_date(), data[db.COLUMNS_DATE]))
            output.append(thead.format('姓名', '修复', '分析转出', '小计'))
            for k, v in data.items():
                # if AppConfig.MEMBERS.__contains__(k):
                if k in AppConfig.MEMBERS:
                    output.append(tbody.format(k, v[db.COLUMNS_FIX], v[db.COLUMNS_OUT], v[db.COLUMNS_TOTAL]))

        data = dbhelper.calc_last()
        if data:
            output.append('')
            output.append('=' * 100)
            output.append('')
            output.append('{0} ~ {1} 的新增Bug'.format(dbhelper.get_last_date(), data[db.COLUMNS_DATE]))
            output.append(thead.format('姓名', '修复', '分析转出', '小计'))
            for k, v in data.items():
                # if AppConfig.MEMBERS.__contains__(k):
                if k in AppConfig.MEMBERS:
                    output.append(tbody.format(k, v[db.COLUMNS_FIX], v[db.COLUMNS_OUT], v[db.COLUMNS_TOTAL]))

        data = dbhelper.get_all_data()
        output.append('')
        output.append('=' * 100)
        output.append('全部Bug数据')
        output.append(thead.format('姓名', '修复', '分析转出', '小计'))
        for k, v in data.items():
            # if AppConfig.MEMBERS.__contains__(k):
            if k in AppConfig.MEMBERS:
                output.append(tbody.format(k, v[db.COLUMNS_FIX], v[db.COLUMNS_OUT], v[db.COLUMNS_TOTAL]))
        output.append('-' * 100)

        for txt in output:
            logging.debug(txt)

        logging.info('output to : {0}'.format(self.__ReportFile))
        with open(self.__ReportFile, mode='w', encoding='utf-8') as rf:
            for txt in output:
                rf.write(txt + '\n')
