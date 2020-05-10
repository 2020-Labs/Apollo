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
import app_config


import team_work_report
import checkdata

import team_weekly_kpi_report

cmd = None

cmds_team_report = ['team-work-report', 'team-weekly-kpi-report']

cmds_personal_report = ['daily-kpi-report', 'weekly-kpi-report', 'check-data']

CMDS = {
    'team-work-report': team_work_report.output_report,
    'daily-kpi-report': daily_kpi_report.output_report,
    'weekly-kpi-report': week_kpi_report.output_report,
    'check-data': checkdata.output_report,
    'team-weekly-kpi-report': team_weekly_kpi_report.output_report,
}

def main():
    #excel_data.run('//work2//git-source//Apollo//Book.xlsx', my_name='AAAA', args= app_config.__args_opts__)
    #excel_data.run('//work2//git-source//Apollo//BookB.xlsx', my_name='BBB', args=__args_opts__)
    #daily_kpi_report.output_report()
    #week_kpi_report.output_report()
    #team_work_report.output_report(__args_opts__)

    cmd = 'daily-kpi-report'
    cmd = 'weekly-kpi-report'
    cmd = 'team-work-report'
    #cmd = 'team-weekly-report'
    #cmd = 'check-data'
    #cmd = 'team-weekly-kpi-report'
    # 只输出个人

    # 允许输出多个报表
    if cmd in cmds_personal_report:
        for name, file in app_config.__excel_files__.items():
            excel_data.run(file)
            CMDS[cmd](app_config.__args_opts__)

    # 团队报表
    elif cmd in cmds_team_report:
        for name , file in app_config.__excel_files__.items():
           excel_data.run(file, name, args = app_config.__args_opts__)
        #team_work_report.output_report(app_config.__args_opts__)
        CMDS[cmd](app_config.__args_opts__)


def logging_initialize():
    LOG_FILE = os.path.join(os.getcwd(), 'log.txt')
    LOG_FMT = '%(asctime)s  %(filename)s %(funcName)s: %(levelname)s  %(message)s'
    logging.basicConfig(format=LOG_FMT, filename=LOG_FILE, level=logging.DEBUG)

    # Output the log for console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(LOG_FMT))
    # Create an instance
    logging.getLogger().addHandler(console)

    logging.info('logging configuration done.')




if __name__ == '__main__':
    # kpi.py --help
    #   --excel=xxx.xlsx
    #   --daily-kpi-report
    #   --weekly-kpi-report
    #   --date=2020-3-1,2020-3-4
    #   --platform=
    #   --

    logging_initialize()
    opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "excel=", 'daily-kpi-report','weekly-kpi-report', 'output=', 'date='])
    app_config.parse_opts(opts)
    main()
