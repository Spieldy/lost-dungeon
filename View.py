from Entity import *
from tkinter import *

SCALE = 1
MANUAL_MODE = False
FOG_MODE = False
INFO_MODE = True

TILE_SIZE = 32 * SCALE
WHITE = '#F4F1EB'
GREEN = '#2D9B7F'
RED = '#FE5B6E'
BLACK = '#2D2005'
INFO_FONT = ('FixedSys', 10 * SCALE)


class View(object):

    def __init__(self, dungeon):
        self.manual_mode = False

        self.dungeon = dungeon
        self.root = Tk()
        self.root.config(background=GREEN)
        self.root.wm_title('Lost Dungeon')
        if MANUAL_MODE:
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
        self.next = self.next.zoom(SCALE)
        self.next_button = Button(self.ui, image=self.next, command=self.next_step_button, bd=0, highlightthickness=0)
        self.next_button.grid(row=0, column=0)
        self.info = Label(self.ui, text='', padx=1 * SCALE, pady=0, bg=GREEN, font=INFO_FONT, fg=BLACK, justify=LEFT)
        self.info.grid(row=0, column=1, columnspan=2)

        # Dungeon
        self.dungeon_canvas = Canvas(self.root, width=size, height=size, background=WHITE, highlightthickness=0)
        self.dungeon_canvas.pack()

        # Contains all the sprites, with second dimension containing explored version of the sprite
        self.sprite = [[PhotoImage() for x in range(2)] for y in range(ENTITY_COUNT)]
        self.load_sprites()

        self.root.bind('<space>', self.next_step)

    def render(self):
        info_text = 'Score: {0}\n{1}'.format(self.dungeon.agent.score, self.dungeon.agent.status_message)
        self.info.config(text=info_text)
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
                    if FOG_MODE:
                        if not self.dungeon.board[x][y].type == WALL:
                            self.dungeon_canvas.create_image(x * TILE_SIZE, y * TILE_SIZE,
                                                             image=self.sprite[FOG][0],
                                                             anchor='nw')
                            continue

                if not self.dungeon.board[x][y].type == EMPTY:
                    self.dungeon_canvas.create_image(x * TILE_SIZE, y * TILE_SIZE,
                                                     image=self.sprite[self.dungeon.board[x][y].type][explored], anchor='nw')
                else:
                    self.dungeon_canvas.create_image(x * TILE_SIZE, y * TILE_SIZE,
                                                     image=self.sprite[self.dungeon.board[x][y].subtype][explored],
                                                     anchor='nw')
                if (self.dungeon.agent.x == x) and (self.dungeon.agent.y == y):
                    self.dungeon_canvas.create_image(x * TILE_SIZE, y * TILE_SIZE,
                                                     image=self.sprite[HERO][1], anchor='nw')

        if INFO_MODE:
            for cell in self.dungeon.agent.frontier:
                pm = cell.monster_probability
                pt = cell.trap_probability
                pc = cell.clear_probability  # 1 - (cell.monster_probability + cell.trap_probability)
                cell_info = '{0:.1f}'.format(pt + pm)
                if pm == 0 and pt == 0 and pc == 0:
                    cell_info = '???'
                if pm >= 1.0:
                    cell_info = 'MON'
                if pt >= 1.0:
                    cell_info = 'TRA'
                if pc >= 1.0:
                    cell_info = 'OK!'
                self.dungeon_canvas.create_text(cell.x * TILE_SIZE + 4 * SCALE, cell.y * TILE_SIZE + TILE_SIZE / 2,
                                                text=cell_info, font=INFO_FONT, fill=RED, anchor=W)
            self.dungeon_canvas.create_image(self.dungeon.agent.target_cell.x * TILE_SIZE,
                                             self.dungeon.agent.target_cell.y * TILE_SIZE, image=self.sprite[TARGET][0], anchor=NW)

    def next_step_button(self):
        self.dungeon.agent.update()
        self.render()

    def next_step(self, event):
        self.next_step_button()

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
        self.sprite[FOG][0] = PhotoImage(file='sprites/fog.gif')
        self.sprite[TARGET][0] = PhotoImage(file='sprites/target.gif')

        for sprite in self.sprite:
            sprite[0] = sprite[0].zoom(SCALE)
            sprite[1] = sprite[1].zoom(SCALE)
