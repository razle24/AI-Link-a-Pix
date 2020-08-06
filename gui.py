import os

import PySimpleGUI as sg

import agent as ag
import game as gm
from heuristics import heuristics_dict
from search import search_dict
from texts import *
from variable_selection import variable_selection_dict

GRAPH_SIZE = 700
MAX_SIZE_TO_SHOW_NUMBERS = 25


def toggle_gui(window, toggle):
    toggle = not toggle
    window['file_selector'].update(disabled=toggle)
    window['combo_search'].update(disabled=toggle)
    window['combo_variable'].update(disabled=toggle)
    window['combo_heuristic'].update(disabled=toggle)
    window['button_run'].update(disabled=toggle)
    window['button_reset'].update(disabled=toggle)
    window['checkbox_show_animation'].update(disabled=toggle)


# *** CSP *** #
def run_paths_based_search_with_animation(window, graph, game):
    while not game.is_goal_state():
        path, color = game.do_move_csp()

        for cell in path:
            window.finalize()
            graph.drew_color_on_board(cell[0], cell[1], graph.colors[color])

        window.finalize()
        window['turn_counter'].update(str(game.get_moves_counter()))


def run_paths_based_search_without_animation(window, graph, game):
    while not game.is_goal_state():
        game.do_move_csp()
        window.finalize()
        window['turn_counter'].update(str(game.get_moves_counter()))

    matrix = game.get_current_coloring_matrix()
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            window.finalize()
            graph.drew_color_on_board(i, j, graph.colors[matrix[i][j]])


# *** A Star *** #
def run_board_based_search_with_animation(window, graph, game):
    while not game.is_goal_state():
        matrix = game.do_move_a_star()

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                window.finalize()
                graph.drew_color_on_board(i, j, graph.colors[matrix[i][j]])

        window.finalize()
        window['turn_counter'].update(str(game.get_moves_counter()))


def run_board_based_search_without_animation(window, graph, game):
    while not game.is_goal_state():
        game.do_move_a_star()
        window.finalize()
        window['turn_counter'].update(str(game.get_moves_counter()))

    matrix = game.get_current_coloring_matrix()
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            window.finalize()
            graph.drew_color_on_board(i, j, graph.colors[matrix[i][j]])


class BoardGraph:
    """
    The board's GUI class
    """

    def __init__(self, graph: sg.Graph, game: gm.Game):
        # GUI object, contains canvas to print board to
        self.graph = graph
        # Contains logic and board state after each move
        self.game = game

        # Board width
        self.w = self.game.get_width()
        # Board height
        self.h = self.game.get_height()

        # Get list with all color rgb values
        self.colors = game.get_colors()

        # 2D array (w*h) contains tuples of ((number, number_color), color) of the board
        self.board = self.game.get_current_numbers_matrix()

        # Dictionary of canvas items, each (x, y) is the key of the correspond item on the canvas
        self.canvas_background = dict()
        self.canvas_numbers = dict()

        self.cell_size = min(GRAPH_SIZE / self.h, GRAPH_SIZE / self.w, 25)

        self.draw_board_borders()
        self.draw_board_numbers()

    def draw_board_borders(self):
        """
        Draws the board borders
        :return:
        """
        curr_w = 0
        for i in range(self.h):
            curr_h = 0
            for j in range(self.w):
                self.canvas_background[(i, j)] = self.graph.DrawRectangle(
                    top_left=(curr_h + 1, curr_w + 1),
                    bottom_right=(curr_h + self.cell_size,
                                  curr_w + self.cell_size),
                    fill_color=self.colors[0],
                    line_color='gray', line_width=2)

                self.graph.send_figure_to_back(self.canvas_background[(i, j)])

                curr_h += self.cell_size
            curr_w += self.cell_size

    def draw_board_numbers(self):
        """
        Draws the numbers on the board
        """
        for i in range(self.h):
            for j in range(self.w):
                cell = self.board[i][j]
                if cell[0] != 0:
                    self.canvas_numbers[(i, j)] = self.graph.DrawText(text=str(cell[0]),
                                                                      color=self.colors[cell[1]],
                                                                      location=(
                                                                          (self.cell_size * j + (self.cell_size / 2)),
                                                                          (self.cell_size * i + (self.cell_size / 2))))

                    self.graph.bring_figure_to_front(self.canvas_numbers[(i, j)])

    def drew_color_on_board(self, x, y, rgb_color):
        """
        Gets a coordinate (x, y) and colors it on the board with the given color.
        :param x:
        :param y:
        :param rgb_color:
        :return:
        """
        self.graph.tk_canvas.itemconfigure(self.canvas_background[(x, y)], fill=rgb_color)

        # The cell also has number, we also need to change the color to the text
        if self.board[x][y][0] != 0:
            if rgb_color == '#ffffff':
                color = self.colors[self.board[x][y][1]]
                self.graph.tk_canvas.itemconfigure(self.canvas_numbers[(x, y)], fill=color)
            else:
                self.graph.tk_canvas.itemconfigure(self.canvas_numbers[(x, y)], fill='white')

    def clear_board(self):
        for cell in self.canvas_background:
            self.graph.tk_canvas.itemconfigure(self.canvas_background[cell], fill='white')

        for number in self.canvas_numbers:
            self.graph.tk_canvas.itemconfigure(self.canvas_numbers[number], fill='black')


