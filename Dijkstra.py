from Agent import *

INFINITY = 999999


# Dijkstra algorithmn to find the shortest path to each cell the agent has explored or is in the frontier.
def dijkstra(agent):  # TODO agent can move through the frontier
    queue = []

    for x in range(agent.dungeon.dimension):
        for y in range(agent.dungeon.dimension):
            t = agent.cell[x][y].type
            #  Only include explored and safe cells, as well as frontier cells in the dijkstra queue
            if (t != -1 and t != MONSTER and t != TRAP and t != WALL) or agent.cell[x][y] in agent.frontier:
                queue.append(agent.cell[x][y])
                agent.cell[x][y].distance = INFINITY
                agent.cell[x][y].previous = None

    agent.cell[agent.x][agent.y].distance = 0

    while queue:
        cell = min_dist(queue)
        queue.remove(cell)
        if cell not in agent.frontier:  # prevents passing through the frontier to get to any other cell
            for neighbour in agent.adjacent_cells(cell.x, cell.y):
                if neighbour in queue:
                    alt = cell.distance + 1
                    if alt < neighbour.distance:
                        neighbour.distance = alt
                        neighbour.previous = cell
    agent.cell[agent.x][agent.y].previous = None


# Get the path to the specified cell after dijkstra has been called
def get_path(cell):
    path = []
    previous = cell
    while previous:
        path.insert(0, previous)
        previous = previous.previous
    return path[1:]


# Finds the closest cell in the dijkstra queue
def min_dist(queue):
    mini = INFINITY
    min_cell = queue[0]
    for cell in queue:
        if cell.distance < mini:
            min_cell = cell
            mini = cell.distance
    return min_cell
