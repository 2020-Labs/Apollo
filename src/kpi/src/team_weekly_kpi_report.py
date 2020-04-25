#!/usr/bin/env python
#-*- coding:utf-8 _*-

"""
@File       : team-weekly-kpi-report.py
@version    : 0.1
@Author     : kelvin
@Time       : 2020-04-25

--------------------------------------------------------------------
@Changes log:
    2020-04-25 : 0.1 Create
"""

__output_excel__ = '诚迈Network周报_{0}_{1}.xlsx'

import logging
import os

import excel_data as db
import app_config

import xlsxwriter
from pandas._libs.tslibs.timestamps import Timestamp, timedelta
import calendar

import utils

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
        'text': '姓名', 'width': 4, 'format': header_center_format
    },
    {
        'cell': 'B1:F1',
        'text': '客观数据', 'width': 50, 'format': header_center_format
    },
    {
        'cell': 'B2:E2',
        'text': '缺陷解决', 'width': 50, 'format': header_center_format
    },
    {
        'cell': 'F2',
        'text': '代码提交', 'width': 8, 'format': header_center_format
    },
    {
        'cell': 'B3',
        'text': '已处理', 'width': 6, 'format': header_center_format
    },
    {
        'cell': 'C3',
        'text': '分析后转出', 'width': 8, 'format': header_center_format
    },
    {
        'cell': 'D3',
        'text': '遗留', 'width': 4, 'format': header_center_format
    },
    {
        'cell': 'E3',
        'text': '修复率', 'width': 6, 'format': header_center_format
    },
    {
        'cell': 'F3',
        'text': '次数', 'width': 8, 'format': header_center_format
    },
    {
        'cell': 'G1:G3',
        'text': '文档', 'width': 4, 'format': header_center_format
    },
    {
        'cell': 'H1:H3',
        'text': '培训', 'width': 4, 'format': header_center_format
    },
    {
        'cell': 'I1:I3',
        'text': '人效', 'width': 4, 'format': header_center_format
    },
    {
        'cell': 'J1:J3',
        'text': '本周关键工作简述&评价', 'width': 80, 'format': header_format
    }
]

def output_report(args=None):
    logging.debug('hello')

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

    db.__db_docs_records__

    week_date_range = utils.get_week_range_ext(__start_date__, __end_date__)

    report_data = []
    for week in week_date_range:
        # 周报数据
        data_by_week = get_report_data_by_week(week[0], week[1])
        if data_by_week:
            #report_data.append(data_by_week)
            #key = '{0} - {1}'.format(week[0], week[1])
            #report_data[key] = data_by_week
            report_data.append({
                '__start_date__': week[0],
                '__end_date__': week[1],
                '__delta__': data_by_week
            })


    logging.debug(report_data)

    for r in report_data:
        excel_file = __output_excel__.format(r['__start_date__'], r['__end_date__'])
        excel_file = os.path.join(app_config.__output__, excel_file)
        output_to_excel(r['__delta__'], excel_file)


def output_to_excel(records, excel_file):
    __workbook__ = xlsxwriter.Workbook(excel_file)

    __worksheet__ = __workbook__.add_worksheet()

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

    # 写数据
    cell_format = __workbook__.add_format(cell_format_string)
    summary_cell_format = __workbook__.add_format(summary_cell_format_string)
    current_row = 3
    for r in records:
        __worksheet__.write(current_row, 0, r['__author__'], cell_format)
        __worksheet__.write(current_row, 1, r['__fixed__'], cell_format)
        __worksheet__.write(current_row, 2, r['__out__'], cell_format)
        __worksheet__.write(current_row, 3, r['__unfix__'], cell_format)
        __worksheet__.write(current_row, 5, r['__codes__'], cell_format)
        __worksheet__.write(current_row, 6, r['__docs__'], cell_format)
        __worksheet__.write(current_row, 7, r['__otj__'], cell_format)
        # 8 人效
        # 9 本周汇总
        __worksheet__.write(current_row, 9, r['__summary__'], summary_cell_format)
        current_row += 1

    __workbook__.close()


def get_report_data_by_week(start_date, end_date):
    __start_date = Timestamp(start_date)
    __end_date = Timestamp(end_date)
    __days = utils.date_range(start_date, end_date)

    output = []


    for u in db.__db_users__:
        records_by_days = {}
        # 查询数据
        records = [r for r in db.__db_bugs_records__ if r[db.FIELD_UPDATE_DATE] in __days and r[db.FIELD_AUTHOR] == u]
        records_by_days[db.DATA_KEY_BUG] = utils.sorted_records(records, db.FIELD_UPDATE_DATE)

        records = [r for r in db.__db_jobs_records__ if r[db.FIELD_UPDATE_DATE] in __days  and r[db.FIELD_AUTHOR] == u]
        records_by_days[db.DATA_KEY_JOB] = utils.sorted_records(records, db.FIELD_UPDATE_DATE)

        records = [r for r in db.__db_docs_records__ if r[db.FIELD_UPDATE_DATE] in __days  and r[db.FIELD_AUTHOR] == u]
        records_by_days[db.DATA_KEY_DOC] = utils.sorted_records(records, db.FIELD_UPDATE_DATE)

        records = [r for r in db.__db_codes_records__ if r[db.FIELD_UPDATE_DATE] in __days  and r[db.FIELD_AUTHOR] == u]
        records_by_days[db.DATA_KEY_CODE] = utils.sorted_records(records, db.FIELD_UPDATE_DATE)


        # Bug
        fixed = sum([1 for r in records_by_days[db.DATA_KEY_BUG] if r[db.FIELD_STATUS] in ['打回', '待验证']])
        out = sum([1 for r in records_by_days[db.DATA_KEY_BUG] if r[db.FIELD_STATUS] in ['分析转出']])
        unfix = sum([1 for r in records_by_days[db.DATA_KEY_BUG] if r[db.FIELD_STATUS] in ['解决中', '新建']])

        # Doc
        # 经验传承
        doc1 = sum([1 for r in records_by_days[db.DATA_KEY_DOC] if r[db.FIELD_STATUS] in ['完成'] and r['category'] in ['经验传承', '失效分析']])
        # 培训
        doc2 = sum([1 for r in records_by_days[db.DATA_KEY_DOC] if r[db.FIELD_STATUS] in ['完成'] and r['category'] in ['OTJ', 'otj']])

        # Code
        code = sum([1 for r in records_by_days[db.DATA_KEY_CODE]])

        logging.debug('{0} ({1} ~ {2})'.format(u, start_date, end_date))
        logging.debug('Bug: 已处理： {0} , 分析转出: {1} , 遗留：{2} , 文档： {3}, OTJ: {4} , 代码提交： {5}'.format(
            fixed, out, unfix, doc1, doc2, code
        ))

        summary = get_summary(records_by_days)

        output.append({
            '__author__': u,
            '__fixed__': fixed,
            '__out__': out,
            '__unfix__': unfix,
            '__docs__': doc1,
            '__otj__': doc2,
            '__codes__': code,
            '__summary__':summary
        })

    return output



def get_summary(records_by_days):
    #start_date = strfdate(__start_date__)
    #end_date = strfdate(__end_date__)
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
        #summary = '{0} ~ {1} 工作汇总 \n'.format(start_date, end_date)
        summary = '工作汇总'
        for r in work_summary_output_text:
            summary += r + '\n'

        summary += '=' * 100 + '\n'
        for r in summary_output_text:
            logging.debug(r)
            summary += r + '\n'
    else:
        summary = 'N/A'

    return summary
