from util import manhattan_distance
import copy


def generate_matrix_from_xml_dict(xml_dict):
    """
    Given xml dictionary, read the beginning and end of each path, add corresponding coordinates to the board
    :param xml_dict: As explained at agent.py
    :param return_goal_matrix: True if we want the matrix to be filled with the answer, otherwise False.
    :return: Matrix (w*h) with the following values [(number, number_color), cell_color].
             If no number in cell the tuple will be filled with zeros [(0, 0), 0]
    """
    numbers_matrix = [[(0, 0) for i in range(xml_dict["width"])] for j in range(xml_dict["height"])]
    coloring_matrix = [[0 for i in range(xml_dict["width"])] for j in range(xml_dict["height"])]
    for number_color, paths in xml_dict["paths"].items():
        # For each path
        for path in paths:
            number = len(path)
            # Fill the matrix with the [(number, number_color), cell_color] of the wanted path
            x, y = path[0]
            end_x, end_y = path[len(path) - 1]
            numbers_matrix[x][y] = (number, number_color)
            numbers_matrix[end_x][end_y] = (number, number_color)

            for cell in path:
                x, y = cell
                coloring_matrix[x][y] = number_color

    return numbers_matrix, coloring_matrix


class Board:
    """
    A Board describes the current state of the game board. It's separate from
    the game engine to allow the Input objects to check if their moves are valid,
    etc... without the help of the game engine.

    The Board stores:
    - board_w/board_h: the width and height of the playing area
    - state: a matrix (2D list) of cells
    - matrix: a matrix (2D list) of [(number, number_color), cell_color]
    - colors: the number of the colors
    """

    def __init__(self, num_of_colors, numbers_matrix, coloring_matrix=None):
        self.num_of_colors = num_of_colors
        self.numbers_matrix = numbers_matrix

        if coloring_matrix is None:
            self.coloring_matrix = [[0 for i in range(self.get_width())] for j in range(self.get_height())]
        else:
            self.coloring_matrix = coloring_matrix

        self.board_score = None
        self.possible_paths = [[None for i in range(self.get_width())] for j in range(self.get_height())]
        self.numbered_cells = [(i, j) for i in range(self.get_height()) for j in range(self.get_width())
                               if self.is_numbered_cell(i, j)]

    def __str__(self):
        out_str = []
        for i in range(self.get_width()):
            for j in range(self.get_height()):
                out_str.append(str(self.coloring_matrix[i][j]))
            out_str.append('\n')
        return ''.join(out_str)

    def __eq__(self, other):
        return self.coloring_matrix == other.coloring_matrix

    def __hash__(self):
        return hash(str(self.numbers_matrix) + str(self.coloring_matrix))

    def __copy__(self):
        cpy_board = self.__new__(self.__class__)  # Create empty object
        cpy_board.__dict__.update(self.__dict__)  # Shallow copy everything
        cpy_board.coloring_matrix = copy.deepcopy(self.coloring_matrix)  # Deep copy only the coloring matrix

        return cpy_board

    # ** Boolean Getters ** #
    def is_numbered_cell(self, x, y):
        """
        :return: True if the cell (x, y) is a head, else False
        """
        return self.get_number_in_cell(x, y) != 0

    def is_colored_cell(self, x, y):
        """
        :return: True if the cell (x, y) is colored, else False
        """
        return self.get_cell_coloring(x, y) != 0

    def is_valid_path(self, path):
        """
        :param path: The path we want to check
        :return: True if the path is valid - no cell is already colored, else False
        """
        for cell in path:
            # Directly check matrix to improve performance
            if self.coloring_matrix[cell[0]][cell[1]]:
                return False
        return True

    # def has_possible_moves(self, x, y):
    #     paths = self.get_possible_paths(x, y)
    #     for path in paths:
    #         if self.is_valid_path(path):
    #             return True
    #     return False

    # ** Getters ** #
    def get_number_in_cell(self, x, y):
        """
        :return: The number in cell (x, y)
        """
        return self.numbers_matrix[x][y][0]

    def get_number_color_in_cell(self, x, y):
        """
        :return: The color of the number in cell (x, y)
        """
        return self.numbers_matrix[x][y][1]

    def get_cell_coloring(self, x, y):
        """
        :return: The color of the cell (x, y)
        """
        return self.coloring_matrix[x][y]

    def get_width(self):
        """
        :return: The board's width
        """
        return len(self.numbers_matrix[0])

    def get_height(self):
        """
        :return: The board's height
        """
        return len(self.numbers_matrix)

    def get_list_of_numbered_cells(self):
        """
        :return: All the (x, y) of the cells that has number in it (the heads)
        """
        return self.numbered_cells

    # def get_board_score(self):
    #     """
    #     :return: The board's current score
    #     """
    #     return self.board_score

    # ** Setters ** #
    def set_cell_coloring(self, x, y, cell_color):
        """
        The function colors the cell (x, y) in the given color
        """
        self.coloring_matrix[x][y] = cell_color

    def set_cells_coloring(self, cells, cell_color):
        """
        Fill all the cells in list with the given color
        :param cells: List of cells (x, y)
        :param cell_color: Color indicator
        """
        for cell in cells:
            self.coloring_matrix[cell[0]][cell[1]] = cell_color

    # def set_board_score(self, score):
    #     self.board_score = score

    def get_possible_moves(self, x, y):
        """
        :return: All valid paths from the head (x, y) to another head
        """
        ret = []
        paths = self.get_possible_paths(x, y)
        for path in paths:
            if self.is_valid_path(path):
                ret += [path]
                continue
        return ret

    # ** Possible Paths Finder ** #
    def get_possible_paths(self, x, y):
        """
        Get all possible paths from the cell (x, y).
        If cell is not number (has value 0), return empty list
        If cell is number (has value different from 0), return all valid paths to all (end_x, end_y) such that
        the number and number_color are the same.
        :param x: Row selector.
        :param y: Column selector.
        :return: List of paths. Path is a list of [(number, number_color), cell_color].
        """
        if self.possible_paths[x][y] is None:
            paths = []
            length = self.get_number_in_cell(x, y)

            # If no path
            if length == 0:
                return []

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

            self.possible_paths[x][y] = paths

        return self.possible_paths[x][y]

    def get_paths(self, x, y, end_x, end_y, length):
        """
        Find all valid paths from (x, y) to (end_x, end_y).
        If values are out of range or not the same (has same number or number_color) return empty list.
        :param x: Row selector for start position.
        :param y: Column selector for start position.
        :param end_x: Row selector for end position.
        :param end_y: Column selector for end position.
        :param length: Length of path to look for.
        :return: List of paths. Path is a list of [(number, number_color), cell_color].
        """
        # If function parameters are not valid, return empty list
        if end_x < 0 or self.get_height() <= end_x or end_y < 0 or self.get_width() <= end_y \
                or self.get_number_in_cell(end_x, end_y) != length \
                or self.get_number_color_in_cell(x, y) != self.get_number_color_in_cell(end_x, end_y):
            return []

        # Run recursive search on board
        paths = self.get_paths_rec([(x, y)], end_x, end_y, length - 1, length)
        paths_mask = [True for i in range(len(paths))]

        # Remove paths with same footprint. The board must have only 1 solution, so if 2 or more paths cover
        # the same cells in different order, all of them must be invalid (Assume one of them is the right path =>
        # => The other is also valid => There is more than one solution to the board).
        for i, path_A in enumerate(paths):
            for j, path_B in enumerate(paths[i + 1:], start=(i + 1)):
                if paths_mask[j] is True and len(path_A) == len(path_B) and set(path_A) == set(path_B):
                    paths_mask[i] = False
                    paths_mask[j] = False

        return [path for i, path in enumerate(paths) if paths_mask[i]]

    def get_paths_rec(self, current_path, end_x, end_y, steps, length):
        """
        Recursive function that finds all valid paths from (x, y) to (end_x, end_y).
        :return: List of paths. Path is a list of [(number, number_color), cell_color].
        """
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
        if manhattan_distance((x, y), (end_x, end_y)) > steps \
                or (self.get_number_in_cell(x, y) != 0 and length - 1 != steps):
            return []

        # Collect valid paths from this point
        paths = []
        possible_steps = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

        for possible_step in possible_steps:
            # If point not on board or point already in path, skip it
            if possible_step[0] < 0 or self.get_height() <= possible_step[0] or possible_step[1] < 0 \
                    or self.get_width() <= possible_step[1] or possible_step in current_path:
                continue

            paths += self.get_paths_rec(current_path + [possible_step], end_x, end_y, steps - 1, length)

        return paths
