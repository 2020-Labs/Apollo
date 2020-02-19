import json
import logging
import os

VERSION = ''

MEMBERS = []

REPORT_TITLE = ''

REPORT_FMT = ''

REPORT_FILE = ''

REPORT_FULL_PATH = ''
RTC1_URL = ''
RTC1_FIX_IDS = []
RTC1_OUT_IDS = []

RTCS = []

DATE = ''


def read_config(file):
    global VERSION, MEMBERS, REPORT_TITLE, REPORT_FMT, DATE , REPORT_FILE , REPORT_FULL_PATH
    data = []
    try:
        with open(file) as f:
            data = json.load(f)
        logging.debug(data)
    except Exception as e:
        logging.error('json decode error')
        import traceback
        traceback.print_exc()
        return False

    VERSION = data['version']
    MEMBERS = data['members']
    REPORT_TITLE = data['report_title']
    REPORT_FMT = data['report_fmt']
    REPORT_FILE = data['report_file']

    REPORT_FULL_PATH = os.path.join(os.path.dirname(file), REPORT_FILE)
    #
    DATE = '2020-2-20'
    # obj = {}
    # obj['url'] = data['rtc1']['url']
    # obj['fix'] = data['rtc1']['fix']
    # obj['out'] = data['rtc1']['out']
    # #logging.debug(obj)
    # #RTCS.append(obj)
    # obj = {}
    # # obj['url'] = data['rtc2']['url']
    # # obj['fix'] = data['rtc2']['fix']
    # # obj['out'] = data['rtc2']['out']
    #
    # # RTCS.append(obj)


    for i in range(1,4):
        key = 'rtc'+str(i)
        if data.get(key):
            obj = {}
            obj['url'] = data.get(key)['url']
            obj['fix'] = data.get(key)['fix']
            obj['out'] = data.get(key)['out']
            RTCS.append(obj)

    logging.debug('RTCS: ' + str(RTCS))

    for obj in RTCS:
        logging.debug(obj)

    return True
