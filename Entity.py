from random import randint

ENTITY_COUNT = 12
EMPTY, WALL, EXIT, MONSTER, BONES, TRAP, TRASH, BONES_TRASH, DEADMONSTER, HERO, FOG, TARGET = range(ENTITY_COUNT)


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

