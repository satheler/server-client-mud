from Segmento import *
from json import *
class Opcao(object):
     pass
     text = [None]
     segmento = None
     def __init__(self, text): #construtor
         self.text = text
         self.segmento = Segmento(text)
         

