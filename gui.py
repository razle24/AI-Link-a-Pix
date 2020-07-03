import PySimpleGUI as sg

from texts import *

if __name__ == '__main__':
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
            sg.InputText(key='file_path', enable_events=True),
            sg.FileBrowse(button_text=FILE_BROWSER_TEXT,
                          initial_folder='./boards', size=(14, 1)),
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

            sg.Text(SLIDER_SPEED_TEXT, size=(40, 1), justification='right'),
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
            sg.Multiline(key='textbox_stats', disabled=True, default_text=SAMPLE_STATS_TEXT,
                         size=(155, 10))
        ]
    ]

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
            # xml = get_xml_from_path(values['file_path'])
            # print(xml['name'])
            print(values['file_path'])

        # if event == 'Run':

    window.close()
