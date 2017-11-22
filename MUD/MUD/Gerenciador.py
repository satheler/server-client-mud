from Historia import *
from json import *
from Cliente import *
from Mapa import *
class Gerenciador(object):#motor do jogo
    pass
    def __init__(self, arquivo):
        self.arquivo = arquivo
    def carregaJson():
        arquivo = open("teste.json")
        texto = load(arquivo)
        historia = Historia(texto)        
        print (historia.text)

        mapa = open("testeMapa.json")
        mapatest = load(mapa)
        map = Mapa(mapatest)
        print (map.direcao)
        print (map.salas)

    def defineInfoJogador():
        nomeJogador = input("Digite seu nome: ")
        idadeJogador = int(input("Digite sua idade: "))
        cliente = Cliente(nomeJogador, idadeJogador)
        print ("Seus dados são:\nNome: ", cliente.nome,"\nIdade: ", cliente.idade)

    def acao():
        escolha = input("Por qual caminho você deseja seguir? ")
        dumps(escolha)

    def mostra():
        print (Historia.text)
def main():
    Gerenciador.defineInfoJogador()
    Gerenciador.carregaJson()
    Gerenciador.acao()
    Gerenciador.mostra()
 
main()