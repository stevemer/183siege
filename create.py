import random, time
from asciiart import *
import asciiart

MAP_WIDTH = 80
MAP_HEIGHT = 38

class GenericItemSelection(Exception):
    pass

class Enemy(object):
    def __init__(self):
        self.name = "GOBLIN"
        self.health = 3
        self.strength = 5
        self.item = RangedWeapon("BOW", "Gnommish Bow", 5, "Normal")

class Item(object):
    def __init__(self):
        raise GenericItemSelection()

class Weapon(Item):
    def __init__(self, name, fancyname, strength, element):
        # later: kwargs
        self.name = name
        self.strength = strength
        self.element = element 
        self.fancyname = fancyname
        

class MeleeWeapon(Weapon):
    def __init__(self, name, fancyname,  strength, element):
        super(MeleeWeapon, self).__init__(name, fancyname, strength, element)
        pass

class RangedWeapon(Weapon):
    def __init__(self, name, fancyname, strength, element):
        super(RangedWeapon, self).__init__(name, fancyname, strength, element)
        pass

class Defense(Weapon):
    def __init__(self, name, fancyname, strength, element):
        super(Defense, self).__init__(name, fancyname, strength, element)
        pass

class Tile(object):
    def __init__(self):
        self.visible = True # False
        self.data = ' '

class Map(object):
    def __init__(self):
    #self.tiles = [ [Tile()] * MAP_WIDTH] * MAP_HEIGHT
        self.tiles = list()
        for i in range(MAP_HEIGHT):
            curr = list()
            for j in range(MAP_WIDTH):
                curr.append(Tile())
            self.tiles.append(curr)
            pass
        pass
    pass 

    def clear(self):
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                self.tiles[i][j] = Tile()
class Game(object):
    def __init__(self):
        self.health = 100
        self.items = [RangedWeapon("BOW", "Big Bow", 5, "Ice"), Defense("SHIELD", "Gnommish Shield", 5, "Fire"),
                      MeleeWeapon("SWORD", "Strong Sword", 5, "Ice"), Defense("SHIELD", "Fire Shield", 5, "Fire"),
                      MeleeWeapon("SWORD", "Sword of Ages", 5, "Ice"), Defense("SHIELD", "Swift Shield", 5, "Fire")]
        self.lefthand = 0
        self.righthand = 0 #TODO will cause probs if less than 2 items held
       
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

def printItems(game): #TODO: list enemy weapon in case we want it?

    # populate list
    itemlist = []
    for i in range(6):
        try: itemlist.append(game.items[i])
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

    miscItems = miscItemData(game)

    lines = []
    #lines.append("- " * 80)
    lines.append("| 1." + " " * 32 + "| 2." + " " * 32 + "| 3." + " " * 32 + "| Equipped" + " " * 44 + "|")
    for i in range(6):
        lines.append("| " + ("{:18s}".format(str(iteminfo[0][i])) if itemlist[0] else " " * 18) + (imagelist[0].split("\n")[i] if itemlist[0] else "            ")
                   + "| " + ("{:18s}".format(str(iteminfo[1][i])) if itemlist[1] else " " * 18) + (imagelist[1].split("\n")[i] if itemlist[1] else "            ")
                   + "| " + ("{:18s}".format(str(iteminfo[2][i])) if itemlist[2] else " " * 18) + (imagelist[2].split("\n")[i] if itemlist[2] else "            ")
                   + "| " + "{:52s}".format(miscItems[i]) + "|")
    lines.append("- " * 54 + "| " + "{:52s}".format(miscItems[6]) + "|")
    for i in range(6):
        lines.append("| " + ("{:18s}".format(str(iteminfo[3][i])) if itemlist[3] else " " * 18) + (imagelist[3].split("\n")[i] if itemlist[3] else "            ")
                   + "| " + ("{:18s}".format(str(iteminfo[4][i])) if itemlist[4] else " " * 18) + (imagelist[4].split("\n")[i] if itemlist[4] else "            ")
                   + "| " + ("{:18s}".format(str(iteminfo[5][i])) if itemlist[5] else " " * 18) + (imagelist[5].split("\n")[i] if itemlist[5] else "            ")
                   + "| " + "{:52s}".format(miscItems[i + 7]) + "|")
    lines.append("- " * 82)
    for line in lines:
        print line

def printMap(map):
    print HEADER
    print '- ' * (MAP_WIDTH + 1) + '-'
    for i in range(MAP_HEIGHT):
        output = ''
        output += '| '
        for j in range(MAP_WIDTH):
            if map.tiles[i][j].visible:
                output += " {}".format(map.tiles[i][j].data)
            else:
                output += "  "
        output += '|'
        print output
    print '- ' * (MAP_WIDTH + 1) + '-'

