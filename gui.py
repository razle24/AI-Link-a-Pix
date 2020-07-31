import os

import PySimpleGUI as sg
from util import manhattan_distance

from texts import *

GRAPH_SIZE = 420


class BoardGraph:
    def __init__(self, graph: sg.Graph, board: list, colors: list, w: int, h: int):
        self.graph = graph
        self.board_numbers = board
        self.colors = colors
        self.board_colors = dict()
        self.w = w
        self.h = h
        self.cell_size = min(GRAPH_SIZE / self.h, GRAPH_SIZE / self.w, 25)

        self.draw_board_borders()
        self.draw_board_numbers()

    def draw_board_borders(self):
        curr_h = 0
        for i in range(self.h):
            curr_w = 0
            for j in range(self.w):
                self.board_colors[(i, j)] = self.graph.DrawRectangle(
                    top_left=(curr_h + 1, curr_w + 1),
                    bottom_right=(curr_h + self.cell_size,
                                  curr_w + self.cell_size),
                    fill_color=self.colors[0],
                    line_color='gray', line_width=2)

                self.graph.send_figure_to_back(self.board_colors[(i, j)])

                curr_w += self.cell_size
            curr_h += self.cell_size

    def draw_board_numbers(self):
        for i in range(self.h):
            for j in range(self.w):
                cell = self.board_numbers[i][j]
                if cell[0] != 0:
                    print('i', i, 'j', j)
                    fig = self.graph.DrawText(text=str(cell[0]), color=colors_test[cell[1]],
                                              location=((self.cell_size * i + (self.cell_size / 2)),
                                              (self.cell_size * j + (self.cell_size / 2))))

                    self.graph.bring_figure_to_front(fig)

    def drew_color_on_board(self, x, y, color):
        cell = self.board_numbers[i][j]
        if cell[0] == 0:
            pass
        else:
            pass


colors_test = ['white', 'black', 'red']
# Tuple of (number, color drawn). if 'number'!=0 the second value is number's color.
# (0, 0) - Empty cell
# (0, 1) - No number, colored black
# (2, 1) - Number shown is 2, its color is black
# (1, 0) = Invalid option
board_test = [
    [(3, 2), (2, 1), (2, 1)],
    [(0, 0), (1, 2), (0, 0)],
    [(3, 2), (0, 1), (0, 2)],
    [(0, 0), (0, 0), (0, 0)]
]


def runGUI(layout):
    # Create the Window
    window = sg.Window(APP_NAME, layout, finalize=True)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        # If user closes window, close the program
        if event == sg.WIN_CLOSED:
            break

        # If player selects file, update to GUI to show file name
        if event == 'file_path':
            print('File selected:', values['file_path'])

            # Show file in GUI
            window['text_puzzle_name'](os.path.basename(values['file_path']))

            # Create board in GUI
            graph = BoardGraph(window['graph_board'], board_test, colors_test,
                               len(board_test[0]), len(board_test))

        if event == 'button_resume':
            print('button_resume')
            graph = BoardGraph(window['graph_board'], board_test, colors_test,
                               len(board_test[0]), len(board_test))


        if event == 'button_pause':
            print('button_pause')

        if event == 'button_reset':
            print('button_reset')

        if event == 'graph_board':
            print(f'Clicked on x: {values["graph_board"][0]}\t y: {values["graph_board"][1]}')

    window.close()


