from Dungeon import *
from View import *
import time

frame_count = 0
dungeon = Dungeon(5)
view = View(dungeon)

while True:
    frame_count += 1
    print(frame_count)
    view.render()
    time.sleep(1)
