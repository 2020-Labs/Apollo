#!/usr/bin/env python
# -*- coding:utf-8 _*-

"""
@File       : week_kpi_report.py
@version    : 0.1
@Author     : kelvin
@Time       : 2020-03-29

--------------------------------------------------------------------
@Changes log:
    2020-03-29 : 0.1 Create
"""

__output_excel__ = 'weekly_kpi_report_{0}.xlsx'

import datetime
import logging
import operator
import os
import time

import pandas as pd
import excel_data as db
import xlsxwriter
from pandas._libs.tslibs.timestamps import Timestamp, timedelta

import calendar
import app_config

header_format = {
    'valign': 'vcenter',
    'align': 'left',
    'fg_color': '#00B050',
    'border': 1,
    'font_size': 10,
    'font_name': '微软雅黑'
}

header_center_format = {
    'valign': 'vcenter',
    'align': 'center',
    'fg_color': '#00B050',
    'border': 1,
    'font_size': 10,
    'font_name': '微软雅黑'
}

cell_format_string = {
    'valign': 'vcenter',
    'align': 'center',
    'font_size': 10,
    'font_name': '微软雅黑'
}

summary_cell_format_string = {
    'valign': 'top',
    'align': 'left',
    'font_size': 10,
    'font_name': '微软雅黑',
    'text_wrap': True
}

headers_cell_setting = [
    {
        'cell': 'A1:A3',
        'text': '周期', 'width': 4, 'format': header_center_format
    },
    {
        'cell': 'B1:B3',
        'text': '星期', 'width': 4, 'format': header_center_format
    },
    {
        'cell': 'C1:C3',
        'text': '日期', 'width': 10, 'format': header_center_format
    },
    {
        'cell': 'D1:H1',
        'text': '客观数据', 'width': 50, 'format': header_center_format
    },
    {
        'cell': 'D2:G2',
        'text': '缺陷解决', 'width': 50, 'format': header_center_format
    },
    {
        'cell': 'H2',
        'text': '代码提交', 'width': 8, 'format': header_center_format
    },
    {
        'cell': 'D3',
        'text': '已处理', 'width': 6, 'format': header_center_format
    },
    {
        'cell': 'E3',
        'text': '分析后转出', 'width': 8, 'format': header_center_format
    },
    {
        'cell': 'F3',
        'text': '遗留', 'width': 4, 'format': header_center_format
    },
    {
        'cell': 'G3',
        'text': '修复率', 'width': 6, 'format': header_center_format
    },
    {
        'cell': 'H3',
        'text': '次数', 'width': 8, 'format': header_center_format
    },
    {
        'cell': 'I1:I3',
        'text': '文档', 'width': 4, 'format': header_center_format
    },
    {
        'cell': 'J1:J3',
        'text': '培训', 'width': 4, 'format': header_center_format
    },
    # {
    #     'cell': 'K1:K3',
    #     'text': '人效', 'width': 4, 'format': header_center_format
    # },
    {
        'cell': 'K1:K3',
        'text': '本周关键工作简述&评价', 'width': 80, 'format': header_format
    }
]

covert_cell_format_text = {
    'font_size': 10,
    'font_name': '微软雅黑',
    'text_wrap': True,
    'valign': 'vcenter',  # 垂直对齐方式
    'align': 'left',  # 水平对齐方式
}

covert_cell_settings = [
    {
        'cell': 'A1',
        'text': '',  'width': 10,   'format': covert_cell_format_text
    },
    {
        'cell': 'B1',
        'text': '填写说明',  'width': 100,   'format': covert_cell_format_text
    },
    {
        'cell': 'B2','width': 100, 'format': covert_cell_format_text,
        'text': '1. 已处理: 待验证,打回',
    },
    {
        'cell': 'B3', 'width': 100, 'format': covert_cell_format_text,
        'text': '2. 分析转出: 转给其他业务组',
    },
    {
        'cell': 'B4', 'width': 100, 'format': covert_cell_format_text,
        'text': '3. Bug工作量, 各平台Bug数量 / 所有平台的Bug数量',
    },
    {
        'cell': 'B5', 'width': 100, 'format': covert_cell_format_text,
        'text': '4. 工作投入: 平台所有工作项投入时长 / 总工时长',
    },
    {
        'cell': 'B6', 'width': 100, 'format': covert_cell_format_text,
        'text': '5. 人效计算方法: 已处理的Bug数量 / 平台投入天数, \n    投入天数: 每个工作日只要有投入,就按1天计算',
    },
]

WEEK_DAY_NAME = ['一', '二', '三', '四', '五', '六', '日']

__worksheet__ = None
__workbook__ = None
__start_date__ = app_config.__start_date__
__end_date__ = None

