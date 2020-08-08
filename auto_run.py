import os
from time import time
from agent import get_xml_from_path
from game import Game

from search import search_dict
from variable_selection import variable_selection_dict
from heuristics import heuristics_dict

TIME_OUT = 180  # In sec
path_puzzles = './boards'
path_results = './report'

puzzles = [f for f in os.listdir(path_puzzles) if f[0] == '4']

def run(game):
    # Start clock
    print(f'Running {game.game_name}... ', end='')
    start = time()

    # Run search
    while not game.is_goal_state():
        game.do_move_csp()
        if time() - start > TIME_OUT:
            print('Takes more than 3 minutes.')
            print('Abort search.')
            return -1

    # End clock and print results
    end = time()
    print('Done.')

    return end - start


if __name__ == '__main__':
    # CSP
    for puzzle in puzzles:
        with open(path_results + '/' + puzzle[:-4] + '_CSP.txt', 'w') as report:
            game = Game(get_xml_from_path(path_puzzles + '/' + puzzle))

            num = len(game.initial_board.get_list_of_numbered_cells())
            report.write(f'Game name: {game.game_name}\n'
                         f'File name: {os.path.basename(puzzle)}\n'
                         f'Best case for this puzzle: {num}\n'
                         f'Worst case for this puzzle: {2 ** num}\n'
                         '\n'
            )

            for variable_selection in variable_selection_dict:
                for heuristics in heuristics_dict:
                    print(f'File name: {puzzle}')
                    report.write(f'Search: CSP\n'
                                 f'Variable selection: {variable_selection}\n'
                                 f'Heuristics: {heuristics}\n'
                    )

                    game.set_boards_generator('CSP', variable_selection, heuristics)
                    run_time = run(game)

                    report.write(f'Time: {run_time}\n'
                                 f'Number of paths taken: {game.get_moves_counter()}\n\n')

                    game.reset_game()
