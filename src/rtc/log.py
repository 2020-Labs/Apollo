import logging
import os


LOG_FILE = os.path.join(os.getcwd(), 'log.txt')
LOG_FMT = '%(asctime)s  %(filename)s %(funcName)s: : %(levelname)s  %(message)s'


def initial():
    log = logging.getLogger(__name__)
    logging.basicConfig(
        format=LOG_FMT,
        filename=LOG_FILE, level=logging.DEBUG)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter(LOG_FMT)
    console.setFormatter(formatter)
    # Create an instance
    logging.getLogger().addHandler(console)

    #logging.debug('this is a message')


#if __name__ == '__main__':
#    initial()