if __name__ == '__main__':
    # List of themes:
    # https://user-images.githubusercontent.com/46163555/70382042-796da500-1923-11ea-8432-80d08cd5f503.jpg

    # Needs to be first line of code for all elements to get this theme
    sg.theme('LightBrown7')

    layout = [
        [
            sg.Text(GAME_MODE_TEXT),

            sg.Radio(key='radio_ai_play', text=RADIO_AI_PLAY_MODE, group_id=MODE_GROUP_ID,
                     default=True),
            sg.Radio(key='radio_ai_build', text=RADIO_AI_BUILD_MODE, group_id=MODE_GROUP_ID,
                     disabled=True),
            sg.Radio(key='radio_human', text=RADIO_HUMAN_MODE, group_id=MODE_GROUP_ID,
                     disabled=True)
        ],
        [
            sg.InputText(key='file_path', enable_events=True, visible=False),
            sg.FileBrowse(button_text=FILE_BROWSER_TEXT, initial_folder='./boards', size=(14, 1)),
            sg.Text(FILE_SELECTED_TEXT),
            sg.Text(key='text_puzzle_name', size=(50, 1), text=NO_PUZZLE_SELECTED_TEXT)
        ],
        [
            sg.Text(AI_MODE),
            sg.Combo(key='combo_select', values=DROP_DOWN_SEARCH_LIST, text_color='black',
                     default_value='Select search type', readonly=True),
            sg.Combo(key='combo_heuristic', values=DROP_DOWN_HEURISTIC_LIST, text_color='black',
                     default_value='Select heuristic', readonly=True)
        ],
        [sg.HorizontalSeparator()],
        [
            sg.Button(key='button_resume', button_text=BUTTON_RESUME_TEXT, size=(8, 1)),
            sg.Button(key='button_pause', button_text=BUTTON_PAUSE_TEXT, size=(8, 1)),
            sg.Button(key='button_reset', button_text=BUTTON_RESET_TEXT, size=(8, 1))

            # sg.Sizer(400),
            #
            # sg.Text(SLIDER_SPEED_TEXT),
            # sg.Slider(key='slider_speed', range=(0, 2), default_value=0, resolution=1,
            #           orientation='h', disable_number_display=True)
        ],
        [
            sg.Graph(key='graph_board', enable_events=True, float_values=True,
                     canvas_size=(GRAPH_SIZE, GRAPH_SIZE),
                     graph_top_right=(GRAPH_SIZE, 0), graph_bottom_left=(0, GRAPH_SIZE),
                     background_color='white')
        ],
        [sg.HorizontalSeparator()],
        [sg.Text(STATS_TEXT)],
        [
            sg.Output(key='textbox_stats', size=(100, 10))
        ]
    ]

    runGUI(layout)


def get_paths(self, path, end_x, end_y, steps):
    """

    :param x:
    :param y:
    :param end_x:
    :param end_y:
    :return:
    """
    if end_x < 0 or self.w <= end_x or end_y < 0 or self.h <= end_y:
        return {}

    return get_paths_rec(path, end_x, end_y, steps)


def get_paths_rec(self, current_path, end_x, end_y, steps):
    x, y = current_path[-1]

    # If end is too far for path, don't try going there
    if manhattan_distance((x, y), (end_x, end_y)) > steps:
        return {}

    # If end of steps
    if steps == 0:
        # And got to end, return path found
        if current_path[-1] == (end_x, end_y):
            return {current_path}
        # Otherwise, path don't lead to end
        else:
            return set()

    # collect valid paths from this point
    paths = {}
    possible_steps = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    for possible_step in possible_steps:
        # If point not on board or point already in path, skip it
        if possible_step[0] < 0 or self.w <= possible_step[0] or possible_step[1] < 0 or self.h <= possible_step[1]\
                or possible_step in current_path:
            continue

        paths += get_paths_rec(current_path + possible_step, end_x, end_y, steps - 1)

    return paths


def get_possable_paths(self, x, y):
    """

    :param self:
    :param x:
    :param y:
    :return:
    """
    paths = {}
    length = self.get_number_in_cell(x, y)

    # If no path
    if length == 0:
        print(f"Got x: {x}, y:{y}, but cell ({x}, {y}) has no number!")
        return None

    # Odd numbers must have odd manhattan distance between start and end
    # Even numbers must have even manhattan distance between start and end
    # This loop will only check possible end coordinates for the path
    offset = length % 2 == 0
    # For every possible x
    for i in range(length + 1):
        # And every other y such that i + j <= length
        for j in range(offset, length - i, 2):
            end_x = x + i
            end_y = y + j

            if i != 0:
                paths += self.get_paths((x, y), end_x, end_y, length)
                paths += self.get_paths((x, y), -end_x, end_y, length)

                if j != 0:
                    paths += self.get_paths((x, y), end_x, -end_y, length)
                    paths += self.get_paths((x, y), -end_x, -end_y, length)

            elif j != 0:
                paths += self.get_paths((x, y), end_x, end_y, length)
                paths += self.get_paths((x, y), end_x, -end_y, length)

        offset = not offset

    return paths
