from Entity import *
UNKNOWN = -1


class Agent(object):

    def __init__(self, x, y, dungeon):
        self.x = x
        self.y = y
        self.dungeon = dungeon
        self.cell = [[Cell(x, y) for x in range(dungeon.dimension)] for y in range(dungeon.dimension)]
        self.frontier = []

    def update_knowledge(self):
        cell_type = self.dungeon.cell[self.x][self.y].type
        self.cell[self.x][self.y].type = cell_type
        for cell in self.adjacent_cells():
            if cell_type == EMPTY:
                cell.monster_probability = 0
                cell.trap_probability = 0

    def reset(self):
        self.frontier.clear()

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
