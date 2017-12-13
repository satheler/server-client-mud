from FileReaderJSON import FileReaderJSON
from Room import Room
import random

class MapCreator(object):
    def createMap(self):

        filereader = FileReaderJSON
        
        centerRoom = None
        rooms = filereader.loadRooms(filereader)
       
        #Procura a primeira cidade que encontra e faz ela ser o centro do mapa
        for room in rooms:
            if room.type == 'City':
                centerRoom = room
                rooms.remove(room)
                break
   
        #contador para preencher as direções
        cont = 0        

        directions = ["East","West","North","South"]

        map = []
        map.append(centerRoom)

        while len(rooms) > 0:
            direction = directions[random.randrange(0, len(directions))]
            originRoom = map[random.randrange(0, len(map))]
            otherRoom = rooms[random.randrange(0, len(rooms))]

            if self.setRoom(self,originRoom,otherRoom,direction):
                map.append(otherRoom)
                rooms.remove(otherRoom)
                
        return map
        
    def setRoom(self,originRoom,otherRoom,direction):
        
        seted = False

        if direction == "East":
            if originRoom.setEast(otherRoom):
                otherRoom.west = originRoom
                seted = True

        elif direction == "West":
            if originRoom.setWest(otherRoom):
                otherRoom.east = originRoom
                seted = True

        elif direction == "South":
            if originRoom.setSouth(otherRoom):
                otherRoom.north = originRoom
                seted = True

        elif direction == "North":
            if originRoom.setNorth(otherRoom):
                otherRoom.south = originRoom
                seted = True

        return seted
               

     

