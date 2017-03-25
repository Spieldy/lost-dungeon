from Entity import *
from tkinter import *

TILE_SIZE = 64
WHITE = '#F4F1EB'
GREEN = '#2D9B7F'
RED = '#FE5B6E'
BLACK = '#2D2005'
info_font = ('FixedSys', 9)


class View(object):

    def __init__(self, dungeon):
        self.dungeon = dungeon
        self.root = Tk()
        self.root.wm_title('Lost Dungeon')
        self.root.bind('<Left>', self.left_key)
        self.root.bind('<Right>', self.right_key)
        self.root.bind('<Up>', self.up_key)
        self.root.bind('<Down>', self.down_key)

        self.root.bind('d', self.shoot_left_key)
        self.root.bind('g', self.shoot_right_key)
        self.root.bind('r', self.shoot_up_key)
        self.root.bind('f', self.shoot_down_key)




        self.dimension = self.dungeon.dimension
        size = self.dimension * TILE_SIZE

        # UI
        self.ui = Frame(self.root, background=GREEN)
        self.ui.pack(fill=BOTH)
        self.next = PhotoImage(file='sprites/next.gif')
        self.next_button = Button(self.ui, image=self.next, command=self.next_step, bd=0, highlightthickness=0)
        self.next_button.grid(row=0, column=0)
        self.info = Label(self.ui, text='Score:', padx=10, bg=GREEN, font=info_font)
        self.info.grid(row=0, column=1, columnspan=2)

        # Dungeon
        self.dungeon_canvas = Canvas(self.root, width=size, height=size, background=WHITE, highlightthickness=0)
        self.dungeon_canvas.pack()

        # Contains all the sprites, with second dimension containing explored version of the sprite
        self.sprite = [[PhotoImage() for x in range(2)] for y in range(ENTITY_COUNT)]
        self.load_sprites()

    def render(self):
        self.dungeon_canvas.delete('all')

        if self.dimension != self.dungeon.dimension:  # Dungeon has been generated to a new size
            self.dimension = self.dungeon.dimension
            size = self.dimension * TILE_SIZE
            self.dungeon_canvas.config(width=size, height=size)
            self.dungeon_canvas.pack()

        for y in range(self.dungeon.dimension):
            for x in range(self.dungeon.dimension):
                if self.dungeon.agent.cell[x][y].type >= 0:
                    explored = 1
                else:
                    explored = 0
                    self.dungeon_canvas.create_image(x * TILE_SIZE, y * TILE_SIZE,
                                                     image=self.sprite[EMPTY][0],
                                                     anchor='nw')
                    continue

                self.dungeon_canvas.create_image(x * TILE_SIZE, y * TILE_SIZE,
                                                 image=self.sprite[self.dungeon.board[x][y].type][explored], anchor='nw')
                if (self.dungeon.agent.x == x) and (self.dungeon.agent.y == y):
                    self.dungeon_canvas.create_image(x * TILE_SIZE, y * TILE_SIZE,
                                                     image=self.sprite[HERO][1], anchor='nw')

        for cell in self.dungeon.agent.frontier:
            pm = cell.monster_probability
            pt = cell.trap_probability
            pc = 1 - (cell.monster_probability + cell.trap_probability)
            cell_info = ''
            if pm >= 1.0:
                cell_info += 'MON'
            if pt >= 1.0:
                cell_info += 'TRA'
            if pc >= 1.0:
                cell_info += 'OK'
            self.dungeon_canvas.create_text(cell.x * TILE_SIZE + 8, cell.y * TILE_SIZE + TILE_SIZE / 2,
                                            text=cell_info, font=info_font, fill=RED, anchor=W)



    def next_step(self):
        self.dungeon.new_dungeon()
        self.render()

    def left_key(self, event):
        self.dungeon.agent.move_left()
        self.render()

    def right_key(self, event):
        self.dungeon.agent.move_right()
        self.render()

    def up_key(self, event):
        self.dungeon.agent.move_up()
        self.render()

    def down_key(self, event):
        self.dungeon.agent.move_down()
        self.render()

    def shoot_left_key(self, event):
        self.dungeon.agent.shoot_left()
        self.render()

    def shoot_right_key(self, event):
        self.dungeon.agent.shoot_right()
        self.render()

    def shoot_up_key(self, event):
        self.dungeon.agent.shoot_up()
        self.render()

    def shoot_down_key(self, event):
        self.dungeon.agent.shoot_down()
        self.render()


    def load_sprites(self):
        self.sprite[EMPTY][1] = PhotoImage(file='sprites/ground-ex.gif')
        self.sprite[EMPTY][0] = PhotoImage(file='sprites/ground-un.gif')
        self.sprite[WALL][1] = PhotoImage(file='sprites/wall-ex.gif')
        self.sprite[WALL][0] = PhotoImage(file='sprites/wall-un.gif')
        self.sprite[EXIT][1] = PhotoImage(file='sprites/exit-ex.gif')
        self.sprite[EXIT][0] = PhotoImage(file='sprites/exit-un.gif')
        self.sprite[MONSTER][1] = PhotoImage(file='sprites/monster-ex.gif')
        self.sprite[MONSTER][0] = PhotoImage(file='sprites/monster-un.gif')
        self.sprite[BONES][1] = PhotoImage(file='sprites/bones-ex.gif')
        self.sprite[BONES][0] = PhotoImage(file='sprites/bones-un.gif')
        self.sprite[TRAP][1] = PhotoImage(file='sprites/trap-ex.gif')
        self.sprite[TRAP][0] = PhotoImage(file='sprites/trap-un.gif')
        self.sprite[TRASH][1] = PhotoImage(file='sprites/trash-ex.gif')
        self.sprite[TRASH][0] = PhotoImage(file='sprites/trash-un.gif')
        self.sprite[BONES_TRASH][1] = PhotoImage(file='sprites/trashbones-ex.gif')
        self.sprite[BONES_TRASH][0] = PhotoImage(file='sprites/trashbones-un.gif')
        self.sprite[DEADMONSTER][1] = PhotoImage(file='sprites/monsterdead-ex.gif')
        self.sprite[DEADMONSTER][0] = PhotoImage(file='sprites/monsterdead-un.gif')
        self.sprite[HERO][1] = PhotoImage(file='sprites/hero.gif')
