import copy
import json
import logging
import os
import time
from json import JSONDecodeError

import config

all_data = {}

initial_data = {}

last_data = {}

COLUMNS_NAME = 'name'
COLUMNS_DATE = 'date'
COLUMNS_FIX = 'fix'
COLUMNS_OUT = 'out'
COLUMNS_TOTAL = 'total'

# data file
DATA_FILE = os.path.join(os.getcwd(), 'db/initial.dat')
DATA_SHADOW_FILE = os.path.join(os.getcwd(), 'db/initial_shadow.dat')
HISTORY_FILE = os.path.join(os.getcwd(), 'db/history_db.dat')

# data sets
db_history_records = []
db_fix = []
db_out = []
db_urls = []

def initial():
    '''
    初始化，加载统计的初始数据
    :return:
    '''
    global initial_data, last_data, db_history_records
    try:
        with open(DATA_FILE) as f:
            data = json.load(f)
        logging.debug(data)
    except (JSONDecodeError, FileNotFoundError) as e:
        data = {}

    initial_data = data.get('initial') if data.get('initial') else {}
    last_data = data.get('last') if data.get('last') else {}

    logging.debug('initial: ' + str(initial_data))
    logging.debug('last: ' + str(last_data))

    try:
        with open(HISTORY_FILE) as f:
            db_history_records = json.load(f)
    except (JSONDecodeError, FileNotFoundError) as e:
        pass

    logging.debug('history:' + str(db_history_records))

    return True


def put_fix(url, data):
    '''
    添加一条数据（修复Bug的数据）
    :param url:
    :param data:
    :return:
    '''
    logging.debug('url: {0} , data: {1}'.format(url, str(data)))
    data['url'] = url
    db_fix.append(data)
    if url not in db_urls:
        db_urls.append(url)


def put_out(url, data):
    '''
    添加一条数据（转出Bug的数据）
    :param url:
    :param data:
    :return:
    '''
    logging.debug('url: {0} , data: {1}'.format(url, str(data)))
    data['url'] = url
    db_out.append(data)
    if url not in db_urls:
        db_urls.append(url)


def calc_all():
    """
    汇总修复bug和转出bug的数据
    :return:
    """
    logging.debug(str(db_fix))
    logging.debug(str(db_out))

    all_data['date'] = config.DATE
    for m in config.MEMBERS:
        # 初始化结构体
        all_data[m] = {'fix': 0, 'out': 0}

        for r in db_fix:
            if r['name'] == m:
                all_data[m]['fix'] += r['fix']

        for r in db_out:
            if r['name'] == m:
                all_data[m]['out'] += r['out']

        all_data[m]['total'] = all_data[m]['fix'] + all_data[m]['out']

    logging.debug('return: ' + dump_to_json(all_data))


def get_all_data():
    return all_data


def calc_new():
    """
    :return:
    """
    if not initial_data.keys():
        logging.debug('empty')
        return None

    result = copy.deepcopy(all_data);
    #logging.debug('old data: ' + str(result))

    for k, v in result.items():
        logging.debug(v)

        #if initial_data and initial_data.get(k) and config.MEMBERS.__contains__(k):
        if k in initial_data.keys() and k in config.MEMBERS:
            v['fix'] -= initial_data[k]['fix']
            v['out'] -= initial_data[k]['out']
            v[COLUMNS_TOTAL] = v[COLUMNS_FIX] + v[COLUMNS_OUT]

    logging.debug('return: ' + dump_to_json(result))
    logging.debug('return2: ' + dump_to_json(all_data))
    return result


def calc_last():
    if not last_data.keys():
        logging.debug('empty')
        return None

    result = copy.deepcopy(all_data);
    logging.debug('old data: ' + str(result))
    for k, v in result.items():
        logging.debug(v)

        #if last_data and last_data.get(k) and config.MEMBERS.__contains__(k):
        if k in last_data.keys() and k in config.MEMBERS:
            v['fix'] -= last_data[k]['fix']
            v['out'] -= last_data[k]['out']
            v[COLUMNS_TOTAL] = v[COLUMNS_FIX] + v[COLUMNS_OUT]
    logging.debug('return: ' + dump_to_json(result))
    logging.debug('return2: ' + dump_to_json(all_data))

    return result

def calc_data_by_file():
    logging.debug(db_urls)

    for url in db_urls:
        _all_data = {}
        for m in config.MEMBERS:
            # 初始化结构体
            _all_data[m] = {'name': m, 'fix': 0, 'out': 0}


            for r in db_fix:
                if r['url'] == url and r['name'] == m:
                    _all_data[m]['fix'] += r['fix']

            for r in db_out:
                if r['url'] == url and r['name'] == m:
                    _all_data[m]['out'] += r['out']

            _all_data[m]['total'] = _all_data[m]['fix'] + _all_data[m]['out']
        logging.debug(_all_data)
        yield url, _all_data.values()

def get_initial_date():
    if initial_data:
        return initial_data.get('date')

    return None


def get_last_date():
    if last_data:
        return last_data.get('date')

    return None


def dump_to_json(dict):
    return json.dumps(dict, indent=4, ensure_ascii=False)


def save_all():
    record = {}
    record['createtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    record['delta'] = get_all_data()
    obj_str = dump_to_json(record)
    logging.debug(obj_str)
    db_history_records.append(record)
    with open(HISTORY_FILE, mode="w", encoding='utf-8') as file:
        file.write(dump_to_json(db_history_records))


    data= {}
    data['initial'] = initial_data
    data['last'] = get_all_data()
    with open(DATA_SHADOW_FILE, mode='w', encoding='utf-8') as file:
        file.write(dump_to_json(data))