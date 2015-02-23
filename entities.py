import random
from weapons import *
from constants import *
from enemy_data import enemies, enemy_freqs

class WeaponConstructor(object):
    def __init__(self):
        self.dropped_shield = False
        self.dropped_bow = False
        self.dropped_sword = False

    def __call__(self, weapon, name, strength):
        if not self.dropped_shield:
            self.dropped_shield = True
            return Defense("SHIELD", "Moldy Shield", 5)
        elif not self.dropped_bow:
            self.dropped_bow = True
            return RangedWeapon("BOW", "Slimy Bow", 5)
        elif not self.dropped_sword:
            self.dropped_sword = True
            return MeleeWeapon("SWORD", "Smelly Dagger", 5)
        elif weapon == "SHIELD":
            return Defense(weapon, name, strength)
        elif not self.dropped_bow or weapon == "BOW":
            return RangedWeapon(weapon, name, strength)
        elif not self.dropped_sword or weapon == "SWORD":
            return MeleeWeapon(weapon, name, strength)
        elif weapon == "CLUB":
            return MeleeWeapon(weapon, name, strength)
        raise Exception("Bad argument to weapon constructor!")

class BaseConstructorException(Exception):
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
        self.health = PLAYER_MAX_HEALTH
        self.hiding = False;

    def hide(self):
        assert(self.hiding == False)
        self.hiding = True;

    def unhide(self):
        assert(self.hiding == True)
        self.hiding = False;

class Enemy(Entity):
    def __init__(self):
        raise BaseConstructorException()

    def __init__(self, image, name, health, item):
        self.image = image
        self.name = name
        self.health = health
        self.item = item
        self.next_attack = 0

class EnemyFactory(object):
    def __init__(self):
        self.weapon_constructor = WeaponConstructor()
        random.seed()
        pass

    def generateEnemy(self, level):
        # compute enemy event
        choice = 0
        p = 0
        event = random.uniform(0,1)
        for i in range(len(enemy_freqs)):
            p += enemy_freqs[i]
            if event <= p:
                choice = i
                break 
        # select enemy
        enemy = enemies[min(choice, level - 1)]
        item = enemy["items"][random.randint(0, len(enemy["items"])-1)] 
        
        return Enemy(
            enemy["image"], 
            enemy["name"], 
            random.randint(enemy["health"]["min"], enemy["health"]["max"]),
            self.weapon_constructor(item["type"], item["name"], item["strength"])
        )
            
            
        
        
