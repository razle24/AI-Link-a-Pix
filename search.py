import util
import math
FAILURE = 'Failure'


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


def mrv_heuristic(heads):
    """
    Sort the list by number value (from small to big)
    :param heads:
    :return:
    """
    heads.sort(key=lambda x: x[0], reverse=False)


def lcv_heuristic(heads, board):
    """
    Sort list by amount of possible paths
    :param heads:
    :param vars:
    :return:
    """
    heads.sort(key=lambda x: len(x.domain), reverse=False)


def csp(board, heads, mrv=False, lcv=False):
    paths = []
    if mrv:
        mrv_heuristic(heads)
    # if lcv:
    #     lcv_heuristic(heads, board)
    backtrack(heads, board, paths)


def backtrack(coords, board, paths):
    i = 0
    is_backtrack = False
    # updates the legal paths through the domain
    board.remove_value(coords[i][0], coords[i][1], is_backtrack)
    
    while 0 <= i < len(coords):
        # get_value = all possible paths from var[i]
        cur_coord = coords[i]
        # checks if we colored the cell and didn't backtrack
        if cur_coord[1] and not is_backtrack:
            i += 1
            if i < len(coords):
                board.remove_value(coords[i][0], coords[i][1], is_backtrack)
            continue
        path = get_value(board, cur_coord)
        if path is None:
            is_backtrack = True
            # deletes last path we colored
            path_to_del = paths.pop(-1)
            board.uncolor_path(path_to_del, is_backtrack)
            # yield path_to_del, 0
            # get back to the last cell of the last path we colored
            i = board.get_pos_by_var(board.get_var_by_pos(path_to_del[0]), coords)
        else:
            is_backtrack = False
            board.color_path(path)
            # yield path, path[0][1]
            paths += [path]
            i += 1
            if i < len(coords):
                board.remove_value(coords[i].pos[0], coords[i].pos[1], is_backtrack)
    if i < 0:
        return FAILURE


def get_value(board, pos):
    cell = board.get_var_by_pos(pos)
    while len(cell.legal_paths) > 0:
        path = cell.legal_paths.pop(0)
        if board.is_path_legal(path):
            return path
    return None
