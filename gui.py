import os

import PySimpleGUI as sg

from texts import *

MAX_BOARD_SIZE = 5


def get_board_layout(size):
    layout = []
    for i in range(size):
        layout += [[sg.Text(key=(i, j), pad=(0, 0), size=(1, 1), background_color='white',
                            text_color='white', visible=True) for j in range(size)]]

    return layout


def build_layout_from_board(window, board, colors):
    w = len(board)
    h = len(board[0])

    for i in range(MAX_BOARD_SIZE):
        for j in range(MAX_BOARD_SIZE):
            window.finalize()
            if i < w and j < h:
                cell = board[i][j]
                if cell[0] == 0:
                    window[(i, j)](visible=True, value='', background_color=colors[cell[1]])
                else:
                    window[(i, j)](visible=True, value=str(cell[0]),
                                   background_color=colors[cell[1]])

            else:
                window[(i, j)](visible=False, value='', background_color='white')

def update_layout_from_board():
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
            window['text_puzzle_name'](os.path.basename(values['file_path']))
            window['frame_board'](visible=False)
            build_layout_from_board(window, board_test, colors_test)
            window.finalize()
            window['frame_board'].expand(expand_x=True, expand_y=True, expand_row=True)
            window['frame_board'](visible=True)

        if event == 'button_resume':
            print('button_resume')

        if event == 'button_pause':
            print('button_pause')

        if event == 'button_reset':
            print('button_reset')

        # if event == 'Run':

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
            sg.Frame(key='frame_board', title='', layout=get_board_layout(MAX_BOARD_SIZE),
                     size=(1100, 400),
                     background_color='white', element_justification='center')
        ],
        [sg.HorizontalSeparator()],
        [sg.Text(STATS_TEXT)],
        [
            sg.Output(key='textbox_stats', size=(155, 10))
        ]
    ]

    runGUI(layout)
