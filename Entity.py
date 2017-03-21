from random import randint

ENTITY_COUNT = 10
EMPTY, WALL, EXIT, MONSTER, BONES, TRAP, TRASH, BONES_TRASH, DEADMONSTER, HERO = range(ENTITY_COUNT)


class Entity(object):

    def __init__(self):
        self.type = EMPTY
        self.subtype = EMPTY
        pass

    def __init__(self, entity_type, entity_subtype):
        self.type = entity_type
        self.subtype = entity_subtype


