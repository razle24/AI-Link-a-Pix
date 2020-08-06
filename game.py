from agent import *
from board import *
from search import *
from heuristics import *


class Game:
    def __init__(self, xml_dict, search_type=None, heuristic=None):
        """

        :param xml_dict:
        :param search_type:
        :param heuristic:
        """
        self.number_of_colors = len(xml_dict["colors"])
        self.colors_dict = xml_dict['colors']

        numbers_matrix, coloring_matrix = generate_matrix_from_xml_dict(xml_dict)

        self.board = Board(self.number_of_colors, numbers_matrix)
        self.initial_board = Board(self.number_of_colors, numbers_matrix)
        self.goal_board = Board(self.number_of_colors, numbers_matrix, coloring_matrix)

        self.search = search_type
        self.heuristic = heuristic

        self.moves_counter = 0

        # Filled only when used
        self.boards_generator = None

    def __str__(self):
        """
        prints the board
        :return:
        """
        return (f'Search: {self.search}\nHeuristic: {self.heuristic}\nMoves counter: {self.moves_counter}'
                f'\nBoard:\n{self.board}')

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

        # If player controls the game
        if x is None:
            self.board, path, color = next(self.boards_generator, (None, None, None))
            return path, color
        else:
            self.board.set_cell_coloring(x, y, cell_color)
            return [((x, y), cell_color)]

    def do_move_a_star(self, x=None, y=None, cell_color=None):
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

        self.board = next(self.boards_generator, None)
        return self.board.coloring_matrix


    def is_goal_state(self):
        return self.board == self.goal_board

    # **  Getters  ** #

    def get_successors(self, board):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        successors = []
        numbered_cells = board.get_list_of_numbered_cells()

        for i, j in numbered_cells:
            paths = board.get_possible_moves(i, j)
            for path in paths:
                current_board = copy.copy(board)
                color = current_board.get_number_color_in_cell(path[0][0], path[0][1])
                current_board.set_cells_coloring(path, color)
                successors += [(current_board, path)]
        return successors

    def get_search(self):
        return self.search

    def get_heuristic(self):
        return self.heuristic

    def get_current_numbers_matrix(self):
        """
        returns the current board matrix
        :return: Matrix of size (w*h) which contains ((number, number_color), cell_color)
        """
        return self.board.numbers_matrix

    def get_current_coloring_matrix(self):
        return self.board.coloring_matrix

    def get_width(self):
        return self.initial_board.get_width()

    def get_height(self):
        return self.initial_board.get_height()

    def get_colors(self):
        return self.colors_dict

    def get_moves_counter(self):
        return self.moves_counter

    def get_initial_board(selfs):
        return selfs.initial_board

    # **  Setters  ** #
    def set_search(self, search):
        self.search = search

    def set_heuristic(self, heuristic):
        self.heuristic = heuristic

    def set_boards_generator(self):
        # self.boards_generator = csp(self.board, self.board.get_list_of_numbered_cells(), False, True)
        self.boards_generator = a_star_search(self, invalid_state)


if __name__ == '__main__':
    xml = get_xml_from_path('boards/tiny_color.xml')
    my_game = Game(xml)
    # print("count empty: ", count_empty_cells(my_game.board))
    heads = my_game.board.get_list_of_numbered_cells()
    my_game.set_boards_generator()
    while True:
        my_game.do_move()
        if my_game.is_goal_state():
            break
    # done_board = csp(my_game.board, heads, True)
    print("Our board:")
    print(my_game)
    print("Goal board:")
    print(my_game.goal_board)
    # print("count empty: ", count_empty_cells(done_board))
    print(f'Same: {my_game.is_goal_state()}')