def runGUI(layout):
    """
    Runs the GUI.
    :param layout:
    """
    # Create the Window
    window = sg.Window(APP_NAME, layout)
    game = None
    graph = None

    # Event Loop to process 'events' and get the 'values' of the inputs
    while True:
        event, values = window.read()

        # If user closes window, close the program
        if event == sg.WIN_CLOSED:
            break

        # If player selects file, update GUI to show file name
        if event == 'file_path':
            print('File selected:', values['file_path'])

            # Show file in GUI
            window['text_puzzle_name'](os.path.basename(values['file_path']))

            # Create game object
            xml_dict = ag.get_xml_from_path(values['file_path'])
            game = gm.Game(xml_dict)

            # Create board in GUI
            window['graph_board'].erase()
            graph = BoardGraph(window['graph_board'], game)

        # Start run the game with given parameters
        if event == 'button_run':
            print('button_run')

            if values['file_path'] != '':
                # Disable buttons on GUI while running the search
                toggle_gui(window, False)

                # Set game to run
                game.set_boards_generator(values['combo_search'], values['combo_variable'], values['combo_heuristic'])

                # Select search, we scarified here generality for performance, since this is the core to the search
                # and we wanted to avoid unnecessary 'if' statements each iteration
                if values['checkbox_show_animation']:
                    if values['combo_search'] == 'CSP':
                        run_paths_based_search_with_animation(window, graph, game)
                    if values['combo_search'] == 'A*':
                        run_board_based_search_with_animation(window, graph, game)
                else:
                    if values['combo_search'] == 'CSP':
                        run_paths_based_search_without_animation(window, graph, game)
                    if values['combo_search'] == 'A*':
                        run_board_based_search_without_animation(window, graph, game)

                window.finalize()
                window['button_reset'].update(disabled=False)

            else:
                print(FILE_NOT_SELECTED_MESSAGE)

        if event == 'button_reset':
            game.reset_game()
            graph.clear_board()

            window.finalize()
            toggle_gui(window, True)
            window['button_reset'].update(disabled=True)

        if event == 'graph_board':
            x, y = values["graph_board"]
            print(f'Clicked on x: {x}\t y: {y}')
            print(f'Figures in location {window["graph_board"].get_figures_at_location((x, y))}')

    window.close()


if __name__ == '__main__':
    # List of themes:
    # https://user-images.githubusercontent.com/46163555/70382042-796da500-1923-11ea-8432-80d08cd5f503.jpg

    # Needs to be first line of code for all elements to get this theme
    sg.theme('LightBrown7')

    search_list = [item for item in search_dict]
    variable_selection_list = [item for item in variable_selection_dict]
    heuristics_list = [item for item in heuristics_dict]

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
            sg.FileBrowse(key='file_selector', button_text=FILE_BROWSER_TEXT, initial_folder='./boards', size=(14, 1)),
            sg.Text(FILE_SELECTED_TEXT),
            sg.Text(key='text_puzzle_name', size=(50, 1), text=NO_PUZZLE_SELECTED_TEXT)
        ],
        [
            sg.Text(AI_MODE),
            sg.Combo(key='combo_search', values=search_list, text_color='black',
                     default_value=search_list[0], readonly=True, size=(16, 1)),
            sg.Combo(key='combo_variable', values=variable_selection_list, text_color='black',
                     default_value=variable_selection_list[0], readonly=True, size=(16, 1)),
            sg.Combo(key='combo_heuristic', values=heuristics_list, text_color='black',
                     default_value=heuristics_list[0], readonly=True, size=(25, 1))
        ],
        [sg.HorizontalSeparator()],
        [
            sg.Button(key='button_run', button_text=BUTTON_RUN_TEXT, size=(8, 1)),
            sg.Button(key='button_reset', button_text=BUTTON_RESET_TEXT, size=(8, 1), disabled=True),
            sg.Checkbox(key='checkbox_show_animation', text=SHOW_ANIMATION_CHECKBOX_TEXT, default=True),
            sg.Sizer(320),
            sg.Text(TURN_COUNTER_TEXT),
            sg.Text(0, key='turn_counter', size=(5, 1))
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
            # TODO: uncomment when done debugging
            # sg.Output(key='textbox_stats', size=(100, 10))
        ]
    ]

    runGUI(layout)
