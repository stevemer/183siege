import asciiart
from weapons import *
from maps import *
from utils import *
from maps import *

class Game(object):
    def __init__(self):
        self.health = 100
        self.items = [MeleeWeapon("SWORD", "Wooden Sword", 1, "Normal"), Defense("SHIELD", "Wooden Shield", 1, "Normal")]         
        self.lefthand = 1
        self.righthand = 2 #TODO will cause probs if less than 2 items held

        self.map = Map()
       
    def equip_left(self, num):
        self.lefthand = num - 1

    def equip_right(self, num):
        self.righthand = num - 1

    def add_item(self, item):
        assert(len(self.items) < 6)
        self.items.append(item)

    def space_exists(self):
        return len(self.items) < 6 

    def drop_item(self, num):
        self.items.pop(num - 1)

    def miscItemData(self):
        data = []
        for i in range(14):
            data.append("") 
        data[1] = ("Left Hand: {}".format(self.lefthand))    
        data[2] = ("Right Hand: {}".format(self.righthand))    

        data[9] = ("Potions: {}".format(9)) # num potions store in game #TODO
        data[10] = ("Keys: {}".format(3)) # num keys in game #TODO
        data[11] = ("Trinkets: {}".format(2)) # num trinkets
        return data

    def printItems(self): #TODO: list enemy weapon in case we want it?

        # populate list
        itemlist = []
        for i in range(6):
            try: itemlist.append(self.items[i])
            except: itemlist.append(None)

        iteminfo = []
        for item in itemlist:
            if item != None:
                itemdata = [item.fancyname, item.strength, item.element, "", "", ""]
                iteminfo.append(itemdata)
            else:
                iteminfo.append(None)

        imagelist = []
        for i in range(6):
            if itemlist[i] != None:
                imagelist.append(getattr(asciiart, itemlist[i].name))

        miscItems = self.miscItemData()

        lines = []
        #lines.append("- " * 80)
        lines.append("| 1." + " " * 32 + "| 2." + " " * 32 + "| 3." + " " * 32 + "| Equipped" + " " * 44 + "|")
        for i in range(6):
            lines.append("| " + ("{:18s}".format(str(iteminfo[0][i])) if itemlist[0] else " " * 18) + (imagelist[0].split("\n")[i] if itemlist[0] else " " * 16)
                       + "| " + ("{:18s}".format(str(iteminfo[1][i])) if itemlist[1] else " " * 18) + (imagelist[1].split("\n")[i] if itemlist[1] else " " * 16)
                       + "| " + ("{:18s}".format(str(iteminfo[2][i])) if itemlist[2] else " " * 18) + (imagelist[2].split("\n")[i] if itemlist[2] else " " * 16)
                       + "| " + "{:52s}".format(miscItems[i]) + "|")
        lines.append("- " * 54 + "| " + "{:52s}".format(miscItems[6]) + "|")
        lines.append("| 4." + " " * 32 + "| 5." + " " * 32 + "| 6." + " " * 32 + "| " + "{:52s}".format(miscItems[7]) + "|")
        for i in range(6):
            lines.append("| " + ("{:18s}".format(str(iteminfo[3][i])) if itemlist[3] else " " * 18) + (imagelist[3].split("\n")[i] if itemlist[3] else " " * 16)
                       + "| " + ("{:18s}".format(str(iteminfo[4][i])) if itemlist[4] else " " * 18) + (imagelist[4].split("\n")[i] if itemlist[4] else " " * 16)
                       + "| " + ("{:18s}".format(str(iteminfo[5][i])) if itemlist[5] else " " * 18) + (imagelist[5].split("\n")[i] if itemlist[5] else " " * 16)
                       + "| " + "{:52s}".format(miscItems[i + 8]) + "|")
        lines.append("- " * 82)
        for line in lines:
            print line

    def printScreen(self, enemy, message):
        printMessageBox(message)
        # print battlefield
        for x in new_split(CHARACTER3, getattr(asciiart, enemy.name), 162, 15): 
            print x
        # print info table
        print SCREEN.format(hp=str(self.health) + "/100", ehp=str(enemy.health), estr=str(enemy.strength))

        # print weapons?
        self.printItems()

    def runEvent(self, enemy):
        # Combat loop
        self.printScreen(enemy, "An enemy Goblin appeared!")
        while enemy.health > 0:
            decision = raw_input("What will you do? (Attack: 'A/a', Run: 'R/r', Switch Weapons: 'S#/s#' to use weapon #")
            while decision not in ['A', 'R', 'S']:
                decision = raw_input("What will you do? (Attack: 'A/a', Run: 'R/r', Switch Weapons: 'S#/s#' to use weapon #")

            message = "No action taken"
            if decision == 'A':
                enemy.health -= 1
                message = "You hit the enemy Goblin for 1 damage!"
            elif decision == 'R':
                message = "You can't run away!"
            elif decision == 'S':
                message = "You chose to switch weapons (but you only have 1)"
            self.printScreen(enemy, message)
            

    def checkEvent(self, tile):
        pass
        #self.runEvent(Enemy())

    def move(self, direction):
        tile = (-1,-1)
        x,y = self.map.player
        if direction == 'UP':
            tile = (x-1,y)
        elif direction == "DOWN":
            tile = (x+1,y)
        elif direction == "RIGHT":
            tile = (x,y+1)
        elif direction == "LEFT":
            tile = (x,y-1)
        # is there something on this square?
        if self.map.canMove(direction):
            if self.map.mapMove(direction):
                return 2
            self.checkEvent(tile)
            return 1 
        else:
            return 0 
