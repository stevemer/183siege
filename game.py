import asciiart
import random
from weapons import *
from maps import *
from utils import *
from maps import *
from getch import getch


class Game(object):
    def __init__(self):
        self.player = Player()
        self.items = [MeleeWeapon("SWORD", "Wooden Sword", 1, "Normal"), Defense("SHIELD", "Wooden Shield", 1, "Normal"),
                      MeleeWeapon("SWORD", "Big Sword", 3, "Normal"), Defense("SHIELD", "Big Shield", 3, "Normal"),
                      RangedWeapon("BOW", "Super Bow", 3, "Ice")]
        self.lefthand = 0
        self.righthand = 1 #TODO will cause probs if less than 2 items held

        self.map = Map()
       
    def equip_left(self, num):
        num -= 1
        # if already in a hand
        if self.righthand == num  or self.lefthand == num:
            return False
        # if no weapon there
        if num >= len(self.items):
            return False       
        self.lefthand = num 
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
        return True

    def add_item(self, item):
        assert(len(self.items) < 6)
        self.items.append(item)

    def space_exists(self):
        return len(self.items) < 6 

    def drop_item(self, num):
        self.items.pop(num - 1)

    def miscItemData(self, enemy):
        # returns a list of 14 strings used to populate the game data

        # the first 7 needed for enemy

        data = []
        for i in range(14):
            data.append("") 
        data[0] = "Type: {}".format(enemy.fancyname)
        data[1] = "Element: {}".format(enemy.element)
        data[2] = "Weapon: {}".format(enemy.item.fancyname)
        data[3] = "Next Attack: {}".format(STRENGTHNAMES[enemy.next_attack])
        data[4] = "- " * 25
        data[5] = "ITEMS"
        
        data[9] = ("Left Hand: {}".format(self.lefthand))    
        data[10] = ("Right Hand: {}".format(self.righthand))    

        data[11] = ("Potions: {}".format(9)) # num potions store in game #TODO
        data[12] = ("Keys: {}".format(3)) # num keys in game #TODO
        data[13] = ("Trinkets: {}".format(2)) # num trinkets
        return data

    def printItems(self, enemy): #TODO: list enemy weapon in case we want it?

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

        miscItems = self.miscItemData(enemy)

        lines = []
        #lines.append("- " * 80)
        lines.append("| 1." + " " * 32 + "| 2." + " " * 32 + "| 3." + " " * 32 + "| ENEMY   " + " " * 44 + "|")
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

    def printScreen(self, enemy, messages):
        # extract messages
        '''
        mailbox = list()
        while (messages):
            mailbox.append(messages.pop(0))
        message = "\n".join(mailbox)
        '''
        while len(messages) > 10:
            messages.pop(0)
        message = "\n".join(messages)

        print
        printMessageBox(message)
        # print battlefield
        for x in new_split(CHARACTER3, getattr(asciiart, enemy.name), 162, 15): 
            print x
        # print info table
        print SCREEN.format(hp=str(self.player.health) + "/100", ehp=str(enemy.health), estr=str(enemy.strength))

        # print weapons?
        self.printItems(enemy)

    def playerTurn(self, enemy):
        # set environment variables
        enemy.next_attack = random.randint(1,5)
        self.messages.append("What will you do?")

        self.printScreen(enemy, self.messages)

        print "What will you do? (Attack: 'x', Shield: 'c', Switch Weapons: 'v + </> + 1/2/3/4/5/6' to equip weapon # in hand </>): ",
        decision = getch()
        while decision not in ['x', 'c', 'v']:
            self.messages.append("What will you do?")
            self.printScreen(enemy, self.messages)
            print "That's not a valid command! (Attack: 'x', Shield: 'c', Switch Weapons: 'v + </> + 1/2/3/4/5/6' to equip weapon # in hand </>) ",
            decision = getch()

        if decision == 'x':
            if isinstance(self.items[self.lefthand], RangedWeapon):
                playerStance = "OFFENSIVE"
                playerDamage = self.items[self.lefthand].strength
                enemy.damage(playerDamage)
                if self.bowTurns:
                    isPlayerTurn = False # reset turns so that we get another turn immediately
                    self.bowTurns -= 1
                    self.messages.append("You shoot the enemy Goblin for {} damage!\nIt runs closer to you.".format(playerDamage))
                    self.printScreen(enemy, self.messages)
                else:
                    self.messages.append("You shoot the enemy Goblin for {} damage!".format(playerDamage))
                    self.printScreen(enemy, self.messages)
            else:
                playerStance = "OFFENSIVE"
                playerDamage = sum([self.items[x].strength for x in [self.lefthand, self.righthand] if isinstance(self.items[x], Weapon) and not isinstance(self.items[x], Defense)])
                enemy.damage(playerDamage)
                self.messages.append("You hit the enemy Goblin for {} damage!".format(playerDamage))
                self.printScreen(enemy, self.messages)
        
        # for if we use items
        elif decision == 'i':
            playerStance = "NEUTRAL"
            # using items
            print "You can't drink a potion now!"
            return False

        elif decision == 'c':
            playerStance = "DEFENSIVE"
            # is there a shield equipped?
            shields = len([self.items[x] for x in [self.lefthand, self.righthand] if self.items[x].name == "SHIELD"]) #TODO untested
            if shields:
                self.messages.append("You raised your shield!")
                self.printScreen(enemy, self.messages)
            else:
                self.messages.append("You try to raise your shield, only to discover you're not holding one. The {} looks confused.".format(enemy.fancyname))
                self.printScreen(enemy, self.messages)
        elif decision == 'v':
            playerStance = "NEUTRAL"
            hand = getch()
            if hand not in [',','.','<','>']:
                # user wants to equip a bow, so both hands will be used.
                try:
                    x = int(hand)
                    if len(self.items) > x - 1 and isinstance(self.items[x-1], RangedWeapon):
                        # we can switch to it
                        if self.equip_both(x):
                            self.messages.append("You successfully switched weapons!")
                            self.printScreen(enemy, self.messages)
                            return True
                        else:
                            self.messages.append("You can't switch to that weapon!")
                            self.printScreen(enemy, self.messages)
                            return False
                    else:
                        raise TypeError
                        
                except TypeError:
                    self.messages.append("You can't switch to that weapon!")
                    self.printScreen(enemy, self.messages)
                    return False

            else:
                num = int(getch())
                if num not in range(6):
                    self.messages.append("You can't switch to that weapon!")
                    self.printScreen(enemy, self.messages)
                    return False
                    
                if hand in [',','<']:
                    # player wants to equip left
                    if self.equip_left(num):
                        self.messages.append("You successfully switched weapons!")
                        self.printScreen(enemy, self.messages)
                    else:
                        self.messages.append("You can't switch to that weapon!")
                        self.printScreen(enemy, self.messages)
                        return False
                else:   
                    # player wants to equip right
                    if self.equip_right(num):
                        self.messages.append("You successfully switched weapons!")
                        self.printScreen(enemy, self.messages)
                    else:
                        self.messages.append("You can't switch to that weapon!")
                        self.printScreen(enemy, self.messages)
                        return False
        else:
            assert(False and "Invalid command specified")
        return True

    def enemyTurn(self, enemy):
        # enemy will of course hit back
        damage = (enemy.item.strength / 2) * enemy.next_attack
        # player is shielding
        shield_level = 0
        if self.playerStance == "DEFENSIVE":
            # find the shields the player has
            if self.items[self.lefthand].name == "SHIELD": #TODO type defnsive
                shield_level += self.items[self.lefthand].strength
            if self.items[self.righthand].name == "SHIELD":
                shield_level += self.items[self.righthand].strength
        block_chance = shield_level * 0.1 
        event_value = random.uniform(0,1)
        if block_chance and event_value <= block_chance + 0.5:
            self.messages.append("You successfully blocked the enemy attack!")
            self.printScreen(enemy, self.messages)
        else:
            self.player.damage(damage)
            self.messages.append("The enemy {0} hits you for {1} damage!".format(enemy.fancyname, damage))
            self.printScreen(enemy, self.messages)
        pass
        return True

    def runEvent(self, enemy):
        # Combat loop
        isPlayerTurn = True
        self.messages = ["An enemy {} appeared!".format(enemy.fancyname)]
        self.playerStance = "NEUTRAL"
        self.bowTurns = 1
    
        while not enemy.isDead() and not self.player.isDead():

            # Player's move
            if isPlayerTurn:
                result = self.playerTurn(enemy)
                if not result:
                    # if the user action failed, retry
                    continue

            # Enemy's move
            else:
                result = self.enemyTurn(enemy)
                if not result:
                    continue

            # Bow is only useful on the first turn
            if self.bowTurns: self.bowTurns -= 1
            # Change whose turn it is
            isPlayerTurn = False if isPlayerTurn else True
        
        # someone died
        if enemy.isDead():
            enemy.name = "DEAD_" + enemy.name
            self.messages.append("You defeated the enemy {}!".format(enemy.fancyname) )
            self.printScreen(enemy, self.messages)
            time.sleep(2)

        elif self.player.isDead():
            print "DEFEAT"
            sys.exit(0)

    def checkEvent(self, tile):
        pass
        random.seed()
        event_probability = 10 / 187.5
        event_value = random.uniform(0,1)
        if event_value <= event_probability:
            self.runEvent(Enemy())

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
