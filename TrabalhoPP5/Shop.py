class Shop(object):
    def __init__(self):
        self.itens = []

    def enterShop(self,player,connection):
        response = "\n--------RF Badiao Shop--------"
        response += "\n\tbuy\n\tsell\n\texit\n"
        response += "------------------------------\n"
        connection.send(response.encode())
        
        option = connection.recv(1024).decode()

        response = "Invalid option!\n"

        if option == 'buy':
            response = self.showItens(player,connection)
        elif option == 'sell':
            response = self.sellItens(player,connection)
        elif option == 'exit':
            response = "You leave the shop!\n"
        return response

    def showItens(self,player,connection):

        response = "\n--------Shop Buy--------\n"
        response += "Your Gold : " + str(player.gold) + "\n" 
        cont = 0
        if len(self.itens) > 0:
            for item in self.itens:
                response += str(cont) + " - " + item.name + " ---\t " + str(item.price) + " gold\n"
                cont+= 1
        else:
            response += "The Shop have no itens for sale!\n"
            response += "------------------------\n"
            return response

        response += "------------------------\n"

        

        response += "What item you wanna buy?\n"
        connection.send(response.encode())
        
        itemNumber = connection.recv(1024).decode()

        if(itemNumber == "none"):
            response = "Exit from shop!\n"
        else:
            itemNumber = int(itemNumber)

            if itemNumber < len(self.itens) and itemNumber >= 0:
                if player.gold >= self.itens[itemNumber].price:
                    player.gold -= self.itens[itemNumber].price
                    player.inventory.itemInventory.append(self.itens[itemNumber])
                    response = "You bought " + self.itens[itemNumber].name + "!\n"
                    self.itens.remove(self.itens[itemNumber])
                else:
                    response = "You dont have gold to buy this item!\n"
            else:
                response = "Invalid item number!\n"
        return response
                    



    def sellItens(self,player,connection):
        response = "\n--------Shop Sell--------\n"
        response += "Your Gold : " + str(player.gold) + "\n" 

        cont = 0
        if len(player.inventory.itemInventory) > 0:
            for item in player.inventory.itemInventory:
                response += str(cont) + " - " + item.name + " ---\t " + str(item.price / 2) + " gold\n"
                cont+= 1
        else:
            response += "You have no itens for sale!\n"
            response += "------------------------\n"
            return response
        response += "------------------------\n"
                
        response += "What item you wanna sell?\n"
        connection.send(response.encode())
        
        itemNumber = connection.recv(1024).decode()

        if(itemNumber == "none"):
            response = "Exit from shop!\n"
        else:
            itemNumber = int(itemNumber)
            if itemNumber < len(player.inventory.itemInventory) and itemNumber >= 0:               
                player.gold += player.inventory.itemInventory[itemNumber].price / 2
                self.itens.append(player.inventory.itemInventory[itemNumber])                
                response = "You sold " + player.inventory.itemInventory[itemNumber].name + "!\n"
                player.inventory.itemInventory.remove(self.itens[itemNumber]) 
            else:
                response = "Invalid item number!\n"
        return response
