from subprocess import Popen, PIPE

opc = ""

while opc != "0":
    print("******************************")
    print("***** ADMINISTRATIVO MUD *****")
    print("*****--------------------*****")
    print("*** 1 - Iniciar servidor   ***")
    print("*** 0 - Sair do servidor   ***")
    print("******************************")

    opc = input("Digite o numero da opcao: ")
    
    if(opc == "1"):
        print("entrou")
        process = Popen(['python', './Run.py'], stdout=PIPE)
        stdout, stderr = process.communicate()