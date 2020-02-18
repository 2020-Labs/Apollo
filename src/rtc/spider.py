import config
import random

class HtmlLoader:
    def load(self,htmlfile):
        self.html_content = ''



    def parser(self):
        pass

    def extract_fix(self, id):
        data_list = []
        for n in config.MEMBERS:
            data = {
                    'name': n,
                    'fix': random.randint(30,80)
                }
            data_list.append(data)
        return data_list

    def extract_out(self, id):
        for n in config.MEMBERS:
            data = {
                    'name': n,
                    'out': random.randint(3,30)
                }
            yield data