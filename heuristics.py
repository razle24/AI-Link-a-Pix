import math
import copy

colors_test = ['white', 'black', 'red']


def null_heuristic(state):
    return 0


def invalid_state(board, path):
    """
    checks if the board is valid. If not - returns -infinity. else - returns 0.
    :param path:
    :param board:
    :return:
    """
    # if path is not legal
    if not board.is_valid_path(path):
        return float('-inf')

    board_copy = copy.deepcopy(board)
    color = board.get_number_color_in_cell(path[0][0], path[0][1])
    board_copy.set_cells_coloring(path, color)

    numbered_cells = board_copy.numbered_cells
    for i, j in numbered_cells:
        if board_copy.is_colored_cell(i, j):
            continue
        if len(board_copy.get_possible_moves(i, j)) == 0:
            return float('-inf')
    return 0


def count_empty_cells(state):
    """
    counts the number of empty cells on the board
    :param state:
    :return:
    """
    return len([1 for i in range(state.board_h) for j in range(state.board_w) if not state.is_colored_cell(i, j)])


def mrv(state):
    pass


def lcv(state, action, successor):
    pass


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


heuristics = {"Null Heuristic": null_heuristic, "Invalid State Heuristic": invalid_state,
              "Count Empty Cells": count_empty_cells}
