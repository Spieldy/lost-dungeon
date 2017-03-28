from Entity import *
UNKNOWN = -1


class Agent(object):

    def __init__(self, x, y, dungeon):
        self.x = x
        self.y = y
        self.respawn_x = None
        self.respawn_y = None
        self.dungeon = dungeon
        self.cell = [[Cell(x, y) for y in range(dungeon.dimension)] for x in range(dungeon.dimension)]
        self.frontier = []
        self.score = (self.dungeon.dimension - 3) * 10
        self.status_message = 'Welcome!'

    def update(self):
        self.update_knowledge()
        cell_type = self.dungeon.board[self.x][self.y].type
        if cell_type == TRAP or cell_type == MONSTER:
            self.respawn()
        if cell_type == EXIT:
            self.status_message = 'Exit found!'.format((self.dungeon.dimension - 2) * 10)
            self.score += (self.dungeon.dimension - 2) * 10
            self.dungeon.reset(self.dungeon.dimension + 1)

    def update_knowledge(self):
        current_cell = self.cell[self.x][self.y]
        cell_type = self.dungeon.board[self.x][self.y].type
        cell_subtype = self.dungeon.board[self.x][self.y].subtype
        current_cell.type = cell_type  # Current cell is now explored

        if current_cell in self.frontier:
            self.frontier.remove(current_cell)

        for adj_cell in self.adjacent_cells(self.x, self.y):
            if self.dungeon.board[adj_cell.x][adj_cell.y].type == WALL:
                self.cell[adj_cell.x][adj_cell.y].type = WALL
            if (adj_cell.type == UNKNOWN) and (adj_cell not in self.frontier):
                self.frontier.append(adj_cell)
            if cell_subtype == EMPTY:
                adj_cell.monster_probability = 0.0
                adj_cell.trap_probability = 0.0
            elif cell_subtype == BONES:
                adj_cell.monster_probability = 1.0
                adj_cell.trap_probability = 0.0
            elif cell_subtype == TRASH:
                adj_cell.monster_probability = 0.0
                adj_cell.trap_probability = 1.0

    def reset_knowledge(self):
        self.cell = [[Cell(x, y) for y in range(self.dungeon.dimension)] for x in range(self.dungeon.dimension)]
        self.frontier.clear()
        self.update_knowledge()

    def adjacent_cells(self, x, y):
        adjacent_cells = list()
        adjacent_cells.append(self.cell[x + 1][y])
        adjacent_cells.append(self.cell[x - 1][y])
        adjacent_cells.append(self.cell[x][y + 1])
        adjacent_cells.append(self.cell[x][y - 1])
        return adjacent_cells

    def respawn(self):
        self.score -= (self.dungeon.dimension - 2) * 10
        self.x = self.respawn_x
        self.y = self.respawn_y
        self.status_message = 'You died.'.format((self.dungeon.dimension - 2) * 10)

    # MOVE functions
    def move_right(self):
        if self.dungeon.board[self.x + 1][self.y].type != WALL:
            self.x += 1
            self.score -= 1
            self.update()

    def move_left(self):
        if self.dungeon.board[self.x - 1][self.y].type != WALL:
            self.x -= 1
            self.score -= 1
            self.update()

    def move_down(self):
        if self.dungeon.board[self.x][self.y + 1].type != WALL:
            self.y += 1
            self.score -= 1
            self.update()

    def move_up(self):
        if self.dungeon.board[self.x][self.y - 1].type != WALL:
            self.y -= 1
            self.score -= 1
            self.update()

    # SHOOT functions
    def shoot_right(self):
        self.score -= 10
        if self.dungeon.board[self.x + 1][self.y].type == MONSTER:
            self.dungeon.board[self.x + 1][self.y].type = DEADMONSTER
            self.update_knowledge()
        self.status_message = 'Shot rightward'

    def shoot_left(self):
        self.score -= 10
        if self.dungeon.board[self.x - 1][self.y].type == MONSTER:
            self.dungeon.board[self.x - 1][self.y].type = DEADMONSTER
            self.update_knowledge()
        self.status_message = 'Shot leftward'

    def shoot_down(self):
        self.score -= 10
        if self.dungeon.board[self.x][self.y + 1].type == MONSTER:
            self.dungeon.board[self.x][self.y + 1].type = DEADMONSTER
            self.update_knowledge()
        self.status_message = 'Shot downward'

    def shoot_up(self):
        self.score -= 10
        if self.dungeon.board[self.x][self.y - 1].type == MONSTER:
            self.dungeon.board[self.x][self.y - 1].type = DEADMONSTER
            self.update_knowledge()

        self.status_message = 'Shot upward'


class Cell(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = UNKNOWN
        self.monster_probability = -0.5
        self.trap_probability = -0.5
