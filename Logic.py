from Agent import *

# Contains logical rules to determine the best cell to explore next.


# is the cell 100% clear of danger?
def safe(cell):
    return cell.clear_probability >= 1.0


# is the cell 100% a monster?
def monster(cell):
    return cell.monster_probability >= 1.0


# is the cell maybe a monster, but not 100%?
def maybe_monster(cell):
    return 0.01 < cell.monster_probability < 0.99


# is the cell 100% a trap?
def trap(cell):
    return cell.trap_probability >= 1.0


# is the cell maybe a trap, but not 100%?
def maybe_trap(cell):
    return 0.01 < cell.trap_probability < 0.99


# is the cell surrounded by already explored cells?
def lone(cell, agent):
    lone_cell = True
    for adj in agent.adjacent_cells(cell.x, cell.y):
        if adj.type == UNKNOWN:
            lone_cell = False
    return lone_cell


# does the cell contain only a chance of monster (no trap), and is it not surrounded by explored cells?
def worthy_monster(cell, agent):
    return not maybe_trap(cell) and not trap(cell) and (maybe_monster(cell) or (monster(cell) and not lone(cell, agent)))


# is cell closer to the agent than other?
def closer(cell, other):
    return cell.distance < other.distance


# does cell have stricly less chance of containing a trap than other?
def safer_trap(cell, other):
    return cell.trap_probability < other.trap_probability


# do both cell and other have the same trap chance?
def as_safe_trap(cell, other):
    return cell.trap_probability == other.trap_probability


# is cell either stricly safer, or as safe and closer than other? also cell is not a 100% trap.
def better_trap(cell, other):
    return not trap(cell) and (safer_trap(cell, other) or (as_safe_trap(cell, other) and closer(cell, other)))


# is cell the closest clear cell in the frontier?
def closest_safe(cell, frontier):
    for other in frontier:
        if not safe(cell) or (safe(other) and closer(other, cell)):
            return False
    return True


# is cell the closest worthy monster in the frontier?
def closest_monster(cell, frontier, agent):
    for other in frontier:
        if not worthy_monster(cell, agent) or worthy_monster(other, agent) and closer(other, cell):
            return False
    return True


# is cell the closest, safest trap in the frontier?
def best_trap(cell, frontier):
    for other in frontier:
        if better_trap(other, cell):
            return False
    return True


# is there a single clear cell in the frontier?
def exist_safe(frontier):
    for cell in frontier:
        if safe(cell):
            return True
    return False


# is there a single worthy monster in the frontier?
def exist_worthy_monster(frontier, agent):
    for cell in frontier:
        if worthy_monster(cell, agent):
            return True
    return False


# not logic. Returns the closest clear cell in the frontier.
def get_closest_safe(frontier):
    for cell in frontier:
        if closest_safe(cell, frontier):
            return cell
    return None


# not logic. Returns the closest worthy monster in the frontier.
def get_closest_monster(frontier, agent):
    for cell in frontier:
        if closest_monster(cell, frontier, agent):
            return cell
    return None


# not logic. Returns the safest, closest trap in the frontier.
def get_best_trap(frontier):
    for cell in frontier:
        if best_trap(cell, frontier):
            return cell
    return None


# Finds the best target cell for agent using all functions above.
def get_target(agent):
    if exist_safe(agent.frontier):
        agent.status_message = 'Target: safe'
        target = get_closest_safe(agent.frontier)
    elif exist_worthy_monster(agent.frontier, agent):
        agent.status_message = 'Target: monster'
        target = get_closest_monster(agent.frontier, agent)
    else:
        agent.status_message = 'Target: trap'
        target = get_best_trap(agent.frontier)
    return target
