import xmltodict


def get_xml_from_path(path):
    """
    Create dictionary with the following items:
    name - Puzzle name
    width - Puzzle width
    height - Puzzle height
    colors - List of RGB values [str]
    paths - dictionary where the keys are the colors and the values are
    lists of lists of paths in the key color
    { RED : [[(i1,j1), (i2,j2)...], [(i3,j3), (i4, j4)...]...]}
    :param path: Path to xml file
    :return: The above dictionary
    """
    with open(path, 'rb') as file:
        my_dict = dict(xmltodict.parse(file)['puzzle'])
        ret_dict = {
            'name': my_dict['header']['properties']['text']['#text'],
            'width': int(my_dict['data']['dimensions']['@width']),
            'height': int(my_dict['data']['dimensions']['@height']),
            'colors': [],
            'paths': dict()
        }

        color_dict = my_dict['data']['palette']['color']
        color_list = create_colors_list(color_dict)
        ret_dict['colors'] = color_list

        path_dict = my_dict['data']['solution']['path']
        paths_dict = create_paths_dict(path_dict, color_list)
        ret_dict['paths'] = paths_dict

        return ret_dict


def create_paths_dict(paths_dict, color_list):
    """
    Creates a dictionary {"color" : [paths]}
    :param color_list:
    :param paths_dict:
    :return:
    """
    result = {i: [] for i in range(len(color_list))}
    for i in range(len(paths_dict)):
        str_path = paths_dict[i]['#text']
        color = int(paths_dict[i]['@color'])
        result[color].append(create_tuple_path(str_path))
    return result


def create_tuple_path(str_path):
    """
    Gets a path as a string - for example : '1 2 3 4' and creates a list of tuples.
    :param str_path:
    :return: a list of tuples - [(1,2), (3,4)]
    """
    result = []
    path_list = str_path.split()
    for i in range(0, len(path_list), 2):
        result.append((int(path_list[i + 1]), int(path_list[i])))
    return result


def create_colors_list(color_dict):
    """
    extract the colors from their section in the xml file, and puts them in a list
    :param color_dict:
    :return: the list of the colors
    """
    ret = []
    for i in range(len(color_dict)):
        ret.append('#' + color_dict[i]['@rgb'])
    return ret


# def readCommand(args):
#     pass


# def runGames(args):
#     # self.path = path
#     # self.gui = GUI()
#     # self.game = Game(get_xml_from_path(path))
#     # self.board = game.get_initial_board()
#     # self.heuristic = heuristic
#     # self.search = search
#     # self.result = search(game, heuristic)
#     # self.expand = 0
#     pass


def calc_err_rate(self):
    pass


def calc_succ_rate(self):
    pass


def get_runtime(self):
    pass
