import getopt
import os
import sys
import log

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
                print("%s ==> %s" % (opt, arg));

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
    if check_arg():
        print(os.getcwd())
        print('check done.')