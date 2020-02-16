import copy
import getopt
import logging
import os
import sys
import log
import config
import spider

CONFIG_FILE = ''


def usage():
    print('Usage: [-c|-h] [--help|--config=]');
    print('   -c|--config=')
    print('     配置文件路径，')


def check_arg():
    global CONFIG_FILE
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:", ["help", "config="]);

        # check all param
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage();
                sys.exit(1);
            elif opt in ("-c", "--config"):
                CONFIG_FILE = arg
            else:
                logging.info("%s ==> %s" % (opt, arg));

    except getopt.GetoptError:
        print("getopt error!");
        usage();
        return False

    if not CONFIG_FILE:
        usage();
        print('-_-' * 20)
        print('错误：-c|--config, 请指定配置文件路径！！')
        return False

    if not os.path.exists(CONFIG_FILE):
        print('文件:{0}不存在！！'.format(CONFIG_FILE))
        return False

    return True


if __name__ == '__main__':
    log.initial()
    if not check_arg():
        sys.exit(-1)

    logging.debug('check done.')

    if not config.read_config(CONFIG_FILE):
        sys.exit(-2)

    logging.debug('-' * 150)
    rtc_data = []

    # 汇总数据
    big_data = {}
    for cfg in config.RTCS:
        htmlloader = spider.HtmlLoader()
        htmlloader.load(cfg['url'])
        htmlloader.parser()

        data = {}
        for m in config.MEMBERS:
            obj = {}
            obj['fix'] = 0
            obj['out'] = 0
            data[m] = obj
            big_data[m] = copy.copy(obj)

        logging.info('url:{0}'.format(cfg['url']))
        for id in cfg['fix']:
            logging.info('fix id:{0}'.format(id))

            for fix in htmlloader.xx_fix(id):
                logging.info(fix)
                obj = data[fix['name']]
                obj['fix'] += fix['fix']
            logging.info('=' * 150)

        for id in cfg['out']:
            logging.info('out id:{0}'.format(id))
            for out in htmlloader.xx_out(id):
                logging.info(out)
                obj = data[out['name']]
                obj['out'] += out['out']

        o = {}
        o['url'] = cfg['url']
        o['result'] = data
        rtc_data.append(o)

    logging.debug('=' * 150)

    for rtc in rtc_data:
        logging.info(rtc['url'])
        for k, v in rtc.get('result').items():
            logging.info('  ' + k + ' : ' + str(v))

    # 计算
    logging.info('')
    for rtc in rtc_data:
        for k, v in rtc.get('result').items():
            big_data[k]['fix'] += v['fix']
            big_data[k]['out'] += v['out']
            big_data[k]['total'] = big_data[k]['fix'] + big_data[k]['out']

    for k, v in big_data.items():
        logging.info('  ' + k + ' : ' + str(v))
    logging.info('-' * 150)
