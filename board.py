import numpy as np
from util import manhattan_distance


def generate_matrix_from_xml_dict(xml_dict, return_goal_matrix=False):
    """
    Given xml dictionary, read the beginning and end of each path, add corresponding coordinates to the board
    :param xml_dict: As explained at agent.py
    :param return_goal_matrix: True if we want the matrix to be filled with the answer, otherwise False.
    :return: Matrix (w*h) with the following values ((number, number_color), cell_color).
             If no number in cell the tuple will be filled with zeros ((0, 0), 0)
    """
    matrix = [[((0, 0), 0) for i in range(xml_dict["width"])] for j in range(xml_dict["height"])]
    for number_color, paths in xml_dict["paths"].items():
        # For each path
        for path in paths:
            number = len(path)

            cell_color = 0
            # If want to return goal matrix, color also the path itself
            if return_goal_matrix:
                cell_color = number_color
                for cell in path:
                    x, y = cell
                    matrix[x][y] = ((0, 0), cell_color)

            # Fill the matrix with the ((number, number_color), cell_color) of the wanted path
            x, y = path[0]
            end_x, end_y = path[len(path) - 1]
            matrix[x][y] = ((number, number_color), cell_color)
            matrix[end_x][end_y] = ((number, number_color), cell_color)

    return matrix


class Cell:
    def __init__(self, x, y, number, number_color, cell_color=0):
        self.x = x
        self.y = y
        self.number = number
        self.number_color = number_color
        self.cell_color = cell_color
        self.colored = False

        self.head = None
        self.domain = []
        self.legal_paths = []

    def remove_value(self, is_backtrack):
        if self.number != 0:
            if is_backtrack:
                self.colored = False
                return
            self.legal_paths = self.domain.copy()
        else:
            self.cell_color = 0
            self.colored = False

    # ** Getters ** #
    def get_coordinates(self):
        return self.x, self.y

    def get_x_coordinate(self):
        return self.x

    def get_y_coordinate(self):
        return self.y

    def get_number(self):
        return self.number

    # ** Setters ** #
    def set_cell_color(self, color):
        self.cell_color = color

        if color == 0:
            self.colored = False
        else:
            self.colored = True

    def set_domain(self, domain):
        self.domain = domain

