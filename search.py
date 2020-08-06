import copy

import util
from heuristics import invalid_state


# *** A star *** #
def a_star_search(game, variable_selection, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    explored = set()
    queue = util.PriorityQueue()

    queue.push(game.get_initial_board(), 0)

    while not queue.isEmpty():
        current_board = queue.pop()
        yield current_board

        if game.is_goal_state():
            return current_board

        successor = get_successors(current_board)

        for next_board, next_path in successor:
            if next_board not in explored:
                total_cost = heuristic(next_board, next_path)
                if total_cost > float('-inf'):
                    queue.push(next_board, total_cost)

        explored.add(current_board)

    return None


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


# *** CSP *** #
def csp(game, variable_selection, heuristic):
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
    board = game.get_initial_board()
    return backtrack(board, 0, variable_selection, heuristic)


def backtrack(board, i, variable_selection, heuristic):
    x, y = variable_selection(board)

    # If cell is already colored (by path created earlier) move to next cell
    if board.is_colored_cell(x, y):
        # yield board, [(x, y)], board.get_number_color_in_cell(x, y)
        yield from backtrack(board, i + 1, variable_selection, heuristic)

    # Get list of all possible paths from the cell. sort next cell using variable selection and paths using heuristic
    paths = board.get_possible_moves(x, y)

    # variable_selection(board)
    if len(paths) > 1:
        paths.sort(key=lambda path: heuristic(board, path), reverse=True)

    for path in paths:
        next_board = copy.copy(board)
        next_board.set_cells_coloring(path, board.get_number_color_in_cell(x, y))

        if not invalid_state(next_board):
            yield next_board, path, board.get_number_color_in_cell(x, y)
            done_board = backtrack(next_board, i + 1, variable_selection, heuristic)
            if done_board is not None:
                yield from done_board

            # Return back the old board and the path we deleted
            yield board, path, 0


search_dict = {
    "CSP": csp,
    # 'BFS': bfs,
    # 'DFS': dfs,
    # 'UFC': ufc,
    "A*": a_star_search
}
