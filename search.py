import util
import math
from variables import *
import itertools
FAILURE = 'Failure'
from gui import get_possable_paths


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


def set_domain_values(vars):
    for var in vars:
        var.domain = get_possable_paths(var.pos)


def get_vars(board):
    vars = []
    rows = board.board_h
    cols = board.board_w
    for i in range(rows):
        for j in range(cols):
            cur_var = Var((i, j), board.state[i][j][0], board.state[i][j][1])
            if board.state[i][j][0] != 0 and board.state[i][j][1] != 0:
                cur_var.head = True
            vars.append(cur_var)
    set_domain_values(vars)
    return vars


def csp(state, mrv=False, lcv=False):
    vars = get_vars(state)
    paths = []
    backtrack(vars, paths)


def get_var_by_pos(pos, vars):
    for var in vars:
        if var.pos == pos:
            return var
      
        
def get_pos_by_var(variable, vars):
    for index, var in enumerate(vars):
        if var == variable:
            return index


def is_path_legal(path, vars):
    for x, y in path[:-1]:
        if get_var_by_pos((x, y), vars).color != 0:
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
    for x, y in path[1:]:
        get_var_by_pos((x, y), vars).color = color


def uncolor_path(vars, path):
    """
    gets vars' array and a path, and colors it's coordinates in the right color.
    :param vars:
    :param path:
    :return: doesn't return anything, just updating the vars' array.
    """
    for x, y in path:
        var = get_var_by_pos((x, y), vars)
        # if not var.head:
        #     var.color = 0
        var.remove_value()


def backtrack(vars, paths):
    i = 0
    while 0 <= i < len(vars):
        if vars[i].color == 0:
            continue
        # get_value = all possible paths from var[i]
        path = get_value(vars, i)
        if path is None:
            # ?????
            if len(paths) == 0:
                return FAILURE
            path_to_del = paths.pop(-1)
            last_head = get_pos_by_var(path_to_del[0], vars)
            uncolor_path(vars, path_to_del)
            # vars[i].remove_value()
            i = last_head
        else:
            color_path(vars, path)
            paths += path
            i += 1
            # if i < len(vars):
            #     vars[i].remove_value()
    if i < 0:
        return FAILURE
    return vars


def get_value(vars, i):
    while len(vars[i].legalValues) > 0:
        value = vars[i].legalValues.pop(0)
        if is_path_legal(value, vars):
            return value
    return None
