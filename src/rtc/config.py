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

RTCs = []

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
    DATE = data['report_time']

    for i in range(1, 4):
        key = 'rtc' + str(i)
        if data.get(key):
            obj = {}
            obj['url'] = data.get(key)['url']
            obj['fix'] = data.get(key)['fix']
            obj['out'] = data.get(key)['out']
            RTCs.append(obj)

    logging.debug('RTCs: ' + str(RTCs))

    for obj in RTCs:
        logging.debug(obj)

    return True
