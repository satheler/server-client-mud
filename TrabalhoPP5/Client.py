import socket


class Client:
    def connect(self):
        self.host = "127.0.0.1"
        self.port = 5000
     
        self.socket = socket.socket()
        self.socket.connect((self.host,self.port))           
       
        response = self.socket.recv(1024).decode()
        print (response)       

        command = None

        while command != 'quit':
            if(command != None):
                self.socket.send(command.encode())
            response = self.socket.recv(1024).decode()
            print (response)
            command = input(" -> ")


c = Client()
c.connect()
