from Entity import *
from Dijkstra import *
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
        self.target_cell = self.cell[0][0]
        self.score = (self.dungeon.dimension - 3) * 10
        self.status_message = 'Welcome!'

    def update(self):
        # self.move()
        self.goto(self.target_cell)
        self.update_knowledge()
        self.update_probabilities()
        cell_type = self.dungeon.board[self.x][self.y].type
        if cell_type == TRAP or cell_type == MONSTER:
            self.respawn()
        if cell_type == EXIT:
            self.status_message = 'Exit found!'.format((self.dungeon.dimension - 2) * 10)
            self.score += (self.dungeon.dimension - 2) * 10
            self.dungeon.reset(self.dungeon.dimension + 1)
        self.take_decision()

    def move(self):
        if self.x < self.target_cell.x:
            self.move_right()
        elif self.x > self.target_cell.x:
            self.move_left()
        elif self.y < self.target_cell.y:
            self.move_down()
        else:
            self.move_up()

    def take_decision(self):
        if self.has_clear():
            self.find_closest_clear()

    def has_clear(self):
        for cell in self.frontier:
            if cell.clear_probability >= 1.0:
                return True
        return False

    def find_closest_clear(self):
        closest_distance = 999999
        for cell in self.frontier:
            if cell.clear_probability >= 1.0:
                distance = abs(cell.x - self.x) + abs(cell.y - self.y)
                if distance < closest_distance:
                    self.target_cell = cell
                    closest_distance = distance

    def update_probabilities(self):
        for cell in self.frontier:
            bones_count = 0
            trash_count = 0
            for adj_cell in self.adjacent_cells(cell.x, cell.y):
                if adj_cell.subtype == EMPTY:
                    cell.set_monster_probability(0.0)
                    cell.set_trap_probability(0.0)
                    bones_count = 0
                    trash_count = 0
                    break  # Cell is 100% clear

                if adj_cell.subtype == BONES:
                    bones_count += 1
                elif adj_cell.subtype == TRASH:
                    trash_count += 1
                elif adj_cell.subtype == BONES_TRASH:
                    trash_count += 1
                    bones_count += 1
            # End for adjacent cell

            cell.set_monster_probability(bones_count * 0.2)
            cell.set_trap_probability(trash_count * 0.2)
        # End for frontier cell

    def update_knowledge(self):
        current_cell = self.cell[self.x][self.y]
        current_cell.type = self.dungeon.board[self.x][self.y].type
        current_cell.subtype = self.dungeon.board[self.x][self.y].subtype  # Current cell is now explored

        if current_cell in self.frontier:
            self.frontier.remove(current_cell)

        for adj_cell in self.adjacent_cells(self.x, self.y):
            if self.dungeon.board[adj_cell.x][adj_cell.y].type == WALL:
                self.cell[adj_cell.x][adj_cell.y].type = WALL
                self.cell[adj_cell.x][adj_cell.y].type = EMPTY
            if current_cell.type != MONSTER and current_cell.type != TRAP:
                if (adj_cell.type == UNKNOWN) and (adj_cell not in self.frontier):
                    self.frontier.append(adj_cell)
                if current_cell.subtype == EMPTY:
                    adj_cell.set_monster_probability(0)

    def reset_knowledge(self):
        self.cell = [[Cell(x, y) for y in range(self.dungeon.dimension)] for x in range(self.dungeon.dimension)]
        self.frontier.clear()
        self.update_knowledge()
        self.take_decision()

    def adjacent_cells(self, x, y):
        adjacent_cells = list()
        if x + 1 < self.dungeon.dimension:
            adjacent_cells.append(self.cell[x + 1][y])
        if x - 1 >= 0:
            adjacent_cells.append(self.cell[x - 1][y])
        if y + 1 < self.dungeon.dimension:
            adjacent_cells.append(self.cell[x][y + 1])
        if y - 1 >= 0:
            adjacent_cells.append(self.cell[x][y - 1])
        return adjacent_cells

    def respawn(self):
        self.score -= (self.dungeon.dimension - 2) * 10
        self.x = self.respawn_x
        self.y = self.respawn_y
        self.status_message = 'You died.'.format((self.dungeon.dimension - 2) * 10)

    # MOVE functions
    def goto(self, cell):
        dijkstra(self)
        path = get_path(cell)
        print('{0},{1}'.format(path[0].x, path[0].y))
        dx = path[0].x - self.x
        dy = path[0].y - self.y

        if dx < 0:
            self.move_left()
        elif dx > 0:
            self.move_right()
        elif dy < 0:
            self.move_up()
        elif dy > 0:
            self.move_down()

    def move_right(self):
        if self.dungeon.board[self.x + 1][self.y].type != WALL:
            self.x += 1
            self.score -= 1

    def move_left(self):
        if self.dungeon.board[self.x - 1][self.y].type != WALL:
            self.x -= 1
            self.score -= 1

    def move_down(self):
        if self.dungeon.board[self.x][self.y + 1].type != WALL:
            self.y += 1
            self.score -= 1

    def move_up(self):
        if self.dungeon.board[self.x][self.y - 1].type != WALL:
            self.y -= 1
            self.score -= 1

    # SHOOT functions
    def shoot_right(self):
        self.score -= 10
        if self.dungeon.board[self.x + 1][self.y].type == MONSTER:
            self.dungeon.board[self.x + 1][self.y].type = DEADMONSTER
        self.status_message = 'Shot rightward'

    def shoot_left(self):
        self.score -= 10
        if self.dungeon.board[self.x - 1][self.y].type == MONSTER:
            self.dungeon.board[self.x - 1][self.y].type = DEADMONSTER
        self.status_message = 'Shot leftward'

    def shoot_down(self):
        self.score -= 10
        if self.dungeon.board[self.x][self.y + 1].type == MONSTER:
            self.dungeon.board[self.x][self.y + 1].type = DEADMONSTER
        self.status_message = 'Shot downward'

    def shoot_up(self):
        self.score -= 10
        if self.dungeon.board[self.x][self.y - 1].type == MONSTER:
            self.dungeon.board[self.x][self.y - 1].type = DEADMONSTER
        self.status_message = 'Shot upward'


class Cell(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = UNKNOWN
        self.subtype = UNKNOWN
        self.monster_probability = 0.0
        self.trap_probability = 0.0
        self.clear_probability = 0.0
        # Used for dijkstra
        self.distance = 999999
        self.previous = None

    def set_monster_probability(self, p):
        self.monster_probability = p
        self.clear_probability = 1.0 - (self.monster_probability + self.trap_probability)

    def set_trap_probability(self, p):
        self.trap_probability = p
        self.clear_probability = 1.0 - (self.monster_probability + self.trap_probability)
