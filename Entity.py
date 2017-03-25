from random import randint

ENTITY_COUNT = 11
EMPTY, WALL, EXIT, MONSTER, BONES, TRAP, TRASH, BONES_TRASH, DEADMONSTER, HERO, FOG = range(ENTITY_COUNT)


class Entity(object):

    def __init__(self):
        self.type = EMPTY
        self.subtype = EMPTY
        pass

    def __init__(self, entity_type, entity_subtype):
        self.type = entity_type
        self.subtype = entity_subtype

    def add_trash(self):
        if self.subtype == BONES or self.subtype == BONES_TRASH:
            self.subtype = BONES_TRASH
        else:
            self.subtype = TRASH

    def add_bones(self):
        if self.subtype == TRASH or self.subtype == BONES_TRASH:
            self.subtype = BONES_TRASH
        else:
            self.subtype = BONES

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

