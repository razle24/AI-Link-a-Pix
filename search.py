import copy

import util
from heuristics import invalid_state


def calc_board_cost(board):
    """
    calculates the number of colored cells in the board
    :param board: The current board
    """
    # borad_size = board.get_height() * board.get_width()
    return sum([1 for i in range(board.get_height()) for j in range(board.get_width())
                if not board.is_colored_cell(i, j)])


# *** A star *** #
def a_star_search(game, variable_selection, HeuristicClass):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    heuristic = HeuristicClass()
    explored = set()
    queue = util.PriorityQueue()
    queue.push(game.get_initial_board(), 0)

    while not queue.isEmpty():
        current_board = queue.pop()
        yield current_board

        if game.is_goal_state():
            yield current_board

        successor = get_successors(current_board)

        for next_board, next_path in successor:
            if next_board not in explored:
                total_cost = calc_board_cost(next_board) + heuristic.cost(next_board, next_path)
                if total_cost > float('-inf'):
                    queue.push(next_board, total_cost)

        explored.add(current_board)

    # yield None


def get_successors(board):
    """
    state: Search state

    For a given state, this should return a list of triples,
    (successor, action, stepCost), where 'successor' is a
    successor to the current state, 'action' is the action
    required to get there, and 'stepCost' is the incremental
    cost of expanding to that successor
    """
    successors = []
    numbered_cells = board.get_list_of_numbered_cells()

    for i, j in numbered_cells:
        paths = board.get_possible_moves(i, j)
        for path in paths:
            current_board = copy.copy(board)
            color = current_board.get_number_color_in_cell(path[0][0], path[0][1])
            current_board.set_cells_coloring(path, color)
            successors += [(current_board, path)]
    return successors


# *** BFS *** #
def breadth_first_search(game, variable_selection, heuristic):
    """
    Search the shallowest nodes in the search tree first.
    """
    explored = set()
    queue = util.Queue()
    queue.push(game.get_initial_board())

    while not queue.isEmpty():
        current_board = queue.pop()
        yield current_board

        if game.is_goal_state():
            yield current_board

        successor = get_successors(current_board)
        for next_board, next_path in successor:
            if next_board not in explored:
                queue.push(next_board)

        explored.add(current_board)

    # yield None


# *** DFS *** #
def depth_first_search(game, variable_selection, heuristic):
    """
    Search the shallowest nodes in the search tree first.
    """
    explored = set()
    stack = util.Stack()
    stack.push(game.get_initial_board())

    while not stack.isEmpty():
        current_board = stack.pop()
        yield current_board

        if game.is_goal_state():
            yield current_board

        successor = get_successors(current_board)
        for next_board, next_path in successor:
            if next_board not in explored:
                stack.push(next_board)

        explored.add(current_board)

    # yield None


# *** UCS *** #
def uniform_cost_search(game, variable_selection, heuristic):
    """
    Search the node of least total cost first.
    """
    explored = set()
    queue = util.PriorityQueue()
    queue.push(game.get_initial_board(), 0)

    while not queue.isEmpty():
        current_board = queue.pop()
        yield current_board

        if game.is_goal_state():
            yield current_board
        successor = get_successors(current_board)

        for next_board, next_path in successor:
            if next_board not in explored:
                total_cost = calc_board_cost(next_board)
                queue.push(next_board, total_cost)

        explored.add(current_board)

    # yield None


# *** CSP *** #
def csp(game, VariableSelectionClass, HeuristicClass):
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
    :param heuristic:
    :param game:
    :param variable_selection:
    :param board:
    :param heads:
    :param mrv:
    :param lcv:
    :return:
    """
    board = game.get_initial_board()
    variable_selection_object = VariableSelectionClass(board)
    heuristic_object = HeuristicClass(board)
    return backtrack(board, variable_selection_object, heuristic_object)


def backtrack(board, variable_selection, heuristic):
    x, y = variable_selection.next_coordinate(board)

    # Get list of all possible paths from the cell. sort next cell using variable selection and paths using heuristic
    paths = board.get_possible_moves(x, y)

    # variable_selection(board)
    if len(paths) > 1:
        paths.sort(key=lambda path: heuristic.cost(board, path), reverse=False)

    for path in paths:
        next_board = copy.copy(board)
        next_board.set_cells_coloring(path, board.get_number_color_in_cell(x, y))

        if not invalid_state(next_board):
            yield next_board, path, board.get_number_color_in_cell(x, y)
            done_board = backtrack(next_board, variable_selection, heuristic)
            if done_board is not None:
                yield from done_board

            # Return back the old board and the path we deleted
            yield board, path, 0

    # yield from None


search_dict = {
    "CSP": csp,
    'BFS': breadth_first_search,
    'DFS': depth_first_search,
    'UCS': uniform_cost_search,
    "A*": a_star_search
}
