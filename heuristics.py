# ** Used every time ** #
def invalid_state(board, path=None):
    """
    A heuristic function that estimates the cost of the current board.
    Checks if the board is valid.
    :param path: The current path we want to color
    :param board: The current board
    :return: -infinity if the board is not valid,  else - 0.
    """
    numbered_cells = board.get_list_of_numbered_cells()

    for i, j in numbered_cells:
        if not board.is_colored_cell(i, j) and len(board.get_possible_moves(i, j)) == 0:
            return float('-inf')

    return 0


# ** Selected by user ** #
def null_heuristic(board=None, path=None):
    """
    A heuristic function that estimates the cost of the current board. This heuristic is trivial.
    :param board:
    :param path:
    :return: 0 for every board
    """
    return 0


def count_possible_paths(board, path):
    x, y = path[0]
    end_x, end_y = path[-1]

    start_moves = board.get_possible_moves(x, y)
    if len(start_moves) == 0:
        return float('inf')
    end_moves = board.get_possible_moves(end_x, end_y)
    if len(end_moves) == 0:
        return float('inf')

    return (-1) * max(1 / len(board.get_possible_moves(x, y)), 1 / len(board.get_possible_moves(end_x, end_y)))


def count_empty_cells(board, path=None):
    """
    A heuristic function that estimates the cost of the current board.
    Counts the number of empty cells on the board.
    :param board: The current board
    :return: The number of empty cells on the board.
    """
    return len([1 for i in range(board.get_height()) for j in range(board.get_width())
                if not board.is_colored_cell(i, j)])


def stick_to_wall(board, path):
    """
    A heuristic function that estimates the cost of the current board.
    Counts the number of cells in the path that are closer to the walls of the board.
    :param path: The current path we want to color
    :param board: The current board
    :return: The number of cells in the path that are closer to the walls of the board
    """
    return (-1) * sum([1 for i, j in path if i == 0 or i == board.get_height() - 1
                or j == 0 or j == board.get_width() - 1]) + 1


def stick_to_path(board, path):
    """
    A heuristic function that estimates the cost of the current board.
    Counts how many cells in the path touches another colored path
    :param path: The current path we want to color
    :param board: The current board
    :return: The number of cells in the path that touches another colored path
    """
    counter = 0
    for x, y in path:
        flag = False
        if x + 1 < board.get_height():
            if board.is_colored_cell(x + 1, y):
                flag = True
        if x - 1 >= 0:
            if board.is_colored_cell(x - 1, y):
                flag = True
        if y + 1 < board.get_width():
            if board.is_colored_cell(x, y + 1):
                flag = True
        if y - 1 >= 0:
            if board.is_colored_cell(x, y - 1):
                flag = True
        if flag:
            counter += 1
    return (-1) * (counter + 1)


def stick_to_path_or_wall(board, path):
    return max(stick_to_wall(board, path), stick_to_path(board, path))

# def photo_recognition(board, action, successor):
#     pass


# def stick_to_same_color(board, action, successor):
#     """
#     heuristic 4
#     :param state:
#     :param action:
#     :param successor:
#     :return:
#     """
#     pass
#
#
# def compact_path(board, action, successor):
#     """
#     heuristic 5
#     :param state:
#     :param action:
#     :param successor:
#     :return:
#     """
#     pass


def all_heuristics(board, path):
    """
    A heuristic function that estimates the cost of the current board.
    Combines different heuristics in different weights
    :param path:
    :param board: The current board
    :return: The linear combination of all the heuristics used
    """
    return 0.5 * count_empty_cells(board) + 10 * stick_to_wall(board, path) + 5 * stick_to_path(board, path) +\
           count_possible_paths(board, path) + 15 * stick_to_path_or_wall(board, path)


heuristics_dict = {
    "Null heuristic": null_heuristic,
    "Count possible paths": count_possible_paths,
    "Stick to walls": stick_to_wall,
    "Stick to other paths": stick_to_path,
    # "Count empty cells": count_empty_cells,
    "Stick to path or wall": stick_to_path_or_wall,
    'Linear combination': all_heuristics
}
