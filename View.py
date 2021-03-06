from Entity import *
from tkinter import *

# Change these values to affect the interface
# Graphical size multiplier. Must be an integer.
SCALE = 2
# Allows moving the agent with arrow keys and shooting with RDFG
MANUAL_MODE = True
# Completely hides all unexplored cells
FOG_MODE = False
# Displays statistics on frontier cells, and highlights target cell
INFO_MODE = True


TILE_SIZE = 32 * SCALE
WHITE = '#F4F1EB'
GREEN = '#2D9B7F'
RED = '#FE5B6E'
BLACK = '#2D2005'
INFO_FONT = ('FixedSys', 10 * SCALE)


# Contains the graphical interface logic
class View(object):

    def __init__(self, dungeon):
        self.manual_mode = False

        self.dungeon = dungeon
        self.root = Tk()
        self.root.config(background=GREEN)
        self.root.wm_title('Lost Dungeon')

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

        if MANUAL_MODE:
            # Key binds
            self.root.bind('<Left>', self.left_key)
            self.root.bind('<Right>', self.right_key)
            self.root.bind('<Up>', self.up_key)
            self.root.bind('<Down>', self.down_key)
            self.root.bind('d', self.shoot_left_key)
            self.root.bind('g', self.shoot_right_key)
            self.root.bind('r', self.shoot_up_key)
            self.root.bind('f', self.shoot_down_key)
        self.root.bind('<space>', self.next_step)

        self.render()
        self.root.mainloop()

    def render(self):
        info_text = 'Score: {0}\n{1}'.format(self.dungeon.agent.score, self.dungeon.agent.status_message)
        self.info.config(text=info_text)
        self.dungeon_canvas.delete('all')

        # Dungeon has been generated to a new size
        if self.dimension != self.dungeon.dimension:
            self.dimension = self.dungeon.dimension
            size = self.dimension * TILE_SIZE
            self.dungeon_canvas.config(width=size, height=size)
            self.dungeon_canvas.pack()

        # Display each tile
        for y in range(self.dungeon.dimension):
            for x in range(self.dungeon.dimension):
                if self.dungeon.agent.cell[x][y].type >= 0:
                    explored = 1
                else:
                    explored = 0
                    if FOG_MODE:  # Display fog instead of tile
                        if not self.dungeon.board[x][y].type == WALL:
                            self.dungeon_canvas.create_image(x * TILE_SIZE, y * TILE_SIZE,
                                                             image=self.sprite[FOG][0],
                                                             anchor='nw')
                            continue
                # Display the cell type
                if not self.dungeon.board[x][y].type == EMPTY and not self.dungeon.board[x][y].type == DEADMONSTER:
                    self.dungeon_canvas.create_image(x * TILE_SIZE, y * TILE_SIZE,
                                                     image=self.sprite[self.dungeon.board[x][y].type][explored], anchor='nw')
                else:
                    self.dungeon_canvas.create_image(x * TILE_SIZE, y * TILE_SIZE,
                                                     image=self.sprite[self.dungeon.board[x][y].subtype][explored],
                                                     anchor='nw')
                if (self.dungeon.agent.x == x) and (self.dungeon.agent.y == y):
                    self.dungeon_canvas.create_image(x * TILE_SIZE, y * TILE_SIZE,
                                                     image=self.sprite[HERO][1], anchor='nw')

        # Display stats and target cell
        if INFO_MODE:
            for cell in self.dungeon.agent.frontier:
                pm = cell.monster_probability * 100
                pt = cell.trap_probability * 100
                pc = cell.clear_probability * 100 # 1 - (cell.monster_probability + cell.trap_probability)
                cell_info = ''
                if pm > 0:
                    cell_info += '{0:.0f}\n'.format(pm)
                else:
                    cell_info += ' -\n'
                if pt > 0:
                    cell_info += '{0:.0f}'.format(pt)
                else:
                    cell_info += ' -'
                # cell_info = 'M{0:.0f}\nT{1:.0f}'.format(pm, pt)
                if pm == 0 and pt == 0 and pc == 0:
                    cell_info = '???'
                if pm >= 100:
                    cell_info = 'MON'
                if pt >= 100:
                    cell_info = 'TRA'
                if pc >= 100:
                    cell_info = 'OK'
                self.dungeon_canvas.create_text(cell.x * TILE_SIZE + 4 * SCALE, cell.y * TILE_SIZE + TILE_SIZE / 2,
                                                text=cell_info, font=INFO_FONT, fill=WHITE, anchor=W)
            if self.dungeon.agent.target_cell:
                self.dungeon_canvas.create_image(self.dungeon.agent.target_cell.x * TILE_SIZE,
                                                 self.dungeon.agent.target_cell.y * TILE_SIZE,
                                                 image=self.sprite[TARGET][0], anchor=NW)

    # Key bind functions
    def next_step_button(self):
        self.dungeon.agent.update()
        self.render()

    def next_step(self, event):
        self.next_step_button()

    def left_key(self, event):
        self.dungeon.agent.move_left()
        self.dungeon.agent.observe()
        self.dungeon.agent.think()
        self.render()

    def right_key(self, event):
        self.dungeon.agent.move_right()
        self.dungeon.agent.observe()
        self.dungeon.agent.think()
        self.render()

    def up_key(self, event):
        self.dungeon.agent.move_up()
        self.dungeon.agent.observe()
        self.dungeon.agent.think()
        self.render()

    def down_key(self, event):
        self.dungeon.agent.move_down()
        self.dungeon.agent.observe()
        self.dungeon.agent.think()
        self.render()

    def shoot_left_key(self, event):
        self.dungeon.agent.shoot_left()
        self.dungeon.agent.observe()
        self.dungeon.agent.think()
        self.render()

    def shoot_right_key(self, event):
        self.dungeon.agent.shoot_right()
        self.dungeon.agent.observe()
        self.dungeon.agent.think()
        self.render()

    def shoot_up_key(self, event):
        self.dungeon.agent.shoot_up()
        self.dungeon.agent.observe()
        self.dungeon.agent.think()
        self.render()

    def shoot_down_key(self, event):
        self.dungeon.agent.shoot_down()
        self.dungeon.agent.observe()
        self.dungeon.agent.think()
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
