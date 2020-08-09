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

puzzles = [f for f in os.listdir(path_puzzles) if f.startswith('5')]
print(puzzles)


def run(game):
    # Start clock
    start = time()

    # Run search
    while not game.is_goal_state():
        game.do_move_other()
        if time() - start > TIME_OUT:
            print(f'Takes more than {TIME_OUT} seconds. Abort.')
            return -1

    # End clock and print results
    end = time()
    print('Done.')

    return end - start


if __name__ == '__main__':
    for puzzle in puzzles:
        game = Game(get_xml_from_path(path_puzzles + '/' + puzzle))

        with open(path_results + '/' + puzzle[:-4] + 'a_star_time.csv', 'w') as report_time:
            with open(path_results + '/' + puzzle[:-4] + 'a_star_turns.csv', 'w') as report_turns:
                report_time.write(os.path.basename(puzzle))
                report_turns.write(os.path.basename(puzzle))

                for heuristic in heuristics_dict:
                    report_time.write(f',{heuristic}')
                    report_turns.write(f',{heuristic}')

                report_time.write('\n')
                report_turns.write('\n')

                # for variable_selection in variable_selection_dict:
                #     report_time.write(variable_selection)
                #     report_turns.write(variable_selection)

                for heuristic in heuristics_dict:
                    if heuristic is not "Count possible paths":
                        continue
                    print(f'running: {puzzle}, {"Top to bottom"}, {heuristic}. ', end='')
                    game.set_boards_generator('A*', "Top to bottom", heuristic)
                    run_time = run(game)

                    report_time.write(f',{run_time}')
                    report_turns.write(f',{game.get_moves_counter()}')

                    game.reset_game()

                report_time.write('\n')
                report_turns.write('\n')
