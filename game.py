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
                "equipment": {
                    "offensive": self.inventory.get_equipped_melee() or self.inventory.get_equipped_ranged(),
                    "defensive": self.inventory.get_equipped_defense(),
                },
                "misc": self.inventory.miscitems,
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
            "Offensive: {}".format(
                self.inventory.get_equipped_melee().name \
                if self.inventory.get_equipped_melee() \
                else self.inventory.get_equipped_ranged().name \
                if self.inventory.get_equipped_ranged() \
                else "Nothing"
                )
        )
        data[7] = (
            "Defensive: {}".format(
                self.inventory.get_equipped_defense().name \
                if self.inventory.get_equipped_defense() \
                else "Nothing"
            )
        )
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
        offensive = self.inventory.get_equipped_ranged() or self.inventory.get_equipped_melee()
        defensive = self.inventory.get_equipped_defense()        

        offensive_image = getattr(asciiart, offensive.image).split('\n') if offensive else None
        defensive_image = getattr(asciiart, defensive.image).split('\n') if defensive else None

        miscItems = self._inventoryData()

        # fill the next 14 lines

        lines = []
        lines.append("Offensive Weapon" + " " * 36 + " | " + "Defensive Weapon" + " " * 37 + "| " + "{:52s}".format(miscItems[0]) + "|")
        lines.append(" " * 53 + "|" + " " * 54 + "| " + "{:52s}".format(miscItems[1]) + "|")

        offensive_stats = ["Name: " + str(offensive.name), "Strength: " + str(offensive.strength)] if offensive else None
        defensive_stats = ["Name: " + str(defensive.name), "Strength: " + str(defensive.strength)] if defensive else \
                          ["Name: None", "Strength: None"]

        for i in range(12):
            lines.append("{:22s}".format(offensive_stats[i] if offensive_stats and i < len(offensive_stats) else "") + (offensive_image[i] if offensive_image and i < len(offensive_image) else " " * 30) + " | "
                       + "{:22s}".format(defensive_stats[i] if defensive_stats and i < len(defensive_stats) else "") + (defensive_image[i] if defensive_image else " " * 30) + " | "
                       + "{:52s}".format(miscItems[i+2]) + "|")
        
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
        while decision[0] not in ['x', 'c', 'i']:
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
                playerAction = "shoot"

            # for non-ranged weapons
            else:
                # deal the damage
                playerAction = "hit"

            playerDamage = self.inventory.get_damage()
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
            item_type = "Potions"
            result = self.inventory.use_misc(item_type)
            # TODO: Not yet fully implemented for things other than Potions
            if result:
                self.playerStance = "NEUTRAL"
                self.player.health = min(
                    result +
                    self.player.health,
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
            #shield_level = self.inventory.get_equipped_defense().strength
            shield_level = self.inventory.get_defense()
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
                self.messages.append("Would you like to pick it up with one of your hands?")
                self.printScreen()
                y_or_n = makeMove(self.getDataForAI("ITEM"))
                while y_or_n not in ['y', 'Y', 'n', 'N']:
                    self.messages.append("Please enter y1/y2/n")
                    self.printScreen()
                    y_or_n = makeMove(self.getDataForAI("ITEM"))
                if y_or_n in ['y1', 'Y1']:
                    # pick up item
                    self.inventory.equip_left(self.current_enemy.item)
                    self.printScreen()
                    time.sleep(2)
                elif y_or_n in ['y2', 'Y2']:
                    self.inventory.equip_right(self.current_enemy.item)
                    self.printScreen()
                    time.sleep(2)

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
