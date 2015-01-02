import random
from weapons import *
from enemy_data import enemies, enemy_freqs

def weaponConstructor(weapon):
    if weapon == "SWORD":
        return MeleeWeapon
    if weapon == "CLUB":
        return MeleeWeapon
    if weapon == "BOW":
        return RangedWeapon
    if weapon == "SHIELD":
        return Defense

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
        self.health = 100

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
        random.seed()
        pass

    def generateEnemy(self):
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
        enemy = enemies[choice]
        item = enemy["items"][random.randint(0, len(enemy["items"])-1)] 
        
        return Enemy(
            enemy["image"], 
            enemy["name"], 
            random.randint(enemy["health"]["min"], enemy["health"]["max"]),
            weaponConstructor(item["type"])(item["type"], item["name"], item["strength"])
        )
            
            
        
        
