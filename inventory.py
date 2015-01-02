from weapons import *
from entities import *

class Inventory(object):
    def __init__(self):
        self.items = [MeleeWeapon("SWORD", "Wooden Sword", 1), Defense("SHIELD", "Wooden Shield", 1)]
        self.miscitems = {"potions": 3, "keys": 0, "trinkets": 0}
        self.lefthand = 0 #TODO should be null?
        self.righthand = 1 #TODO will cause probs if less than 2 items held

    def equip_left(self, num):
        num -= 1
        # if already in a hand
        if self.righthand == num  or self.lefthand == num:
            return False
        # if no weapon there
        if num >= len(self.items):
            return False       
        self.lefthand = num 
        
        if isinstance(self.items[self.righthand], RangedWeapon):
            self.righthand = 0
        return True

    def equip_both(self, num):
        num -= 1
        if self.righthand == num or self.lefthand == num:
            return False
        if num >= len(self.items):
            return False       
        self.righthand = self.lefthand = num
        return True

    def equip_right(self, num):
        num -= 1
        # if already in a hand
        if self.righthand == num  or self.righthand == num:
            return False
        # if no weapon there
        if num >= len(self.items):
            return False       
        self.righthand = num 

        if isinstance(self.items[self.lefthand], RangedWeapon):
            self.lefthand = 0
        return True

    def add_item(self, item):
        assert(len(self.items) < 6)
        self.items.append(item)

    def space_exists(self):
        return len(self.items) < 6 

    def drop_item(self, num):
        self.items.pop(num - 1)

    def get_items(self):
        return self.items
