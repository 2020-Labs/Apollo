#!/usr/bin/env python
#-*- coding:utf-8 _*-

"""
@File       : week_kpi_report.py
@version    : 0.1
@Author     : kelvin
@Time       : 2020-03-29

--------------------------------------------------------------------
@Changes log:
    2020-03-29 : 0.1 Create
"""

__output_excel__ = '/work2//git-source//Apollo//src//kpi//docs//kpi_report.xlsx'

import pandas as pd
import xlsxwriter


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

headers_cell_setting = [
    {
        'cell': 'A1:A3',
        'text': '周期',  'width': 4,   'format': header_center_format
    },
    {
        'cell': 'B1:B3',
        'text': '星期',   'width': 4,  'format': header_center_format
    },
    {
        'cell': 'C1:C3',
        'text': '日期',   'width': 10, 'format': header_center_format
    },
    {
        'cell': 'D1:H1',
        'text': '客观数据',   'width': 50, 'format': header_center_format
    },
    {
        'cell': 'D2:G2',
        'text': '缺陷解决',   'width': 50, 'format': header_center_format
    },
    {
        'cell': 'H2',
        'text': '代码提交',   'width': 8, 'format': header_center_format
    },
    {
        'cell': 'D3',
        'text': '待验证',   'width': 6, 'format': header_center_format
    },
    {
        'cell': 'E3',
        'text': '分析后转出',   'width': 8, 'format': header_center_format
    },
    {
        'cell': 'F3',
        'text': '遗留',   'width': 4, 'format': header_center_format
    },
    {
        'cell': 'G3',
        'text': '修复率',   'width': 6, 'format': header_center_format
    },
    {
        'cell': 'H3',
        'text': '次数',   'width': 8, 'format': header_center_format
    },
    {
        'cell': 'I1:I3',
        'text': '文档',   'width': 4, 'format': header_center_format
    },
    {
        'cell': 'J1:J3',
        'text': '培训',   'width': 4, 'format': header_center_format
    },
    {
        'cell': 'K1:K3',
        'text': '人效',   'width': 4, 'format': header_center_format
    },
    {
        'cell': 'L1:L3',
        'text': '本周关键工作简述&评价',   'width': 50, 'format': header_format
    }
]

def output_report(args):
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
    worksheet.set_row(1, 20)
    worksheet.set_row(2, 20)

    workbook.close()