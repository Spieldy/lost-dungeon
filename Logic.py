from Agent import *


# TODO agent goes on 100% trap and switches target after killing monster
# (Actually it's way more fucked than that)
def get_target(agent):
    if exist_safe(agent.frontier):
        target = get_closest_safe(agent.frontier)
    elif exist_worthy_monster(agent.frontier, agent):
        target = get_closest_monster(agent.frontier, agent)
    else:
        target = get_best_trap(agent.frontier)
    return target


def safe(cell):
    return cell.clear_probability >= 1.0


def monster(cell):
    return cell.monster_probability >= 1.0


def maybe_monster(cell):
    return 0.0 < cell.monster_probability < 1.0


def trap(cell):
    return cell.trap_probability >= 1.0


def maybe_trap(cell):
    return 0.0 < cell.trap_probability < 1.0


def lone(cell, agent):
    lone_cell = True
    for adj in agent.adjacent_cells(cell.x, cell.y):
        if adj.type == UNKNOWN:
            lone_cell = False
    return lone_cell


def worthy_monster(cell, agent):
    return not maybe_trap(cell) and maybe_monster(cell) or (monster(cell) and not lone(cell, agent))


def closer(cell, other):
    return cell.distance < other.distance


def safer_trap(cell, other):
    return cell.trap_probability <= other.trap_probability


def better_trap(cell, other):
    return maybe_trap(cell) and safer_trap(cell, other) and closer(cell, other)


def closest_safe(cell, frontier):
    for other in frontier:
        if safe(other) and closer(other, cell):
            return False
    return True


def closest_monster(cell, frontier, agent):
    for other in frontier:
        if worthy_monster(other, agent) and closer(other, cell):
            return False
    return True


def best_trap(cell, frontier):
    for other in frontier:
        if better_trap(other, cell):
            return False
    return True


def exist_safe(frontier):
    for cell in frontier:
        if safe(cell):
            return True
    return False


def exist_worthy_monster(frontier, agent):
    for cell in frontier:
        if worthy_monster(cell, agent):
            return True
    return False


def get_closest_safe(frontier):
    for cell in frontier:
        if closest_safe(cell, frontier):
            return cell
    return None


def get_closest_monster(frontier, agent):
    for cell in frontier:
        if closest_monster(cell, frontier, agent):
            return cell
    return None


def get_best_trap(frontier):
    for cell in frontier:
        if best_trap(cell, frontier):
            return cell
    return None
