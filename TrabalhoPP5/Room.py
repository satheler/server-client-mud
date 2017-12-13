class Room:
    def __init__(self):
        self.name = None
        self.description = None
        self.type = None
        self.enemies = []       
        
        self.east = None
        self.west = None
        self.north = None
        self.south = None
        self.players = []
        self.runes = []
   
    def setEast(self,room):
        if self.east == None:
            self.east = room
            return True
        else:
            return False

    def setWest(self,room):
        if self.west == None:
            self.west = room
            return True
        else:
            return False

    def setNorth(self,room):
        if self.north == None:
            self.north = room
            return True
        else:
            return False

    def setSouth(self,room):
        if self.south == None:
            self.south = room
            return True
        else:
            return False

    def setPlayer(self,player):
        self.players.append(player)

    def setRunes(self,rune):
        self.runes.append(rune)