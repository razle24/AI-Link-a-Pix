import util
import math
from variables import *
import itertools
FAILURE = 'Failure'
from board import *


class StateNode:
    """
    Fix problem with util.PriorityQueue which tried (and failed) to use '<' operator on a tuple.
    This class is basically the same tuple with overloaded '<' operator.
    """

    def __init__(self, state, actions):
        self.state = state
        self.actions = actions

    def __lt__(self, other):
        return self.state.score(0) < other.score(0)

    def __iter__(self):
        yield self.state
        yield self.actions


def a_star_search(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    i = 0
    explored = set()
    queue = util.PriorityQueue()

    # Contains 'state', 'total cost from start to state' and 'list of actions to the state'
    queue.push(StateNode(problem.get_start_state(), []), 0)

    while not queue.isEmpty():
        current, actions_to_current = queue.pop()

        if problem.is_goal_state(current):
            return actions_to_current

        for child_state, action, step_cost in problem.get_successors(current):
            if child_state not in explored:
                total_cost = step_cost + heuristic(child_state, problem)
                if total_cost != math.inf:
                    queue.push(StateNode(child_state, actions_to_current + [action]), total_cost)
        explored.add(current)
    return None


def set_domain_values(vars, board):
    for var in vars:
        domain = board.get_possible_paths(var.pos[0], var.pos[1])
        var.domain = domain
        # if domain is not None:
        #     if len(domain) > 600:
        #         print(var.pos)


def get_vars(board):
    vars = []
    rows = board.board_h
    cols = board.board_w
    for i in range(rows):
        for j in range(cols):
            cur_var = Var((i, j), board.state[i][j][0][0], board.state[i][j][0][1])
            if board.state[i][j][0] != (0, 0):
                cur_var.head = True
            vars.append(cur_var)
    set_domain_values(vars, board)
    return vars


def get_var_by_pos(pos, vars):
    for var in vars:
        if var.pos == pos:
            return var


def get_pos_by_var(var, coords):
    for index in range(len(coords)):
        if var.pos == coords[index].pos:
            return index


def is_path_legal(path, vars):
    if len(path) == 1:
        num = get_var_by_pos(path[0], vars).number
        is_head = get_var_by_pos(path[0], vars).head
        if num == 1 and is_head:
            return True

        return False

    for x, y in path:
        var = get_var_by_pos((x, y), vars)
        if get_var_by_pos((x, y), vars).colored:
            return False
    return True


def color_path(vars, path):
    """
    gets vars' array and a path, and colors it's coordinates in the right color.
    :param vars:
    :param path:
    :return: doesn't return anything, just updating the vars' array.
    """
    color = get_var_by_pos(path[0], vars).color
    for x, y in path:
        get_var_by_pos((x, y), vars).set_value(color)


def uncolor_path(vars, path, is_backtrack):
    """
    gets vars' array and a path, and colors it's coordinates in the right color.
    :param vars:
    :param path:
    :return: doesn't return anything, just updating the vars' array.
    """
    for x, y in path:
        var = get_var_by_pos((x, y), vars)
        var.remove_value(is_backtrack)


def mrv_heuristic(heads, vars):
    heads.sort(key=lambda x: x.number, reverse=False)


def lcv_heuristic(heads, vars):
    heads.sort(key=lambda x: len(x.domain), reverse=False)


def get_heads(heads, vars):
    heads_vars = []
    for x, y in heads:
        heads_vars.append(get_var_by_pos((x, y), vars))
    return heads_vars


def csp(state, heads, mrv=False, lcv=False):
    vars = get_vars(state)
    heads_vars = get_heads(heads, vars)
    paths = []
    if mrv:
        mrv_heuristic(heads_vars, vars)
    if lcv:
        lcv_heuristic(heads_vars, vars)
    backtrack(heads_vars, vars, paths, state.board_w)
    return vars


def backtrack(coords, vars, paths, cols):
    i = 0
    # j is the index for Vars instead of (i,j)
    j = (coords[i].pos[0] * cols) + coords[i].pos[1]
    is_backtrack = False
    # updates the legal paths through the domain
    vars[j].remove_value(is_backtrack)
    
    while 0 <= i < len(coords):
        # get_value = all possible paths from var[i]
        cur_coord = coords[i]
        # checks if we colored the cell and didn't backtrack
        if get_var_by_pos(cur_coord.pos, vars).colored and not is_backtrack:
            i += 1
            if i < len(coords):
                j = (coords[i].pos[0] * cols) + coords[i].pos[1]
                vars[j].remove_value(is_backtrack)
            continue
            
        path = get_value(vars, (coords[i].pos[0] * cols) + coords[i].pos[1])
        if path is None:
            is_backtrack = True
            # deletes last path we colored
            path_to_del = paths.pop(-1)
            uncolor_path(vars, path_to_del, is_backtrack)
            # yield path_to_del, 0
            # get back to the last cell of the last path we colored
            i = get_pos_by_var(get_var_by_pos(path_to_del[0], vars), coords)
        else:
            is_backtrack = False
            color_path(vars, path)
            # yield path, path[0][1]
            paths += [path]
            i += 1
            if i < len(coords):
                j = (coords[i].pos[0] * cols) + coords[i].pos[1]
                vars[j].remove_value(is_backtrack)
    if i < 0:
        return FAILURE
    return vars


def printVarBoard(vars, cols, rows):
    for i in range(rows):
        for j in range(cols):
            print(vars[i * cols + j].color, end="", flush=True)
            print(" ", end="", flush=True)
        print()


def get_value(vars, i):
    while len(vars[i].legal_paths) > 0:
        value = vars[i].legal_paths.pop(0)
        if is_path_legal(value, vars):
            return value
    return None


if __name__ == '__main__':
    mat = [[(1, 1), (7, 1), (0, 0), (1, 1), (1, 1)],
           [(4, 1), (1, 1), (0, 0), (0, 0), (7, 1)],
           [(0, 0), (0, 0), (4, 1), (0, 0), (0, 0)],
           [(1, 1), (4, 1), (0, 0), (5, 1), (1, 1)],
           [(3, 1), (4, 1), (0, 0), (0, 0), (5, 1)],
           [(0, 0), (4, 1), (0, 0), (0, 0), (0, 0)],
           [(3, 1), (9, 1), (0, 0), (0, 0), (0, 0)],
           [(0, 0), (0, 0), (4, 1), (5, 1), (0, 0)],
           [(0, 0), (0, 0), (0, 0), (9, 1), (5, 1)],
           [(1, 1), (1, 1), (0, 0), (0, 0), (1, 1)]]

    heads = [(0, 0), (0, 3), (0, 4), (1, 1), (3, 0), (3, 4), (9, 0), (9, 1), (9, 4), (4, 0), (6, 0),
             (1, 0), (2, 2), (3, 1), (4, 1), (5, 1), (7, 2), (3, 3), (4, 4), (7, 3), (8, 4), (0, 1),
             (1, 4), (6, 1), (8, 3)]

    board = Board(4, None, mat)
    csp(board, heads)
    # printVarBoard(vars, 5, 10)
