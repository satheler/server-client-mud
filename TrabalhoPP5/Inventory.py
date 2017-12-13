class Inventory(object):
    def __init__(self):
        self.itemInventory =[]        
        self.runes = []
        self.equip = [None,None,None,None]             
        self.weapon = None

    def showEquipament(self):

        response = "----Equipament----"

        if self.weapon != None:
            response += "\nWeapon - "+ self.weapon.name
        else:
            response += "\nWeapon - "+ "nothing" 
        
        cont = 1
        for equip in self.equip:
            if equip != None:
                response += "\nEquip " + str(cont)+ " - "+ equip.name
            else:
                response += "\nEquip " + str(cont)+ " - nothing"        
            cont+= 1
        response += "\n------------------"
        return response

    def showInventory(self):

        response = "----Item Inventory----\n"

        cont = 0

        if len(self.itemInventory) == 0:
            response += "Empty Inventory\n"
        else:            
            for item in self.itemInventory:
                response += str(cont) +" - "+  item.name+"\n"
                cont += 1
        response += "----------------------\n"
        return response
