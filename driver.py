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
random.seed()         


entranceAnimation()

levelCount = 0
game = Game()
user = '\0'
result = True
while (user != 'q'):
    #handle move
    game.map.printMap()
    try:
        if result == 2:
            if levelCount < 3:
                for i in range(22): print
                print " " * 70 + "Level {} Complete".format(levelCount)
                for i in range(22): print
                levelCount += 1
                print "Press [ENTER] to continue..."
                getch()
                game.map = Map()
            else:
                raise Victory("You have defeated the Fortress of Dorf!")
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
    except Defeat as e:
        for i in range(22): print
        print " " * 60 + str(e)
        for i in range(22): print
        sys.exit()
    except Victory as e:
        for i in range(22): print
        print " " * 60 + str(e)
        for i in range(22): print
        sys.exit()

print "Bye"
    
