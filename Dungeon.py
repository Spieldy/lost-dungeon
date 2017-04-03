from Entity import *
from Agent import *
from random import randint

# Global variables defining generation probabilities
MONSTER_PROBABILITY = 30
TRAP_PROBABILITY = 30


# Contains the actual static dungeon state and generation logic.
class Dungeon(object):
    def __init__(self, dimension):
        self.dimension = dimension
        self.board = [[Entity(EMPTY, EMPTY) for x in range(dimension)] for y in range(dimension)]
        self.agent = Agent(1, 1, self)
        self.reset(dimension)

    # Generates a new room with specified size
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
        while self.board[self.agent.x][self.agent.y].type == EXIT:
            self.agent.x = randint(1, dimension - 2)
            self.agent.y = randint(1, dimension - 2)

        self.agent.respawn_x = self.agent.x
        self.agent.respawn_y = self.agent.y

        self.populate()
        self.agent.reset_knowledge()

    # Places monsters and traps
    def populate(self):
        for x in range(1, self.dimension-1):
            for y in range(1, self.dimension-1):

                # MONSTER
                if self.board[x][y].type == EMPTY and not (self.agent.x == x and self.agent.y == y):
                    event_occurred = randint(0, 99)
                    if event_occurred < MONSTER_PROBABILITY:
                        self.board[x][y].type = MONSTER
                        # Generate BONES around the MONSTER
                        self.board[x - 1][y].add_bones()
                        self.board[x + 1][y].add_bones()
                        self.board[x][y - 1].add_bones()
                        self.board[x][y + 1].add_bones()

                # TRAP
                if self.board[x][y].type == EMPTY and not (self.agent.x == x and self.agent.y == y):
                    event_occurred = randint(0, 99)
                    if event_occurred < TRAP_PROBABILITY:
                        self.board[x][y].type = TRAP
                        # Generate TRASH around the TRAP
                        self.board[x - 1][y].add_trash()
                        self.board[x + 1][y].add_trash()
                        self.board[x][y - 1].add_trash()
                        self.board[x][y + 1].add_trash()
