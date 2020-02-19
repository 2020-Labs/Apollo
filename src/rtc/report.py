


'''
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

import config
import db
import rtckpi

REPORT_FILE = ''

def initial():
    global REPORT_FILE
    REPORT_FILE = config.REPORT_FULL_PATH

def report_render():
    output = []
    output.append('-'*100)
    output.append('标题：{0}'.format(config.REPORT_TITLE))
    output.append('数据采集时间：{0}'.format(config.DATE))
    output.append('报告生成时间: {0}'.format(time.strftime('%Y-%m-%d_%H:%M%S', time.localtime())))
    output.append('-' * 100)


    data = db.calc_new()
    output.append('{0} ~ {1} 的新增Bug'.format(db.get_initial_date(), data[db.COLUMNS_DATE]))
    thead = "{0:<10}\t{1:<10}\t{2:<10}\t{3:<10}"
    tbody = "{0:<10}\t{1:<10}\t{2:<15}\t{3:<15}"
    output.append(thead.format('姓名','修复','分析转出','小计'))
    for k, v in data.items():
        if config.MEMBERS.__contains__(k):
            output.append(tbody.format(k,v[db.COLUMNS_FIX],v[db.COLUMNS_OUT], v[db.COLUMNS_TOTAL]))

    data = db.calc_last()
    output.append('')
    output.append('{0} ~ {1} 的新增Bug'.format(db.get_last_date(),data[db.COLUMNS_DATE]))
    output.append(thead.format('姓名', '修复', '分析转出', '小计'))
    for k, v in data.items():
        if config.MEMBERS.__contains__(k):
            output.append(tbody.format(k,v[db.COLUMNS_FIX],v[db.COLUMNS_OUT], v[db.COLUMNS_TOTAL]))


    data = db.get_all_data()
    output.append('')
    output.append('全部Bug数据')
    output.append(thead.format('姓名', '修复', '分析转出', '小计'))
    for k, v in data.items():
        if config.MEMBERS.__contains__(k):
            output.append(tbody.format(k,v[db.COLUMNS_FIX],v[db.COLUMNS_OUT], v[db.COLUMNS_TOTAL]))

    for str in output:
        logging.debug(str)

    logging.info('output to : {0}'.format(REPORT_FILE))
    with open(REPORT_FILE, mode='w',encoding='utf-8') as rf:
        for str in output:
            rf.write(str + '\n')


