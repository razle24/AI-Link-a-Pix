import pickle

from sklearn.preprocessing import OneHotEncoder
from sklearn.neural_network import MLPRegressor

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
