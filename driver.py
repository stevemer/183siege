import random, time
from asciiart import *
from weapons import *
from constants import *
from maps import *
from utils import *
from game import *
import asciiart



####################################################

         
game = Game()
user = '\0'
result = True
while (user != 'q'):
    #handle move
    game.map.printMap()
    if result == 2:
        print VICTORY_SCREEN
    elif result == 1: 
        user = raw_input ("Sir Knight, input your move. (W: up, S: down, A: left, D: right, X: automatic): ")
    elif result == 0:
        user = raw_input ("Sorry, that's a wall. Try again? (W: up, S: down, A: left, D: right, X: automatic): ")
    if user == 'w':
        result = game.move("UP") 
    elif user == 's':
        result = game.move("DOWN")
    elif user == 'a':
        result = game.move("LEFT")
    elif user == 'd':
        result = game.move("RIGHT")
    
