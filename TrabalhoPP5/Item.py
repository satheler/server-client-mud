class Item(object):
    def __init__(self):
        self.name = None
        self.description = None        
        self.price = None
        self.type = None
        self.equippable = None

class Weapon(Item):
    def __init__(self):
        super().__init__()
        self.damage = None

class Armor(Item):
    def __init__(self):
        super().__init__()
        self.armor = None

class Potion(Item):
    def __init__(self):
        super().__init__()
        self.hpHeal = None
