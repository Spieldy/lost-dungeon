from Entity import *
from tkinter import *

TILE_SIZE = 64
WHITE = '#F4F1EB'
GREEN = '#2D9B7F'
RED = '#FE5B6E'
BLACK = '#2D2005'


class View(object):

    def __init__(self, dungeon):
        self.dungeon = dungeon
        self.root = Tk()
        self.root.wm_title('Lost Dungeon')
        size = self.dungeon.dimension * TILE_SIZE - 2  # No idea why -2 but it removes a 2px wide border
        self.canvas = Canvas(self.root, width=size, height=size, background=GREEN)
        self.canvas.pack()

        self.sprite = [PhotoImage for x in range(9)]
        self.sprite[WALL] = PhotoImage(file='sprites/wall-ex.png')
        self.sprite[HERO] = PhotoImage(file='sprites/hero.png')
        self.sprite[EMPTY] = PhotoImage(file='sprites/ground-ex.png')
        self.sprite[EXIT] = PhotoImage(file='sprites/exit-ex.png')

    def render(self):
        self.canvas.delete('all')
        for y in range(self.dungeon.dimension):
            for x in range(self.dungeon.dimension):
                if (self.dungeon.x_agent == x) and (self.dungeon.y_agent == y):
                    self.canvas.create_image(x * TILE_SIZE, y * TILE_SIZE,
                                             image=self.sprite[HERO], anchor='nw')
                else:
                    self.canvas.create_image(x * TILE_SIZE, y * TILE_SIZE,
                                             image=self.sprite[self.dungeon.cell[x][y].type], anchor = 'nw')
        self.root.update()
