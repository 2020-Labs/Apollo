import copy
import getopt
import json
import logging
import os
import sys

import db
import log
import config
import report
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

    db.initial()
    report.initial()

    logging.debug('-' * 150)

    for cfg in config.RTCS:
        htmlloader = spider.HtmlLoader()
        htmlloader.load(cfg['url'])
        htmlloader.parser()

        logging.info('url:{0}'.format(cfg['url']))

        #fix
        for id in cfg['fix']:
            logging.info('fix id:{0}'.format(id))
            for fix in htmlloader.extract_fix(id):
                logging.info(fix)
                db.put_fix(cfg['url'], fix)

            logging.info('=' * 150)

        #out
        for id in cfg['out']:
            logging.info('out id:{0}'.format(id))
            for out in htmlloader.extract_out(id):
                logging.info(out)
                db.put_out(cfg['url'], out)

    db.print_out()

    db.calc_new()

    db.calc_last()

    report.report_render()



