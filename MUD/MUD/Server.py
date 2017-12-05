# -*- encoding: utf-8 -*-

import time
from ServerConfig import ServerConfig as serverconfig
from Player import Player

class Server(object):
    roomStart = None
    rooms = {}
    server = None
    players = {}
    timeStart = 0

    registers = []

    def __init__(self, rooms, timeStart):
        self.server = serverconfig()
        self.roomStart = "Unipampa"
        self.rooms = rooms
        self.players = {}
        self.timeStart = timeStart
        self.registers = []

    def start(self):
        # Loop principal.
        while True:
            # Pause de 200ms em cada loop, para evitar sobrecarga de CPU
            time.sleep(0.2)

            # Este método serve para manter o jogo em execucao
            # Alem de manter o jogo atualizado
            self.server.update()

            self.new_players()

            self.disconnected_players()

            self.commands()

    # Captura qualquer novo jogador tentanto conectar
    def new_players(self):

        # Envie ao novo jogador um pedido para o seu nome.
        #self.server.send_message(-1, "Voce deseja logar ou registrar?")

        for id in self.server.get_new_players():

            # player(id, user, password, nick, gold, room)
            self.players[id] = {
                "name": None,
                "room": None,
            }

            # Envia ao novo jogador um pedido para o seu nome.
            self.server.send_message(id, "Insira seu nick.")
    
    # Passa por qualquer jogador desconectado recentemente
    def disconnected_players(self):
        for id in self.server.get_disconnected_players():

            # if for any reason the player isn't in the player map, skip them and
            # move on to the next one
            if id not in self.players:
                continue

            # go through all the players in the game
            for pid, pl in self.players.items():
                # send each player a message to tell them about the diconnected
                # player
                self.server.send_message(pid, "{} saiu do jogo".format(self.players[id]["name"]))

            # remove the player's entry in the player dictionary
            del(self.players[id])

    # Passa por qualquer novo comando enviado pelos jogadores
    def commands(self):
        for id, command, params in self.server.get_commands():

            # if for any reason the player isn't in the player map, skip them and
            # move on to the next one
            if id not in self.players:
                continue

            # if the player hasn't given their name yet, use this first command as
            # their name and move them to the starting room.
            if self.players[id]["name"] is None:

                self.players[id]["name"] = command
                self.players[id]["room"] = self.roomStart

                # go through all the players in the game
                for pid, pl in self.players.items():
                    # send each player a message to tell them about the new player
                    self.server.send_message(pid, "{} entrou no jogo".format(self.players[id]["name"]))

                # send the new player a welcome message
                self.server.send_message(id, "Bem-vindo ao jogo, {}. ".format(self.players[id]["name"]) + "Digite 'ajuda' para lista de comandos. Divirta-se!")

                # send the new player the description of their current room
                self.server.send_message(id, self.rooms[self.players[id]["room"]]["description"])

                self.registers.append(self.players[id])

            # each of the possible commands is handled below. Try adding new
            # commands to the game!

            # 'help' command
            elif command == "ajuda":

                # send the player back the list of possible commands
                self.server.send_message(id, "Comandos:")
                self.server.send_message(id, "  falar <mensagem>   - Diz algo em voz alta. Por exemplo 'Hi Hi Guys'")
                self.server.send_message(id, "  observar           - Olha aos arredores.")
                self.server.send_message(id, "  caminhar <lugar>      - Anda para o caminho especificado, e.g. 'caminhar unipampa'")

            # 'say' command
            elif command == "falar":

                # go through every player in the game
                for pid, pl in self.players.items():
                    # if they're in the same room as the player
                    if self.players[pid]["room"] == self.players[id]["room"]:
                        # send them a message telling them what the player said
                        self.server.send_message(pid, "{} says: {}".format(self.players[id]["name"], params))

            # 'look' command
            elif command == "observar":

                # store the player's current room
                rm = self.rooms[self.players[id]["room"]]

                # send the player back the description of their current room
                self.server.send_message(id, rm["description"])

                playershere = []
                # go through every player in the game
                for pid, pl in self.players.items():
                    # if they're in the same room as the player
                    if self.players[pid]["room"] == self.players[id]["room"]:
                        # ... and they have a name to be shown
                        if self.players[pid]["name"] is not None:
                            # add their name to the list
                            playershere.append(self.players[pid]["name"])

                # send player a message containing the list of players in the room
                self.server.send_message(id, "Jogadores nesta area: {}".format(", ".join(playershere)))

                # send player a message containing the list of exits from this room
                self.server.send_message(id, "As saidas sao: {}".format(", ".join(rm["exits"])))


            elif command == "caminhar":

                # store the exit name
                ex = params.lower()

                # store the player's current room
                rm = self.rooms[self.players[id]["room"]]

                # if the specified exit is found in the room's exits list
                if ex in rm["exits"]:

                    # go through all the players in the game
                    for pid, pl in self.players.items():
                        # if player is in the same room and isn't the player
                        # sending the command
                        if self.players[pid]["room"] == self.players[id]["room"] and pid != id:
                            # send them a message telling them that the player
                            # left the room
                            self.server.send_message(pid, "{} foi para '{}'".format(self.players[id]["name"], ex))

                    # update the player's current room to the one the exit leads to
                    self.players[id]["room"] = rm["exits"][ex]
                    rm = self.rooms[self.players[id]["room"]]

                    # go through all the players in the game
                    for pid, pl in self.players.items():
                        # if player is in the same (new) room and isn't the player
                        # sending the command
                        if self.players[pid]["room"] == self.players[id]["room"] \
                                and pid != id:
                            # send them a message telling them that the player
                            # entered the room
                            self.server.send_message(pid, "{} chegou por '{}'".format(self.players[id]["name"], ex))

                    # send the player a message telling them where they are now
                    self.server.send_message(id, "Voce chegou em '{}'".format(self.players[id]["room"]))

                # the specified exit wasn't found in the current room
                else:
                    # send back an 'unknown exit' message
                    self.server.send_message(id, "caminho desconhecido '{}'".format(ex))

            elif command == "desligar":
                self.server.shutdown()

            elif command == "desconectados":
                self.server.send_message(id, "Jogadores desconectados: {}".format(", ".join(server.get_disconnected_players())))

            elif command == "sair":
                self.server.send_message(id, "fazendo")
                
            else:
                # send back an 'unknown command' message
                self.server.send_message(id, "ETA !@$%! QUE COMANDU E ECI '{}'".format(command))

        # Salva os usuarios conectados 
   
   # Salva todos os usuarios conectados
    def save_users():
        try:
            arquivo = open("Dados.bin", "wb")
        except IOError:
            print("Erro ao abrir o arquivo")
    
        arquivo.write(self.register)
        arquivo.close()

    # Carrega os usuarios anteriormente conectados
    def load_users():
        try:
            arquivo = open("Dados.bin","rb")
        except IOError:
            print("Erro ao abrir o arquivo")

        arquivo.seek(0,2)
        tamanho = arquivo.tell()
        arquivo.seek(0)
        buffer = arquivo.read(tamanho)
        print(buffer)
        arquivo.close()