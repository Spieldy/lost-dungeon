from Entity import *
from Agent import *


class Dungeon(object):
    def __init__(self, dimension):
        self.dimension = dimension
        self.cell = [[Entity(EMPTY) for x in range(dimension)] for y in range(dimension)]
        self.agent = Agent(dimension)
        self.x_agent = 1
        self.y_agent = 1
        self.reset(dimension)

    def reset(self, dimension):
        self.dimension = dimension
        self.cell = [[Entity(EMPTY) for x in range(dimension)] for y in range(dimension)]


        # Create WALL
        for i in range(self.dimension):
            self.cell[i][0].type = WALL
            self.cell[i][self.dimension-1].type = WALL
            self.cell[0][i].type = WALL
            self.cell[self.dimension-1][i].type = WALL

        self.cell[randint(1, dimension-2)][randint(1, dimension-2)].type = EXIT

        self.x_agent = randint(1, dimension - 2)
        self.y_agent = randint(1, dimension - 2)
        while self.cell[self.x_agent][self.y_agent].type == EXIT:
            self.x_agent = randint(1, dimension - 2)
            self.y_agent = randint(1, dimension - 2)

    def update(self):
        self.dimension += 1
        self.reset(self.dimension)
