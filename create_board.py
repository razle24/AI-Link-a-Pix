import os

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


def build_board_from_image(image, number_of_colors, output_to_board_object=True, file_path=None):
    """
    To create board from an image, we want to meet the following requirements:

    * The game must have SINGLE solution
    * We shouldn't keep colored cell without a path going through it.
    * We shouldn't make a path thought empty space or different color
    * As there are many options to build a game, some of them not interesting (for example fill all colored cells
      with number 1, which makes the game trivial). We want to maximize the following formula:
          sum(number_in_cell(i, j)^1.15) foreach cell (i, j) on the board

      This way, we try and make longer paths, but not make the game with 1 long path.
    * More subjective requirement, but try to make the game challenging and not repetitive

    :param image: 2D array of ints with size (w*h), contains the number of the color in the cell
    :param number_of_colors: The number of colors in the picture
    :param output_to_board_object: Change to False if you want only to output to xml file
    :param file_path: Keep empty if you want only to output to board object
    :return: If output_to_board_object is True, output board object, otherwise None
    """
    w = len(image[0])
    h = len(image)
    board = [[((0, 0), 0) for i in range(w)] for j in range(h)]
    paths = []

    # ...

    if file_path is not None:
        xml = create_xml_from_board(paths, w, h, os.path.basename(file_path))
        with open(file_path, 'w') as file:
            file.write(xml)

    if output_to_board_object:
        return Board(number_of_colors, paths, board)

    return None
