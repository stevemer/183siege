class GenericItemSelection(Exception):
    pass

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

