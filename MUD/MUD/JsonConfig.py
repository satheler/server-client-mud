from datetime import datetime
import json  #Outra opção é usar o import cPickle as pickle, que possui os mesmos métodos para JSON listados abaixo
#dump() serializa arquivos abertos, dumps({dados}, sort_keys = true, indent = value, separatos = ',', ':') serializa caracteres, load(open()) deserializa objetos do tipo file, loads() deserializa caeacteres
class CustomEncoder(json.JSONEncoder): #Precisa ser implementado para grafos complexos(quando temos mais de uma classe), separa em chaves cada tipo de dado que queremos serializar, exemplo do site:

    def default(self, o): #Método padrão a ser implementado

         if isinstance(o, Historia): #retorna se a data for uma instância de historia / comparações para separar o retorno de cada classe
 
             return {'__Historia__': o.__dict__} 
 
         return {'__{}__'.format(o.__class__.__name__): o.__dict__} #retorna os dados de outra classe