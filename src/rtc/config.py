#!/usr/bin/env python
#-*- coding:utf-8 _*-

"""
@File       : AppConfig.py
@version    : 0.1
@Author     : Kelvin
@Time       : 2020-03-01

--------------------------------------------------------------------
@Changes log:
    2020-03-01 : 0.1 Create

"""

import json
import logging
import os

KEY_URL = 'url'
KEY_FIX = 'fix'
KEY_OUT = 'out'


class AppConfig:

    __cfg_file__ = ''

    VERSION = ''

    MEMBERS = []

    REPORT_TITLE = ''

    REPORT_FMT = ''

    REPORT_FILE = ''

    RTCs = []

    DATE = ''

    BASE_PATH = ''

    def __init__(self, file):
        logging.info('read config: {0}'.format(file))
        AppConfig.__cfg_file__ = file

    @staticmethod
    def readConfig():
        logging.info('read config: {0}'.format(AppConfig.__cfg_file__ ))
        file = AppConfig.__cfg_file__

        try:
            with open(AppConfig.__cfg_file__, encoding='utf-8') as f:
                data = json.load(f)
            logging.debug(data)
        except Exception as e:
            logging.error('json decode error')
            import traceback
            traceback.print_exc()
            return False

        AppConfig.MEMBERS = data['members']
        AppConfig.VERSION = data['version']
        AppConfig.MEMBERS = data['members']
        AppConfig.REPORT_TITLE = data['report_title']
        AppConfig.REPORT_FMT = data['report_fmt']
        AppConfig.REPORT_FILE = data['report_file']
        AppConfig.BASE_PATH = os.path.dirname(file)
        AppConfig.DATE = data['report_time']

        for i in range(1, 4):
            key = 'rtc' + str(i)
            if data.get(key):
                obj = {}
                obj['url'] = data.get(key)['url']
                obj['fix'] = data.get(key)['fix']
                obj['out'] = data.get(key)['out']
                AppConfig.RTCs.append(obj)

        logging.debug('RTCs: ' + str(AppConfig.RTCs))

        for obj in AppConfig.RTCs:
            logging.debug(obj)
        return True
