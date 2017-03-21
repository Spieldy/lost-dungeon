from Entity import *
from Agent import *
from random import randint

# Global variables defining generation probabilities
INSERT_PROBABILITY = 5


class Dungeon(object):
    def __init__(self, dimension):
        self.dimension = dimension
        self.board = [[Entity(EMPTY, EMPTY) for x in range(dimension)] for y in range(dimension)]
        self.agent = Agent(1, 1, self)
        self.reset(dimension)

    def reset(self, dimension):
        self.dimension = dimension
        self.board = [[Entity(EMPTY, EMPTY) for x in range(dimension)] for y in range(dimension)]


        # Create WALL
        for i in range(self.dimension):
            self.board[i][0].type = WALL
            self.board[i][self.dimension - 1].type = WALL
            self.board[0][i].type = WALL
            self.board[self.dimension - 1][i].type = WALL

        # Create EXIT
        self.board[randint(1, dimension - 2)][randint(1, dimension - 2)].type = EXIT

        # Random start position of the HERO == Agent
        self.agent.x = randint(1, dimension - 2)
        self.agent.y = randint(1, dimension - 2)
        self.agent.respawn_x = self.agent.x
        self.agent.respawn_y = self.agent.y

        while self.board[self.agent.x][self.agent.y].type == EXIT:
            self.agent.x = randint(1, dimension - 2)
            self.agent.y = randint(1, dimension - 2)
            self.agent.respawn_x = self.agent.x
            self.agent.respawn_y = self.agent.y

        self.populate()

        self.agent.reset()

    def populate(self):
        # Populate
        for x in range(self.dimension):
            for y in range(self.dimension):

                # TRAP
                event_occurred = randint(0, 99)
                if event_occurred < INSERT_PROBABILITY:
                    event_x = randint(1, self.dimension - 2)
                    event_y = randint(1, self.dimension - 2)
                    while not self.board[event_x][event_y].is_priority() and (
                            self.agent.x == event_x and self.agent.y == event_y):
                        event_x = randint(1, self.dimension - 2)
                        event_y = randint(1, self.dimension - 2)
                    self.board[event_x][event_y].type = TRAP

                    # Generate TRASH around the TRAP
                    if event_x > 1 and not self.board[event_x - 1][event_y].is_priority():
                        if self.board[event_x - 1][event_y].is_spoiled():
                            self.board[event_x - 1][event_y].type = BONES_TRASH
                        else:
                            self.board[event_x - 1][event_y].type = TRASH
                    if event_x < self.dimension - 2 and not self.board[event_x + 1][event_y].is_priority():
                        if self.board[event_x + 1][event_y].is_spoiled():
                            self.board[event_x + 1][event_y].type = BONES_TRASH
                        else:
                            self.board[event_x + 1][event_y].type = TRASH
                    if event_y > 1 and not self.board[event_x][event_y - 1].is_priority():
                        if self.board[event_x][event_y - 1].is_spoiled():
                            self.board[event_x][event_y - 1].type = BONES_TRASH
                        else:
                            self.board[event_x][event_y - 1].type = TRASH
                    if event_y < self.dimension - 2 and not self.board[event_x][event_y + 1].is_priority():
                        if self.board[event_x][event_y + 1].is_spoiled():
                            self.board[event_x][event_y + 1].type = BONES_TRASH
                        else:
                            self.board[event_x][event_y + 1].type = TRASH


                # MONSTER
                event_occurred = randint(0, 99)
                if event_occurred < INSERT_PROBABILITY:
                    event_x = randint(1, self.dimension - 2)
                    event_y = randint(1, self.dimension - 2)
                    while not self.board[event_x][event_y].is_priority() and (
                                    self.agent.x == event_x and self.agent.y == event_y):
                        event_x = randint(1, self.dimension - 2)
                        event_y = randint(1, self.dimension - 2)
                    self.board[event_x][event_y].type = MONSTER

                    # Generate BONES around the MONSTER
                    if event_x > 1 and not self.board[event_x - 1][event_y].is_priority():
                        if self.board[event_x - 1][event_y].is_spoiled():
                            self.board[event_x - 1][event_y].type = BONES_TRASH
                        else:
                            self.board[event_x - 1][event_y].type = BONES
                    if event_x < self.dimension - 2 and not self.board[event_x + 1][event_y].is_priority():
                        if self.board[event_x + 1][event_y].is_spoiled():
                            self.board[event_x + 1][event_y].type = BONES_TRASH
                        else:
                            self.board[event_x + 1][event_y].type = BONES
                    if event_y > 1 and not self.board[event_x][event_y - 1].is_priority():
                        if self.board[event_x][event_y - 1].is_spoiled():
                            self.board[event_x][event_y - 1].type = BONES_TRASH
                        else:
                            self.board[event_x][event_y - 1].type = BONES
                    if event_y < self.dimension - 2 and not self.board[event_x][event_y + 1].is_priority():
                        if self.board[event_x][event_y + 1].is_spoiled():
                            self.board[event_x][event_y + 1].type = BONES_TRASH
                        else:
                            self.board[event_x][event_y + 1].type = BONES

    def new_dungeon(self):
        self.dimension += 1
        self.reset(self.dimension)
        pass
