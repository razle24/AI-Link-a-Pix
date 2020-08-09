import os
import itertools
import random

from board import *

# def evaluate_board(board):
#     board_value = 0
#     for i in board.board_h:
#         for j in board.board_w:
#             board_value += board.get_number_in_cell(i, j) ** 1.15
#
#     return board_value


def create_xml_from_board(paths, w, h, name):
    return 'hii'


def are_adjacent_cells(cell_a, cell_b):
    return abs(cell_a[0] - cell_b[0]) + abs(cell_a[1] - cell_b[1]) == 1


def has_one_valid_solution(paths, num_of_colors):
    pass


def combine_paths(path_a, path_b):
    # If different colors, return None
    if path_a[0][1] != path_b[0][1]:
        return None

    # Check if has possible connection
    if are_adjacent_cells(path_a[-1], path_b[0]):
        return path_a + path_b

    if are_adjacent_cells(path_b[-1], path_a[0]):
        return path_b + path_a

    if are_adjacent_cells(path_a[0], path_b[0]):
        return path_a[::-1] + path_b

    if are_adjacent_cells(path_a[-1], path_b[-1]):
        return path_a + path_b[::-1]

    # Cannot combine paths, return None
    return None


def build_board_from_image(image, colors_pallet, output_to_board_object=True, file_path=None):
    """
    To create board from an image, we want to meet the following requirements:

    * The game must have SINGLE solution
    * We shouldn't keep colored cell without a path going through it.
    * We shouldn't make a path thought empty space or different color
    * As there are many options to build a game, some of them not interesting (for example
    fill all colored cells with number 1, which makes the game trivial).
    We want to maximize the following formula:
          sum(number_in_cell(i, j)^1.15) foreach cell (i, j) on the board

      This way, we try and make longer paths, but not make the game with 1 long path.
    * More subjective requirement, but try to make the game challenging and not repetitive

    :param image: 2D array of ints with size (w*h), contains the number of the color in the cell
    :param colors_pallet: List with RGB values, size of list is amount of colors on board
    :param output_to_board_object: Change to False if you want only to output to xml file
    :param file_path: Keep empty if you want only to output to board object
    :return: If output_to_board_object is True, output board object, otherwise None
    """
    w = len(image[0])
    h = len(image)
    average_path_length = int(max(w, h) * 0.5)
    num_of_colors = len(colors_pallet)

    # Create trivial board, all cells are filled with ones
    board = [[(1, image[i][j]) for i in range(h)] for j in range(w)]
    paths = [[(i, j)] for i in range(h) for j in range(w) if image[i][j] != 0]

    change = True

    while change:
        change = False
        random.shuffle(paths)
        for path_a, path_b in list(itertools.combinations(paths, 2)):
            new_path = combine_paths(path_a, path_b)

            new_paths = copy.deepcopy(paths)
            new_paths.remove(path_a)
            new_paths.remove(path_b)
            new_paths.append(new_path)

            if new_path is not None and has_one_valid_solution(new_paths, num_of_colors):
                change = True
                paths = new_paths
                break

    print('g')

    # if file_path is not None:
    #     xml = create_xml_from_board(paths, w, h, os.path.basename(file_path))
    #     with open(file_path, 'w') as file:
    #         file.write(xml)
    #
    # if output_to_board_object:
    #     return Board(num_of_colors, paths, board)
    #
    # return None


if __name__ == '__main__':
    image = [[1, 1, 1, 1, 1, 1, 2, 1, 2, 2],
             [1, 1, 1, 1, 0, 1, 1, 1, 1, 2],
             [1, 3, 3, 3, 4, 0, 1, 2, 1, 1],
             [1, 1, 1, 1, 0, 0, 1, 1, 1, 2],
             [1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
             [1, 1, 1, 0, 0, 1, 1, 1, 1, 1],
             [1, 1, 0, 0, 1, 1, 1, 1, 1, 1],
             [1, 0, 4, 4, 4, 1, 1, 1, 1, 1],
             [1, 0, 4, 4, 4, 4, 4, 1, 1, 1],
             [1, 0, 0, 4, 4, 4, 4, 4, 1, 1],
             [1, 1, 0, 0, 0, 0, 0, 4, 4, 1],
             [0, 1, 1, 3, 1, 3, 0, 1, 1, 1],
             [1, 5, 1, 3, 1, 3, 3, 1, 1, 0],
             [5, 5, 5, 3, 5, 1, 3, 3, 1, 5],
             [5, 5, 5, 3, 5, 5, 5, 3, 5, 5]]

    colors_pallet = ["ffffff", "3398ff", "ef9a50", "ff150e", "000000", "50f000"]

    build_board_from_image(image, colors_pallet)
