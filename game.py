

class Game:
    def __init__(self, file):
        """
        :param file: XML file that represents the board
        """
        # TODO represent the board as coordinates
        self.initial_board = None
        self.board = None
        self.goal_board = None
        
    def __str__(self):
        """
        prints the board
        :return:
        """
        pass
    
    def get_initial_board(self):
        return self.initial_board
    
    def get_current_board(self):
        """
        returns the current board object
        :return:
        """
        pass

    def get_all_possible_actions(self, x, y):
        pass
    
    def get_possible_actions(self, all_possible_actions):
        pass
    
    def get_successors(self, cur_state, possible_actions):
        pass
    
    def is_goal_state(self):
        return self.board == self.goal_board
    
    # def do_action(self, cur_state, action):
    #     """
    #     move
    #     :param action:
    #     :return:
    #     """
    #     pass