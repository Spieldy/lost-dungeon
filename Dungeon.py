from Entity import *
from Agent import *


class Dungeon(object):
    def __init__(self, dimension):
        self.dimension = dimension
        self.cell = [[Entity(EMPTY) for x in range(dimension+2)] for y in range(dimension+2)]
        self.agent = Agent()
        self.x_agent = 1
        self.y_agent = 1
        self.reset(dimension)

    def reset(self, dimension):
        self.dimension = dimension
        for i in range(self.dimension):
            self.cell[i][0].type = WALL
            self.cell[i][self.dimension-1].type = WALL
            self.cell[0][i].type = WALL
            self.cell[self.dimension-1][i].type = WALL

        self.cell[randint(1, dimension-2)][randint(1, dimension-2)].type = EXIT

        self.x_agent = randint(1, dimension + 1)
        self.y_agent = randint(1, dimension + 1)

    def update(self):
        pass
