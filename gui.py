import os

import PySimpleGUI as sg

from texts import *

# MAX_BOARD_SIZE = 5
#
#
# def get_board_layout(size):
#     layout = []
#     for i in range(size):
#         layout += [[sg.Text(key=(i, j), pad=(0, 0), size=(1, 1), background_color='white',
#                             text_color='white', visible=True) for j in range(size)]]
#
#     return layout
#
#
# def build_layout_from_board(window, board, colors):
#     w = len(board)
#     h = len(board[0])
#
#     for i in range(MAX_BOARD_SIZE):
#         for j in range(MAX_BOARD_SIZE):
#             window.finalize()
#             if i < w and j < h:
#                 cell = board[i][j]
#                 if cell[0] == 0:
#                     window[(i, j)](visible=True, value='', background_color=colors[cell[1]])
#                 else:
#                     window[(i, j)](visible=True, value=str(cell[0]),
#                                    background_color=colors[cell[1]])
#
#             else:
#                 window[(i, j)](visible=False, value='', background_color='white')


GRAPH_HEIGHT = 100.0
GRAPH_WIDTH = 100.0


class BoardGraph:
    def __init__(self, graph: sg.Graph, board: list, colors: list, w: int, h: int):
        self.graph = graph
        self.board_numbers = board
        self.colors = colors
        self.board_colors = dict()
        self.w = w
        self.h = h

        self.draw_board_borders()
        self.draw_board_numbers()

    def draw_board_borders(self):
        h_offset = GRAPH_HEIGHT / self.h
        w_offset = GRAPH_WIDTH / self.w

        curr_h = 0
        for i in range(self.h):
            curr_w = 0
            for j in range(self.w):
                self.board_colors[(i, j)] = self.graph.DrawRectangle(
                    top_left=(curr_h + 1, curr_w + 1),
                    bottom_right=(curr_h + h_offset,
                                  curr_w + w_offset),
                    fill_color=self.colors[0],
                    line_color='gray', line_width=2)

                self.graph.send_figure_to_back(self.board_colors[(i, j)])

                curr_w += w_offset
            curr_h += h_offset

    def draw_board_numbers(self):
        h_offset = GRAPH_HEIGHT / self.h
        w_offset = GRAPH_WIDTH / self.w

        for i in range(self.h):
            for j in range(self.w):
                cell = self.board_numbers[i][j]
                if cell[0] != 0:
                    print('i', i, 'j', j)
                    text = self.graph.DrawText(text=str(cell[0]), color='white',
                                               location=((h_offset + 1) * i + (h_offset / 2),
                                                         (w_offset + 1) * j + (w_offset / 2))
                                               )
                    self.graph.bring_figure_to_front(text)
                    self.board_colors[(i, j)].SetColor(self.colors[cell[1]])

    def drew_colors_on_board(self, x, y, color_index):
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
            sg.Radio(key='radio_ai_build', text=RADIO_AI_BUILD_MODE, group_id=MODE_GROUP_ID),
            sg.Radio(key='radio_human', text=RADIO_HUMAN_MODE, group_id=MODE_GROUP_ID),
        ],
        [
            sg.InputText(key='file_path', enable_events=True, visible=False),
            sg.FileBrowse(button_text=FILE_BROWSER_TEXT, initial_folder='./boards', size=(14, 1)),
            sg.Text(FILE_SELECTED_TEXT),
            sg.Text(key='text_puzzle_name', size=(80, 1), text=NO_PUZZLE_SELECTED_TEXT)
        ],
        [
            sg.Text(AI_MODE),
            sg.Combo(key='combo_select', values=DROP_DOWN_SEARCH_LIST,
                     default_value='Select search type', readonly=True, text_color='black'),
            sg.Combo(key='combo_heuristic', values=DROP_DOWN_HEURISTIC_LIST,
                     default_value='Select heuristic', readonly=True, text_color='black')
        ],
        [sg.HorizontalSeparator()],
        [
            sg.Button(key='button_resume', button_text=BUTTON_RESUME_TEXT, size=(8, 1)),
            sg.Button(key='button_pause', button_text=BUTTON_PAUSE_TEXT, size=(8, 1)),
            sg.Button(key='button_reset', button_text=BUTTON_RESET_TEXT, size=(8, 1)),

            sg.Sizer(400),

            sg.Text(SLIDER_SPEED_TEXT),
            sg.Slider(key='slider_speed', range=(0, 2), default_value=0, resolution=1,
                      orientation='h', disable_number_display=True)
        ],
        [
            sg.Graph(key='graph_board', enable_events=True, float_values=True,
                     canvas_size=(300, 300),
                     graph_top_right=(GRAPH_WIDTH, 0), graph_bottom_left=(0, GRAPH_HEIGHT),
                     background_color='white')

            # sg.Frame(key='frame_board', title='', layout=get_board_layout(MAX_BOARD_SIZE),
            #          size=(1100, 400),
            #          background_color='white', element_justification='center')
        ],
        [sg.HorizontalSeparator()],
        [sg.Text(STATS_TEXT)],
        [
            sg.Output(key='textbox_stats', size=(155, 10))
        ]
    ]

    runGUI(layout)


def get_paths(x, y, end_x, end_y):
    """

    :param x:
    :param y:
    :param end_x:
    :param end_y:
    :return:
    """
    pass

def get_possable_paths(self, x, y):
    """

    :param self:
    :param x:
    :param y:
    :return:
    """
    # odd numbers must have odd manhattan distance between start and end
    # even numbers must have even manhattan distance between start and end
    paths = []
    length = self.get_number_in_cell(x, y)

    # If no path
    if length == 0:
        print(f"Got x: {x}, y:{y}, but cell ({x}, {y}) has no number!")
        return None

    # This loop will only check possible end coordinates for the path
    offset = length % 2 == 0
    # for every possible x
    for i in range(length + 1):
        # and every other y
        for j in range(offset, length - i, 2):
            # if not (0, 0) AND has the same number in end positions, return all possible paths
            if (i != 0 or j != 0)
                continue
            end_x = x + i
            end_y = y + j
            if self.get_number_in_cell(   end_x,  end_y) == length:
                paths += get_paths(x, y,  end_x,  end_y)
            if self.get_number_in_cell(  -end_x,  end_y) == length:
                paths += get_paths(x, y, -end_x,  end_y)
            if self.get_number_in_cell(   end_x, -end_y) == length:
                paths += get_paths(x, y,  end_x, -end_y)
            if self.get_number_in_cell(  -end_x, -end_y) == length:
                paths += get_paths(x, y, -end_x, -end_y)
                
        offset = not offset

    return paths