DATE_FORMAT = '%Y-%m-%d'

SHEET_NAME = '周工作汇总'


def output_report(args=None):
    global __workbook__, __worksheet__, __start_date__, __end_date__

    logging.debug(' args: ' + str(args))
    __start_date__ = app_config.__start_date__
    __end_date__ = app_config.__end_date__
    records_list = [db.__db_bugs_records__, db.__db_jobs_records__, db.__db_docs_records__]
    days = sorted({r[db.FIELD_UPDATE_DATE] for rec in records_list for r in rec})

    if len(days) == 1:
        __start_date__ = days.copy()
        __end_date__ = __start_date__
    else:
        __start_date__ = days[0]
        __end_date__ = days[-1]

    excel_file = __output_excel__.format(db.__my_name__)

    excel_file = os.path.join(app_config.__output__, excel_file)
    __workbook__ = xlsxwriter.Workbook(excel_file)
    output_covert_sheet()
    __worksheet__ = __workbook__.add_worksheet(SHEET_NAME)

    for cell in headers_cell_setting:
        header_cell_format = __workbook__.add_format(cell['format'])
        cell_id = cell['cell']
        if cell_id.find(':') > 0:
            __worksheet__.merge_range(cell['cell'], cell['text'], header_cell_format)
            __worksheet__.set_column(cell_id, cell['width'])
        else:
            __worksheet__.write(cell['cell'], cell['text'], header_cell_format)
            __worksheet__.set_column('{0}:{0}'.format(cell_id), cell['width'])

    __worksheet__.set_row(0, 30)
    __worksheet__.set_row(1, 30)
    __worksheet__.set_row(2, 30)

    week_date_range = get_week_range_ext(__start_date__, __end_date__)
    #week_date_range = get_week_range_ext(__start_date__, __end_date__, first_week_day=calendar.THURSDAY)

    report_data = []
    for week in week_date_range:
        # 周报数据
        data_by_week = get_report_data_by_week(week[0], week[1])
        if data_by_week:
            report_data.append(data_by_week)

    # 输出Excel
    cell_format = __workbook__.add_format(cell_format_string)
    summary_cell_format = __workbook__.add_format(summary_cell_format_string)
    current_row = 3
    for rec in report_data:
        week_name = None
        for r in rec['__delta__']:
            day = Timestamp(r['__date__'])

            if not week_name:
                week_name = 'W' + str(day.week)
            __worksheet__.write(current_row, 1, WEEK_DAY_NAME[day.dayofweek], cell_format)

            __worksheet__.write(current_row, 2, r['__date__'].__format__('%Y-%m-%d'), cell_format)
            __worksheet__.write(current_row, 3, r['__fixed__'], cell_format)
            __worksheet__.write(current_row, 4, r['__out__'], cell_format)
            __worksheet__.write(current_row, 5, r['__unfix__'], cell_format)
            __worksheet__.write(current_row, 7, r['__codes__'], cell_format)
            __worksheet__.write(current_row, 8, r['__docs__'], cell_format)
            __worksheet__.write(current_row, 9, r['__otj__'], cell_format)

            __worksheet__.set_row(current_row, 25)
            current_row += 1

        # 本周汇总
        merge_start_row = current_row - len(rec['__delta__']) + 1
        merge_end_row = current_row
        __worksheet__.merge_range('K{0}:K{1}'.format(merge_start_row, merge_end_row), rec['__summary__'],
                                  cell_format=summary_cell_format)
        __worksheet__.merge_range('A{0}:A{1}'.format(merge_start_row, merge_end_row), week_name,
                                  cell_format=summary_cell_format)

    __workbook__.close()


def date_range(beginDate, endDate):
    dates = []
    _start = Timestamp(beginDate)
    _end = Timestamp(endDate)
    _date = _start
    while _date <= _end:
        dates.append(_date)
        _date = _date + timedelta(1)

    return dates


