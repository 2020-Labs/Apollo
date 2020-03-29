#!/usr/bin/env python
#-*- coding:utf-8 _*-

"""
@File       : daily_kpi_report.py
@version    : 0.1
@Author     : kelvin
@Time       : 2020-03-29

--------------------------------------------------------------------
@Changes log:
    2020-03-29 : 0.1 Create
"""
import datetime
import logging
import operator

import excel_data as db

__output_excel__ = '/work2//git-source//Apollo//src//kpi//docs//kpi_report.xlsx'

import pandas as pd
import xlsxwriter
from pandas._libs.tslibs.timestamps import Timestamp

header_format = {
    'valign': 'vcenter',
    'align': 'left',
    'fg_color': '#B4C6E7',
    'border': 1,
    'font_size': 10,
    'font_name': '微软雅黑'
}

header_center_format = {
    'valign': 'vcenter',
    'align': 'center',
    'fg_color': '#B4C6E7',
    'border': 1,
    'font_size': 10,
    'font_name': '微软雅黑'
}


week_day_name = ['一','二','三','四','五','六','日']

cell_default_format_text = {
    'valign': 'vcenter',  # 垂直对齐方式
    'align': 'left',  # 水平对齐方式
    'border': 1,  # 单元格边框宽度
    'font_size': 10,
    'font_name': '微软雅黑',
    'text_wrap': True
}

center_cell_format_text = {
    'border': 1,  # 单元格边框宽度
    'font_size': 10,
    'font_name': '微软雅黑',
    'text_wrap': True,
    'valign': 'vcenter',  # 垂直对齐方式
    'align': 'center',  # 水平对齐方式
}

headers_cell_setting = [
    {
        'cell': 'A1',
        'text': '序号',  'width': 4,   'format': header_center_format
    },
    {
        'cell': 'B1',
        'text': '周期',  'width': 4,   'format': header_center_format
    },
    {
        'cell': 'C1',
        'text': '星期',   'width': 4,  'format': header_center_format
    },
    {
        'cell': 'D1',
        'text': '日期',   'width': 10, 'format': header_center_format
    },
    {
        'cell': 'E1',
        'text': '关键工作简述&评价',   'width': 50, 'format': header_format
    }
]

def output_header(workbook,worksheet):
    pass

def output_report(args):
    logging.info('args: '.format(args))

    #new_records = sorted(db.__db_bugs_records__, key=operator.itemgetter(db.FIELD_UPDATE_DATE), reverse=False)

    records_list = [db.__db_bugs_records__, db.__db_jobs_records__ , db.__db_docs_records__]
    days = sorted({r[db.FIELD_UPDATE_DATE] for rec in records_list for r in rec})


    if len(days) == 1:
        new_days = days.copy()
    else:
        first_day = days[0]
        last_day = days[-1]
        diff_day = last_day - first_day

        new_days = [first_day]

        for i in range(diff_day.days):
            day = first_day.replace(day=first_day.day + i)
            new_days.append(day)
        new_days.append(last_day)

    logging.debug(new_days)

    all_days_report = {}

    for day in new_days:
        records_by_day = {}

        records= [r for r in db.__db_bugs_records__ if r[db.FIELD_UPDATE_DATE] == day]
        records_by_day[db.DATA_KEY_BUG] = records

        records = [r for r in db.__db_jobs_records__ if r[db.FIELD_UPDATE_DATE] == day]
        records_by_day[db.DATA_KEY_JOB] = records

        records = [r for r in db.__db_docs_records__ if r[db.FIELD_UPDATE_DATE] == day]
        records_by_day[db.DATA_KEY_DOC] = records

        report_text = output_report_by_day(records_by_day)

        all_days_report[day] = report_text


    output_excel_report(all_days_report)



def output_excel_report(records):
    workbook = xlsxwriter.Workbook(__output_excel__)
    worksheet = workbook.add_worksheet()

    for cell in headers_cell_setting:
        cell_format = workbook.add_format(cell['format'])
        cell_id = cell['cell']
        if cell_id.find(':') > 0:
            worksheet.merge_range(cell['cell'], cell['text'], cell_format)
            worksheet.set_column(cell_id, cell['width'])
        else:
            worksheet.write(cell['cell'], cell['text'], cell_format)
            worksheet.set_column('{0}:{0}'.format(cell_id), cell['width'])

    worksheet.set_row(0, 20)

    _row = 1
    default_cell_format = workbook.add_format(cell_default_format_text)
    center_cell_format = workbook.add_format(center_cell_format_text)

    for day, report_text in records.items():
        worksheet.write(_row, 0, str(_row), center_cell_format)
        worksheet.write(_row, 1, 'W' + str(day.week), center_cell_format)
        worksheet.write(_row, 2, week_day_name[day.dayofweek], center_cell_format)
        worksheet.write(_row, 3, day.strftime('%Y-%m-%d'), center_cell_format)

        worksheet.write(_row, 4, report_text, default_cell_format)

        _row += 1

    workbook.close()

def output_report_by_day(records):
    output_text = []

    #platforms = [r for r in {r[db.FIELD_PLATFORM] for r in records}]
    #logging.debug(platforms)


    #platforms = [rec for rec in {r[db.FIELD_PLATFORM] for k,r in records.items()}]
    platforms = [rec for rec in {r[db.FIELD_PLATFORM] for k, recs in records.items() for r in recs if r.get(db.FIELD_PLATFORM)}]
    #logging.debug(platforms)


    result = []

    for platform in platforms:
        new_records = [r for r in records[db.DATA_KEY_BUG] if r[db.FIELD_PLATFORM] == platform]

        #Bug
        if len(new_records) > 0:
            output_text.append(platform)

        for r in new_records:

            if r[db.FIELD_STATUS] in ['解决中', '待验证', '打回', '分析转出']:
                r['__type__'] = db.DATA_KEY_BUG
                result.append(r)
                output_text.append(' - Bug {0} {1}'.format(r['BugId'], r[db.FIELD_TITLE]))
                output_text.append('   状态：{0}'.format(r[db.FIELD_STATUS]))
                output_text.append('   进展：{0}'.format(r[db.FIELD_DETAILED]))

        #Job
        new_records = [r for r in records[db.DATA_KEY_JOB] if r[db.FIELD_PLATFORM] == platform]
        if len(new_records) > 0:
            output_text.append(platform)

        for r in new_records:
            if r[db.FIELD_STATUS] in ['进行中', '完成']:
                r['__type__'] = db.DATA_KEY_JOB
                result.append(r)
                output_text.append(' - {0} {1} '.format(r['category'], r[db.FIELD_TITLE]))
                output_text.append('   状态：{0}'.format(r[db.FIELD_STATUS]))
                output_text.append('   进展：{0}'.format(r[db.FIELD_DETAILED]))

    #Docs
    new_records = [r for r in records[db.DATA_KEY_DOC]]
    if len(new_records) > 0:
        output_text.append('文档输出：')
    for r in new_records:
        if r[db.FIELD_STATUS] in ['进行中', '完成']:
            r['__type__'] = db.DATA_KEY_DOC
            result.append(r)
            output_text.append(' - {0} {1} '.format(r['category'], r[db.FIELD_TITLE]))



    #ouput


    result_text = ''

    for r in output_text:
        result_text += r + '\n'

    #logging.debug(result_text)

    return result_text






