from asciiart import *
from weapons import *
from constants import *
from maps import *
from utils import *
from game import *
from getch import getch
from dungeon_generator import *
import asciiart

import random, time, sys


####################################################

random.seed()         
game = Game()
outmap = Map()
outside = getEntrance()
for line in outside:
    print line
print "Press [ENTER] to begin your adventure..."
getch()

user = '\0'
result = True
while (user != 'q'):
    #handle move
    game.map.printMap()
    if result == 2:
        print VICTORY_SCREEN
        raw_input("[ENTER] to quit")
        sys.exit(0)
    elif result == 1: 
        print "Sir Knight, input your move. (W: up, S: down, A: left, D: right, X: automatic): ",
        user = getch()
        print
    elif result == 0:
        print "Sorry, that's a wall. Try again? (W: up, S: down, A: left, D: right, X: automatic): ",
        user = getch()
        print
    if user == 'w':
        result = game.move("UP") 
    elif user == 's':
        result = game.move("DOWN")
    elif user == 'a':
        result = game.move("LEFT")
    elif user == 'd':
        result = game.move("RIGHT")
print "Bye"
    
