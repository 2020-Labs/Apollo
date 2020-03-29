#!/usr/bin/env python
#-*- coding:utf-8 _*-

"""
@File       : rtckpi.py
@version    : 0.1
@Author     : Kelvin
@Time       : 2020-03-01

--------------------------------------------------------------------
@Changes log:
    2020-03-01 : 0.1 Create
"""
import getopt
import logging
import os
import sys

import config
import db
import log
import report

from config import AppConfig
from spider import RtcSpider

CONFIG_FILE = ''

ERROR_ARGS = -1

ERROR_CONFIG_FILE_NOT_FOUND = -2


def usage():
    print('Usage: [-c|-h] [--help|--config-file=]');
    print('   -c|--config-file=')
    print('     配置文件路径，')


def check_arg():
    global CONFIG_FILE
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:", ["help", "config-file="]);

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage();
                sys.exit(1);
            elif opt in ("-c", "--config-file"):
                CONFIG_FILE = arg
            else:
                logging.info("%s ==> %s" % (opt, arg));

    except getopt.GetoptError:
        print("getopt error!");
        usage()
        return False

    if not CONFIG_FILE:
        usage()
        print('-_-' * 20)
        print('错误：-c|--config, 请指定配置文件路径！！')
        return False

    if not os.path.exists(CONFIG_FILE):
        print('文件:{0}不存在！！'.format(CONFIG_FILE))
        return False

    return True


def run():
    log.initial()
    if not check_arg():
        sys.exit(ERROR_ARGS)

    logging.info('check done.')

    if not AppConfig(CONFIG_FILE).readConfig():
        sys.exit(ERROR_CONFIG_FILE_NOT_FOUND)

    #db.initial()
    db2 = db.DbHelper.getInstance()

    logging.info('-' * 150)


    for cfg in AppConfig.RTCs:
        htmlloader = RtcSpider(os.path.join(AppConfig.BASE_PATH, cfg[config.KEY_URL]), AppConfig.MEMBERS)
        htmlloader.load()

        logging.info('url:{0}'.format(cfg[config.KEY_URL]))

        for id in cfg[config.KEY_FIX]:
            logging.info('fix id:{0}'.format(id))
            for fix in htmlloader.extract_fix(id):
                logging.info(fix)
                db2.put_fix(cfg[config.KEY_URL], fix)

            logging.info('=' * 150)

        #out
        for id in cfg[config.KEY_OUT]:
            logging.info('out id:{0}'.format(id))
            for out in htmlloader.extract_out(id):
                logging.info(out)
                db2.put_out(cfg[config.KEY_URL], out)

    db2.calc_all()

    db2.calc_new()

    db2.calc_last()
    rpt = report.ReportText()
    rpt.output_report()

    db2.save_all()

if __name__ == '__main__':
    run()



