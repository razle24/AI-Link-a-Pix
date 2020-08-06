import math
import copy
from search import *

colors_test = ['white', 'black', 'red']


def null_heuristic(board=None, path=None):
    return 0


def invalid_state(board, path=None):
    """
    Checks if every uncolored cell has at least one valid path.
    :param path:
    :param board:
    :return: If board is valid - return 0, otherwise return '-infinity'
    """
    numbered_cells = board.numbered_cells
    for i, j in numbered_cells:
        if not board.is_colored_cell(i, j) and len(board.get_possible_moves(i, j)) == 0:
            return float('-inf')

    return 0


def count_possible_paths(board, path):
    x, y = path[0]
    end_x, end_y = path[-1]

    start_moves = board.get_possible_moves(x, y)
    if len(start_moves) == 0:
        return float('-inf')
    end_moves = board.get_possible_moves(end_x, end_y)
    if len(end_moves) == 0:
        return float('-inf')

    return max(1/len(board.get_possible_moves(x, y)), 1/len(board.get_possible_moves(end_x, end_y)))


def count_empty_cells(state):
    """
    counts the number of empty cells on the board
    :param state:
    :return:
    """
    return len([1 for i in range(state.board_h) for j in range(state.board_w) if not state.is_colored_cell(i, j)])


def stick_to_path_wall_heuristic(board, path):
    """
    returns the number of cells in the path that are closer to the walls of the board
    :param board:
    :param path:
    :return:
    """
    stick_to_walls = sum([1 for i, j in path if i == 0 or i == board.get_height() - 1 or
                          j == 0 or j == board.get_width() - 1])
    # stick_to_path = get_stick_to_path(board, path)
    stick_to_path = 0
    return stick_to_path + stick_to_walls


def get_stick_to_path(board, path):
    """
    gets a path and counts how many cells in it touches another colored path
    :param board:
    :param path:
    :return: the number of cells in the path that touches another colored path
    """
    counter = 0
    for x, y in path:
        flag = False
        if x + 1 < board.get_height():
            if board.is_colored_cell(x+1, y):
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
    return counter
        


def photo_recognition(state, action, successor):
    pass


def stick_to_same_color(state, action, successor):
    """
    heuristic 4
    :param state:
    :param action:
    :param successor:
    :return:
    """
    pass


def compact_path(state, action, successor):
    """
    heuristic 5
    :param state:
    :param action:
    :param successor:
    :return:
    """
    pass


def all_heuristics(state):
    pass


heuristics_dict = {
    "Null Heuristic": null_heuristic,
    "Count Empty Cells": count_empty_cells,
    "MRV": mrv_heuristic,
    "LCV": lcv_heuristic
}
