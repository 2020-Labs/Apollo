#!/usr/bin/env python
#-*- coding:utf-8 _*-

"""
@File       : utils.py
@version    : 0.1
@Author     : kelvin
@Time       : 2020-04-25

--------------------------------------------------------------------
@Changes log:
    2020-04-25 : 0.1 Create
"""
import calendar
import logging
import operator

from pandas._libs.tslibs.timestamps import Timestamp, timedelta

DATE_FORMAT = '%Y-%m-%d'

def date_range(beginDate, endDate):
    dates = []
    _start = Timestamp(beginDate)
    _end = Timestamp(endDate)
    _date = _start
    while _date <= _end:
        dates.append(_date)
        _date = _date + timedelta(1)

    return dates

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