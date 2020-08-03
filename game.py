from agent import *
from board import *
from search import *


class Game:
    def __init__(self, xml_dict, search_type=None, heuristic=None):
        """
        :param file: XML file that represents the board
        """
        self.number_of_colors = len(xml_dict["colors"])
        self.colors_dict = xml_dict['colors']

        start_matrix = generate_matrix_from_xml_dict(xml_dict)
        goal_matrix = generate_matrix_from_xml_dict(xml_dict, True)

        self.board = Board(self.number_of_colors, start_matrix)
        self.initial_board = Board(self.number_of_colors, start_matrix)
        self.goal_board = Board(self.number_of_colors, goal_matrix)

        self.search = search_type
        self.heuristic = heuristic

        self.successors = []
        self.moves_counter = 0

    def __str__(self):
        """
        prints the board
        :return:
        """
        print(f'Search: {self.search}')
        print(f'Heuristic: {self.heuristic}')
        print(f'Moves counter: {self.moves_counter}')
        print(f'Board:\n{self.board}')

    def do_move(self, x=None, y=None, cell_color=None):
        """
        If no coordinates given, do the next move of the backtrack.
        If coordinates are given, color the cell (x, y) with the color of 'cell_color'
        Will increment moves counter by 1.
        :param x: Row selection
        :param y: Column selection
        :param cell_color: Color index
        :return: List of all changed cells, with their new colors (list of ((number, color_number), cell_color))
        """
        self.moves_counter += 1

        if x is not None:
            self.board.update_cell(x, y, cell_color)
            return [((x, y), cell_color)]

        else:
            pass

    def is_goal_state(self):
        return self.board == self.goal_board

    # **  Getters  ** #
    def get_search(self):
        return self.search

    def get_heuristic(self):
        return self.heuristic

    def get_current_matrix(self):
        """
        returns the current board matrix
        :return: Matrix of size (w*h) which contains ((numner, number_color), cell_color)
        """
        return self.board.matrix

    def get_width(self):
        return self.initial_board.get_width()

    def get_height(self):
        return self.initial_board.get_height()

    def get_colors(self):
        return self.colors_dict

    def get_moves_counter(self):
        return self.moves_counter

    # **  Setters  ** #
    def set_search(self, search):
        self.search = search

    def set_heuristic(self, heuristic):
        self.heuristic = heuristic


def get_heads(board):
    heads = []
    for i in range(board.board_h):
        for j in range(board.board_w):
            if board.is_numbered_cell(i, j):
                heads.append(board.state[(i, j)])
    return heads


def print_var_board(board, cols, rows):
    for i in range(rows):
        for j in range(cols):
            print(board.state[(i, j)].color, end="", flush=True)
            print(" ", end="", flush=True)
        print()


if __name__ == '__main__':
    xml = get_xml_from_path('boards/small_color.xml')
    my_game = Game(xml)
    heads = get_heads(my_game.board)
    csp(my_game.board, heads, True)

    print_var_board(my_game.board, 15, 15)
    print()
    print_var_board(my_game.goal_board, 15, 15)
