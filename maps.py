from constants import *
from dungeon_generator import getMap, getEntrance
import time, random, heapq
from asciiart import *
from copy import deepcopy

class Tile(object):
    def __init__(self):
        self.visible = False
        self.data = ' '

class Map(object):
    def __init__(self):
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
        self.victory = (random.randint(0, MAP_HEIGHT - 1), random.randint(0, MAP_WIDTH - 1))
        while self.tiles[self.victory[0]][self.victory[1]].data != '.':
            self.victory = (random.randint(0, MAP_HEIGHT - 1), random.randint(0, MAP_WIDTH - 1))
        self.tiles[self.player[0]][self.player[1]].data = 'X'
        self.tiles[self.victory[0]][self.victory[1]].data = '@'
        for i in range(MAP_HEIGHT):
            for j in range(MAP_WIDTH):
                if self.tiles[i][j].data == '.':
                    self.tiles[i][j].data = ' '
                pass
            pass
        self._visited = set()
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

    def printMap(self, danger, health, potions, message):
        for i in range(3): print
        #"Currently hiding!" if hiding else "Visible!"
        print HEADER.format(DANGERS[danger], str(health), str(potions), message)
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

    def _isInBounds(self,loc):
        return 0 <= loc[0] < MAP_HEIGHT and 0 <= loc[1] < MAP_WIDTH

    def locIsFree(self, loc):
        if not self._isInBounds(loc):
            return False
        return self.tiles[loc[0]][loc[1]].data == ' '

    def _locIsDoor(self,loc):
        if not self._isInBounds(loc):
            return False
        return self.tiles[loc[0]][loc[1]].data == '='

    def _locIsWall(self,loc):
        return self.tiles[loc[0]][loc[1]].data == '#'

    @staticmethod
    def manDist(src, dest):
        return abs(src[0] - dest[0]) + abs(src[1] - dest[1])

    def findPath(self):
        src, dest = self.player, self.victory

        visited = deepcopy(self._visited)
        queue = [(self.manDist(src, dest), src, 0),]
        cameFrom = {}

        while queue:
            currentLoc, cost = queue[0][1], queue[0][2]
            if currentLoc == dest:
                return self._constructPath(cameFrom, currentLoc)

            heapq.heappop(queue)
            visited.add(currentLoc)
            for diff in (-1,1):
                xLoc = (currentLoc[0] + diff, currentLoc[1])
                if xLoc not in visited:
                    queueItem = (cost + self.manDist(xLoc, dest) + 1, xLoc, cost + 1)
                    if (self._isInBounds(xLoc) and not self._locIsWall(xLoc)) and (queueItem not in queue or (cost + 1 < cameFrom[xLoc][1])):
                        cameFrom[xLoc] = (currentLoc, cost + 1) # update cameFrom map so that xLoc -> where I came from, and distance
                        if queueItem not in queue:
                            heapq.heappush(queue, queueItem)

                yLoc = (currentLoc[0], currentLoc[1] + diff)
                if yLoc not in visited:
                    queueItem = (cost + self.manDist(yLoc, dest) + 1, yLoc, cost + 1)
                    if (self._isInBounds(yLoc) and not self._locIsWall(yLoc)) and (queueItem not in queue or (cost + 1 < cameFrom[yLoc][1])):
                        cameFrom[yLoc] = (currentLoc, cost + 1)  # update cameFrom map so that yLoc -> where I came from, and distance
                        if queueItem not in queue:
                            heapq.heappush(queue, queueItem)
        return None

    def _constructPath(self, cameFromMap, current):
        path = [current,]
        while current in cameFromMap.keys():
            tempKey = current
            current = cameFromMap[current][0]
            del cameFromMap[tempKey]
            path.append(current)
        path.reverse()
        path.pop(0) # remove self.player position
        return path
