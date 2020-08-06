from random import sample


def top_to_bottom(board):
    for x, y in board.get_list_of_numbered_cells():
        if not board.is_colored_cell(x, y):
            return x, y


def mrv(board):
    """
    Sort the list by number value (from small to big)
    :param board: board object
    :return: doesn't return anything. Sorts the numbered_cells list in the board.
    """
    list = sorted(board.get_list_of_numbered_cells(),
                  key=lambda coord: board.get_number_in_cell(coord[0], coord[1]), reverse=False)

    for x, y in list:
        if not board.is_colored_cell(x, y):
            return x, y


def lcv(board):
    """
    Sort list by amount of possible paths
    :param board:
    :return:
    """
    list = sorted(board.get_list_of_numbered_cells(),
                  key=lambda coord: len(board.get_possible_moves(coord[0], coord[1])), reverse=False)

    for x, y in list:
        if not board.is_colored_cell(x, y):
            return x, y


def random_variable_selection(board):
    list = sample(board.get_list_of_numbered_cells(), len(board.get_list_of_numbered_cells()))

    for x, y in list:
        if not board.is_colored_cell(x, y):
            return x, y


variable_selection_dict = {
    "Top to bottom": top_to_bottom,
    "MRV": mrv,
    "LCV": lcv,
    "Random selection": random_variable_selection,
}
