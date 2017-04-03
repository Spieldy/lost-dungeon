UNKNOWN = -1


# Represents a cell for the mental model of the agent. Similar to Entity but with additional information
class Cell(object):

    def __init__(self, x, y):
        # Cell position
        self.x = x
        self.y = y
        # When the cell has been explored, these are the same contained in the dungeon entity (see Entity.py)
        self.type = UNKNOWN
        self.subtype = UNKNOWN
        # Probabilities for frontier cells
        self.monster_probability = 0.0
        self.trap_probability = 0.0
        self.clear_probability = 0.0
        # has the cell been shot by the agent?
        self.shot_down = False
        # Used for dijkstra
        self.distance = 999999
        self.previous = None

    def set_monster_probability(self, p):
        self.monster_probability = p
        self.clear_probability = 1.0 - (self.monster_probability + self.trap_probability)

    def set_trap_probability(self, p):
        self.trap_probability = p
        self.clear_probability = 1.0 - (self.monster_probability + self.trap_probability)
