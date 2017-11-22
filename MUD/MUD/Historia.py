from Opcao import *
from Segmento import *
from json import *
class Historia(object):
    pass
    text = None
    opcao = None
    
    def __init__(self, text): #construtor
        self.text = text;
        self.opcao = Opcao(text)