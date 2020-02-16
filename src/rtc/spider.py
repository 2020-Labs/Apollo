import config
import random

class HtmlLoader:
    def load(self,htmlfile):
        self.content = ''


    def parser(self):
        pass

    def xx_fix(self, id):
        for n in config.MEMBERS:
            data = {
                    'name': n,
                    'fix': random.randint(30,80)
                }
            yield data

    def xx_out(self, id):
        for n in config.MEMBERS:
            data = {
                    'name': n,
                    'out': random.randint(3,30)
                }
            yield data