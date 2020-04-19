#!/usr/bin/env python
#-*- coding:utf-8 _*-

"""
@File       : team_work_report.py
@version    : 0.1
@Author     : kelvin
@Time       : 2020-04-12

--------------------------------------------------------------------
@Changes log:
    2020-04-12 : 0.1 Create
"""
import logging

import excel_data as db
import xlsxwriter

import app_config

OUTOUT_EXCEL = '/work2//git-source//Apollo//src//kpi//docs//{0}_平台投入度统计.xlsx'

header_center_format = {
    'valign': 'vcenter',
    'align': 'center',
    'fg_color': '#00B050',
    'border': 1,
    'font_size': 10,
    'font_name': '微软雅黑'
}

NUMERIC_CELL_FORMAT = {
    'valign': 'vcenter',
    'align': 'center',
    'font_size': 10,
    'font_name': '微软雅黑',

}

CELL_FORMAT = {
    'valign': 'vcenter',
    'align': 'left',
    'font_size': 10,
    'font_name': '微软雅黑',
}

headers_cell_setting = [
    {
        'cell': 'A1:F1',
        'text': '', 'width': 9, 'format': header_center_format
    },
    {
        'cell': 'A2:A3',
        'text': '姓名',  'width': 9,   'format': header_center_format
    },
    {
        'cell': 'B2:B3',
        'text': '业务组',  'width': 9,   'format': header_center_format
    },
    {
        'cell': 'C2:C3',
        'text': '参与的平台',   'width': 20,  'format': header_center_format
    },

]

__worksheet__ = None
__workbook__ = None

REPORT_KEY_PLATFORMS = 'platforms'
SHEET_NAME = '一周各平台工作投入度'

def output_report(args):
    global  __workbook__, __worksheet__

    logging.debug(db.__db_users__)

    report_data = get_report_data()

    suffix = '{0}_{1} 各平台投入度'.format(app_config.__start_date__, app_config.__end_date__)
    excel_file = OUTOUT_EXCEL.format(suffix)
    __workbook__ = xlsxwriter.Workbook(excel_file)
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

    __worksheet__.set_row(0, 20)
    __worksheet__.set_row(1, 20)

    # 将统计日期 写入表头
    __worksheet__.write('A1', '{0} ~ {1} 各平台投入度'.format(app_config.__start_date__, app_config.__end_date__), header_cell_format)

    platforms = get_all_platforms()

    platforms_cols = {}

   # 各平台 数据列
    col = 3
    for p in platforms:
        __worksheet__.write(1, col, p , header_cell_format)
        platforms_cols[p] = col
        col += 1

    # D的assic码是68
    _col_name_assic = 68
    start_col = chr(_col_name_assic)
    end_col = chr(_col_name_assic + len(platforms) -1)
    cell_id = '{0}2:{1}3'.format(start_col, end_col)
    __worksheet__.merge_range(cell_id, '各平台投入度', header_cell_format)

    #logging.debug(chr(68))


    numeric_cell_format = __workbook__.add_format(NUMERIC_CELL_FORMAT)
    cell_format = __workbook__.add_format(CELL_FORMAT)
    row = 3
    for r in report_data:
        __worksheet__.write(row, 0, r[db.FIELD_AUTHOR], cell_format)
        __worksheet__.write(row, 2, r[REPORT_KEY_PLATFORMS], cell_format)

        for p, col in platforms_cols.items():
            if r.get(p):
                __worksheet__.write(row, col, r[p] , numeric_cell_format)

        row += 1

    __workbook__.close()


def get_report_data():
    report_data = []
    all_platforms = get_all_platforms()

    for u in db.__db_users__:
        records_by_u = {}
        records = [r for r in db.__db_bugs_records__ if r[db.FIELD_AUTHOR] == u]
        records_by_u[db.DATA_KEY_BUG] = records

        records = [r for r in db.__db_jobs_records__ if r[db.FIELD_AUTHOR] == u]
        records_by_u[db.DATA_KEY_JOB] = records

        records = [r for r in db.__db_docs_records__ if r[db.FIELD_AUTHOR] == u]
        records_by_u[db.DATA_KEY_DOC] = records

        platforms = [rec for rec in
                     {r[db.FIELD_PLATFORM] for k, recs in records_by_u.items() for r in recs if r.get(db.FIELD_PLATFORM)}]

        total_hours = sum(
            [r[db.FIELD_HOUR] for k, recs in records_by_u.items() for r in recs if r.get(db.FIELD_HOUR)])

        report = {db.FIELD_AUTHOR: u}
        report[REPORT_KEY_PLATFORMS] = str(platforms)[1:-1].replace("'", '').replace(',', '')
        for p in platforms:
            hours = sum(
                [r[db.FIELD_HOUR] for k, recs in records_by_u.items() for r in recs if r.get(db.FIELD_HOUR) and r.get(db.FIELD_PLATFORM) == p]
            )

            report[p] = hours

        report_data.append(report)

        logging.debug(report_data)

    return report_data



def get_all_platforms():
    all_records = {}
    records = [r for r in db.__db_bugs_records__]
    all_records[db.DATA_KEY_BUG] = records

    records = [r for r in db.__db_jobs_records__]
    all_records[db.DATA_KEY_JOB] = records

    platforms = [rec for rec in
                 {r[db.FIELD_PLATFORM] for k, recs in all_records.items() for r in recs if r.get(db.FIELD_PLATFORM)}]

    return sorted(platforms)

