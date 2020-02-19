import copy
import json
import logging
import os

import config

data_list_fix = []
data_list_out = []
big_data = {}

initial_data = {}

last_data = {}

COLUMNS_DATE = 'date'
COLUMNS_FIX = 'fix'
COLUMNS_OUT = 'out'
COLUMNS_TOTAL = 'total'

DATA_FILE = os.path.join(os.getcwd(), 'db/initial.dat')

def initial():
    global initial_data,last_data
    with open(DATA_FILE) as f:
        data = json.load(f)
    logging.debug(data)

    initial_data = data.get('initial')
    last_data = data.get('last')
    logging.debug('initial: ' + str(initial_data))
    logging.debug('last: ' + str(last_data))


def put_fix(url,data):
    logging.debug('url: {0} , data: {1}'.format(url, str(data)))
    data['url'] = url
    data_list_fix.append(data)

def put_out(url,data):
    logging.debug('url: {0} , data: {1}'.format(url, str(data)))
    data['url'] = url
    data_list_out.append(data)

def print_out():

    logging.debug(str(data_list_fix))
    logging.debug(str(data_list_out))

    big_data['date'] = config.DATE
    for m in config.MEMBERS:
        #初始化结构体
        obj = {}
        obj['fix'] = 0
        obj['out'] = 0
        big_data[m] = obj

        for r in data_list_fix:
            if r['name'] == m:
                big_data[m]['fix'] += r['fix']

        for r in data_list_out:
            if r['name'] == m:
                big_data[m]['out'] += r['out']

        big_data[m]['total'] = big_data[m]['fix'] + big_data[m]['out']

    logging.debug('return: ' + dump_to_json(big_data))


def get_all_data():
    return big_data

def calc_new():
    result = copy.deepcopy(big_data);
    logging.debug('old data: ' + str(result))
    for k, v in result.items():
        logging.debug(v)

        if initial_data and initial_data.get(k) and config.MEMBERS.__contains__(k):
            v['fix'] -= initial_data[k]['fix']
            v['out'] -= initial_data[k]['out']
            v[COLUMNS_TOTAL] = v[COLUMNS_FIX] + v[COLUMNS_OUT]

    logging.debug('return: ' + dump_to_json(result))
    logging.debug('return2: ' + dump_to_json(big_data))
    return result


def calc_last():
    result = copy.deepcopy(big_data);
    logging.debug('old data: ' + str(result))
    for k, v in result.items():
        logging.debug(v)

        if last_data and last_data.get(k) and config.MEMBERS.__contains__(k):
            v['fix'] -= last_data[k]['fix']
            v['out'] -= last_data[k]['out']
            v[COLUMNS_TOTAL] = v[COLUMNS_FIX] + v[COLUMNS_OUT]
    logging.debug('return: ' + dump_to_json(result))
    logging.debug('return2: ' + dump_to_json(big_data))

    return result

def get_initial_date():
    if initial_data:
        return initial_data.get('date')

    return None

def get_last_date():
    if last_data:
        return last_data.get('date')

    return None


def dump_to_json(dict):
    return json.dumps(dict, indent=4)

def save_all():
    pass