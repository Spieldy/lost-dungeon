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

    def is_priority(self):
        temp = False
        if self.type == EXIT or self.type == MONSTER or self.type == TRAP or self.type == WALL:
            temp = True
        return temp

    def is_spoiled(self):
        temp = False
        if self.subtype == TRASH or self.subtype == BONES:
            temp = True
        return temp

    def is_type_empty(self):
        temp = False
        if self.type == EMPTY:
            temp = True
        return temp

    def is_subtype_empty(self):
        temp = False
        if self.subtype == EMPTY:
            temp = True
        return temp

