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
    cells_list = sorted(board.get_list_of_numbered_cells(),
                  key=lambda coord: board.get_number_in_cell(coord[0], coord[1]), reverse=False)

    for x, y in cells_list:
        if not board.is_colored_cell(x, y):
            return x, y


def lcv(board):
    """
    Sort list by amount of possible paths
    :param board:
    :return:
    """
    cells_list = sorted(board.get_list_of_numbered_cells(),
                  key=lambda coord: len(board.get_possible_moves(coord[0], coord[1])), reverse=False)

    for x, y in cells_list:
        if not board.is_colored_cell(x, y):
            return x, y


def by_bullets(board):
    # bullet_w = int(board.get_width() / 3)
    # bullet_h = int(board.get_height() / 3)
    
    for i in range(3):
        for j in range(3):
            for k in range(int(i * board.get_width() / 3), int((i + 1) * board.get_width() / 3)):
                for l in range(int(j * board.get_height() / 3), int((j + 1) * board.get_height() / 3)):
                    if board.is_numbered_cell(l, k) and not board.is_colored_cell(l, k):
                        return l, k
    
    
def by_color(board):
    cells_list = sorted(board.get_list_of_numbered_cells(),
                  key=lambda coord: board.get_number_color_in_cell(coord[0], coord[1]))

    for x, y in cells_list:
        if not board.is_colored_cell(x, y):
            return x, y
    
    
def random_variable_selection(board):
    cells_list = sample(board.get_list_of_numbered_cells(), len(board.get_list_of_numbered_cells()))

    for x, y in cells_list:
        if not board.is_colored_cell(x, y):
            return x, y


variable_selection_dict = {
    "Top to bottom": top_to_bottom,
    "MRV": mrv,
    "LCV": lcv,
    "Random selection": random_variable_selection,
    "By bullets": by_bullets,
    "By color": by_color
}
