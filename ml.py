import csv
import os
import pickle

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeRegressor

import xml_parser as ag

PATH_TO_TRAIN_SET = './learner/train_set.csv'
PATH_TO_PREDICTOR = './learner/predictor'
PATH_TO_ONE_HOT_ENCODER = './learner/OneHotEncoder'


# *** Helper functions *** #
def move_path(path):
    x_change = path[0][0]
    y_change = path[0][1]

    return [(cell[0] - x_change, cell[1] - y_change) for cell in path]


def rotate_path(path):
    # If single cell or already going up, dont change the path
    if len(path) == 1 or path[1][0] == 1:
        return path  # new cell is (x, y)

    # If going down
    if path[1][0] == -1:
        return [(-cell[0], -cell[1]) for cell in path]  # new cell is (-x, -y)

    # If going left
    if path[1][1] == 1:
        return [(cell[1], -cell[0]) for cell in path]  # new cell is (-y, x)

    # If going right (path[1][1] == -1)
    return [(-cell[1], cell[0]) for cell in path]  # new cell is (y, -x)


def mirror_path(path):
    # If not straight line
    for cell in path:
        # Go to the right, dont change the path
        if cell[1] == 1:
            return path

        # iF go to left, return mirror path
        if cell[1] == -1:
            return [(cell[0], -cell[1]) for cell in path]

    # Path is straight, return as is
    return path


def normalize_path(path):
    '''
    Move path to always start at (0,0)
    Rotate so the path goes up on first step
    Mirror so the path will go right first change of discretion
    :param path: Path to normalize
    :return: Normalized path
    '''
    return mirror_path(rotate_path(move_path(path)))


# *** Use predictor *** #
class Predictor:
    def __init__(self, board):
        self.w = board.get_width()
        self.h = board.get_height()
        self.number_of_colors = board.get_number_of_colors()

        number_of_cells = self.w * self.h
        numbered_cells = board.get_list_of_numbered_cells()
        number_of_filled_cells = 0
        for cell in numbered_cells:
            number = board.get_number_in_cell(cell[0], cell[1])
            if number == 1:
                number_of_filled_cells += 1
            else:
                number_of_filled_cells += number / 2
        self.percent_of_filled_cells = round((number_of_filled_cells / number_of_cells) * 100, 2)

        with open(PATH_TO_PREDICTOR, 'rb') as file:
            self.predictor = pickle.load(file)
        print('Predictor is read from disk')

        with open(PATH_TO_ONE_HOT_ENCODER, 'rb') as file:
            self.ohe = pickle.load(file)
        print('Encoder is read from disk')

    def predict(self, path):
        path_start_x, path_start_y = path[0]
        path_end_x, path_end_y = path[-1]

        row = [
            self.w, self.h,
            self.number_of_colors,
            self.percent_of_filled_cells,
            path_start_x, path_start_y,
            path_end_x, path_end_y,
            str(normalize_path(path))
        ]
        new_row = row[:-1]
        new_row.extend(self.ohe.transform([[row[-1]]])[0])
        return self.predictor.predict([new_row])


# *** Create train set *** #
def convert_xml_dict_to_rows(xml_dict):
    # Most be here to avoid circular imports
    from game import Game

    w = xml_dict['width']
    h = xml_dict['height']
    number_of_colors = len(xml_dict['colors'])
    number_of_cells = w * h
    number_of_filled_cells = sum(
        [len(path) for color, paths in xml_dict['paths'].items() for path in paths])
    percent_of_filled_cells = round((number_of_filled_cells / number_of_cells) * 100, 2)

    rows = []
    solution_paths = []
    # Get least of solution paths, score them 100
    for color, paths in xml_dict['paths'].items():
        for path in paths:
            solution_paths += paths
            path_start_x, path_start_y = path[0]
            path_end_x, path_end_y = path[-1]
            rows += [[
                w, h,
                number_of_colors,
                percent_of_filled_cells,
                path_start_x, path_start_y,
                path_end_x, path_end_y,
                str(normalize_path(path)),
                100
            ]]

    # Get list of wrong paths, score them 0
    game = Game(xml_dict)
    for cell in game.initial_board.get_list_of_numbered_cells():
        paths = game.board.get_possible_moves(cell[0], cell[1])
        for path in paths:
            path_start_x, path_start_y = path[0]
            path_end_x, path_end_y = path[-1]
            if path not in solution_paths:
                rows += [[
                    w, h,
                    number_of_colors,
                    percent_of_filled_cells,
                    path_start_x, path_start_y,
                    path_end_x, path_end_y,
                    str(normalize_path(path)),
                    0
                ]]

    return rows


def create_train_file():
    path_puzzles = './boards'
    train_set = [['w', 'h', 'number_of_colors', 'percent_of_filled_cells', 'path_start_x',
                  'path_start_y', 'path_end_x', 'path_end_y', 'normalize_path', 'label']]

    puzzles = [f for f in os.listdir(path_puzzles)]

    with open('learner/train_set.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(train_set)

        for i, puzzle in enumerate(puzzles[:-2]):
            print(f'{i} out of {len(puzzles[:-2])}')
            xml_dict = ag.get_xml_from_path(path_puzzles + '/' + puzzle)
            train_set = convert_xml_dict_to_rows(xml_dict)

            writer.writerows(train_set)

    print('Train set is written to disk')


# *** Create predictor *** #
def create_predictor():
    # Read from train_set.csv
    train_set = pd.read_csv(PATH_TO_TRAIN_SET)
    train_label = train_set['label']
    del train_set['label']

    print('1) Create one hot matrix')
    ohe = OneHotEncoder(sparse=False, handle_unknown='ignore')
    one_hot_data_set = ohe.fit_transform(train_set['normalize_path'].to_numpy().reshape(-1, 1))

    print('2) Delete path strings and convert data frame to uint8')
    del train_set['normalize_path']
    train_set = train_set.astype(np.uint8)

    print('3) Convert one hot matrix to data frame of booleans')
    pd_one_hot_data_set = pd.DataFrame(one_hot_data_set, dtype='bool')

    print('4) Join to existing data')
    train_set = train_set.join(pd_one_hot_data_set)

    print('5) Train model on data')
    decision_tree_model = DecisionTreeRegressor(min_samples_split=0.05, min_samples_leaf=0.05)
    predictor = decision_tree_model.fit(train_set, train_label)

    with open(PATH_TO_PREDICTOR, 'wb') as file:
        pickle.dump(predictor, file)
    print('6) Predictor is written to disk')

    with open(PATH_TO_ONE_HOT_ENCODER, 'wb') as file:
        pickle.dump(ohe, file)
    print('7) Encoder is written to disk')


# *** Main *** #
if __name__ == '__main__':
    # create_train_file()
    create_predictor()
