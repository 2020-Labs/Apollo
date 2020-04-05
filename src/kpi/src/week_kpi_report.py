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

import logging

import pandas as pd
import excel_data as db
import xlsxwriter
from pandas._libs.tslibs.timestamps import Timestamp

import calendar

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

    records_list = [db.__db_bugs_records__, db.__db_jobs_records__ , db.__db_docs_records__]
    days = sorted({r[db.FIELD_UPDATE_DATE] for rec in records_list for r in rec})

    first_day = days[0]
    last_day = days[-1]

    week_of_fist_day = first_day.dayofweek

    diff_day = last_day - first_day

    #day = first_day.replace(day=first_day.day + i)

    dayofweek_start = 2
    dayofweek_end = 1

    weeks = []


    for i in range(diff_day.days + 1):
        _day = first_day.replace(day=first_day.day + i)
        _dayofweek = _day.dayofweek

        if _dayofweek == dayofweek_start:
            logging.debug(_day)

            _start = _day
            #_end = _day.replace(day=_day.day + 6)
            _end = 6
            weeks.append([_start, _end])
        elif _day == first_day:
            _start = _day

            _day_step = 0

            # if(_start.dayofweek > dayofweek_start):
            #     _day_step = (7 - dayofweek_start) + (7 - dayofweek_end)
            # elif (_start.dayofweek < dayofweek_start):
            #     _day_step = dayofweek_end - _start + 1

            _day.dayofweek - dayofweek_start

            #_day_start =

            #_end = _day.replace(day=_day.day + _day_step)
            weeks.append([_start, _day_step])

        # elif _day == last_day or _dayofweek == dayofweek_end:
        #     logging.debug(_day)
        #     logging.debug('<' * 5)
        #     _w.append(_day)
        # else:
        #     continue

    first_week_day = calendar.THURSDAY
    last_week_day = calendar.WEDNESDAY
    calendar.setfirstweekday(first_week_day)
    weeks = calendar.monthcalendar(first_day.year, first_day.month)
    days = []
    days_week = []
    for w in weeks:
        for day in w:
            if day == 0:
                continue
            else:
                date_str = '2020-3-' + str(day)
                days.append(date_str)

    logging.debug(days)

    for w in weeks:
        week = []
        for day in w:
            if day == 0:
                date_str = 'N/A'
            else:
                date_str = '2020-3-' + str(day)

            if date_str == 'N/A':
                week.append(date_str)
            else:
                week.append(Timestamp(date_str))


        days_week.append(week)

    logging.debug(days_week)

    _step = 0

    _test_day = Timestamp('2020-3-25')

    if _test_day.dayofweek > first_week_day:
        _step = calendar.SUNDAY - _test_day.dayofweek + last_week_day + 1
    elif _test_day.dayofweek < last_week_day:
        _step = last_week_day - _test_day.dayofweek

    logging.debug('day: {0} , step: {1}'.format(_test_day ,  str(_step)))

    t1 = Timestamp('2020-1-1')
    t2 = Timestamp('2020-01-01')

    for w in days_week:
        if first_day in w:
            logging.debug(w)




    logging.debug('t1 == t2 ? ' + str(t1 == t2))

    #print(calendar.monthcalendar(2020, 4))




    #logging.debug(weeks)
    # for _days in weeks:
    #     day_start = _days[0]
    #     day_end = _days[1]
    #     records = [r for r in db.__db_bugs_records__ if r[db.FIELD_UPDATE_DATE] >=day_start and r[db.FIELD_UPDATE_DATE]<=day_end]
    #
    #     logging.debug(_days)
    #     for r in records:
    #         logging.debug(r)
    #justdo()
    #(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY) = range(7)
    get_week_range('2020-3-3', '2020-4-5')
    get_week_range('2020-3-3', '2020-4-5', first_week_day=calendar.WEDNESDAY)
    get_week_range('2020-3-3', '2020-4-5', first_week_day=calendar.THURSDAY)
    get_week_range('2020-3-3', '2020-4-5', first_week_day=calendar.FRIDAY)
    get_week_range('2020-3-3', '2020-4-5', first_week_day=calendar.SATURDAY)



def get_days(start_date,end_date):
    _first_year = start_date.year
    _first_month = start_date.month

    _last_year = end_date.year
    _last_month = end_date.month

    years = []

    if start_date.day < 7:
        years.append(calendar._prevmonth(_first_year, _first_month))

    y_m = (_first_year, _first_month)
    while y_m <= (_last_year, _last_month):
        years.append(y_m)
        y_m = calendar._nextmonth(y_m[0], y_m[1])

    if end_date.day > calendar._monthlen(_last_year, _last_month) - 7:
        years.append(calendar._nextmonth(_last_year, _last_month))

    __days = []
    for ym in years:
        y = ym[0]
        m = ym[1]
        days = [Timestamp('{0}-{1}-{2}'.format(y, m, d)) for d in calendar.Calendar().itermonthdays(ym[0], ym[1]) if d > 0]
        #logging.debug(days)

        __days.extend(days)

    return __days


