from variables import Var


def get_numbered_cells(board):
    cells = []
    for i in range(board.board_w):
        for j in range(board.board_h):
            if board.state[i][j][0] != (0, 0):
                cells += Var((i, j), board.state[i][j][0][0], board.state[i][j][0][1])

    return cells


def row_by_row(board):
    return get_numbered_cells(board)


def low_number_to_high(board):
    return sorted(get_numbered_cells(board), key=lambda var: var.number)


def low_amount_of_possible_paths_to_high(board):
    cells = get_numbered_cells(board)
    for cell in cells:
        cell.legal_paths = board.get_possible_paths(cell.pos[0], cell.pos[1])

    return sorted(cells, key=lambda var: len(var.legal_paths))
