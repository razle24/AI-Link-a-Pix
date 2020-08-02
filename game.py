import copy
from agent import *
from search import *
from board import *


class Game:
    def __init__(self, xml_dict, search_type=None, heuristic=None):
        """
        :param file: XML file that represents the board
        """
        initial_board = [[((0, 0), 0) for i in range(xml_dict["width"])] for j in range(xml_dict["height"])]
        cur_board = [[((0, 0), 0) for i in range(xml_dict["width"])] for j in range(xml_dict["height"])]
        goal_board = [[((0, 0), 0) for i in range(xml_dict["width"])] for j in range(xml_dict["height"])]
        cur_num_of_colors = len(xml_dict["colors"])

        self.board = Board(cur_num_of_colors, None, cur_board)
        self.initial_board = Board(cur_num_of_colors, None, initial_board)
        self.goal_board = Board(cur_num_of_colors, None, goal_board)

        self.search = search_type
        self.heuristic = heuristic

        self.successors = []
        self.generate_boards(xml_dict)

        self.colors_dict = xml_dict['colors']

    def generate_boards(self, xml_dict):
        for color, paths in xml_dict["paths"].items():
            for path in paths:
                # fill the initial board with the (len,color) of the wanted path
                cur_num = len(path)
                start = path[0]
                end = path[len(path) - 1]
                self.initial_board.state[start[0]][start[1]] = ((cur_num, color), 0)

                # now the we have board to work on
                self.board.state[start[0]][start[1]] = ((cur_num, color), 0)

                # fill the first and last entries of the path in goal board
                self.goal_board.state[start[0]][start[1]] = ((cur_num, color), 0)

    def __str__(self):
        """
        prints the board
        :return:
        """
        print(self.board)

    def get_initial_board(self):
        return self.initial_board

    def set_heuristic(self, heuristic):
        self.heuristic = heuristic

    def get_heuristic(self):
        return self.heuristic

    def get_current_board(self):
        """
        returns the current board object
        :return:
        """
        return self.board.state

    # TODO get_possible_actions
    def get_all_possible_actions(self, x, y):
        pass

    def get_possible_actions(self, all_possible_actions):
        pass

    def set_successors(self, possible_actions):
        successors = []
        for act_pat in possible_actions:
            successors.append(self.get_successor(act_pat))
        self.successors = successors

    def get_successors(self):
        return self.successors

    def get_successor(self, action):
        w = len(self.board[0])
        h = len(self.board)
        result = [[(0, 0) for i in range(w)] for j in range(h)]
        color = self.board[action[0][0]][action[0][1]][1]
        size = len(action)
        result[action[0][0]][action[0][1]] = (size, color)
        result[action[len(action)-1][0]][action[len(action)-1][1]] = (size, color)
        for i, j in action[1: (len(action) - 1)]:
            result[i][j] = (0, color)
        return result

    def set_successor(self, action):
        self.board = self.get_successor(action)

    def is_goal_state(self):
        return self.board == self.goal_board

    def get_width(self):
        return self.initial_board.get_width()

    def get_height(self):
        return self.initial_board.get_height()

    def get_colors(self):
        return self.colors_dict

    # def do_action(self, cur_state, action):
    #     """
    #     move
    #     :param action:
    #     :return:
    #     """
    #     pass

def get_heads(board):
    heads = []
    for i in range(board.board_h):
        for j in range(board.board_w):
            if board.state[i][j][0] != 0 and board.state[i][j][1] != 0:
                heads.append(board.state[i][j])
    return heads

if __name__ == '__main__':
    xml = get_xml_from_path('/Users/razlevi/Documents/Studies/YEAR_2/Semester_B/AI/ai_final_project/boards/small_bw.xml')
    my_game = Game(xml)
    heads = get_heads(my_game.board)
    csp(my_game.board, heads)

