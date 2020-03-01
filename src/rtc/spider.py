import random


class RtcSpider:

    __members = []
    def __init__(self, filename, members):
        self.__file = filename
        self.__members = members

    def load(self):
        #从htmlfile文件中加载html内容
        self.__html_content = ''

    def extract_fix(self, id):
        for n in self.__members:
            yield {
                    'name': n,
                    'fix': random.randint(30, 80)
                }

    def extract_out(self, id):
        for n in self.__members:
            yield {
                    'name': n,
                    'out': random.randint(3, 30)
                }
