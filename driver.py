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
    message_list = []
    while (userMove != 'q'):
        #handle move
        game.map.printMap(game.danger, game.player.health, game.inventory.miscitems["Potions"])
        for message in message_list: print message
        message_list = []
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
                print "Sir Knight, input your move. (W: up, S: down, A: left, D: right, X: automatic, I: potion, H: hide/unhide): ",
                userMove = makeMove(game.getDataForAI("MOVE"))
                print
            elif resultOfMove == ERROR:
                print "Sorry, you can't do that. Try again? (W: up, S: down, A: left, D: right, X: automatic, I: potion, H: hide/unhide): ",
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
            elif userMove == 'i':
                item_type = "Potions"
                result = game.inventory.use_misc(item_type)
                # TODO: Not yet fully implemented for things other than Potions
                if result:
                    game.player.health = min(result + game.player.health, PLAYER_MAX_HEALTH)
                    message_list.append("You drank a potion and recovered {} health!".format(result))
                else:
                    #self.messages.append("You don't have any Potions!")
                    message_list.append("You don't have any Potions!")
                    #resultOfMove = ERROR
                resultOfMove = GOOD
            elif userMove == 'h':
                if not game.player.hiding:
                    game.move("HIDE")
                    message_list.append("You hid behind a dusty statue!")
            elif userMove == 'x':
                #assert(False)
                path = game.map.findPath()
                game.map._visited.add(game.map.player)
                if path[0][0] < game.map.player[0]:
                    resultOfMove = game.move("UP")
                elif path[0][0] > game.map.player[0]:
                    resultOfMove = game.move("DOWN")
                elif path[0][1] < game.map.player[1]:
                    resultOfMove = game.move("LEFT")
                elif path[0][1] > game.map.player[1]:
                    resultOfMove = game.move("RIGHT")
                else:
                    raise Exception("Find Path returned player's current square")
            game.update_danger()
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
