from random import sample


# class VariablesSelection:
#     def __init__(self, list_of_cells):
#         self.list_of_uncolored_number_cells = set(list_of_cells)
#         self.list_of_colored_number_cells = {}
#
#     def lcv(self, board):
#         """
#         Sort list by amount of possible paths
#         :param board:
#         :return:
#         """
#         min_cell = min(self.list_of_uncolored_number_cells,
#                        key=lambda cell: len(board.get_possible_moves(cell[0], cell[1])))
#
#         self.list_of_uncolored_number_cells.remove(min_cell)
#         self.list_of_colored_number_cells += min_cell
#         return min_cell


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
    "Random selection": random_variable_selection
}
