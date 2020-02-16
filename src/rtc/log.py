import logging
import os


def initial():
    log = logging.getLogger(__name__)
    logging.basicConfig(
        format='%(asctime)s  %(filename)s %(funcName)s: : %(levelname)s  %(message)s',
        filename=os.path.join(os.getcwd(), 'log.txt'), level=logging.DEBUG)

    console = logging.StreamHandler()  # 定义console handler
    console.setLevel(logging.DEBUG)  # 定义该handler级别
    formatter = logging.Formatter('%(asctime)s  %(filename)s %(funcName)s: %(levelname)s  %(message)s')  # 定义该handler格式
    console.setFormatter(formatter)
    # Create an instance

    logging.getLogger().addHandler(console)  # 实例化添加handler

    logging.debug('this is a message')


#if __name__ == '__main__':
#    initial()
