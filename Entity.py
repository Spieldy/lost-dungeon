from random import randint

ENTITY_COUNT = 10
EMPTY, WALL, EXIT, MONSTER, BONES, TRAP, TRASH, BONES_TRASH, DEADMONSTER, HERO = range(ENTITY_COUNT)


class Entity(object):

    def __init__(self):
        pass

    def __init__(self, entity_type):
        self.type = entity_type
