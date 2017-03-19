from Entity import *
UNKNOWN = -1


class Agent(object):

    def __init__(self, x, y, dungeon):
        self.x = x
        self.y = y
        self.dungeon = dungeon
        self.cell = [[Cell(x, y) for y in range(dungeon.dimension)] for x in range(dungeon.dimension)]
        self.frontier = []

    def update_knowledge(self):
        current_cell = self.cell[self.x][self.y]
        cell_type = self.dungeon.board[self.x][self.y].type
        current_cell.type = cell_type  # Current cell is now explored
        if current_cell in self.frontier:
            self.frontier.remove(current_cell)
        for adj_cell in self.adjacent_cells():
            if self.dungeon.board[adj_cell.x][adj_cell.y].type == WALL:
                self.cell[adj_cell.x][adj_cell.y].type = WALL
            if (adj_cell.type == UNKNOWN) and (adj_cell not in self.frontier):
                self.frontier.append(adj_cell)
            if cell_type == EMPTY:
                adj_cell.monster_probability = 0
                adj_cell.trap_probability = 0

    def move_right(self):
        if self.dungeon.board[self.x + 1][self.y].type != WALL:
            self.x += 1
            self.update_knowledge()

    def move_left(self):
        if self.dungeon.board[self.x - 1][self.y].type != WALL:
            self.x -= 1
            self.update_knowledge()

    def move_down(self):
        if self.dungeon.board[self.x][self.y + 1].type != WALL:
            self.y += 1
            self.update_knowledge()

    def move_up(self):
        if self.dungeon.board[self.x][self.y - 1].type != WALL:
            self.y -= 1
            self.update_knowledge()

    def reset(self):
        self.cell = [[Cell(x, y) for y in range(self.dungeon.dimension)] for x in range(self.dungeon.dimension)]
        self.frontier.clear()
        self.update_knowledge()

    def adjacent_cells(self):
        adjacent_cells = list()
        adjacent_cells.append(self.cell[self.x + 1][self.y])
        adjacent_cells.append(self.cell[self.x - 1][self.y])
        adjacent_cells.append(self.cell[self.x][self.y + 1])
        adjacent_cells.append(self.cell[self.x][self.y - 1])
        return adjacent_cells


class Cell(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = UNKNOWN
        self.monster_probability = -0.5
        self.trap_probability = -0.5
