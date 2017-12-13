import socket
import random
import _thread
from FileReaderJSON import FileReaderJSON
from MapCreator import MapCreator
from Player import Player
from PlayersInteract import PlayersInteract
from Shop import Shop
from Battle import Battle


class Server(object):
    
    def create(self):
        self.host = "127.0.0.1"
        self.port = 5000        
        self.players = []
        self.socket = socket.socket()
        self.socket.bind((self.host,self.port))
        self.socket.listen(10)           
        self.map = None
        self.playersInteract = PlayersInteract()
        self.shop = Shop()
        self.enemies = []
        self.itens = []
        self.cityCommandsString = ""
        self.battleCommandsString = ""
        self.commonCommandsString = ""
        self.dungeonCommandsString = ""
     
    def start(self):
       filereader = FileReaderJSON

       self.createCommandsList()

       print("Start server on:")
       print("Ip: " + self.host + "")
       print("Port: " + str(self.port) + "\n")
       self.map = MapCreator.createMap(MapCreator)
       print("Map is Ready")
       self.enemies = filereader.loadEnemies(filereader)
       print("Enemies loaded")
       self.itens = filereader.loadItens(filereader)
       print("Itens loaded")
       self.listenConnections()     
   
    def createCommandsList(self):

        self.battleCommandsString = "attack - Attack enemy with your might\ndefend - multiply your armor x 2\nrun - enemy is too strong for you\nuse potion - use potions to recover hp"
        self.commonCommandsString = "move - see directions to move\nobserve - look around\nshow equip - show your equipament\ninventory - show your inventory\nequip - equip item from your inventory"
        self.dungeonCommandsString = "search battle - search enemies to battle\n"+self.commonCommandsString
        self.cityCommandsString = "shop - sell and buy itens\n"+self.commonCommandsString


    def update(self):

        while True:
            self.listenConnections()
            self.listenEvents()
    
    def clientThread(self,connection):
        connection.send("Welcome do PP World!".encode())
        connection.send("What is your name:".encode())
        name = connection.recv(1024).decode()

        player = Player()
        player.name = name
        player.status = "inCity"
        player.room = self.map[0]
        player.lastCity = self.map[0]
        player.room.players.append(player)
        player.connection = connection
        self.players.append(player)


        message = name + " you are in " + player.room.name + ", your goal here is to collect the four elemental runes to return peace to this kingdom."

        connection.send(message.encode())

        while True:
            command = connection.recv(1024).decode()
            
            response = self.processCommand(player,command,connection) 
            
            connection.send(response.encode())

    def processCommand(self,player,command,connection):

        if player.status == 'inCity':
            response = self.cityCommands(player,command,connection)
        elif  player.status == 'inDungeon':
            response = self.dungeonCommands(player,command,connection)
        elif  player.status == 'inBattle':
            response = self.battleCommands(player,command,connection)
    
        return response
    
    def cityCommands(self,player,command,connection):       
        
        if command == 'shop':
            response = self.shop.enterShop(player,connection)
        elif command == 'commands':
            response = self.cityCommandsString
        elif command != '': 
            response = self.commonCommands(player,command,connection)        
        return response

    def showDirections(self,player,connection):

        directions = "\tWhere you want to go:\n"

        room = player.room

        if room.east != None:
            directions += "\teast - " + room.east.name + "\n"
        if room.west != None:
            directions += "\twest - " + room.west.name + "\n"
        if room.north != None:
            directions += "\tnorth - " + room.north.name + "\n"
        if room.south != None:
            directions += "\tsouth - " + room.south.name
        
        connection.send(directions.encode())

        direction = connection.recv(1024).decode()

        response = self.moveTo(direction,player)

        if response == "":
            response = "There's nothing in this directions!"

        return response

    def  moveTo(self,direction,player):

        response = "Invalid direction!"

        if direction == "east":
            response = player.moveEast()
        elif direction == "west":
            response = player.moveWest()
        elif direction == 'north':
            response = player.moveNorth()
        elif direction == 'south':
            response = player.moveSouth()
        return response 

    def commonCommands(self,player,command,connection):
        response = "invalid command, type commands to see all commands"
        if command == 'move':
            response = self.showDirections(player,connection)
        elif command == 'show equip':
            response = player.inventory.showEquipament()
        elif command == 'inventory':
            response = player.inventory.showInventory()
        elif command == 'equip':
            response = self.equipItem(player,connection)
        elif command == 'observe':
            response = player.room.description
        elif command == 'players':
            response = self.playersInteract.startInteract(player,self.players)
        return response

    def dungeonCommands(self,player,command,connection): 
        if command == 'search battle':
            response = self.searchBattle(player,command,connection)
        elif command == 'commands':
            response = self.dungeonCommandsString
        elif command != '': 
            response = self.commonCommands(player,command,connection)        
        return response

    def equipItem(self,player,connection):

        if len(player.inventory.itemInventory) == 0:
            response = "Your inventory is empty!\n"
        else:
            response = player.inventory.showInventory()
            response += "Choose a item to equipe:\n"
            connection.send(response.encode())
            itemNumber = connection.recv(1024).decode()
            response = player.equipItem(itemNumber,connection)
        return response

    def battleCommands(self,player,command,connection):

        battle = Battle(player,self.itens)
        response = "Invalid battle commands"

        if command == 'attack':
            response = battle.attack()
        elif command == 'defend':
            response = "The best defense is the attack."
        elif command == 'run':
            response = battle.run()
        elif command == 'commands':
            response = self.battleCommandsString
        return response

    def searchBattle(self,player,command,connection):

        roomEnemies = player.room.enemies
        enemyIndex = roomEnemies[random.randrange(0,len(roomEnemies))]
        enemy = self.enemies[enemyIndex]

        response = "You started a battle with a "+enemy.name
        player.status = 'inBattle'
        player.battleEnemy = enemy

        return response

    def listenConnections(self):

        while True:
            connection, address = self.socket.accept()
            print("Connection from: " + str(address))
            _thread.start_new_thread(self.clientThread,(connection,))



server = Server()
server.create()
server.start()