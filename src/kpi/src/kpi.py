#!/usr/bin/env python
#-*- coding:utf-8 _*-

"""
@File       : kpi.py
@version    : 0.1
@Author     : kelvin
@Time       : 2020-03-29

--------------------------------------------------------------------
@Changes log:
    2020-03-29 : 0.1 Create
"""
import getopt
import logging
import os
import sys

import excel_data
import daily_kpi_report
import week_kpi_report

__args_opts__ = None

def main():
    excel_data.run('//work2//git-source//Apollo//src//kpi//docs//Book.xlsx')
    daily_kpi_report.output_report(__args_opts__)
    #week_kpi_report.output_report(__args_opts__)




def logging_initialize():
    LOG_FILE = os.path.join(os.getcwd(), 'log.txt')
    LOG_FMT = '%(asctime)s  %(filename)s %(funcName)s: %(levelname)s  %(message)s'
    logging.basicConfig(format=LOG_FMT,filename=LOG_FILE, level=logging.DEBUG)

    # Output the log for console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(LOG_FMT))
    # Create an instance
    logging.getLogger().addHandler(console)

    logging.info('logging configuration done.')


if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "excel=", 'daily-kpi-report', 'output='])
    __args_opts__ = opts
    logging_initialize()
    main()
