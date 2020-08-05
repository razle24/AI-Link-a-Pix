import math
import copy
from search import *

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

    board_copy = copy.copy(board)
    color = board.get_number_color_in_cell(path[0][0], path[0][1])
    board_copy.set_cells_coloring(path, color)

    numbered_cells = board_copy.numbered_cells
    for i, j in numbered_cells:
        if board_copy.is_colored_cell(i, j):
            continue
        if len(board_copy.get_possible_moves(i, j)) == 0:
            return float('-inf')
    return 0


def count_possible_paths(board, path):
    x, y = path[0]
    end_x, end_y = path[-1]
    
    if len(board.get_possible_moves(x, y)) != 0 and len(board.get_possible_moves(end_x, end_y)) != 0:
        return max(1/len(board.get_possible_moves(x, y)), 1/len(board.get_possible_moves(end_x, end_y)))
    return float('-inf')


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


# heuristics = {"Null Heuristic": null_heuristic, "Invalid State Heuristic": invalid_state,
#               "Count Empty Cells": count_empty_cells, "MRV": mrv_heuristic, "LCV": lcv_heuristic}
