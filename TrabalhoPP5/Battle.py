import random
class Battle(object):
    def __init__(self,player,itens):
        self.player = player
        self.enemy = player.battleEnemy
        self.itens = itens

    def attack(self):

        damage = self.player.damage - self.enemy.armor

        if damage < 0:
            damage = 0
        
        self.enemy.hp -= damage

        response = "You inflicted " + str(damage) + " damage!\n" 

        if self.enemy.hp <= 0:
            response += "The " + self.enemy.name + " died!\n"
            response += "You received " + str(self.enemy.xp) + " xp!"
            response += self.player.gainXp(self.enemy.xp)

            dropIndex = self.enemy.drop[random.randrange(0,len(self.enemy.drop))]

            drop = self.itens[dropIndex]

            response += "\nEnemy droped " + drop.name + "!"

            self.player.inventory.itemInventory.append(drop)

            self.player.battleEnemy = None
            self.player.verifyRoomStatus()
        else:
            response += self.enemyAttack()

        return response

    def enemyAttack(self):
        damage = self.enemy.damage - self.player.armor

        if damage < 0:
            damage = 0
        
        self.player.hp -= damage

        message = "You received " + str(damage) + " damage!" 

        if(self.player.hp <= 0):
            message += "\n You died!\nReturning to " + self.player.lastCity.name + "!"
            self.player.room.players.remove(self.player)
            self.player.room = self.player.lastCity
            self.player.room.players.append(self.player)
            self.player.verifyRoomStatus()
            self.player.hp = self.player.maxHp

        return message

    def run(self):
        response = "You run from the battle!"
        self.player.verifyRoomStatus()
        self.player.battleEnemy = None
        return response