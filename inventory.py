from weapons import *
from entities import *

class Inventory(object):
    def __init__(self):
        self.offensive_weapon = MeleeWeapon("SWORD", "Wooden Sword", 1)
        self.defensive_weapon = None #Defense("SHIELD", "Wooden Shield", 1)
        self.miscitems = {
            "Potions": 3, 
            "Keys": 0, 
            "Trinkets": 0,
        }

    def equip(self, item):
        if isinstance(item, RangedWeapon):
            self.offensive_weapon = item
            self.defensive_weapon = None
        elif isinstance(item, MeleeWeapon):
            self.offensive_weapon = item
        elif isinstance(item, Defense):
            if isinstance(self.offensive_weapon, RangedWeapon):
                self.offensive_weapon = None
            self.defensive_weapon = item
    
        else:
            raise Exception("Equipped item has invalid type")

    def get_equipped(self):
        return [
            self.offensive_weapon,
            self.defensive_weapon
        ]

    def get_equipped_defense(self):
        return self.defensive_weapon

    def get_equipped_melee(self):
        return self.offensive_weapon if isinstance(self.offensive_weapon, MeleeWeapon) else None

    def get_equipped_ranged(self):
        return self.offensive_weapon if isinstance(self.offensive_weapon, RangedWeapon) else None

    def get_items(self):
        return self.get_equipped()

    def add_misc(self, misc, count):
        assert(misc in self.miscitems.keys())
        self.miscitems[misc] += count

    def have_misc(self, misc):
        assert(misc in self.miscitems.keys())
        # a more verbose version for clarity
        return True if self.miscitems[misc] != 0 else False

    def use_misc(self, misc):
        assert(misc in self.miscitems.keys())
        # Note: Must return non-zero value for item, otherwise bugs will ensue
        if not self.have_misc(misc): return False
        self.miscitems[misc] -= 1
        return ITEM_STRENGTHS[misc]
        
