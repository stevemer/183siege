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

DIRS = {
    'w': 'UP',
    'a': 'LEFT',
    's': 'DOWN',
    'd': 'RIGHT',
}

if __name__ == "__main__":
    random.seed()         

    entranceAnimation()

    VICTORY = 2
    GOOD = 1
    ERROR = 0

    game = Game()
    userMove = '\0'
    resultOfMove = True
    message_list = []
    while (userMove != 'q'):
        message = ''
        if message_list:
            assert(len(message_list) == 1)
            message = message_list[0]
            message_list = []
        game.map.printMap(game.danger, game.player.health, game.inventory.miscitems["Potions"], message)
        #handle move
        userMove = makeMove(game.getDataForAI("MOVE"))
        try:
            if userMove in ['w', 's', 'a', 'd']:
                resultOfMove = game.move(DIRS[userMove])
            elif userMove == 'i':
                item_type = "Potions"
                result = game.inventory.use_misc(item_type)
                # TODO: Not yet fully implemented for things other than Potions
                if result:
                    game.player.health = min(result + game.player.health, PLAYER_MAX_HEALTH)
                    message_list.append("You drank a potion and recovered {} health!".format(result))
                else:
                    message_list.append("You don't have any Potions!")
                    #resultOfMove = ERROR
            elif userMove == 'h':
                if not game.player.hiding:
                    game.move("HIDE")
                    message_list.append(HIDING_MSGS[random.randint(0,len(HIDING_MSGS) - 1)])
            elif userMove == 'x':
                path = game.map.findPath()
                assert(path != None)
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
                pass
            elif resultOfMove == ERROR:
                message_list.append("Sorry, you can't do that!") 
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