class Board:
    """
    A Board describes the current state of the game board. It's separate from
    the game engine to allow the Input objects to check if their moves are valid,
    etc... without the help of the game engine.

    The Board stores:
    - board_w/board_h: the width and height of the playing area
    - state: a matrix (2D list) of cells
    - matrix: a matrix (2D list) of ((number, number_color), cell_color)
    - colors: the number of the colors
    """
    def __init__(self, num_of_colors, b_matrix):
        self.board_w = len(b_matrix[0])
        self.board_h = len(b_matrix)
        self.num_of_colors = num_of_colors
        self.matrix = b_matrix
        self.state = dict()
        self.create_board(b_matrix)

        # Fill only when used
        self.numbered_cells = None

    def __str__(self):
        out_str = []
        for i in range(self.board_h):
            for j in range(self.board_w):
                out_str.append(str(self.matrix[i][j][1]))
            out_str.append('\n')
        return ''.join(out_str)

    def __eq__(self, other):
        return self.matrix == other.matrix

    def __hash__(self):
        return hash(str(self.matrix))

    # TODO: Not our function
    def __copy__(self):
        cpy_board = Board(self.board_w, self.board_h, self.num_players, self.piece_list)
        cpy_board.state = np.copy(self.state)
        cpy_board._legal = np.copy(self._legal)
        cpy_board.connected = np.copy(self.connected)
        cpy_board.pieces = np.copy(self.pieces)
        cpy_board.scores = self.scores[:]
        return cpy_board

    def create_board(self, b_matrix):
        for i in range(self.board_h):
            for j in range(self.board_w):
                number, number_color = b_matrix[i][j][0]
                self.state[(i, j)] = Cell(i, j, number, number_color)
                self.state[(i, j)].set_domain(self.get_possible_paths(i, j))

    def remove_value(self, x, y, is_backtrack):
        self.state[(x, y)].remove_value(is_backtrack)

    def is_path_legal(self, path):
        if len(path) == 1:
            num = self.state[path[0]].number
            is_head = self.state[path[0]].head
            if num == 1 and is_head:
                return True

            return False

        for x, y in path:
            if self.state[(x, y)].colored:
                return False
        return True

    def color_path(self, path):
        """
        gets vars' array and a path, and colors it's coordinates in the right color.
        :param vars:
        :param path:
        :return: doesn't return anything, just updating the vars' array.
        """
        color = self.state[path[0]].color
        for x, y in path:
            self.set_cell_color(x, y, color)

    def uncolor_path(self, path, is_backtrack):
        """
        gets vars' array and a path, and colors it's coordinates in the right color.
        :param vars:
        :param path:
        :return: doesn't return anything, just updating the vars' array.
        """
        for x, y in path:
            self.remove_value(x, y, is_backtrack)

    # def add_move(self, move):
    #     """
    #     Try to add <player>'s <move>.
    #
    #     If the move is legal, the board state is updated; if it's not legal, a
    #     ValueError is raised.
    #
    #     Returns the number of tiles placed on the board.
    #     """
    # if not self.check_move_valid(player, move):
    #     raise ValueError("Move is not allowed")
    #
    # piece = move.piece
    # self.pieces[player, move.piece_index] = False  # mark piece as used
    #
    # # Update internal state for each tile
    # for (xi, yi) in move.orientation:
    #     (x, y) = (xi + move.x, yi + move.y)
    #     self.state[y, x] = player
    #
    #     # Nobody can play on this square
    #     for p in range(self.num_players):
    #         self._legal[p][y][x] = False
    #
    #     # This player can't play next to this square
    #     if x > 0:
    #         self._legal[player, y, x - 1] = False
    #     if x < self.board_w - 1:
    #         self._legal[player, y, x + 1] = False
    #     if y > 0:
    #         self._legal[player, y - 1, x] = False
    #     if y < self.board_h - 1:
    #         self._legal[player, y + 1, x] = False
    #
    #     # The diagonals are now attached
    #     if x > 0 and y > 0:
    #         self.connected[player, y - 1, x - 1] = True
    #     if x > 0 and y < self.board_h - 1:
    #         self.connected[player, y + 1, x - 1] = True
    #     if x < self.board_w - 1 and y < self.board_h - 1:
    #         self.connected[player, y + 1, x + 1] = True
    #     if x < self.board_w - 1 and y > 0:
    #         self.connected[player, y - 1, x + 1] = True
    #
    # self.scores[player] += piece.get_num_tiles()
    # return piece.get_num_tiles()

    # def do_move(self, player, move):
    #     """
    #     Performs a move, returning a new board
    #     """
    #     new_board = self.__copy__()
    #     new_board.add_move(player, move)
    #
    #     return new_board
    #
    # def get_legal_moves(self, player):
    #     """
    #     Returns a list of legal moves for given player for this board state
    #     """
    #     # Generate all legal moves
    #     move_list = []
    #     for piece in self.piece_list:
    #         for x in range(self.board_w):
    #             for y in range(self.board_h):
    #                 for ori in piece:
    #                     new_move = Move(piece,
    #                                     self.piece_list.pieces.index(piece),
    #                                     ori, x, y)
    #                     if self.check_move_valid(player, new_move):
    #                         move_list.append(new_move)
    #     return move_list
    #
    # def check_move_valid(self, player, move):
    #     """
    #     Check if <player> can legally perform <move>.
    #
    #     For a move to be valid, it must:
    #     - Use a piece that is available
    #     - Be completely in bounds
    #     - Not be intersecting any other tiles
    #     - Not be adjacent to any of the player's other pieces
    #     - Be diagonally attached to one of the player's pieces or their corner
    #
    #     Return True if the move is legal or False otherwise.
    #     """
    #     if not self.pieces[player, move.piece_index]:
    #         # piece has already been used
    #         return False
    #
    #     attached_corner = False
    #
    #     for (x, y) in move.orientation:
    #         # If any tile is illegal, this move isn't valid
    #         if not self.check_tile_legal(player, x + move.x, y + move.y):
    #             return False
    #
    #         if self.check_tile_attached(player, x + move.x, y + move.y):
    #             attached_corner = True
    #
    #         # If at least one tile is attached, this move is valid
    #     return attached_corner

    # def check_tile_legal(self, player, x, y):
    #     """
    #     Check if it's legal for <player> to place one tile at (<x>, <y>).
    #
    #     Legal tiles:
    #     - Are in bounds
    #     - Don't intersect with existing tiles
    #     - Aren't adjacent to the player's existing tiles
    #
    #     Returns True if legal or False if not.
    #     """
    #
    #     # Make sure tile in bounds
    #     if x < 0 or x >= self.board_w or y < 0 or y >= self.board_h:
    #         return False
    #
    #     # Otherwise, it's in the lookup table
    #     return self._legal[player, y, x]

    # def check_tile_attached(self, player, x, y):
    #     """Check if (<x>, <y>) is diagonally attached to <player>'s moves.
    #
    #     Note that this does not check if this move is legal.
    #
    #     Returns True if attached or False if not.
    #     """
    #
    #     # Make sure tile in bounds
    #     if x < 0 or x >= self.board_w or y < 0 or y >= self.board_h:
    #         return False
    #
    #     # Otherwise, it's in the lookup table
    #     return self.connected[player, y, x]

    # ** Boolean Getters ** #
    def is_numbered_cell(self, x, y):
        return self.get_number_in_cell(x, y) != 0

    def is_colored_cell(self, x, y):
        return self.get_cell_color(x, y) != 0

    # ** Getters ** #
    def get_var_by_pos(self, pos):
        return self.state[pos]

    def get_pos_by_var(self, cell, coords):
        for index in range(len(coords)):
            if cell.pos == coords[index].pos:
                return index

    def get_number_in_cell(self, x, y):
        return self.matrix[x][y][0][0]

    def get_number_color_in_cell(self, x, y):
        return self.matrix[x][y][0][1]

    def get_cell_color(self, x, y):
        return self.matrix[x][y][1]

    def get_width(self):
        return self.board_w

    def get_height(self):
        return self.board_h

    def get_list_of_numbered_cells(self):
        if self.numbered_cells is None:
            self.numbered_cells = []
            for i in range(self.board_h):
                for j in range(self.board_w):
                    if self.is_numbered_cell(i, j):
                        self.numbered_cells.append((i, j))
            return self.numbered_cells
        else:
            return self.numbered_cells

    # ** Setters ** #
    def set_cell_color(self, x, y, cell_color):
        self.matrix[x][y][1] = cell_color
        self.state[(x, y)].set_cell_color(cell_color)

    # ** Possible Paths Finder ** #
    def get_possible_paths(self, x, y):
        """
        Get all possible paths from the cell (x, y).
        If cell is not number (has value 0), return None
        If cell is number (has value different from 0), return all valid paths to all (end_x, end_y) such that
        the number and number_color are the same.
        :param x: Row selector.
        :param y: Column selector.
        :return: List of paths. Path is a list of ((number, number_color), cell_color).
        """
        paths = []
        length = self.get_number_in_cell(x, y)

        # If no path
        if length == 0:
            return None

        # If path contains only 1 cell, return the only possible path
        if length == 1:
            return [[(x, y)]]

        # Odd numbers must have odd manhattan distance between start and end
        # Even numbers must have even manhattan distance between start and end
        # This loop will only check possible end coordinates for the path
        offset = length % 2 == 0
        # For every possible x
        for i in range(length + 1):
            # And every other y such that i + j <= length
            for j in range(offset, length - i, 2):
                end_x = x + i
                m_end_x = x - i

                end_y = y + j
                m_end_y = y - j

                if i != 0:
                    paths += self.get_paths(x, y, end_x, end_y, length)
                    paths += self.get_paths(x, y, m_end_x, end_y, length)

                    if j != 0:
                        paths += self.get_paths(x, y, end_x, m_end_y, length)
                        paths += self.get_paths(x, y, m_end_x, m_end_y, length)

                elif j != 0:
                    paths += self.get_paths(x, y, end_x, end_y, length)
                    paths += self.get_paths(x, y, end_x, m_end_y, length)

            offset = not offset

        return paths

    def get_paths(self, x, y, end_x, end_y, length):
        """
        Find all valid paths from (x, y) to (end_x, end_y).
        If values are out of range or not the same (has same number or number_color) return empty list.
        :param x: Row selector for start position.
        :param y: Column selector for start position.
        :param end_x: Row selector for end position.
        :param end_y: Column selector for end position.
        :param length: Length of path to look for.
        :return: List of paths. Path is a list of ((number, number_color), cell_color).
        """
        # If function parameters are not valid, return empty list
        if end_x < 0 or self.board_h <= end_x or end_y < 0 or self.board_w <= end_y \
                or self.get_number_in_cell(x, y) != length \
                or self.get_number_in_cell(end_x, end_y) != length \
                or self.get_number_color_in_cell(x, y) != self.get_number_color_in_cell(end_x, end_y):
            return []

        # Run recursive search on board
        paths = self.get_paths_rec([(x, y)], end_x, end_y, length - 1, length)
        paths_mask = [True for i in range(len([paths]))]

        # Remove paths with same footprint. The board must have only 1 solution, so if 2 or more paths cover
        # the same cells, all of must be invalid (Assume one of them is the right path => The other is also valid =>
        # => There is more than one solution to the board).
        for i, path_A in enumerate(paths):
            for j, path_B in enumerate(paths[i + 1:], start=(i + 1)):
                if paths_mask[j] is True and len(path_A) == len(path_B) and set(path_A) == set(path_B):
                    paths_mask[i] = False
                    paths_mask[j] = False

        return [path for i, path in enumerate(paths) if paths_mask[i]]

    def get_paths_rec(self, current_path, end_x, end_y, steps, length):
        x, y = current_path[-1]

        # If end of steps
        if steps == 0:
            # And got to end, return path found
            if current_path[-1] == (end_x, end_y):
                return [current_path]
            # Otherwise, path don't lead to end
            else:
                return []

        # If end is too far for path or we got to a number (we checked earlier and this is not the end point)
        #  don't continue search for this direction
        if manhattan_distance((x, y), (end_x, end_y)) > steps or self.get_number_in_cell(x, y) != 0:
            return []

        # Collect valid paths from this point
        paths = []
        possible_steps = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

        for possible_step in possible_steps:
            # If point not on board or point already in path, skip it
            if possible_step[0] < 0 or self.board_h <= possible_step[0] or possible_step[1] < 0 or self.board_w <= \
                    possible_step[1] or possible_step in current_path:
                continue

            paths += self.get_paths_rec(current_path + [possible_step], end_x, end_y, steps - 1, length)

        return paths


