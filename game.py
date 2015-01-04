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
from ai import makeMove


class Game(object):

    def __init__(self):
        self.map = Map()
        self.player = Player()
        self.inventory = Inventory()
        self.enemy_factory = EnemyFactory()

        self.current_enemy = None
        self.level = 0

    def levelUp(self):
        self.level += 1

    def getDataForAI(self, moveType):
        return {
            "decision": moveType,
            "enemy": None if not self.current_enemy else {
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
                "left_equipped": self.inventory.lefthand + 1 if self.inventory.lefthand else None,
                "right_equipped": self.inventory.righthand + 1 if self.inventory.righthand else None,
            },
            "level": self.level,
        }

    def _inventoryData(self):
        # returns a list of 14 strings used to populate the bottom-right corner
        # of the war screen
        data = []
        for i in range(14):
            data.append("")
        data[0] = "Type: {}".format(self.current_enemy.name)
        #data[1] = "Element: {}".format(self.current_enemy.element)
        data[1] = "Weapon: {}".format(self.current_enemy.item.name)
        data[2] = "Next Attack: {}".format(
            STRENGTHNAMES[
                self.current_enemy.next_attack])
        data[3] = "- " * 26
        data[4] = "Equipment"

        data[6] = (
            "Left Hand: {}".format(
                self.inventory.lefthand +
                1 if self.inventory.lefthand else None))
        data[7] = (
            "Right Hand: {}".format(
                self.inventory.righthand +
                1 if self.inventory.righthand else None))
        data[8] = "- " * 26
        data[9] = "INVENTORY"
        data[11] = (
            "Potions: {}".format(
                self.inventory.miscitems['Potions']))  # num Potions store in game #TODO
        data[12] = (
            "Keys: {}".format(
                self.inventory.miscitems['Keys']))  # num keys in game #TODO
        data[13] = (
            "Trinkets: {}".format(
                self.inventory.miscitems['Trinkets']))  # num trinkets
        return data

    def printItems(self):  # TODO: list enemy weapon in case we want it?

        # populate list
        itemlist = []
        for i in range(6):
            try:
                itemlist.append(self.inventory.get_items()[i])
            except:
                itemlist.append(None)

        iteminfo = []
        for item in itemlist:
            if item is not None:
                itemdata = [
                    item.name,
                    "Strength: {}".format(
                        item.strength),
                    "",
                    "",
                    "",
                    ""]  # replaced [2] with item.element to ""
                iteminfo.append(itemdata)
            else:
                iteminfo.append(None)

        imagelist = []
        for i in range(6):
            if itemlist[i] is not None:
                imagelist.append(getattr(asciiart, itemlist[i].image))

        miscItems = self._inventoryData()

        lines = []
        #lines.append("- " * 80)
        lines.append(
            "| 1." +
            " " *
            32 +
            "| 2." +
            " " *
            32 +
            "| 3." +
            " " *
            32 +
            "| Enemy   " +
            " " *
            44 +
            "|")
        for i in range(6):
            lines.append("| " +
                         ("{:18s}".format(str(iteminfo[0][i])) if itemlist[0] else " " *
                          18) +
                         (imagelist[0].split("\n")[i] if itemlist[0] else " " *
                          16) +
                         "| " +
                         ("{:18s}".format(str(iteminfo[1][i])) if itemlist[1] else " " *
                             18) +
                         (imagelist[1].split("\n")[i] if itemlist[1] else " " *
                             16) +
                         "| " +
                         ("{:18s}".format(str(iteminfo[2][i])) if itemlist[2] else " " *
                             18) +
                         (imagelist[2].split("\n")[i] if itemlist[2] else " " *
                             16) +
                         "| " +
                         "{:52s}".format(miscItems[i]) +
                         "|")
        lines.append("- " * 54 + "| " + "{:52s}".format(miscItems[6]) + "|")
        lines.append(
            "| 4." +
            " " *
            32 +
            "| 5." +
            " " *
            32 +
            "| 6." +
            " " *
            32 +
            "| " +
            "{:52s}".format(
                miscItems[7]) +
            "|")
        for i in range(6):
            lines.append("| " +
                         ("{:18s}".format(str(iteminfo[3][i])) if itemlist[3] else " " *
                          18) +
                         (imagelist[3].split("\n")[i] if itemlist[3] else " " *
                          16) +
                         "| " +
                         ("{:18s}".format(str(iteminfo[4][i])) if itemlist[4] else " " *
                             18) +
                         (imagelist[4].split("\n")[i] if itemlist[4] else " " *
                             16) +
                         "| " +
                         ("{:18s}".format(str(iteminfo[5][i])) if itemlist[5] else " " *
                             18) +
                         (imagelist[5].split("\n")[i] if itemlist[5] else " " *
                             16) +
                         "| " +
                         "{:52s}".format(miscItems[i +
                                                   8]) +
                         "|")
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
        printBattlefield(
            CHARACTER3,
            getattr(
                asciiart,
                self.current_enemy.image),
            162,
            15)
        # print info bar
        print SCREEN.format(hp=str(self.player.health) + "/100", ehp=str(self.current_enemy.health))
        # print equipment and items
        self.printItems()

    def _getUserMove(self):
        self.messages.append("What will you do?")
        self.printScreen()

        print "What will you do? ('h' for help)",
        decision = makeMove(self.getDataForAI("ATTACK"))
        while decision[0] not in ['x', 'c', 'v', 'i']:
            self.messages.append(
                "That's not a valid command - what will you do?")
            self.printScreen()
            print "That's not a valid command! ('h' for help) ",
            decision = makeMove(self.getDataForAI("ATTACK"))

            if decision == 'h':
                printHelpScreen()
                decision = makeMove(self.getDataForAI("ATTACK"))
        return decision

    def playerTurn(self):
        # set environment variables
        self.printScreen()
        self.current_enemy.next_attack = random.randint(1, 5)
        decisions = [x for x in self._getUserMove()]
        playerDamage = 0
        playerAction = ""

        # ATTACKING
        if decisions[0] == 'x':
            self.playerStance = "OFFENSIVE"
            # are we attacking with a ranged weapon?
            ranged_items = self.inventory.get_equipped_ranged()
            if ranged_items:
                # deal the damage
                playerDamage = ranged_items[0].strength
                playerAction = "shoot"

            # for non-ranged weapons
            else:
                # deal the damage
                playerDamage = sum(
                    [x.strength for x in self.inventory.get_equipped_melee()])
                playerAction = "hit"

            # deal the damage and update
            self.current_enemy.damage(playerDamage)
            self.messages.append(
                "You {0} the {1} for {2} damage!".format(
                    playerAction,
                    self.current_enemy.name,
                    playerDamage))
            print "HIT"

            return True

        # ITEMS
        elif decisions[0] == 'i':
            item_type = "Potion"
            result = self.inventory.use_misc(item_type)
            # TODO: Not yet fully implemented for things other than Potions
            if result:
                self.playerStance = "NEUTRAL"
                self.player.health = min(
                    result +
                    self.player_health,
                    PLAYER_MAX_HEALTH)
                self.messages.append(
                    "You drank a potion and recovered {} health!".format(result))
                self.printScreen()
                return True
            else:
                self.messages.append("You don't have any Potions!")
                return False

        # SHIELDING
        elif decisions[0] == 'c':
            # is there a shield equipped?
            shields = self.inventory.get_equipped_defense()
            if shields:
                self.playerStance = "DEFENSIVE"
                self.messages.append("You raised your shield!")
                return True
            else:
                self.messages.append(
                    "You try to raise your shield, only to discover you're not holding one. The {} looks confused.".format(
                        self.current_enemy.name))
                return True

        # SWITCHING ITEMS
        elif decisions[0] == 'v':
            success = True
            hand = decisions[1] if USE_AI else getch()
            if hand not in [',', '.', '<', '>']:
                try:
                    x = int(hand)
                except:
                    success = False
                else:
                    # user wants to equip a bow, so both hands will be used.
                    if len(
                        self.inventory.get_items()) > x - 1 and isinstance(
                        self.inventory.get_items()[
                            x - 1],
                            RangedWeapon):
                        # we can switch to it
                        success = self.inventory.equip_both(x)
                    else:
                        success = False

            else:
                num = decisions[2] if USE_AI else getch()
                try:
                    num = int(num)
                except:
                    success = False

                if num not in range(6):
                    success = False
                elif hand in [',', '<']:
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
        damage = int(
            (float(
                self.current_enemy.item.strength) *
                ENEMY_DAMAGE_CONSTANT) *
            self.current_enemy.next_attack)
        # player is shielding
        shield_level = 0
        if self.playerStance == "DEFENSIVE":
            # find the shields the player has
            shields = self.inventory.get_equipped_defense()
            shield_level = sum([x.strength for x in shields])
        block_chance = shield_level * SHIELD_LEVEL_BONUS
        event_value = random.uniform(0, 1)
        if block_chance and event_value <= block_chance + SHIELD_BASE_CHANCE:
            self.messages.append("You successfully blocked the enemy attack!")
        else:
            self.player.damage(damage)
            damageType = "hit" if not isinstance(
                self.current_enemy.item,
                RangedWeapon) else "shoot"
            self.messages.append(
                "The {0} {2}s you for {1} damage!".format(
                    self.current_enemy.name,
                    damage,
                    damageType))
        return True

    def runEvent(self):
        # Combat loop
        isPlayerTurn = True
        self.messages = [
            "A {} appeared!".format(
                self.current_enemy.name)]  # TODO verbage
        self.playerStance = "NEUTRAL"
        # Assume player will not make a mistake until he does
        success = True
        # Is player or enemy using a bow?
        self.rangedEncounter = False
        if self.inventory.get_equipped_ranged() or isinstance(
                self.current_enemy.item,
                RangedWeapon):
            self.rangedEncounter = True

        self.printScreen()
        while not self.current_enemy.isDead() and not self.player.isDead():

            if self.rangedEncounter:
                if self.inventory.get_equipped_ranged():
                    while not self.playerTurn():  # Loop on invalid moves
                        self.printScreen()
                if isinstance(self.current_enemy.item, RangedWeapon):
                    self.enemyTurn()

            # Player's move
            elif isPlayerTurn:
                while not self.playerTurn():  # Loop on invalid moves
                    self.printScreen()

            # enemy's move
            else:
                self.enemyTurn()
            # update
            self.printScreen()

            # Bow is only useful on the first turn
            if self.rangedEncounter:
                self.rangedEncounter = False
                if not self.current_enemy.isDead() and not self.player.isDead() and not isinstance(
                        self.current_enemy.item,
                        RangedWeapon):
                    self.messages.append(
                        "The {} runs closer to you...".format(
                            self.current_enemy.name))
            else:
                # Change whose turn it is
                isPlayerTurn = False if isPlayerTurn else True

        # someone died
        if self.current_enemy.isDead():
            self.current_enemy.image = "DEAD_" + self.current_enemy.image
            self.messages.append(
                "You defeated the {}!".format(
                    self.current_enemy.name))
            self.printScreen()
            self.messages = [
                "You defeated the {}!".format(
                    self.current_enemy.name)]
            self.printScreen()

            p = random.uniform(0, 1)
            if p <= ITEM_DROP_PROBABILITY:
                self.messages.append(
                    "The {0} dropped a {1}...".format(
                        self.current_enemy.name,
                        self.current_enemy.item.name))
                self.current_enemy.image = "BLANK_ENEMY"
                if self.inventory.space_exists():
                    self.messages.append("Would you like to pick it up?")
                    self.printScreen()
                    y_or_n = makeMove(self.getDataForAI("ITEM"))
                    while y_or_n not in ['y', 'Y', 'n', 'N']:
                        self.messages.append("Please enter y/n")
                        self.printScreen()
                        y_or_n = makeMove(self.getDataForAI("ITEM"))
                    if y_or_n in ['y', 'Y']:
                        # pick up item
                        self.inventory.add_item(self.current_enemy.item)
                        self.printScreen()
                        time.sleep(2)
                else:
                    # TODO replace items??? maybe, maybe not
                    self.messages.append("Your inventory is full!")
                    self.printScreen()

        elif self.player.isDead():
            raise Defeat("You have been defeated.")

    def checkEvent(self, tile):
        pass
        random.seed()
        event_value = random.uniform(0, 1)
        if event_value <= ENEMY_ENCOUNTER_CHANCE:
            # spawn an enemy TODO generator
            self.current_enemy = self.enemy_factory.generateEnemy()
            self.runEvent()

    def move(self, direction):
        tile = (-1, -1)
        x, y = self.map.player
        if direction == 'UP':
            tile = (x - 1, y)
        elif direction == "DOWN":
            tile = (x + 1, y)
        elif direction == "RIGHT":
            tile = (x, y + 1)
        elif direction == "LEFT":
            tile = (x, y - 1)
        # is there something on this square?
        if self.map.canMove(direction):
            if self.map.mapMove(direction):
                return 2
            self.checkEvent(tile)
            return 1
        else:
            return 0
