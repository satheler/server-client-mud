class Player(object):
    id = 0
    user = ""
    password = ""
    gold = 0
    room = ""

    def __init__(self, id, user, password, nick, gold, room):
        self.id = id
        self.user = user
        self.password = password
        self.gold = gold
        self.room = room