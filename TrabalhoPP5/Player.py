from Inventory import Inventory

class Player(object):
    def __init__(self):
        self.level = 1
        self.name = None
        self.maxHp = 2000
        self.hp = self.maxHp
        self.damage = 1000
        self.armor = 20
        self.room = None
        self.status = None        
        self.xp = 0
        self.nextLevel = 100
        self.gold = 1000
        self.battleEnemy = None
        self.lastCity = None
        self.inventory = Inventory()

    def setMap(self,room):
        self.room = room

    def gainXp(self,xp):
        self.xp += xp

        response = ""

        if(self.xp >= self.nextLevel):
            self.level += 1
            self.maxHp *= 2
            self.nextLevel *= 2
            self.damage += 10
            response = "\nYou gain a level you are now level "+ str(self.level)+"!"

        return response

    def moveEast(self):
        message = ""
        if(self.room.east != None):
            message = self.swapRoom(self.room.east)
        return message

    def moveWest(self):
        message = ""
        if(self.room.west != None):
            message = self.swapRoom(self.room.west)
        return message

    def moveNorth(self):
        message = ""
        if(self.room.north != None):
            message = self.swapRoom(self.room.north)
        return message

    def moveSouth(self):
        message = ""
        if(self.room.south != None):
            message = self.swapRoom(self.room.south)
        return message

    def swapRoom(self,room):
        self.room.players.remove(self)
        newRoom = room
        newRoom.players.append(self)
        self.room = newRoom        
        message = "You moved to "+self.room.name
        self.verifyRoomStatus()
        return message

    def verifyRoomStatus(self):

        if self.room.type == 'City':
            self.status = 'inCity'
            self.lastCity = self.room
        elif self.room.type == 'Dungeon':
            self.status = 'inDungeon'
        elif self.room.type == 'Rune':
            self.status = 'inDungeon'
            
    def equipItem(self, number,connection):

        response = ""

        number = int(number)

        if len(self.inventory.itemInventory) > number and number >= 0:
            item = self.inventory.itemInventory[number]

            if item.equippable:
                if item.type == 'weapon':
                    if self.inventory.weapon == None:
                        self.inventory.weapon = item
                        self.inventory.itemInventory.remove(item)
                        self.damage += item.damage
                        response += "The " + item.name + " was equipped!\n"
                    else:
                        self.damage -= self.inventory.weapon.damage
                        response += "The " + self.inventory.weapon.name + " was sent to inventory!\n"
                        self.inventory.itemInventory.append(self.inventory.weapon)
                        self.inventory.weapon = item
                        self.inventory.itemInventory.remove(item)
                        self.damage += item.damage
                        response += "The " + item.name + " was equipped!\n"
                if item.type == 'armor':

                    response += "Choose a slot to equipe:\n"
                    connection.send(response.encode())
                    slotNumber = connection.recv(1024).decode()

                    slotNumber = int(slotNumber)-1

                    if(slotNumber < 0 or slotNumber > 3):
                        return "\nInvalid Slot Number"

                    if self.inventory.equip[slotNumber] == None:
                        self.inventory.equip[slotNumber] = item
                        self.inventory.itemInventory.remove(item)
                        self.armor += item.armor
                        response += "The " + item.name + " was equipped!\n"
                    else:
                        self.armor -= self.inventory.equip[slotNumber].armor
                        response += "The " + self.inventory.equip[slotNumber].name + " was sent to inventory!\n"
                        self.inventory.itemInventory.append(self.inventory.equip[slotNumber])
                        self.inventory.equip[slotNumber] = item
                        self.inventory.itemInventory.remove(item)
                        self.armor += item.armor
                        response += "The " + item.name + " was equipped!\n"              
            else:
                response += "The " + item.name + " is not equippable!\n"
        else:
             response += "Invalid equippament number!"
        return response