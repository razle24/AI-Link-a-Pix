import os

import PySimpleGUI as sg

from texts import *


def build_layout_from_board(board):
    w = len(board)
    h = len(board[0])

    layout = 1

    return layout


def update_layout_from_board():
    pass


def runGUI(layout):
    # https://user-images.githubusercontent.com/46163555/70382042-796da500-1923-11ea-8432-80d08cd5f503.jpg
    sg.theme('LightBrown7')

    # Create the Window
    window = sg.Window(APP_NAME, layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        # If user closes window, close the program
        if event == sg.WIN_CLOSED:
            break

        # If player loads a file
        if event == 'file_path':
            print('File selected:', values['file_path'])
            window['text_puzzle_name'](os.path.basename(values['file_path']))

        # if event == 'Run':

    window.close()


if __name__ == '__main__':
    # Tuple of ((number, number color), color drawn). None means no number.
    # Board should look like:
    # 3  2  2
    # _  1  _
    # 3  b  r
    board_test = [
        [((3, 2), 0), ((2, 1), 0), ((2, 1), 0)],
        [(None, 0), ((1, 2), 0), (None, 0)],
        [((3, 2), 0), (None, 1), (None, 2)]
    ]
    colors_test = ['white', 'black', 'red']

    puzzle_file_name = NO_PUZZLE_SELECTED_TEXT
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
            sg.Text(key='text_puzzle_name', size=(80, 1), enable_events=True, text=puzzle_file_name)
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
            sg.Button(BUTTON_RESUME_TEXT, size=(8, 1)),
            sg.Button(BUTTON_PAUSE_TEXT, size=(8, 1)),
            sg.Button(BUTTON_RESET_TEXT, size=(8, 1)),

            sg.Sizer(400),

            sg.Text(SLIDER_SPEED_TEXT),
            sg.Slider(key='silder_speed', range=(0, 2), default_value=0, resolution=1,
                      orientation='h', disable_number_display=True)
        ],
        [
            sg.Graph(key='graph_game_board', canvas_size=(1100, 400), graph_bottom_left=(0, 0),
                     graph_top_right=(1100, 400), background_color='white')
        ],
        [sg.HorizontalSeparator()],
        [sg.Text(STATS_TEXT)],
        [
            sg.Output(key='textbox_stats', size=(155, 10))
        ]
    ]

    runGUI(layout)
