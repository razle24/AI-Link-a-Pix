import sys


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
    pass


# 	tree = etree.parse("some_file.xml")
# 	etree_to_dict(tree.getroot())
#
# 	result = dict()
# 	# result['name'] = tree.puzzle.header.properties.
#
# def etree_to_dict(t):
# 	d = {t.tag: map(etree_to_dict, t.iterchildren())}
# 	d.update(('@' + k, v) for k, v in t.attrib.iteritems())
# 	d['text'] = t.text
# 	return d


def readCommand(args):
    pass


def runGames(args):
    # self.path = path
    # self.gui = GUI()
    # self.game = Game(get_xml_from_path(path))
    # self.board = game.get_initial_board()
    # self.heuristic = heuristic
    # self.search = search
    # self.result = search(game, heuristic)
    # self.expand = 0
    pass


def calc_err_rate(self):
    pass


def calc_succ_rate(self):
    pass


def get_runtime(self):
    pass


if __name__ == '__main__':
    args = readCommand(sys.argv[1:])  # Get game components based on input
    runGames(**args)
# TODO - change
