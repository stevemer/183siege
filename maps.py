from constants import *
from dungeon_generator import getMap
import time, random
from asciiart import *

class Tile(object):
    def __init__(self):
        self.visible = False
        self.data = ' '

class Map(object):
    def __init__(self):
    #self.tiles = [ [Tile()] * MAP_WIDTH] * MAP_HEIGHT
        map_grid = getMap(MAP_WIDTH, MAP_HEIGHT)
        self.tiles = list()
        for i in range(MAP_HEIGHT):
            curr = list()
            for j in range(MAP_WIDTH):
                curr.append(Tile())
            self.tiles.append(curr)
            pass
        pass
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                self.tiles[i][j].data = map_grid[i][j]
                pass
            pass
        self.player = (random.randint(0, MAP_HEIGHT - 1), random.randint(0, MAP_WIDTH - 1))
        while self.tiles[self.player[0]][self.player[1]].data != '.':
            self.player = (random.randint(0, MAP_HEIGHT - 1), random.randint(0, MAP_WIDTH - 1))
        # generate a victory location
        victory = (random.randint(0, MAP_HEIGHT - 1), random.randint(0, MAP_WIDTH - 1))
        while self.tiles[victory[0]][victory[1]].data != '.':
            victory = (random.randint(0, MAP_HEIGHT - 1), random.randint(0, MAP_WIDTH - 1))
        self.tiles[self.player[0]][self.player[1]].data = 'X'
        self.tiles[victory[0]][victory[1]].data = '@'
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                if self.tiles[i][j].data == '.':
                    self.tiles[i][j].data = ' '
                pass
            pass
        self.revealRoom()

    def clear(self):
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                self.tiles[i][j] = Tile()

    def revealRoom(self):
        visible = []
        self.tiles[self.player[0]][self.player[1]].visible = True
        visible.append(self.player)
        while len(visible):
            x,y = visible.pop()
            if self.tiles[x][y].data in VISIBLE_TILES or (x,y) == self.player:
                # make all adjacent tiles visible
                left = down = up = right = False
                if x < MAP_HEIGHT - 1 and not self.tiles[x+1][y].visible:
                    self.tiles[x+1][y].visible = True
                    visible.append((x+1,y))
                if x > 0 and not self.tiles[x-1][y].visible:
                    self.tiles[x-1][y].visible = True
                    visible.append((x-1,y))
                if y < MAP_WIDTH - 1 and not self.tiles[x][y+1].visible:
                    self.tiles[x][y+1].visible = True
                    visible.append((x,y+1))
                if y > 0 and not self.tiles[x][y-1].visible:
                    self.tiles[x][y-1].visible = True
                    visible.append((x,y-1))
    
                if x < MAP_HEIGHT - 1 and y < MAP_WIDTH - 1 and not self.tiles[x+1][y+1].visible:
                    self.tiles[x+1][y+1].visible = True
                    visible.append((x+1,y+1))
                if x < MAP_HEIGHT - 1 and y > 0 and not self.tiles[x+1][y-1].visible:
                    self.tiles[x+1][y-1].visible = True
                    visible.append((x+1,y-1))
                if x > 0 and y < MAP_WIDTH - 1 and not self.tiles[x-1][y+1].visible:
                    self.tiles[x-1][y+1].visible = True
                    visible.append((x-1,y+1))
                if x > 0 and y > 0 and not self.tiles[x-1][y-1].visible:
                    self.tiles[x-1][y-1].visible = True
                    visible.append((x-1,y-1))

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

    def canMove(self, direction):
        x,y = self.player
        if direction == 'UP':
            return x > 0 and self.tiles[x-1][y].data != '#'
        elif direction == "DOWN":
            return x < MAP_HEIGHT - 1 and self.tiles[x+1][y].data != '#'
        elif direction == "RIGHT":
            return y < MAP_WIDTH - 1 and self.tiles[x][y+1].data != '#'
        elif direction == "LEFT":
            return y > 0 and self.tiles[x][y-1].data != '#'
    
    def mapMove(self, direction):   
        x,y = self.player
        self.tiles[x][y].data = ' '
        if direction == 'UP':
            self.player = (x-1,y)
        elif direction == "DOWN":
            self.player = (x+1,y)
        elif direction == "RIGHT":
            self.player = (x,y+1)
        elif direction == "LEFT":
            self.player = (x,y-1)
        if self.tiles[self.player[0]][self.player[1]].data == '@':
            print "VICTORY! You've found the magical staircase!"
            return True
        self.tiles[self.player[0]][self.player[1]].data = 'X'
        self.revealRoom()
        return False
