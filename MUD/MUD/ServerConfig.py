import socket
import select
import time
import sys
from Client import Client as client # Utilizado somente na linha 189

class ServerConfig(object):

    # Configuraão SOCKET
    # Normalmente o server é o IP
    # Porta de conexão. Padrão 23.
    _server = "0.0.0.0"     
    _port = 8080

    # Usado para armazenar diferentes tipos de ocorrências
    _EVENT_NEW_PLAYER = 1
    _EVENT_PLAYER_LEFT = 2
    _EVENT_COMMAND = 3

    # Estados diferentes em que podemos estar enquanto lemos dados do cliente
    # Veja a funcao _process_sent_data
    _READ_STATE_NORMAL = 1
    _READ_STATE_COMMAND = 2
    _READ_STATE_SUBNEG = 3

    # Códigos de comando usados pelo protocolo Telnet
    # Veja funcao _process_sent_data
    _TN_INTERPRET_AS_COMMAND = 255
    _TN_ARE_YOU_THERE = 246
    _TN_WILL = 251
    _TN_WONT = 252
    _TN_DO = 253
    _TN_DONT = 254
    _TN_SUBNEGOTIATION_START = 250
    _TN_SUBNEGOTIATION_END = 240

    # socket usado para atender novos clientes
    _listen_socket = None

    # Contém informações sobre os clientes
    _clients = {}

    # Contador para atribuir a cada cliente um novo ID
    _nextid = 0

    # Lista de ocorrências em espera para ser tratado pelo algoritmo
    _events = []

    # Lista de ocorrências recém-adicionadas
    _new_events = []

    def __init__(self):
        self._clients = {}
        self._nextid = 0
        self._events = []
        self._new_events = []

        # Cria um novo socket TCP (protocolo de transmissão) que será usado para ouvir novos clientes
        self._listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define uma opção especial no soquete que permite que a porta seja
        # Imediatamente sem ter que esperar
        self._listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Dados para criar a conexao
        self._listen_socket.bind((self._server, self._port))

        # Modo anti-bloquerio.
        # Ou seja, quando chamar o socket, ele retornara
        # imediatamente sem esperar por uma conexao
        self._listen_socket.setblocking(False)

        # Comeca a aceitar conexoes no socket
        self._listen_socket.listen(1)

    def update(self):
        # Verifica se ha coisas novas
        self._check_for_new_connections()
        self._check_for_disconnected()
        self._check_for_messages()

        # Move os novos eventos para a lista de eventos pricipais para que eles 
        # possam ser obtidos com 'get_new_players', 'get_disconnected_players'
        # e 'get_commands'. Os eventos anteriores são descartados
        self._events = list(self._new_events)
        self._new_events = []

    def get_new_players(self):
        retval = []
        # Passa por todos os eventos na lista principal
        for ev in self._events:

            # Se o evento for uma ocorrência de novo jogador
            # Adicione a informação a lista
            if ev[0] == self._EVENT_NEW_PLAYER:
                retval.append(ev[1])

        # Retorna a lista com a informacao
        return retval

    def get_disconnected_players(self):
        retval = []
        # Passa por todos os eventos da lista principal
        for ev in self._events:
            # Se o evento for uma ocorrencia de desconexao do jogador,
            # adicione a informacao a lista
            if ev[0] == self._EVENT_PLAYER_LEFT:
                retval.append(ev[1])
                
        # Retorna a lista com a informacao
        return retval

    def get_commands(self):
        retval = []
        # go through all the events in the main list
        for ev in self._events:
            # if the event is a command occurence, add the info to the list
            if ev[0] == self._EVENT_COMMAND:
                retval.append((ev[1], ev[2], ev[3]))
        # return the info list
        return retval

    def send_message(self, to, message):
        """Sends the text in the 'message' parameter to the player with
        the id number given in the 'to' parameter. The text will be
        printed out in the player's terminal.
        """
        # we make sure to put a newline on the end so the client receives the
        # message on its own line
        self._attempt_send(to, message+"\n\r")

    def shutdown(self):
        """Closes down the server, disconnecting all clients and
        closing the listen socket.
        """
        # Para cada jogador conectado
        for cl in self._clients.values():
            # Fecha o socket, desconectando os jogadores
            cl.socket.shutdown()
            cl.socket.close()
            
        # Para de atender a novas requisicoes
        self._listen_socket.close()

    def _attempt_send(self, clid, data):
        try:
            # Procura o jogador na lista de jogador e use 'sendall' para enviar
            # a string da mensagem no socket. 
            # O comando 'sendall' garante que todos os dados são enviados de uma só vez
            self._clients[clid].socket.sendall(bytearray(data, "latin1"))
        # O KeyError será gerado se não houver jogador com o id especificado no mapa
        except KeyError:
            pass
        # Se houver um problema de conexão com o jogador (por exemplo, eles foram desconectados)
        # um erro de socket será gerado
        except socket.error:
            self._handle_disconnect(clid)

    def _check_for_new_connections(self):

        # 'select' is used to check whether there is data waiting to be read
        # from the socket. We pass in 3 lists of sockets, the first being those
        # to check for readability. It returns 3 lists, the first being
        # the sockets that are readable. The last parameter is how long to wait
        # - we pass in 0 so that it returns immediately without waiting
        rlist, wlist, xlist = select.select([self._listen_socket], [], [], 0)

        # if the socket wasn't in the readable list, there's no data available,
        # meaning no clients waiting to connect, and so we can exit the method
        # here
        if self._listen_socket not in rlist:
            return

        # 'accept' returns a new socket and address info which can be used to
        # communicate with the new client
        joined_socket, addr = self._listen_socket.accept()

        # set non-blocking mode on the new socket. This means that 'send' and
        # 'recv' will return immediately without waiting
        joined_socket.setblocking(False)

        # construct a new _Client object to hold info about the newly connected
        # client. Use 'nextid' as the new client's id number
        self._clients[self._nextid] = client(joined_socket, addr[0],"", time.time())

        # add a new player occurence to the new events list with the player's
        # id number
        self._new_events.append((self._EVENT_NEW_PLAYER, self._nextid))

        # add 1 to 'nextid' so that the next client to connect will get a
        # unique id number
        self._nextid += 1

    def _check_for_disconnected(self):

        # go through all the clients
        for id, cl in list(self._clients.items()):

            # if we last checked the client less than 5 seconds ago, skip this
            # client and move on to the next one
            if time.time() - cl.lastcheck < 5.0:
                continue

            # send the client an invisible character. It doesn't actually
            # matter what we send, we're really just checking that data can
            # still be written to the socket. If it can't, an error will be
            # raised and we'll know that the client has disconnected.
            self._attempt_send(id, "\x00")

            # update the last check time
            cl.lastcheck = time.time()

    def _check_for_messages(self):

        # go through all the clients
        for id, cl in list(self._clients.items()):

            # we use 'select' to test whether there is data waiting to be read
            # from the client socket. The function takes 3 lists of sockets,
            # the first being those to test for readability. It returns 3 list
            # of sockets, the first being those that are actually readable.
            rlist, wlist, xlist = select.select([cl.socket], [], [], 0)

            # if the client socket wasn't in the readable list, there is no
            # new data from the client - we can skip it and move on to the next
            # one
            if cl.socket not in rlist:
                continue

            try:
                # read data from the socket, using a max length of 4096
                data = cl.socket.recv(4096).decode("latin1")

                # process the data, stripping out any special Telnet commands
                message = self._process_sent_data(cl, data)

                # if there was a message in the data
                if message:

                    # remove any spaces, tabs etc from the start and end of
                    # the message
                    message = message.strip()

                    # separate the message into the command (the first word)
                    # and its parameters (the rest of the message)
                    command, params = (message.split(" ", 1) + ["", ""])[:2]

                    # add a command occurence to the new events list with the
                    # player's id number, the command and its parameters
                    self._new_events.append((self._EVENT_COMMAND, id,
                                             command.lower(), params))

            # if there is a problem reading from the socket (e.g. the client
            # has disconnected) a socket error will be raised
            except socket.error:
                self._handle_disconnect(id)

    def _handle_disconnect(self, clid):

        # remove the client from the clients map
        del(self._clients[clid])

        # add a 'player left' occurence to the new events list, with the
        # player's id number
        self._new_events.append((self._EVENT_PLAYER_LEFT, clid))

    def _process_sent_data(self, client, data):

        # the Telnet protocol allows special command codes to be inserted into
        # messages. For our very simple server we don't need to response to
        # any of these codes, but we must at least detect and skip over them
        # so that we don't interpret them as text data.
        # More info on the Telnet protocol can be found here:
        # http://pcmicro.com/netfoss/telnet.html

        # start with no message and in the normal state
        message = None
        state = self._READ_STATE_NORMAL

        # go through the data a character at a time
        for c in data:

            # handle the character differently depending on the state we're in:

            # normal state
            if state == self._READ_STATE_NORMAL:

                # if we received the special 'interpret as command' code,
                # switch to 'command' state so that we handle the next
                # character as a command code and not as regular text data
                if ord(c) == self._TN_INTERPRET_AS_COMMAND:
                    state = self._READ_STATE_COMMAND

                # if we get a newline character, this is the end of the
                # message. Set 'message' to the contents of the buffer and
                # clear the buffer
                elif c == "\n":
                    message = client.buffer
                    client.buffer = ""

                # some telnet clients send the characters as soon as the user
                # types them. So if we get a backspace character, this is where
                # the user has deleted a character and we should delete the
                # last character from the buffer.
                elif c == "\x08":
                    client.buffer = client.buffer[:-1]

                # otherwise it's just a regular character - add it to the
                # buffer where we're building up the received message
                else:
                    client.buffer += c

            # command state
            elif state == self._READ_STATE_COMMAND:

                # the special 'start of subnegotiation' command code indicates
                # that the following characters are a list of options until
                # we're told otherwise. We switch into 'subnegotiation' state
                # to handle this
                if ord(c) == self._TN_SUBNEGOTIATION_START:
                    state = self._READ_STATE_SUBNEG

                # if the command code is one of the 'will', 'wont', 'do' or
                # 'dont' commands, the following character will be an option
                # code so we must remain in the 'command' state
                elif ord(c) in (self._TN_WILL, self._TN_WONT, self._TN_DO,
                                self._TN_DONT):
                    state = self._READ_STATE_COMMAND

                # for all other command codes, there is no accompanying data so
                # we can return to 'normal' state.
                else:
                    state = self._READ_STATE_NORMAL

            # subnegotiation state
            elif state == self._READ_STATE_SUBNEG:

                # if we reach an 'end of subnegotiation' command, this ends the
                # list of options and we can return to 'normal' state.
                # Otherwise we must remain in this state
                if ord(c) == self._TN_SUBNEGOTIATION_END:
                    state = self._READ_STATE_NORMAL

        # return the contents of 'message' which is either a string or None
        return message