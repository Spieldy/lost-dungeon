from Entity import *
from Cell import *
from Dijkstra import *
from Logic import *


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
        self.act()
        self.observe()
        self.think()

    # Updates what the agent has explored and the list of frontier cells, and undergos current cell effect (death, exit)
    def observe(self):
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

        if current_cell.type == TRAP or current_cell.type == MONSTER:
            self.respawn()
        if current_cell.type == EXIT:
            self.status_message = 'Exit found!'.format((self.dungeon.dimension - 2) * 10)
            self.score += (self.dungeon.dimension - 2) * 10
            self.dungeon.reset(self.dungeon.dimension + 1)

    # Updates frontier cell probabilities, calculates known cells distance from current position,
    # and uses logic to find the target cell
    def think(self):
        self.update_probabilities()
        dijkstra(self)
        self.take_decision()

    # Acts on the environment, ie, either shoot or move
    def act(self):
        if self.target_cell:
            self.goto(self.target_cell)

    def take_decision(self):
        if False:
            if self.has_clear():
                self.find_closest_clear()
            elif self.has_monster():
                self.find_closest_monster()
            else:
                self.find_lowest_trap()
        self.target_cell = get_target(self)

        if not self.target_cell:
            self.status_message = 'Stuck! Game over'

    def has_clear(self):
        for cell in self.frontier:
            if cell.clear_probability >= 1.0:
                return True
        return False

    def has_monster(self):
        for cell in self.frontier:
            if cell.monster_probability > 0.0 and cell.trap_probability <= 0.0:
                for adj in self.adjacent_cells(cell.x, cell.y):
                    if adj.type == UNKNOWN:  # TODO should not go only if lone AND 100% monster
                        return True
        return False

    def find_closest_monster(self):
        closest_distance = INFINITY
        for cell in self.frontier:
            if cell.monster_probability > 0.0 and cell.trap_probability <= 0.0:
                lone_cell = True
                for adj in self.adjacent_cells(cell.x, cell.y):
                    if adj.type == UNKNOWN:
                        lone_cell = False
                if cell.distance < closest_distance and not lone_cell:
                    self.target_cell = cell
                    closest_distance = cell.distance

    def find_closest_clear(self):
        closest_distance = INFINITY
        for cell in self.frontier:
            if cell.clear_probability >= 1.0:
                if cell.distance < closest_distance:
                    self.target_cell = cell
                    closest_distance = cell.distance

    def find_lowest_trap(self):
        lowest_probability = 0.99
        self.target_cell = None
        closest_distance = INFINITY
        for cell in self.frontier:
            if cell.trap_probability < lowest_probability:
                self.target_cell = cell
                lowest_probability = cell.trap_probability
                closest_distance = cell.distance
            if cell.trap_probability == lowest_probability and cell.distance < closest_distance:
                self.target_cell = cell
                closest_distance = cell.distance

    def update_probabilities(self):
        for cell in self.frontier:
            bones_count = 0
            trash_count = 0
            for adj_cell in self.adjacent_cells(cell.x, cell.y):
                if adj_cell.subtype == EMPTY:  # Cell is 100% clear
                    cell.set_monster_probability(0.0)
                    cell.set_trap_probability(0.0)
                    bones_count = 0
                    trash_count = 0
                    break

                # Check for 100% danger
                if adj_cell.type != UNKNOWN:
                    explored_count = 0
                    for c in self.adjacent_cells(adj_cell.x, adj_cell.y):
                        if c.type == EMPTY:
                            explored_count += 1
                    if explored_count >= 3:
                        if adj_cell.subtype == BONES:
                            bones_count = 5
                        elif adj_cell.subtype == TRASH:
                            trash_count = 5
                        break

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

            if cell.shot_down:
                cell.set_monster_probability(0)
            if cell.monster_probability == 0 and self.dungeon.board[cell.x][cell.y].type == MONSTER:
                print("OOPS")
        # End for frontier cell

    def reset_knowledge(self):
        self.cell = [[Cell(x, y) for y in range(self.dungeon.dimension)] for x in range(self.dungeon.dimension)]
        self.frontier.clear()
        self.observe()
        self.think()

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
        path = get_path(cell)
        dx = path[0].x - self.x
        dy = path[0].y - self.y
        monster = path[0].monster_probability > 0 or path[0].type == MONSTER

        if dx < 0:
            if monster:
                self.shoot_left()
            else:
                self.move_left()
        elif dx > 0:
            if monster:
                self.shoot_right()
            else:
                self.move_right()
        elif dy < 0:
            if monster:
                self.shoot_up()
            else:
                self.move_up()
        elif dy > 0:
            if monster:
                self.shoot_down()
            else:
                self.move_down()

    def move_right(self):
        if self.dungeon.board[self.x + 1][self.y].type != WALL:
            self.x += 1
            self.score -= 1
            self.status_message = 'Move right'

    def move_left(self):
        if self.dungeon.board[self.x - 1][self.y].type != WALL:
            self.x -= 1
            self.score -= 1
            self.status_message = 'Move left'

    def move_down(self):
        if self.dungeon.board[self.x][self.y + 1].type != WALL:
            self.y += 1
            self.score -= 1
            self.status_message = 'Move down'

    def move_up(self):
        if self.dungeon.board[self.x][self.y - 1].type != WALL:
            self.y -= 1
            self.score -= 1
            self.status_message = 'Move up'

    # SHOOT functions
    def shoot_right(self):
        self.score -= 10
        if self.dungeon.board[self.x + 1][self.y].type == MONSTER:
            self.dungeon.board[self.x + 1][self.y].type = DEADMONSTER
        self.cell[self.x + 1][self.y].shot_down = True
        self.status_message = 'Shot rightward'

    def shoot_left(self):
        self.score -= 10
        if self.dungeon.board[self.x - 1][self.y].type == MONSTER:
            self.dungeon.board[self.x - 1][self.y].type = DEADMONSTER
        self.cell[self.x - 1][self.y].shot_down = True
        self.status_message = 'Shot leftward'

    def shoot_down(self):
        self.score -= 10
        if self.dungeon.board[self.x][self.y + 1].type == MONSTER:
            self.dungeon.board[self.x][self.y + 1].type = DEADMONSTER
        self.cell[self.x][self.y + 1].shot_down = True
        self.status_message = 'Shot downward'

    def shoot_up(self):
        self.score -= 10
        if self.dungeon.board[self.x][self.y - 1].type == MONSTER:
            self.dungeon.board[self.x][self.y - 1].type = DEADMONSTER
        self.cell[self.x][self.y - 1].shot_down = True
        self.status_message = 'Shot upward'
