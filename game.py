from board import *
from heuristics import heuristics_dict
from search import search_dict
from variable_selection import variable_selection_dict

import os

class Game:
    """
    Game engine class stores the current game state and controls when to
    get input/draw output
    """

    def __init__(self, xml_dict):
        """
        :param xml_dict: dictionary with the following items: Puzzle name, Puzzle width, Puzzle height,
        List of RGB values, paths, lists of lists of paths in the key color
        """
        self.game_name = xml_dict["name"]

        self.number_of_colors = len(xml_dict["colors"])
        self.colors_dict = xml_dict['colors']

        numbers_matrix, coloring_matrix = generate_matrix_from_xml_dict(xml_dict)

        self.board = Board(self.number_of_colors, numbers_matrix)
        self.initial_board = Board(self.number_of_colors, numbers_matrix)
        self.goal_board = Board(self.number_of_colors, numbers_matrix, coloring_matrix)

        self.search = None
        self.variable_selection = None
        self.heuristic = None

        self.moves_counter = 0

        # Filled only when used
        self.boards_generator = None

    def __str__(self):
        """
        prints the board
        """
        return (f'Search: {self.search}\nHeuristic: {self.heuristic}\nMoves counter: {self.moves_counter}'
                f'\nBoard:\n{self.board}')

    def do_move_csp(self):
        """
        If no coordinates given, do the next move of the backtrack.
        If coordinates are given, color the cell (x, y) with the color of 'cell_color'
        Will increment moves counter by 1.
        :return: List of all changed cells, with their new colors (list of ((number, color_number), cell_color))
        """
        self.moves_counter += 1

        self.board, path, color = next(self.boards_generator, (None, None, None))
        return path, color

    def do_move_other(self):
        """
        If no coordinates given, do the next move of the backtrack.
        If coordinates are given, color the cell (x, y) with the color of 'cell_color'
        Will increment moves counter by 1.
        :return: List of all changed cells, with their new colors (list of ((number, color_number), cell_color))
        """
        self.moves_counter += 1

        self.board = next(self.boards_generator, None)
        return self.board.coloring_matrix

    def is_goal_state(self):
        """
        :return: True if we reached the goal state, else False
        """
        return self.board == self.goal_board

    # ***  Getters  *** #
    def get_initial_board(self):
        return self.initial_board

    def get_current_numbers_matrix(self):
        """
        returns the current board matrix
        :return: Matrix of size (w*h) which contains [(number, number_color), cell_color]
        """
        return self.board.numbers_matrix

    def get_current_coloring_matrix(self):
        """
        :return: The current colors matrix
        """
        return self.board.coloring_matrix

    def get_width(self):
        """
        :return: The board's width
        """
        return self.initial_board.get_width()

    def get_height(self):
        """
        :return: The board's height
        """
        return self.initial_board.get_height()

    def get_colors(self):
        """
        :return: All the colors of the board
        """
        return self.colors_dict

    def get_moves_counter(self):
        """
        :return: The number of moves made
        """
        return self.moves_counter

    # ***  Setters  *** #
    def set_boards_generator(self, search, variable_selection, heuristic):
        self.search = search_dict[search]
        self.variable_selection = variable_selection_dict[variable_selection]
        self.heuristic = heuristics_dict[heuristic]

        self.boards_generator = self.search(self, self.variable_selection, self.heuristic)

    def reset_game(self):
        self.moves_counter = 0
        self.board = copy.copy(self.initial_board)
        self.boards_generator = None

#
# if __name__ == '__main__':
#     xml = get_xml_from_path('boards/tiny_color.xml')
#     my_game = Game(xml)
#     # print("count empty: ", count_empty_cells(my_game.board))
#     heads = my_game.board.get_list_of_numbered_cells()
#     my_game.set_boards_generator()
#     while True:
#         my_game.do_move()
#         if my_game.is_goal_state():
#             break
#     # done_board = csp(my_game.board, heads, True)
#     print("Our board:")
#     print(my_game)
#     print("Goal board:")
#     print(my_game.goal_board)
#     # print("count empty: ", count_empty_cells(done_board))
#     print(f'Same: {my_game.is_goal_state()}')
