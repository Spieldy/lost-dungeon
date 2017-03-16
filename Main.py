from Dungeon import *
from View import *

frame_count = 0
dungeon = Dungeon(5)
view = View(dungeon)
view.render()
view.root.mainloop()
