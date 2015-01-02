import sys
import asciiart
import random
from weapons import *
from entities import Player, Enemy, EnemyFactory
from maps import *
from utils import *
from maps import *
from inventory import Inventory
from getch import getch


class Game(object):
    def __init__(self):
        self.map = Map()
        self.player = Player()
        self.inventory = Inventory()
        self.enemy_factory = EnemyFactory()

        self.current_enemy = None

    def _inventoryData(self):
        # returns a list of 14 strings used to populate the bottom-right corner of the war screen
        data = []
        for i in range(14):
            data.append("") 
        data[0] = "Type: {}".format(self.current_enemy.name)
        #data[1] = "Element: {}".format(self.current_enemy.element)
        data[1] = "Weapon: {}".format(self.current_enemy.item.name)
        data[2] = "Next Attack: {}".format(STRENGTHNAMES[self.current_enemy.next_attack])
        data[3] = "- " * 26
        data[4] = "Equipment"
        
        data[6] = ("Left Hand: {}".format(self.inventory.lefthand + 1))    
        data[7] = ("Right Hand: {}".format(self.inventory.righthand + 1))    
        data[8] = "- " * 26
        data[9] = "INVENTORY"
        data[11] = ("Potions: {}".format(self.inventory.miscitems['potions'])) # num potions store in game #TODO
        data[12] = ("Keys: {}".format(self.inventory.miscitems['keys'])) # num keys in game #TODO
        data[13] = ("Trinkets: {}".format(self.inventory.miscitems['trinkets'])) # num trinkets
        return data

    def printItems(self): #TODO: list enemy weapon in case we want it?

        # populate list
        itemlist = []
        for i in range(6):
            try: itemlist.append(self.inventory.get_items()[i])
            except: itemlist.append(None)

        iteminfo = []
        for item in itemlist:
            if item != None:
                itemdata = [item.name, item.strength, "", "", "", ""] # replaced [2] with item.element to ""
                iteminfo.append(itemdata)
            else:
                iteminfo.append(None)

        imagelist = []
        for i in range(6):
            if itemlist[i] != None:
                imagelist.append(getattr(asciiart, itemlist[i].image))

        miscItems = self._inventoryData()

        lines = []
        #lines.append("- " * 80)
        lines.append("| 1." + " " * 32 + "| 2." + " " * 32 + "| 3." + " " * 32 + "| Enemy   " + " " * 44 + "|")
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

    def printScreen(self):
        # update to remove old messages
        while len(self.messages) > 8:
            self.messages.pop(0)
        message = "\n".join(self.messages)

        print
        # print the message box
        printMessageBox(message)
        # print battlefield
        printBattlefield(CHARACTER3, getattr(asciiart, self.current_enemy.image), 162, 15)
        # print info bar
        print SCREEN.format(hp=str(self.player.health) + "/100", ehp=str(self.current_enemy.health), estr=str("NONE"))
        # print equipment and items
        self.printItems()

    def _getUserMove(self):
        self.messages.append("What will you do?")
        self.printScreen()

        print "What will you do? ('h' for help)",
        decision = getch()
        while decision not in ['x', 'c', 'v', 'i']:
            self.messages.append("That's not a valid command - what will you do?")
            self.printScreen()
            print "That's not a valid command! ('h' for help) ",
            decision = getch()
        return decision

    def playerTurn(self):
        # set environment variables
        self.printScreen()
        self.current_enemy.next_attack = random.randint(1,5)
        decision = self._getUserMove()
        playerDamage = 0
        playerAction = ""
        runs = False

        # ATTACKING
        if decision == 'x':
            self.playerStance = "OFFENSIVE"
            # are we attacking with a ranged weapon?
            if isinstance(self.inventory.get_items()[self.inventory.lefthand], RangedWeapon):
                # deal the damage
                playerDamage = self.inventory.get_items()[self.inventory.lefthand].strength
                playerAction = "shoot"
                # if it's the first turn, we can shoot again.
                if self.bowTurns:
                    self.bowTurns -= 1
                    runs = True

            # for non-ranged weapons
            else:
                # deal the damage
                playerDamage = sum([self.inventory.get_items()[x].strength 
                                for x in [self.inventory.lefthand, self.inventory.righthand] 
                                if isinstance(self.inventory.get_items()[x], Weapon)
                                and not isinstance(self.inventory.get_items()[x], Defense)])
                playerAction = "hit"

            # deal the damage and update
            self.current_enemy.damage(playerDamage)
            self.messages.append("You {0} the {1} for {2} damage!".format(playerAction, self.current_enemy.name, playerDamage))
            print "HIT"
            if runs and not self.current_enemy.isDead():
                self.messages.append("The {} runs closer to you...".format(self.current_enemy.name))

            # if the self.current_enemy ran towards us, we can take another turn for free
            if runs and not self.player.isDead() and not self.current_enemy.isDead():
                self.playerTurn()
            return True
        
        # ITEMS
        elif decision == 'i':
            if self.inventory.miscitems["potions"] > 0:
                self.playerStance = "NEUTRAL"
                self.inventory.miscitems["potions"] -= 1
                self.messages.append("You drank a potion and recovered 25 health!")
                self.printScreen()
                return True
            else:
                self.messages.append("You don't have any potions!")
                return False

        # SHIELDING
        elif decision == 'c':
            # is there a shield equipped?
            shields = len([self.inventory.get_items()[x] for x in [self.inventory.lefthand, self.inventory.righthand] if self.inventory.get_items()[x].image == "SHIELD"]) #TODO untested
            if shields:
                self.playerStance = "DEFENSIVE"
                self.messages.append("You raised your shield!")
                return True
            else:
                self.messages.append("You try to raise your shield, only to discover you're not holding one. The {} looks confused.".format(self.current_enemy.name))
                return True # TODO false?

        # SWITCHING ITEMS
        elif decision == 'v':
            success = True
            hand = getch()
            if hand not in [',','.','<','>']:
                try:
                    x = int(hand)
                except:
                    success = False
                else:
                    # user wants to equip a bow, so both hands will be used.
                    if len(self.inventory.get_items()) > x - 1 and isinstance(self.inventory.get_items()[x-1], RangedWeapon):
                        # we can switch to it
                        success = self.inventory.equip_both(x)
                    else:
                        success = False

            else:
                num = getch()
                try: num = int(num)
                except: success = False

                if num not in range(6):
                    success = False
                elif hand in [',','<']:
                    # player wants to equip left
                    success = self.inventory.equip_left(num)
                else:   
                    # player wants to equip right
                    success = self.inventory.equip_right(num)
            
            # check the results of our equip stage
            if success:
                self.playerStance = "NEUTRAL"
                self.messages.append("You successfully switched weapons!")
                return True
            else:
                self.messages.append("You can't switch to that weapon!")
                return False

        # BAD COMMAND
        else:
            assert(False and "Invalid command specified")

    def enemyTurn(self):
        # enemy will of course hit back
        damage = int((float(self.current_enemy.item.strength) / 2) * self.current_enemy.next_attack)
        # player is shielding
        shield_level = 0
        if self.playerStance == "DEFENSIVE":
            # find the shields the player has
            if self.inventory.get_items()[self.inventory.lefthand].image == "SHIELD": #TODO type defnsive
                shield_level += self.inventory.get_items()[self.inventory.lefthand].strength
            if self.inventory.get_items()[self.inventory.righthand].image == "SHIELD":
                shield_level += self.inventory.get_items()[self.inventory.righthand].strength
        block_chance = shield_level * 0.05 
        event_value = random.uniform(0,1)
        if block_chance and event_value <= block_chance + 0.75:
            self.messages.append("You successfully blocked the enemy attack!")
        else:
            self.player.damage(damage)
            self.messages.append("The {0} hits you for {1} damage!".format(self.current_enemy.name, damage))
        return True

    def runEvent(self):
        # Combat loop
        isPlayerTurn = True
        self.messages = ["A {} appeared!".format(self.current_enemy.name)] #TODO verbage
        self.playerStance = "NEUTRAL"
        self.bowTurns = 1
        success = True

        self.printScreen()
        while not self.current_enemy.isDead() and not self.player.isDead():

            # Player's move
            if isPlayerTurn:
                success = self.playerTurn()
            # enemy's move
            else:
                success = self.enemyTurn()
            # update
            self.printScreen()

            if success:
                # Bow is only useful on the first turn
                if self.bowTurns:
                    self.bowTurns = 0
                # Change whose turn it is
                isPlayerTurn = False if isPlayerTurn else True
        
        # someone died
        if self.current_enemy.isDead():
            self.current_enemy.image = "DEAD_" + self.current_enemy.image
            self.messages.append("You defeated the {}!".format(self.current_enemy.name) )
            self.printScreen()
            # drop their weapon? TODO probablity chance that they drop weapon
            self.messages = ["You defeated the {}!".format(self.current_enemy.name),
                             "The {0} dropped a {1}...".format(self.current_enemy.name, self.current_enemy.item.name)]
            self.current_enemy.image = "BLANK_ENEMY"
            if self.inventory.space_exists():
                self.messages.append("Would you like to pick it up?")
                self.printScreen()
                y_or_n = getch()
                while y_or_n not in ['y', 'Y', 'n', 'N']:
                    self.messages.append("Please enter y/n")
                    self.printScreen()
                    y_or_n = getch()
                if y_or_n in ['y', 'Y']:
                    # pick up item
                    self.inventory.add_item(self.current_enemy.item)
                    self.printScreen()
                    time.sleep(2)
            else:
                self.messages.append("Your inventory is full!") #TODO replace items??? maybe, maybe not
                self.printScreen()

        elif self.player.isDead():
            print "DEFEAT"
            sys.exit(0)

    def checkEvent(self, tile):
        pass
        random.seed()
        event_probability = 10 / 187.5
        event_value = random.uniform(0,1)
        if event_value <= event_probability:
            # spawn an enemy TODO generator
            self.current_enemy = self.enemy_factory.generateEnemy()
            self.runEvent()

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
