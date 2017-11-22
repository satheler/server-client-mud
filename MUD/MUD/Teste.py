from json import *
class Pessoa(object):
        def __init__(self):
            self.codigo = 0
            self.nome = ''
            self.endereco = Endereco()

class Endereco(object):
    def __init__(self):
        self.codigo = 0
        self.logradouro = ''
        self.bairro = ''
        self.cidade = Cidade()

class Cidade(object):
    def __init__(self):
        self.codigo = 0
        self.nome = ''
        self.uf = ''
import json

class Teste(object):

    def para_dict(obj):
        # Se for um objeto, transforma num dict
        if hasattr(obj, '__dict__'):
            obj = obj.__dict__

        # Se for um dict, lê chaves e valores; converte valores
        if isinstance(obj, dict):
            return { k:para_dict(v) for k,v in obj.items() }
        # Se for uma lista ou tupla, lê elementos; também converte
        elif isinstance(obj, list) or isinstance(obj, tuple):
            return [para_dict(e) for e in obj]
        # Se for qualquer outra coisa, usa sem conversão
        else: 
            return obj
def main():
    p = Pessoa()
    s = json.dumps(p)
    print (s)
main()