def get_week_range(start_date, end_date, first_week_day=calendar.MONDAY):
    if not (first_week_day >= calendar.MONDAY and first_week_day <= calendar.SUNDAY):
        raise ValueError('first_week_day is invalid')

    if first_week_day == calendar.MONDAY:
        last_week_day = calendar.SUNDAY
    else:
        last_week_day = first_week_day - 1

    logging.debug('first-day:{0} , last-day: {1}'.format(str(first_week_day), str(last_week_day)))

    _first_day = Timestamp(start_date)
    _last_day = Timestamp(end_date)

    __days = get_days(_first_day, _last_day)

    logging.debug(__days)

    _first_day_index = __days.index(_first_day)
    _last_day_index = __days.index(_last_day)

    if first_week_day == calendar.MONDAY:
        _first_day_dayofweek_index = _first_day_index - _first_day.dayofweek
        _last_day_dayofweek_index = _last_day_index + (calendar.SUNDAY - _last_day.dayofweek)
    else:
        if _first_day.dayofweek >= first_week_day:
            _first_day_dayofweek_index = _first_day_index - (_first_day.dayofweek - first_week_day)
        else:
            _first_day_dayofweek_index = _first_day_index - (calendar.SUNDAY - first_week_day + 1 + _first_day.dayofweek)

        if _last_day.dayofweek >= first_week_day:
            _tail_step = calendar.SUNDAY - _last_day.dayofweek + last_week_day + 1
        elif _last_day.dayofweek <= last_week_day:
            _tail_step = last_week_day - _last_day.dayofweek

        _last_day_dayofweek_index = _last_day_index + _tail_step

    for i in range(_first_day_dayofweek_index,_last_day_dayofweek_index, 7):
        end_index = i + 6
        logging.debug('{0}(index={1}) - {2}(index={3})'.format(__days[i],i, __days[end_index],end_index))




def justdo():
    _first_day = Timestamp('2020-3-2')
    _last_day = Timestamp('2020-3-3')
    first_week_day = calendar.MONDAY
    last_week_day = calendar.SUNDAY

    first_week_day = calendar.THURSDAY
    last_week_day = calendar.WEDNESDAY

    _first_year = _first_day.year
    _first_month = _first_day.month

    _last_year = _last_day.year
    _last_month = _last_day.month


    diff_day = _last_day - _first_day

    #for m in range(_first_month, _last_month):

    years = []

    years.append(calendar._prevmonth(_first_year, _first_month))
    y_m = (_first_year, _first_month)

    while y_m <= (_last_year, _last_month):
        years.append(y_m)
        y_m = calendar._nextmonth(y_m[0], y_m[1])


    years.append(calendar._nextmonth(_last_year, _last_month))
    logging.debug(years)

    __days = []
    for ym in years:
        y = ym[0]
        m = ym[1]
        days = [Timestamp('{0}-{1}-{2}'.format(y, m, d)) for d in calendar.Calendar().itermonthdays(ym[0], ym[1]) if d > 0]
        #logging.debug(days)

        __days.extend(days)
        #__days.append('{0}-{1}-{2}'.format(y,m,))


    _first_day_index = __days.index(_first_day)

    _last_day_index = __days.index(_last_day)

    #__days = [d for d in __days if d>=_first_day and d<=_last_day]
    #logging.debug(__days)




    #计算第一天所在周内第一天

    if first_week_day == calendar.MONDAY:
        _first_day_dayofweek_index = _first_day_index - _first_day.dayofweek
    else:
        if _first_day.dayofweek >= first_week_day:
            _first_day_dayofweek_index = _first_day_index - (_first_day.dayofweek - first_week_day)
        else:
            _first_day_dayofweek_index = _first_day_index - (calendar.SUNDAY - first_week_day + 1 + _first_day.dayofweek)


        # if _last_day.dayofweek >= first_week_day:
        #     _last_day_dayofweek_index = _last_day_index - (_last_day.dayofweek - last_week_day)
        # else:
        #     _last_day_dayofweek_index = _last_day_index - (calendar.SUNDAY - last_week_day + 1 + _last_day.dayofweek)


    logging.debug('first day: {0} , {1}'.format(__days[_first_day_dayofweek_index], __days[_first_day_index]))


    #找出第一天所在周的周内最后一天
    #周一是一周第一天
    if first_week_day == calendar.MONDAY:
        _head_step = last_week_day - _first_day.dayofweek
        _tail_step = last_week_day - _last_day.dayofweek
        _last_day_dayofweek_index = _last_day_index + (calendar.SUNDAY  - _last_day.dayofweek)
    else:
        if _first_day.dayofweek >= first_week_day:
            _head_step = calendar.SUNDAY - _first_day.dayofweek + last_week_day + 1
        elif _first_day.dayofweek <= last_week_day:
            _head_step = last_week_day - _first_day.dayofweek

        if _last_day.dayofweek >= first_week_day:
            _tail_step = calendar.SUNDAY - _last_day.dayofweek + last_week_day + 1
        elif _last_day.dayofweek <= last_week_day:
            _tail_step = last_week_day - _last_day.dayofweek

        _last_day_dayofweek_index = _last_day_index + _tail_step



    # _result = [[_first_day, __days[_head_step]]]
    # for i in range(_head_step + 1, diff_day.days + _tail_step, 7):
    #     end_index = i + 6
    #     if end_index <= len(days):
    #         logging.debug('{0} - {1}'.format(__days[i] , __days[end_index]))
    #         _result.append([__days[i] , __days[end_index]])
    #     else:
    #         logging.debug('{0} - {1}'.format(__days[i], __days[-1]))
    #         _result.append([__days[i], __days[-1]])

    _result = []

    for i in range(_first_day_dayofweek_index,_last_day_dayofweek_index, 7):
        end_index = i + 6
        logging.debug('{0}(index={1}) - {2}(index={3})'.format(__days[i],i, __days[end_index],end_index))

    logging.debug(_result)

