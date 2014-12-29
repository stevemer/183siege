import random, time
from asciiart import *
from weapons import *
from constants import *
from maps import *
from utils import *
from game import *
import asciiart



####################################################

         
myMap = Map()
player = (10, 10)
myMap.generateRoom(player)
game = Game()
myMap.tiles[10][10].data = 'X'
myMap.printMap()
user = raw_input ("input your move: ")
while (user != 'q'):
    #handle move
    if user == 'l':
        player = game.move(myMap, player)
    myMap.printMap()
    user = raw_input ("input your move: ")
