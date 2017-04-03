from Entity import *
from Cell import *
from Dijkstra import *
from Logic import *


class Agent(object):

    def __init__(self, x, y, dungeon):
        # Position
        self.x = x
        self.y = y
        # Spawn position
        self.respawn_x = None
        self.respawn_y = None
        # Dungeon
        self.dungeon = dungeon
        # Mental representation of the dungeon. Contains everything known and deduced.
        self.cell = [[Cell(x, y) for y in range(dungeon.dimension)] for x in range(dungeon.dimension)]
        # Contains all cells at the edge of the explored area. Each of these cells contains probabilities on its content
        self.frontier = []
        # The frontier cell the agent wants to visit next.
        self.target_cell = self.cell[0][0]
        # This is absolutely useless
        self.score = (self.dungeon.dimension - 3) * 10
        # To display info on the last movement.
        self.status_message = 'Welcome!'

    # Main function called each step
    def update(self):
        self.act()
        self.observe()
        self.think()

    # Updates what the agent has explored and the list of frontier cells, and undergos current cell effect (death, exit)
    def observe(self):
        current_cell = self.cell[self.x][self.y]
        # Change known data on the current_cell if it was unexplored
        if current_cell.type == UNKNOWN:
            current_cell.type = self.dungeon.board[self.x][self.y].type
            current_cell.subtype = self.dungeon.board[self.x][self.y].subtype
            current_cell.set_monster_probability(0)
            current_cell.set_trap_probability(0)
            # Current cell is now explored

        # Update the frontier and consider adjacent walls explored
        if current_cell in self.frontier:
            self.frontier.remove(current_cell)
        for adj_cell in self.adjacent_cells(self.x, self.y):
            if self.dungeon.board[adj_cell.x][adj_cell.y].type == WALL:
                self.cell[adj_cell.x][adj_cell.y].type = WALL
                self.cell[adj_cell.x][adj_cell.y].subtype = EMPTY
            if current_cell.type != MONSTER and current_cell.type != TRAP:
                if (adj_cell.type == UNKNOWN) and (adj_cell not in self.frontier):
                    self.frontier.append(adj_cell)

        # Change agent state if it stepped on a special tile (dead or exit)
        if current_cell.type == TRAP or current_cell.type == MONSTER:
            self.respawn()
        if current_cell.type == EXIT:
            self.status_message = 'Exit found!'.format((self.dungeon.dimension - 2) * 10)
            self.score += (self.dungeon.dimension - 2) * 10
            self.dungeon.reset(self.dungeon.dimension + 1)
    # End observe()

    # Updates frontier cell probabilities, calculates known cells distance from current position,
    # and uses logic to find the target cell
    def think(self):
        self.update_probabilities()
        dijkstra(self)
        self.target_cell = get_target(self)
        if not self.target_cell:
            self.status_message = 'Stuck! Game over'

    # Acts on the environment, ie, either shoot or move
    def act(self):
        if self.target_cell:
            self.goto(self.target_cell)

    # Updates probabilities on the content of each cell based on heuristics.
    def update_probabilities(self):
        for cell in self.frontier:
            bones_count = 0
            trash_count = 0
            for adj_cell in self.adjacent_cells(cell.x, cell.y):

                # Check for 100% clear
                if adj_cell.subtype == EMPTY:
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
                            trash_count = 0
                        elif adj_cell.subtype == TRASH:
                            trash_count = 5
                            bones_count = 0
                        break

                # Count surrounding features
                if adj_cell.subtype == BONES:
                    bones_count += 1
                elif adj_cell.subtype == TRASH:
                    trash_count += 1
                elif adj_cell.subtype == BONES_TRASH:
                    trash_count += 1
                    bones_count += 1
            # End for adjacent cell

            # Update probabilities
            cell.set_monster_probability(bones_count * 0.2)
            cell.set_trap_probability(trash_count * 0.2)
            if cell.shot_down:
                cell.set_monster_probability(0)
        # End for frontier cell

    # Resets mental state when a new dungeon is generated
    def reset_knowledge(self):
        self.cell = [[Cell(x, y) for y in range(self.dungeon.dimension)] for x in range(self.dungeon.dimension)]
        self.frontier.clear()
        self.observe()
        self.think()

    # Returns a list of all existing adjacent cells to specified position
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

    # When the agent dies
    def respawn(self):
        self.score -= (self.dungeon.dimension - 2) * 10
        self.x = self.respawn_x
        self.y = self.respawn_y
        self.status_message = 'You died.'.format((self.dungeon.dimension - 2) * 10)

    # Processes the first move in the dijkstra path to target cell.
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

    # MOVE functions
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
