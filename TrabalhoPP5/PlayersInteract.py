class PlayersInteract(object):
    def startInteract(self,player,players):
        response = "-----Players List-----\n"
        if len(players) > 1:
            cont = 0
            for otherPlayer in players:                
                if otherPlayer != player:
                    response += str(cont) + " - " + otherPlayer.name + "\n"
                cont+= 1
        else:
            response += "There are no players in this map!\n"
            response += "----------------------\n"
            return response
        response+= "----------------------\n"
        response+= "Which player do you want to interact?\n"
        player.connection.send(response.encode())
        playerIndex = player.connection.recv(1024).decode()

        try:
            playerIndex = int(playerIndex)
        except RuntimeError:
            return "Invalid option!"

        if playerIndex < len(players) and playerIndex >= 0:
            otherPlayer = players[playerIndex]
            if otherPlayer == player:
                return "Stop with this autism you can't interact with yourself!"
            elif otherPlayer.status == 'inBattle':
                return "This player is in a Battle, you can't interact with him now!"
            elif otherPlayer.status == 'inCity' or otherPlayer.status == "inDungeon":
                response = "what type of iteraction you want to do?\nduel\ntrade\n"
                player.connection.send(response.encode())
                option = player.connection.recv(1024).decode()

                if option == 'duel':
                    self.startDuel(player,otherPlayer)
                elif option == 'trade':
                    self.startTrade(player.otherPlayer)
                return "Invalid option!\n"


    def startDuel(self,player,otherPlayer):
        message = "The player "+player.name+" start a duel with you!\n"
        otherPlayer.connection.send(message.encode())
        
        while(player.hp > 0 or otherPlayer.hp > 0):
            message = "Your Turn:"
            otherPlayer.connection.send(message.encode())            
            otherPlayer.connection.recv(1024).decode()
            player.hp -= otherPlayer.damage - player.armor
            
            message = "Your Turn:"
            player.connection.send(message.encode())            
            player.connection.recv(1024).decode()
            otherPlayer.hp -= player.damage - otherPlayer.armor 