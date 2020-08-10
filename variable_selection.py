from random import sample


class TopToBottom:
    def __init__(self, init_board):
        self.list = init_board.get_list_of_numbered_cells()

    def next_coordinate(self, board=None):
        for x, y in self.list:
            if not board.is_colored_cell(x, y):
                return x, y


class SmallToBig:
    def __init__(self, init_board):
        self.list = sorted(init_board.get_list_of_numbered_cells(),
                           key=lambda cell: init_board.get_number_in_cell(cell[0], cell[1]), reverse=False)

    def next_coordinate(self, board):
        """
        Sort the list by number value (from small to big)
        :param board: board object
        :return: doesn't return anything. Sorts the numbered_cells list in the board.
        """
        for x, y in self.list:
            if not board.is_colored_cell(x, y):
                return x, y


class MRV:
    def __init__(self, init_board):
        self.list = sorted(init_board.get_list_of_numbered_cells(),
                           key=lambda cell: len(init_board.get_possible_moves(cell[0], cell[1])), reverse=True)

    def next_coordinate(self, board):
        """
        Sort list by amount of possible paths (descending order)
        :param board:
        :return:
        """
        for x, y in self.list:
            if not board.is_colored_cell(x, y):
                return x, y


class LCV:
    def __init__(self, init_board=None):
        pass

    def next_coordinate(self, board):
        """
        Sort list by amount of possible paths (ascending order)
        :param board:
        """
        cells_list = sorted(board.get_list_of_numbered_cells(),
                            key=lambda cell: len(board.get_possible_moves(cell[0], cell[1])), reverse=False)

        for x, y in cells_list:
            if not board.is_colored_cell(x, y):
                return x, y


class ByBullets:
    def __init__(self, init_board=None):
        pass

    def next_coordinate(self, board):
        for i in range(3):
            for j in range(3):
                for k in range(int(i * board.get_width() / 3), int((i + 1) * board.get_width() / 3)):
                    for l in range(int(j * board.get_height() / 3), int((j + 1) * board.get_height() / 3)):
                        if board.is_numbered_cell(l, k) and not board.is_colored_cell(l, k):
                            return l, k


class ByColor:
    def __init__(self, init_board):
        self.list = sorted(init_board.get_list_of_numbered_cells(),
                           key=lambda cell: init_board.get_number_color_in_cell(cell[0], cell[1]))

    def next_coordinate(self, board):
        """
        Sort list by amount of possible paths (descending order)
        :param board:
        :return:
        """
        for x, y in self.list:
            if not board.is_colored_cell(x, y):
                return x, y


class RandomVariableSelection:
    def __init__(self, init_board=None):
        self.list = sample(init_board.get_list_of_numbered_cells(), len(init_board.get_list_of_numbered_cells()))

    def next_coordinate(self, board):
        for x, y in self.list:
            if not board.is_colored_cell(x, y):
                return x, y


variable_selection_dict = {
    "Top to bottom": TopToBottom,
    "MRV": MRV,
    "Small to big": SmallToBig,
    "LCV": LCV,
    "Random selection": RandomVariableSelection,
    "By bullets": ByBullets,
    "By color": ByColor
}
