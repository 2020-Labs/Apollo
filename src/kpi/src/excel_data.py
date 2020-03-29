#!/usr/bin/env python
#-*- coding:utf-8 _*-

"""
@File       : excel_data.py
@version    : 0.1
@Author     : kelvin
@Time       : 2020-03-28

--------------------------------------------------------------------
@Changes log:
    2020-03-28 : 0.1 Create
"""
import logging
import os
from datetime import datetime

import pandas as pd


__excel_file__ = ''

DATA_MAPPING_NAME = 'name'
DATA_MAPPING_COLUMNS = 'columns'
DATA_MAPPING_COL = 'column'
DATA_MAPPING_FIELD = 'field'
DATA_MAPPING_TYPE = 'type'

FIELD_UPDATE_DATE = 'update_date'
FIELD_PLATFORM = 'platform'
FIELD_STATUS = 'status'
FIELD_TITLE = 'title'
FIELD_DETAILED = 'detailed'

DATA_KEY_BUG = 'Bugs'
DATA_KEY_JOB = 'Jobs'
DATA_KEY_DOC = 'Docs'

__data_mapping__ = [
    {
        #BugId 平台	项目	投入时长	标题	进展	状态	日期	风险
        "name": "Bugs",
        "columns": [
            {"column": "BugId", "field":  "BugId", "type": str},
            {"column": "平台", "field":  "platform", "type": str},
            {"column": "项目", "field":  "project", "type": str},
            {"column": "日期", "field": "update_date", "type": datetime.date},
            {"column": "投入时长", "field": "hour", "type": float},
            {"column": "标题", "field": "title", "type": str},
            {"column": "进展", "field": "detailed", "type": str},
            {"column": "状态", "field": "status", "type": str},
            {"column": "风险", "field": "risk", "type": str},
       ]
    },
    {#分类	标题	文档地址	投入时长	进展	状态	日期
        "name": "Docs",
        "columns": [
            {"column": "分类", "field":  "category", "type": str},
            {"column": "标题", "field": "title", "type": str},
            {"column": "进展", "field": "detailed", "type": str},
            {"column": "状态", "field": "status", "type": str},
            {"column": "日期", "field": "update_date", "type": datetime.date},
            {"column": "投入时长", "field": "hour", "type": float}
        ]
    },
    {
        #分类	平台	项目	投入时长	标题	进展	状态	日期
        "name": "Jobs",
        "columns": [
            {"column": "分类", "field": "category", "type": str},
            {"column": "平台", "field": "platform", "type": str},
            {"column": "项目", "field": "project", "type": str},
            {"column": "投入时长", "field": "hour", "type": float},
            {"column": "标题", "field": "title", "type": str},
            {"column": "进展", "field": "detailed", "type": str},
            {"column": "状态", "field": "status", "type": str},
            {"column": "日期", "field": "update_date", "type": datetime.date},
        ]
    }
]

__db_bugs_records__ = []
__db_docs_records__ = []
__db_jobs_records__ = []


def initialize():
    pass


def read_excel(name):
    if not os.path.exists(__excel_file__):
        print('File not found')
        return

    df = pd.read_excel(__excel_file__, sheet_name=name)

    cols = [r for r in df.columns]

    rows = [r for r in df.values]

    records = []

    records = [{cols[i]: rec[i] for i in range(len(cols))} for rec in rows]

    [logging.debug(r) for r in records]

    return records


def data_filter():
    pass




def run(excel_file):
    global __excel_file__, __db_bugs_records__ , __db_jobs_records__, __db_docs_records__

    if not os.path.exists(excel_file):
        print('File not found')
        return
    __excel_file__ = excel_file


    __db_bugs_records__ = setup_data(DATA_KEY_BUG)
    __db_docs_records__ = setup_data(DATA_KEY_DOC)
    __db_jobs_records__ = setup_data(DATA_KEY_JOB)


def data_mapping(sheet, records):
    __mapping =[r for r in __data_mapping__ if r[DATA_MAPPING_NAME] == sheet]

    _columns = __mapping[0][DATA_MAPPING_COLUMNS]

    new_records = []
    for rec in records:
        obj = {}
        new_records.append(obj)
        for col in _columns:
            obj[col[DATA_MAPPING_FIELD]] = rec[col[DATA_MAPPING_COL]]

    return new_records


def setup_data(sheet):
    records = read_excel(sheet)
    return data_mapping(sheet, records)


if __name__ == '__main__':
    run('//work2//git-source//Apollo//src//kpi//docs//Book.xlsx')
