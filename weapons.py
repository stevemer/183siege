class GenericItemSelection(Exception):
    pass

class Item(object):
    def __init__(self):
        raise GenericItemSelection()

class Weapon(Item):
    def __init__(self, image, name, strength):
        # later: kwargs
        self.image = image
        self.name = name
        self.strength = strength

class MeleeWeapon(Weapon):
    def __init__(self, image, name,  strength):
        super(MeleeWeapon, self).__init__(image, name, strength)
        pass

class RangedWeapon(Weapon):
    def __init__(self, image, name, strength):
        super(RangedWeapon, self).__init__(image, name, strength)
        pass

class Defense(Weapon):
    def __init__(self, image, name, strength):
        super(Defense, self).__init__(image, name, strength)
        pass

