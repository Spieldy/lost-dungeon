from Dungeon import *
from View import *

frame_count = 0
dungeon = Dungeon(10)
view = View(dungeon)
view.render()
view.root.mainloop()
