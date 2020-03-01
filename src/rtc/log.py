#!/usr/bin/env python
#-*- coding:utf-8 _*-

"""
@File       : log.py
@version    : 0.1
@Author     : Kelvin
@Time       : 2020-03-01

--------------------------------------------------------------------
@Changes log:
    2020-03-01 : 0.1 Create

"""

import logging
import os


LOG_FILE = os.path.join(os.getcwd(), 'log.txt')
LOG_FMT = '%(asctime)s  %(filename)s %(funcName)s: %(levelname)s  %(message)s'


def initial():
    logging.basicConfig(format=LOG_FMT,filename=LOG_FILE, level=logging.DEBUG)

    # Output the log for console
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(LOG_FMT))
    # Create an instance
    logging.getLogger().addHandler(console)

    logging.info('logging configuration done.')

