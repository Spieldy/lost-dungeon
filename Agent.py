from Entity import *

class Agent(object):

    def __init__(self, dimension):
        self.cell = [[Entity(EMPTY) for x in range(dimension)] for y in range(dimension)]
