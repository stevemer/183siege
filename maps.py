from constants import *
import time, random
from asciiart import *

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

    def printMap(self):
        print HEADER
        print '- ' * (MAP_WIDTH + 1) + '-'
        for i in range(MAP_HEIGHT):
            output = ''
            output += '| '
            for j in range(MAP_WIDTH):
                if self.tiles[i][j].visible:
                    output += " {}".format(self.tiles[i][j].data)
                else:
                    output += "  "
            output += '|'
            print output
        print '- ' * (MAP_WIDTH + 1) + '-'

    def generateRoom(self, player_location):
        width = random.randint(1, MAP_WIDTH - player_location[1])
        height = random.randint(1, MAP_HEIGHT - player_location[0])

        for i in [player_location[0] - 1, player_location[0] + height]:
            for j in range(player_location[1] - 1, player_location[1] + width + 1):
                self.tiles[i][j].data = '-'
        
        for i in range(player_location[0], player_location[0] + height):
            for j in [player_location[1] - 1, player_location[1] + width]:
                self.tiles[i][j].data = '|'
        self.tiles[player_location[0] + height - 1][player_location[1] + width - 1].data = '#'


    def mapFind(self, symbol):
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                if self.tiles[i][j].data == symbol:
                    return (i,j)