def get_report_data_by_week(start_date, end_date):
    __start_date = Timestamp(start_date)
    __end_date = Timestamp(end_date)
    __days = date_range(start_date, end_date)
    # 查询数据
    records_by_days = {}

    records = [r for r in db.__db_bugs_records__ if r[db.FIELD_UPDATE_DATE] in __days]
    records_by_days[db.DATA_KEY_BUG] = sorted_records(records, db.FIELD_UPDATE_DATE)

    records = [r for r in db.__db_jobs_records__ if r[db.FIELD_UPDATE_DATE] in __days]
    records_by_days[db.DATA_KEY_JOB] = sorted_records(records, db.FIELD_UPDATE_DATE)

    records = [r for r in db.__db_docs_records__ if r[db.FIELD_UPDATE_DATE] in __days]
    records_by_days[db.DATA_KEY_DOC] = sorted_records(records, db.FIELD_UPDATE_DATE)

    records = [r for r in db.__db_codes_records__ if r[db.FIELD_UPDATE_DATE] in __days]
    records_by_days[db.DATA_KEY_CODE] = sorted_records(records, db.FIELD_UPDATE_DATE)

    # 统计

    output = []
    # 按天统计 Bugs,文档,培训,代码提交
    for day in __days:
        # Bug
        __records = [r for r in records_by_days[db.DATA_KEY_BUG] if r[db.FIELD_UPDATE_DATE] == day]

        fixed = sum([1 for r in __records if r[db.FIELD_STATUS] in ['打回', '待验证']])
        out = sum([1 for r in __records if r[db.FIELD_STATUS] in ['分析转出']])
        unfix = sum([1 for r in __records if r[db.FIELD_STATUS] in ['解决中', '新建']])

        # Doc
        __records = [r for r in records_by_days[db.DATA_KEY_DOC] if r[db.FIELD_UPDATE_DATE] == day]
        # 经验传承
        doc1 = sum([1 for r in __records if r[db.FIELD_STATUS] in ['完成'] and r['category'] in ['经验传承', '失效分析']])
        # 培训
        doc2 = sum([1 for r in __records if r[db.FIELD_STATUS] in ['完成'] and r['category'] in ['OTJ', 'otj']])

        # Code
        __records = [r for r in records_by_days[db.DATA_KEY_CODE] if r[db.FIELD_UPDATE_DATE] == day]
        code = sum([1 for r in __records])

        logging.debug('日期：{0} ， Bug: 已处理： {1} , 分析转出: {2} , 遗留：{3} , 文档： {4}, OTJ: {5} , 代码提交： {6}'.format(
            day, fixed, out, unfix, doc1, doc2, code
        ))

        output.append({
            '__date__': day,
            '__fixed__': fixed,
            '__out__': out,
            '__unfix__': unfix,
            '__docs__': doc1,
            '__otj__': doc2,
            '__codes__': code,
        })

    summary = get_summary(records_by_days)

    result = {
        '__start__': start_date,
        '__end__': end_date,
        '__delta__': output,
        '__summary__': summary
    }

    return result


def get_summary(records_by_days):
    start_date = strfdate(__start_date__)
    end_date = strfdate(__end_date__)
    # 总用时
    total_hours = sum([r[db.FIELD_HOUR] for k, recs in records_by_days.items() for r in recs if r.get(db.FIELD_HOUR)])

    work_summary_output_text = []

    summary_output_text = []

    new_records = [r for r in records_by_days[db.DATA_KEY_BUG]]
    __new_records = {r[db.BUGS_FIELD_ID]: r for r in new_records}.values()
    bugs_count = sum([1 for o in {r[db.BUGS_FIELD_ID] for r in __new_records}])

    thead = "{0:>5}\t    {1:<16}     {2:<18}    {3:<19}"
    tbody = "{0:>6}\t    {1:<20}   {2:<20}    {3:<15}"

    summary_output_text.append(thead.format('平台', 'Bug工作量', '工时投入', '人效'))
    platforms = sorted([rec for rec in
                        {r[db.FIELD_PLATFORM] for k, recs in records_by_days.items() for r in recs if
                         r.get(db.FIELD_PLATFORM)}])

    for platform in platforms:

        work_summary_output_text.append('[{0}]'.format(platform))
        hour_ = sum([r[db.FIELD_HOUR] for k, recs in records_by_days.items() for r in recs if
                     r.get(db.FIELD_HOUR) and r.get(db.FIELD_PLATFORM) == platform])

        # Bugs
        new_records = [r for r in records_by_days[db.DATA_KEY_BUG] if r[db.FIELD_PLATFORM] == platform]
        __new_records = {r[db.BUGS_FIELD_ID]: r for r in new_records}.values()
        bugs = {r[db.BUGS_FIELD_ID] for r in __new_records}

        # 统计各状态的Bug数量
        count_fixed = sum(
            [1 for o in {r[db.BUGS_FIELD_ID] for r in __new_records if r[db.FIELD_STATUS] in ['待验证', '打回']}])
        count_process = sum(
            [1 for o in {r[db.BUGS_FIELD_ID] for r in __new_records if r[db.FIELD_STATUS] in ['解决中', '新建']}])
        count_out = sum([1 for o in {r[db.BUGS_FIELD_ID] for r in __new_records if r[db.FIELD_STATUS] in ['分析转出']}])
        bugs_count_by_platform = sum([1 for o in {r[db.BUGS_FIELD_ID] for r in __new_records}])

        if len(bugs) > 0:
            days = sum([1 for o in {r[db.FIELD_UPDATE_DATE] for r in __new_records}])

            bugs_delta = ' - 已处理：{0}， 解决中：{1}， 分析转出：{2}'.format(count_fixed, count_process, count_out)

            work_summary_output_text.append('  - Bugs: ({0} 个) , {1}'.format(len(bugs), bugs_delta))
            work_summary_output_text.append('    {0}'.format(str(bugs)[1:-1].replace("'", '').replace(',', ' ')))
            work_summary_output_text.append('')

            summary_1 = '{0:>2} / {1:>2} = {2:>4}'.format(bugs_count_by_platform, bugs_count,
                                                          format(float(bugs_count_by_platform / bugs_count), '0.00%'))
            summary_3 = '{0:>2} / {1:>2} = {2:>5.2f}'.format(count_fixed + count_out, days,
                                                             (count_fixed + count_out) / days)

        else:
            summary_1 = 'N/A'
            summary_3 = 'N/A'
        summary_2 = '{0:>4} / {1:>4} = {2:>4}'.format(hour_, total_hours, format(float(hour_ / total_hours), '0.00%'))

        summary = tbody.format(platform, summary_1, summary_2, summary_3)
        summary_output_text.append(summary)

        # 代码提交
        new_records = [r for r in records_by_days[db.DATA_KEY_CODE] if r[db.FIELD_PLATFORM] == platform]
        if len(new_records) > 0:
            work_summary_output_text.append('  - 代码提交: {0}笔'.format(len(new_records)))
            work_summary_output_text.append('')
        work_summary_output_text.append('-' * 20)

    # 文档
    new_records = [r for r in records_by_days[db.DATA_KEY_DOC]]
    if len(new_records) > 0:
        work_summary_output_text.append('')
        work_summary_output_text.append('文档输出: {0} 篇'.format(len(new_records)))
        work_summary_output_text.append('')

    if len(work_summary_output_text) > 0:
        summary = '{0} ~ {1} 工作汇总 \n'.format(start_date, end_date)
        for r in work_summary_output_text:
            summary += r + '\n'

        summary += '=' * 100 + '\n'
        for r in summary_output_text:
            logging.debug(r)
            summary += r + '\n'
    else:
        summary = 'N/A'

    return summary