def generateRoom(map, player_location):
    width = random.randint(1, MAP_WIDTH - player_location[1])
    height = random.randint(1, MAP_HEIGHT - player_location[0])

    for i in [player_location[0] - 1, player_location[0] + height]:
        for j in range(player_location[1] - 1, player_location[1] + width + 1):
            map.tiles[i][j].data = '-'
    
    for i in range(player_location[0], player_location[0] + height):
        for j in [player_location[1] - 1, player_location[1] + width]:
            map.tiles[i][j].data = '|'
    map.tiles[player_location[0] + height - 1][player_location[1] + width - 1].data = '#'


def mapFind(map, symbol):
    for i in range(MAP_HEIGHT):
        for j in range(MAP_WIDTH):
            if map.tiles[i][j].data == symbol:
                return (i,j)

####################################################

def new_split(img, img2, width, height):
    final_image = []
    image = img.split("\n")
    image2 = img2.split("\n")
    if len(image) > height:
        return ["BAD IMAGE SPLIT"] * height
    if len(image2) > height:
        return ["BAD IMAGE2 SPLIT"] * height
    if len(image) < height:
        for i in range(height - len(image)): image.insert(0, "|")
    if len(image2) < height:
        for i in range(height - len(image2)): image2.append("|")
    for i in range(height):
        final_image.append(image[i] + " " * (width + 1 - len(image[i]) - len(image2[i])) + image2[i]) 
    return final_image

def printMessageBox(message):
    print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    msg = message.split("\n")
    for i in range(min(8, len(msg))):
        print "| {:80s}                                                                                |".format(msg[i])
    if len(msg) < 8:
        for i in range(8 - len(msg)):
            print "| {:80s}                                                                                |".format("")
    print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"

def miscItemData(game):
    data = []
    for i in range(13):
        data.append("") 
    data[1] = ("Left Hand: {}".format(game.lefthand))    
    data[2] = ("Right Hand: {}".format(game.righthand))    

    data[9] = ("Potions: {}".format(9)) # num potions store in game #TODO
    data[10] = ("Keys: {}".format(3)) # num keys in game #TODO
    data[11] = ("Trinkets: {}".format(2)) # num trinkets
    return data




def printScreen(game, enemy, message):
    printMessageBox(message)
    # print battlefield
    for x in new_split(CHARACTER3, getattr(asciiart, enemy.name), 162, 15): 
        print x
    # print info table
    print SCREEN.format(hp=str(game.health) + "/100", ehp=str(enemy.health), estr=str(enemy.strength))

    # print weapons?
    printItems(game)

def runEvent(game, enemy):
    # Combat loop
    printScreen(game, enemy, "An enemy Goblin appeared!")
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
        printScreen(game, enemy, message)
        

def checkEvent(game, map, tile):
    pass
    runEvent(game, Enemy())
    #if tile == mapFind(map, '#'):
    #    time.sleep(3)

def move(game, map, player):
    map.tiles[player[0]][player[1]].data = ' ' 
    loc = mapFind(map, '#') 
    offset = [0,0]
    if loc[0] > player[0]:
        offset[0] = 1
    elif loc[0] < player[0]:
        offset[0] = -1
    # implicit else of 0

    if loc[1] > player[1]:
        offset[1] = 1
    elif loc[1] < player[1]:
        offset[1] = -1
    #implicit else of 0

    newTile = (player[0] + offset[0], player[1] + offset[1])
    
    if newTile == mapFind(map, '#'):
        # if have completed room
        map.tiles[newTile[0]][newTile[1]].data = 'X'  
        printMap(map)

        map.clear()
        player = (10, 10)
        generateRoom(map, player)
        map.tiles[10][10].data = 'X'
        return (10, 10)

    # is there something on this square?
    checkEvent(game, map, newTile)

    map.tiles[newTile[0]][newTile[1]].data = 'X'
    return newTile 

         
myMap = Map()
player = (10, 10)
generateRoom(myMap, player)
game = Game()
myMap.tiles[10][10].data = 'X'
printMap(myMap)
user = raw_input ("input your move: ")
while (user != 'q'):
    #handle move
    if user == 'l':
        player = move(game, myMap, player)
    printMap(myMap)
    user = raw_input ("input your move: ")







def findWalls(map, player):
    left, right, up, down  = 0,0,0,0
    x,y = player[0], player[1]
    while not left:
        x -= 1
        if map.tiles[i][j].data == '|':
            left = x
    while not right:
        x += 1
        if map.tiles[i][j].data == '|':
            right = x
    while not up:
        x -= 1
        if map.tiles[i][j].data == '-':
            up = x
    while not down:
        x += 1
        if map.tiles[i][j].data == '-':
            down = x
