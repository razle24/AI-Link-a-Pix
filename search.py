import copy
import math
from heuristics import *
import util
from board import Board

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


class Problem:
    """
    represents the problem we want to solve.
    """
    def __init__(self, board, goal_board, starting_point=(0, 0)):
        self.board = board
        self.goal_state = goal_board
        self.starting_point = starting_point
        self.expanded = 0
    
    # TODO - check if needed
    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return state == self.goal_state

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # # Note that for the search problem, there is only one player - #0
        # self.expanded = self.expanded + 1
        # numbered_cells = state.numbered_cells
        # for i, j in numbered_cells:
        #     paths = state.get_possible_moves(i, j)
        #     for path in paths:
        pass


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


def mrv_heuristic(board):
    """
    Sort the list by number value (from small to big)
    :param heads:
    :return:
    """
    board.numbered_cells.sort(key=lambda coord: board.get_number_in_cell(coord[0], coord[1]), reverse=False)


def lcv_heuristic(board):
    """
    Sort list by amount of possible paths
    :param heads:
    :param vars:
    :return:
    """
    board.numbered_cells.sort(key=lambda coord: len(board.get_possible_moves(coord[0], coord[1])), reverse=False)


def csp(board, heads, mrv=False, lcv=False):
    """
    Works as follows:
        state - Board state (what cells are filled and with what color). Since there are many invalid board states,
                we decided to search for paths instead of individual cells, skipping many invalid routes.
        goal state - Given Board which is filled correctly.
        variables - Cell (x,y) on the board. Some of them has color coded number.
        domain - Different paths from (x,y) in length of the cell's number.
        constraints -
            # Cell must be assigned only 1 color
            # Cell with number most be assigned the same color as the number.
            # Colored cell must be part of a path of given length (Path is connected in both sides with numbered cell).

        Search - We use backtracking to for the search. Each time we find a path for 2 numbered cells at a time.
                 So we skip many invalid states.

        variable selection - We can choose the order of the cells assignment by changing the order of 'heads'
        domain selection - Each path can be scored using heuristic and than ordered from best to worst.
                           We can also remove path that will cause inevitable failure (blocking a cell from
                           forming a path)
    :param board:
    :param heads:
    :param mrv:
    :param lcv:
    :return:
    """
    paths = []
    if mrv:
        mrv_heuristic(board)

    if lcv:
        lcv_heuristic(board)

    return backtrack(board, 0, heads)


def backtrack(board, i, numbered_cells):
    if i == len(numbered_cells):
        return board
    x, y = numbered_cells[i]
    if board.is_colored_cell(x, y):
        yield board, [(x, y)], board.get_number_color_in_cell(x, y)
        yield from backtrack(board, i + 1, numbered_cells)
    lcv_heuristic(board)
    paths = board.get_possible_paths(x, y)
    if len(paths) > 1:
        paths.sort(key=lambda path: count_possible_paths(board, path), reverse=True)
    for path in paths:
        end_x, end_y = path[-1]
        if board.is_valid_path(path):
            if invalid_state(board, path):
                continue

            next_board = copy.copy(board)
            next_board.set_cells_coloring(path, board.get_number_color_in_cell(x, y))

            yield next_board, path, board.get_number_color_in_cell(x, y)
            done_board = backtrack(next_board, i + 1, numbered_cells)
            if done_board is not None:
                yield from done_board
            yield board, path, 0


search_dict = {"CSP": csp, "A*": a_star_search}


#
# def backtrack(coords, board, paths):
#     i = 0
#     is_backtrack = False
#     # updates the legal paths through the domain
#     board.remove_value(coords[i][0], coords[i][1], is_backtrack)
#
#     while 0 <= i < len(coords):
#         # get_value = all possible paths from var[i]
#         cur_coord = coords[i]
#         # checks if we colored the cell and didn't backtrack
#         if cur_coord[1] and not is_backtrack:
#             i += 1
#             if i < len(coords):
#                 board.remove_value(coords[i][0], coords[i][1], is_backtrack)
#             continue
#         path = get_value(board, cur_coord)
#         if path is None:
#             is_backtrack = True
#             # deletes last path we colored
#             path_to_del = paths.pop(-1)
#             board.uncolor_path(path_to_del, is_backtrack)
#             # yield path_to_del, 0
#             # get back to the last cell of the last path we colored
#             i = board.get_pos_by_var(board.get_var_by_pos(path_to_del[0]), coords)
#         else:
#             is_backtrack = False
#             board.color_path(path)
#             # yield path, path[0][1]
#             paths += [path]
#             i += 1
#             if i < len(coords):
#                 board.remove_value(coords[i].pos[0], coords[i].pos[1], is_backtrack)
#     if i < 0:
#         return FAILURE
#
#
# def get_value(board, pos):
#     cell = board.get_var_by_pos(pos)
#     while len(cell.legal_paths) > 0:
#         path = cell.legal_paths.pop(0)
#         if board.is_path_legal(path):
#             return path
#     return None
