UNKNOWN = -1


class Cell(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = UNKNOWN
        self.subtype = UNKNOWN
        self.monster_probability = 0.0
        self.trap_probability = 0.0
        self.clear_probability = 0.0
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
