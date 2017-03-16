from Entity import *
from tkinter import *

TILE_SIZE = 64


class View(object):

    def __init__(self, dungeon):
        self.dungeon = dungeon
        self.root = Tk()
        self.root.wm_title('Lost Dungeon')
        size = self.dungeon.dimension * TILE_SIZE
        self.canvas = Canvas(self.root, width=size, height=size, background='#F4F1EB')
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
                self.canvas.create_image(x*TILE_SIZE, y*TILE_SIZE, image=self.sprite[self.dungeon.cell[x][y].type], anchor = 'nw')
        self.root.update()
