from getch import getch
from constants import *
import time, random
random.seed()

'''
        ---------------------------
        |      DATA OVERVIEW      |
        ---------------------------
{
    "decision": "ACTION",
    "enemy": {
        "name": self.current_enemy.name,
        "health": self.current_enemy.health,
        "item": {
            "type": self.current_enemy.item.image,
            "name": self.current_enemy.item.name,
            "strength": self.current_enemy.item.strength,
        },
        "next_attack:": STRENGTHNAMES[self.current_enemy.next_attack],
    },
    "player": {
        "health": self.player.health,
    },
    "inventory": {
        "items": [{
            "type": x.image,
            "name": x.name,
            "strength": x.strength,
        } for x in self.inventory.items],
        "misc": self.inventory.miscitems,
        "left_equipped": self.inventory.lefthand + 1,
        "right_equipped": self.inventory.righthand + 1,
    },
    "level": self.level,
}
'''

def makeMove(options):
    """ Students will implement this function """
    if not USE_AI:
        return getch()
    time.sleep(0.02)
    if options["decision"] == "ATTACK":
        return "x"
    elif options["decision"] == "ITEM":
        return "3"
    elif options["decision"] == "MOVE":
        if options['danger'] > 1:
            return 'h'
        return 'x'
        #random.choice(["w", 'a', 's', 'd'])

