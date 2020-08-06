def mrv(board):
    """
    Sort the list by number value (from small to big)
    :param board: board object
    :return: doesn't return anything. Sorts the numbered_cells list in the board.
    """
    board.numbered_cells.sort(key=lambda coord: board.get_number_in_cell(coord[0], coord[1]), reverse=False)


def lcv(board):
    """
    Sort list by amount of possible paths
    :param board:
    :return:
    """
    board.numbered_cells.sort(key=lambda coord: len(board.get_possible_moves(coord[0], coord[1])), reverse=False)


def random_variable_selection(board):
    pass


variable_selection_dict = {
    "MRV": mrv,
    "LCV": lcv,
    "Random selection": random_variable_selection
}