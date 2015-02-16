from weapons import *
from entities import *

class Inventory(object):
    def __init__(self):
        self.left_weapon = MeleeWeapon("SWORD", "Wooden Sword", 1)
        self.right_weapon = None #Defense("SHIELD", "Wooden Shield", 1)
        self.miscitems = {
            "Potions": 3, 
            "Keys": 0, 
            "Trinkets": 0,
        }

    def equip_left(self, item):
        if isinstance(item, RangedWeapon):
            self.left_weapon = item
            self.right_weapon = None
        elif isinstance(item, MeleeWeapon):
            self.left_weapon = item
        elif isinstance(item, Defense):
            if isinstance(self.left_weapon, RangedWeapon):
                self.right_weapon = None
            self.left_weapon = item
    
        else:
            raise Exception("Equipped item has invalid type")
    
    def equip_right(self, item):
        if isinstance(item, RangedWeapon):
            self.left_weapon = item
            self.right_weapon = None
        elif isinstance(item, MeleeWeapon):
            self.left_weapon = item
        elif isinstance(item, Defense):
            if isinstance(self.left_weapon, RangedWeapon):
                self.left_weapon = None
            self.right_weapon = item
    
        else:
            raise Exception("Equipped item has invalid type")

    def get_equipped(self):
        return [
            self.left_weapon,
            self.right_weapon
        ]

    def get_equipped_defense(self):
        if isinstance(self.left_weapon, Defense): return self.left_weapon
        elif isinstance(self.right_weapon, Defense): return self.right_weapon
        else: return None

    def get_equipped_melee(self):
        if isinstance(self.left_weapon, MeleeWeapon): return self.left_weapon
        elif isinstance(self.right_weapon, MeleeWeapon): return self.right_weapon
        else: return None

    def get_equipped_ranged(self):
        if isinstance(self.left_weapon, RangedWeapon):
            assert(self.right_weapon == None)
            return self.left_weapon
        elif isinstance(self.right_weapon, RangedWeapon):
            assert(self.left_weapon == None)
            return self.right_weapon
        else: 
            return None

    def get_damage(self):
        damage = 0
        # ranged dmg applies * 1.5
        if isinstance(self.left_weapon, RangedWeapon):
            damage += self.left_weapon.strength
        elif isinstance(self.left_weapon, MeleeWeapon):
            damage += self.left_weapon.strength
        if isinstance(self.right_weapon, RangedWeapon):
            assert(0)
            damage += self.right_weapon.strength
        elif isinstance(self.right_weapon, MeleeWeapon):
            damage += self.right_weapon.strength * OFFHAND_FACTOR
        return damage 
   
    def get_defense(self):
        defense = 0
        if isinstance(self.left_weapon, Defense):
            defense += self.left_weapon.strength
        elif isinstance(self.right_weapon, Defense):
            defense += self.right_weapon.strength
        return damage
 
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
        
