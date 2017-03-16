from random import randint

EMPTY, WALL, EXIT, MONSTER, BONES, TRAP, TRASH, DEAD_MONSTER, HERO = range(9)


class Entity(object):

    def __init__(self):
        pass

    def __init__(self, entity_type):
        self.type = entity_type

'''
class EntityType(object):
    EMPTY = 0
    WALL = 1
    MONSTER = 2
    BONES = 3
    TRAP = 4
    TRASH = 5
    DEAD_MONSTER = 6
    EXIT = 7
'''