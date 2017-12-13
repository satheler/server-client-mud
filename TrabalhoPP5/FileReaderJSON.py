from json import *
from Room import Room
from Enemy import Enemy
from Item import *

class FileReaderJSON(object):    
    
    def __init__(self):
        self.arquivo = None

    def loadJson(self):
        return load(open(self.arquivo))


    def loadRooms(self):
        self.arquivo = "./files/Maps.json"
        roomsJson = self.loadJson(self)

        rooms = []

        for indexRoom in roomsJson:
            room = Room()
            room.name = roomsJson[indexRoom]['name']
            room.description = roomsJson[indexRoom]['description'] 
            room.type = roomsJson[indexRoom]['type']
            room.enemies = roomsJson[indexRoom]['enemies']

            rooms.append(room)

        return rooms

    def loadEnemies(self):
        self.arquivo = "./files/Enemies.json"
        enemiesJson = self.loadJson(self)

        enemies = []

        for indexEnemy in enemiesJson:
            enemy = Enemy()
            enemy.name = enemiesJson[indexEnemy]['name']
            enemy.description = enemiesJson[indexEnemy]['description']             
            enemy.hp = enemiesJson[indexEnemy]['hp']
            enemy.damage = enemiesJson[indexEnemy]['damage']
            enemy.armor = enemiesJson[indexEnemy]['armor']
            enemy.drop = enemiesJson[indexEnemy]['drops']
            #enemy.gold = enemiesJson[indexEnemy]['gold']
            enemy.xp = enemiesJson[indexEnemy]['xp']

            enemies.append(enemy)

        return enemies

    def loadItens(self):        
        self.arquivo = "./files/Itens.json"
        itensJson = self.loadJson(self)

        itens = []

        for indexItem in itensJson:

            item = Item()

            if itensJson[indexItem ]['type'] == 'weapon':
                item = Weapon()
                item.damage = itensJson[indexItem ]['damage']
            elif itensJson[indexItem ]['type'] == 'armor':
                item = Armor()
                item.armor = itensJson[indexItem]['armor']
            elif itensJson[indexItem ]['type'] == 'potion':
                item = Potion()
                item.hpHeal = itensJson[indexItem ]['hpHeal']

            item.name = itensJson[indexItem ]['name']
            item.description = itensJson[indexItem ]['description']             
            item.price = itensJson[indexItem ]['price']
            item.type = itensJson[indexItem ]['type']
            item.equippable = itensJson[indexItem]['equippable']
           
            itens.append(item)

        return itens