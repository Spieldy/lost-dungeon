# All entity types and displayable tiles.
ENTITY_COUNT = 12
EMPTY, WALL, EXIT, MONSTER, BONES, TRAP, TRASH, BONES_TRASH, DEADMONSTER, HERO, FOG, TARGET = range(ENTITY_COUNT)


# Represents an actual cell for the dungeon. Not to be confused with Cell.
class Entity(object):

    def __init__(self):
        # type is either EMPTY, WALL, EXIT, MONSTER, TRAP (ie features that interact directly with the agent)
        self.type = EMPTY
        # type is either EMPTY, BONES, TRASH, or BONES_TRASH (ie features that interact with probabilities)
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

