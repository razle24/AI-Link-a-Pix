from ml import Predictor


# ** Used every time ** #
def invalid_state(board):
    """
    A heuristic function that estimates the cost of the current board.
    Checks if the board is valid.
    :param path: The current path we want to color
    :param board: The current board
    :return: -infinity if the board is not valid,  else - 0.
    """
    numbered_cells = board.get_list_of_numbered_cells()

    for i, j in numbered_cells:
        if not board.is_colored_cell(i, j) and len(board.get_possible_moves(i, j)) == 0:
            return float('-inf')

    return 0


# ** Selected by user ** #
class NullHeuristic:
    def __init__(self, init_board=None):
        pass

    def cost(self, board=None, path=None):
        """
        A heuristic function that estimates the cost of the current board. This heuristic is trivial.
        :param board:
        :param path:
        :return: 0 for every board
        """
        return 0


class CountPossiblePaths:
    def __init__(self, init_board=None):
        pass

    def cost(self, board, path):
        x, y = path[0]
        end_x, end_y = path[-1]

        start_moves = board.get_possible_moves(x, y)
        if len(start_moves) == 0:
            return float('inf')
        end_moves = board.get_possible_moves(end_x, end_y)
        if len(end_moves) == 0:
            return float('inf')

        return max(len(board.get_possible_moves(x, y)), len(board.get_possible_moves(end_x, end_y)))


class StickToWalls:
    def __init__(self, init_board=None):
        pass

    def cost(self, board, path):
        """
        A heuristic function that estimates the cost of the current board.
        Counts the number of cells in the path that are closer to the walls of the board.
        :param path: The current path we want to color
        :param board: The current board
        :return: The number of cells in the path that are closer to the walls of the board
        """
        return (-1) * (sum([1 for i, j in path if i == 0 or i == board.get_height() - 1
                            or j == 0 or j == board.get_width() - 1]) + 1)


class StickToOtherPaths:
    def __init__(self, init_board=None):
        pass

    def cost(self, board, path):
        """
        A heuristic function that estimates the cost of the current board.
        Counts how many cells in the path touches another colored path
        :param path: The current path we want to color
        :param board: The current board
        :return: The number of cells in the path that touches another colored path
        """
        counter = 0
        for x, y in path:
            flag = False
            if x + 1 < board.get_height():
                if board.is_colored_cell(x + 1, y):
                    flag = True
            if x - 1 >= 0:
                if board.is_colored_cell(x - 1, y):
                    flag = True
            if y + 1 < board.get_width():
                if board.is_colored_cell(x, y + 1):
                    flag = True
            if y - 1 >= 0:
                if board.is_colored_cell(x, y - 1):
                    flag = True
            if flag:
                counter += 1
        return (-1) * (counter + 1)


class StickToPathsOrWalls:
    def __init__(self, init_board=None):
        self.stick_to_walls = StickToWalls()
        self.stick_to_other_paths = StickToOtherPaths()

    def cost(self, board, path):
        return max(self.stick_to_walls.cost(board, path), self.stick_to_other_paths.cost(board, path))


class AllHeuristics:
    def __init__(self, init_board=None):
        self.stick_to_walls = StickToWalls()
        self.stick_to_other_paths = StickToOtherPaths()
        self.count_possible_paths = CountPossiblePaths()
        self.stick_to_path_or_wall = StickToPathsOrWalls()

    def cost(self, board, path):
        """
        A heuristic function that estimates the cost of the current board.
        Combines different heuristics in different weights
        :param path:
        :param board: The current board
        :return: The linear combination of all the heuristics used
        """
        return (10 * self.stick_to_walls.cost(board, path) +
                5 * self.stick_to_other_paths.cost(board, path) +
                1 * self.count_possible_paths.cost(board, path) +
                15 * self.stick_to_path_or_wall.cost(board, path))


class MachineLearning:
    def __init__(self, init_board):
        self.predictor = Predictor(init_board)

    def cost(self, board, path):
        """

        :param board:
        :param path:
        :return:
        """
        cost = self.predictor.predict(path)
        print(cost)
        # For predictor, higher is better, for heuristics lower is better
        return (-1) * cost


heuristics_dict = {
    "Null heuristic": NullHeuristic,
    "Count possible paths": CountPossiblePaths,
    "Stick to walls": StickToWalls,
    "Stick to other paths": StickToOtherPaths,
    "Stick to path or wall": StickToPathsOrWalls,
    'Linear combination': AllHeuristics,
    "Machine learning": MachineLearning
}
