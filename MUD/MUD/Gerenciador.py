from Historia import *
from json import *
from Cliente import *
class Gerenciador(object):#motor do jogo
    pass
    def __init__(self, arquivo):
        self.arquivo = arquivo
    def carregaJson():
        test = open("teste.json")
        nome = load(test)
        historia = Historia(nome)        
        print (historia.text)

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