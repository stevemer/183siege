from weapons import *
from entities import *

class Inventory(object):
    def __init__(self):
        self.items = [
            RangedWeapon("BOW", "Big bow", 1),
            MeleeWeapon("SWORD", "Wooden Sword", 1),
            Defense("SHIELD", "Wooden Shield", 1),
        ]
        self.miscitems = {
            "Potions": 3, 
            "Keys": 0, 
            "Trinkets": 0,
        }
        self.lefthand = 0 #None
        self.righthand = 0 #None

    def swap_weapons(self):
        temp = self.lefthand
        self.lefthand = self.righthand
        self.righthand = temp
        return True
    
    def equip_left(self, num):
        num -= 1
        if num >= len(self.items): return False
        # this function should only handle single handed items
        assert(not isinstance(self.items[num], RangedWeapon))
        if self.lefthand == num: return False
        elif self.righthand == num: return self.swap_weapons()
        elif self.get_equipped_ranged(): self.righthand = None
        self.lefthand = num 
        return True

    def equip_both(self, num):
        num -= 1
        if num >= len(self.items): return False
        # this function should only handle double handed items
        assert(isinstance(self.items[num], RangedWeapon))
        if self.lefthand == num and self.righthand == num: return False
        # if we have a two-handed weapon and hands aren't together, that's bad
        assert(not self.lefthand == num and not self.righthand == num)
        self.lefthand = self.righthand = num
        return True

    def equip_right(self, num):
        num -= 1
        if num >= len(self.items): return False
        # this function should only handle single handed items
        assert(not isinstance(self.items[num], RangedWeapon))
        if self.righthand == num: return False
        elif self.lefthand == num: return self.swap_weapons()
        elif self.get_equipped_ranged(): self.lefthand = None
        self.righthand = num 
        return True

    def _get_equipped(self):
        return [
            self.items[self.lefthand] if self.lefthand is not None else None,
            self.items[self.righthand] if self.righthand is not None else None
        ]

    def get_equipped_defense(self):
        return filter(lambda x: isinstance(x, Defense), self._get_equipped())

    def get_equipped_melee(self):
        return filter(lambda x: isinstance(x, MeleeWeapon), self._get_equipped())

    def get_equipped_ranged(self):
        return filter(lambda x: isinstance(x, RangedWeapon), self._get_equipped())

    def add_item(self, item):
        assert(len(self.items) < 6)
        self.items.append(item)

    def space_exists(self):
        return len(self.items) < 6 

    def get_items(self):
        return self.items

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
        
