class GenericItemSelection(Exception):
    pass

class Entity(object):
    def __init__(self):
        self.health = 5
        pass

    def damage(self, num):
        self.health -= min(self.health, num)

    def isDead(self):
        return not self.health

class Player(Entity):
    def __init__(self):
        self.health = 100

class Enemy(Entity):
    def __init__(self):
        self.name = "GOBLIN"
        self.fancyname = "Cave Goblin"
        self.health = 3
        self.strength = 5
        self.item = RangedWeapon("BOW", "Gnommish Bow", 5, "Normal")

class Item(object):
    def __init__(self):
        raise GenericItemSelection()

class Weapon(Item):
    def __init__(self, name, fancyname, strength, element):
        # later: kwargs
        self.name = name
        self.strength = strength
        self.element = element 
        self.fancyname = fancyname
        

class MeleeWeapon(Weapon):
    def __init__(self, name, fancyname,  strength, element):
        super(MeleeWeapon, self).__init__(name, fancyname, strength, element)
        pass

class RangedWeapon(Weapon):
    def __init__(self, name, fancyname, strength, element):
        super(RangedWeapon, self).__init__(name, fancyname, strength, element)
        pass

class Defense(Weapon):
    def __init__(self, name, fancyname, strength, element):
        super(Defense, self).__init__(name, fancyname, strength, element)
        pass

