#!/usr/bin/env python
#-*- coding:utf-8 _*-

"""
@File       : db.py
@version    : 0.1
@Author     : Kelvin
@Time       : 2020-03-01

--------------------------------------------------------------------
@Changes log:
    2020-03-01 : 0.1 Create

"""
import copy
import json
import logging
import os
import time
from json import JSONDecodeError
from config import AppConfig


COLUMNS_NAME = 'name'
COLUMNS_DATE = 'date'
COLUMNS_FIX = 'fix'
COLUMNS_OUT = 'out'
COLUMNS_TOTAL = 'total'
COLUMNS_CREATE_TIME = 'createtime'
COLUMNS_URL = 'url'

KEY_INITIAL = 'initial'
KEY_LASTEST = 'last'
KEY_DATE = 'date'
KEY_DELTA = 'delta'
KEY_CREATE_TIME = 'createtime'

class DbHelper:

    # data file
    __DATA_FILE_INITIAL = os.path.join(os.getcwd(), 'db/initial.db')
    __DATA_FILE_SHADOW = os.path.join(os.getcwd(), 'db/initial_shadow.db')
    __DATA_FILE_HISTORY = os.path.join(os.getcwd(), 'db/history_records.db')

    # data sets
    __db_history_records = []
    __db_fix = []
    __db_out = []
    __db_urls = []

    __initial_data = {}

    __last_data = {}

    __view_all_data = {}

    __instance = None

    @staticmethod
    def getInstance():
        if DbHelper.__instance is None:
            DbHelper.__instance = DbHelper()

        return DbHelper.__instance

    def __init__(self):
        try:
            with open(self.__DATA_FILE_INITIAL) as f:
                data = json.load(f)
            logging.debug(data)
        except (JSONDecodeError, FileNotFoundError) as e:
            data = {}

        self.__initial_data = data.get(KEY_INITIAL) if data.get(KEY_INITIAL) else {}
        self.__last_data = data.get(KEY_LASTEST) if data.get(KEY_LASTEST) else {}

        logging.info('__initial: ' + str(self.__initial_data))
        logging.info('__last: ' + str(self.__last_data))

    def put_fix(self, url, data):
        '''
        添加一条数据（修复Bug的数据）
        :param url:
        :param data:
        :return:
        '''
        if COLUMNS_FIX not in data.keys():
            raise Exception('Not found column [{0}] in keys'.format(COLUMNS_FIX))

        logging.debug('url: {0} , data: {1}'.format(url, str(data)))
        data[COLUMNS_URL] = url
        data[COLUMNS_CREATE_TIME] = self.__get_current_time()
        self.__db_fix.append(data)

        if url not in self.__db_urls:
            self.__db_urls.append(url)

    def put_out(self, url, data):
        '''
        添加一条数据（转出Bug的数据）
        :param url:
        :param data:
        :return:
        '''
        if COLUMNS_OUT not in data.keys():
            raise Exception('Not found column [{0}] in keys'.format(COLUMNS_OUT))

        logging.debug('url: {0} , data: {1}'.format(url, str(data)))
        data[COLUMNS_URL] = url
        data[COLUMNS_CREATE_TIME] = self.__get_current_time()
        self.__db_out.append(data)
        if url not in self.__db_urls:
            self.__db_urls.append(url)

    def __get_current_time(self):
        return time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime())

    def calc_all(self):
        """
        汇总修复bug和转出bug的数据
        :return:
        """

        self.__view_all_data[COLUMNS_DATE] = AppConfig.DATE
        for m in AppConfig.MEMBERS:
            # 初始化结构体
            self.__view_all_data[m] = {COLUMNS_NAME: m, COLUMNS_FIX: 0, COLUMNS_OUT: 0}

            for rec in self.__db_fix:
                if rec[COLUMNS_NAME] == m:
                    self.__view_all_data[m][COLUMNS_FIX] += rec[COLUMNS_FIX]

            for rec in self.__db_out:
                if rec[COLUMNS_NAME] == m:
                    self.__view_all_data[m][COLUMNS_OUT] += rec[COLUMNS_OUT]

            self.__view_all_data[m][COLUMNS_TOTAL] = self.__view_all_data[m][COLUMNS_FIX] \
                                                        + self.__view_all_data[m][COLUMNS_OUT]

        logging.debug('return: ' + self.__dump_to_json(self.__view_all_data))

    def get_all_data(self):
        return self.__view_all_data

    def calc_new(self):
        """
        :return:
        """
        if not self.__initial_data.keys():
            logging.debug('empty')
            return None

        result = copy.deepcopy(self.__view_all_data)

        for k, v in result.items():
            logging.debug(v)

            if k in self.__initial_data.keys() and k in AppConfig.MEMBERS:
                v[COLUMNS_FIX] -= self.__initial_data[k][COLUMNS_FIX]
                v[COLUMNS_OUT] -= self.__initial_data[k][COLUMNS_OUT]
                v[COLUMNS_TOTAL] = v[COLUMNS_FIX] + v[COLUMNS_OUT]

        logging.debug('return: ' + self.__dump_to_json(result))
        return result

    def calc_last(self):
        if not self.__last_data.keys():
            logging.debug('empty')
            return None

        result = copy.deepcopy(self.__view_all_data);

        for k, v in result.items():
            logging.debug(v)
            if k in self.__last_data.keys() and k in AppConfig.MEMBERS:
                v[COLUMNS_FIX] -= self.__last_data[k][COLUMNS_FIX]
                v[COLUMNS_OUT] -= self.__last_data[k][COLUMNS_OUT]
                v[COLUMNS_TOTAL] = v[COLUMNS_FIX] + v[COLUMNS_OUT]
        logging.debug('return: ' + self.__dump_to_json(result))
        return result

    def calc_data_by_file(self):
        logging.debug(self.__db_urls)

        for url in self.__db_urls:
            _all_data = {}
            for m in AppConfig.MEMBERS:
                logging.debug(m)

                # 初始化结构体
                _all_data[m] = {COLUMNS_NAME: m, COLUMNS_FIX: 0, COLUMNS_OUT: 0}

                for r in self.__db_fix:
                    if r[COLUMNS_URL] == url and r[COLUMNS_NAME] == m:
                        _all_data[m][COLUMNS_FIX] += r[COLUMNS_FIX]

                for r in self.__db_out:
                    logging.debug(r)
                    if r[COLUMNS_URL] == url and r[COLUMNS_NAME] == m:
                        _all_data[m][COLUMNS_OUT] += r[COLUMNS_OUT]

                _all_data[m][COLUMNS_TOTAL] = _all_data[m][COLUMNS_FIX] + _all_data[m][COLUMNS_OUT]
            logging.debug(_all_data)
            yield url, _all_data.values()

    def get_initial_date(self):
        if self.__initial_data:
            return self.__initial_data.get('date')

        return None

    def get_last_date(self):
        if self.__last_data:
            return self.__last_data.get('date')

        return None

    def __dump_to_json(self, data):
        return json.dumps(data, indent=4, ensure_ascii=False)

    def save_all(self):
        record = {
            KEY_CREATE_TIME: self.__get_current_time(),
            KEY_DELTA: self.get_all_data()
        }

        with open(self.__DATA_FILE_HISTORY, mode="a", encoding='utf-8') as file:
            file.write(str(record) + "\n")

        data = {
            KEY_INITIAL: self.__initial_data,
            KEY_LASTEST: self.__last_data
        }
        with open(self.__DATA_FILE_SHADOW, mode='w', encoding='utf-8') as file:
            file.write(self.__dump_to_json(data))

