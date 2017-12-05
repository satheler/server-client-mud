from json import *

class LeitorJSON(object):
    arquivo = None
    
    def __init__(self, arquivo):
        self.arquivo = arquivo

    def carregarJson(self):
        return load(open(self.arquivo))