def get_week_range_ext(start_date, end_date, first_week_day=calendar.MONDAY):
    if not (first_week_day >= calendar.MONDAY and first_week_day <= calendar.SUNDAY):
        raise ValueError('first_week_day is invalid')

    if first_week_day == calendar.MONDAY:
        last_week_day = calendar.SUNDAY
    else:
        last_week_day = first_week_day - 1

    first_date = Timestamp(start_date)
    last_date = Timestamp(end_date)

    ## 根据参数中指定的开始日期和结束日期, 计算出开始日期所在周(星期)的第1天, 结束日期所在周的最后1天
    if first_week_day == calendar.MONDAY:
        first_day_dayofweek_step = first_date.dayofweek
        last_day_dayofweek_step = (calendar.SUNDAY - last_date.dayofweek)
    else:
        if first_date.dayofweek >= first_week_day:
            first_day_dayofweek_step = first_date.dayofweek - first_week_day
        else:
            first_day_dayofweek_step = calendar.SUNDAY - first_week_day + 1 + first_date.dayofweek

        if last_date.dayofweek >= first_week_day:
            last_day_dayofweek_step = calendar.SUNDAY - last_date.dayofweek + last_week_day + 1
        elif last_date.dayofweek <= last_week_day:
            last_day_dayofweek_step = last_week_day - last_date.dayofweek

    first_date = first_date - timedelta(first_day_dayofweek_step)
    last_date = last_date + timedelta(last_day_dayofweek_step)

    days = date_range(first_date, last_date)

    # 计算出每周的开始和结束日期
    result_date = []
    for i in range(0, len(days), 7):
        end_index = i + 6
        result_date.append([strfdate(days[i]), strfdate(days[end_index])])
        logging.debug('{0} - {1}'.format(strfdate(days[i]), strfdate(days[end_index])))

    return result_date


def strfdate(date):
    if isinstance(date, Timestamp):
        return date.__format__(DATE_FORMAT)

    return date


def sorted_records(records, fields, order_desc=False):
    recs = sorted(records, key=operator.itemgetter(fields), reverse=order_desc)
    return recs

def output_covert_sheet():
    worksheet = __workbook__.add_worksheet('填写说明')
    for cell in covert_cell_settings:
        cell_format = __workbook__.add_format(cell['format'])
        cell_id = cell['cell']
        worksheet.write(cell['cell'], cell['text'], cell_format)
        worksheet.set_column('{0}:{0}'.format(cell_id), cell['width'])