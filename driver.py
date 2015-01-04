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
from ai import makeMove

if __name__ == "__main__":
    random.seed()         

    #entranceAnimation()

    VICTORY = 2
    GOOD = 1
    ERROR = 0

    game = Game()
    userMove = '\0'
    resultOfMove = True
    while (userMove != 'q'):
        #handle move
        game.map.printMap()
        try:
            if resultOfMove == VICTORY:
                if game.level < 3:
                    for i in range(22): print
                    print " " * 70 + "Level {} Complete".format(game.level)
                    for i in range(22): print
                    game.levelUp()
                    print "Press [ENTER] to continue..."
                    getch()
                    game.map = Map()
                else:
                    raise Victory("You have defeated the Fortress of Dorf!")
            elif resultOfMove == GOOD: 
                print "Sir Knight, input your move. (W: up, S: down, A: left, D: right, X: automatic): ",
                userMove = makeMove(game.getDataForAI("MOVE"))
                print
            elif resultOfMove == ERROR:
                print "Sorry, that's a wall. Try again? (W: up, S: down, A: left, D: right, X: automatic): ",
                userMove = makeMove(game.getDataForAI("MOVE"))
                print
            if userMove == 'w':
                resultOfMove = game.move("UP") 
            elif userMove == 's':
                resultOfMove = game.move("DOWN")
            elif userMove == 'a':
                resultOfMove = game.move("LEFT")
            elif userMove == 'd':
                resultOfMove = game.move("RIGHT")
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

    # user quit the game
    print "Bye"
