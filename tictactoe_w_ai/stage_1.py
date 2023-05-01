# STAGE 1
# just print the board, make it possible to move
# and add the game status logic

b_inp = input('enter the board (_XXOO_OX_ for example): ').replace('_', ' ')
board = [
    [b_inp[0], b_inp[1], b_inp[2]],
    [b_inp[3], b_inp[4], b_inp[5]],
    [b_inp[6], b_inp[7], b_inp[8]]]


def print_board():
    print(f'''
---------
| {board[0][0]} {board[0][1]} {board[0][2]} |
| {board[1][0]} {board[1][1]} {board[1][2]} |
| {board[2][0]} {board[2][1]} {board[2][2]} |
---------''')


print_board()


def ask_move(mark: str):  # asks what move, check correct move, print board
    coord_inp = input('Enter the coordinates: ')
    while not check_vaild_move(coord_inp):
        coord_inp = input('Enter the coordinates: ')
    coords = coord_inp.split(' ')
    board[int(coords[0]) - 1][int(coords[1]) - 1] = mark
    print_board()


def check_vaild_move(coords_: str):
    if len(coords_) != 3 or (not coords_[0].isdigit() and not coords_[2].isdigit()):
        print('You should enter numbers!')
    elif coords_[0] not in '123' or coords_[2] not in '123':
        print('Coordinates should be from 1 to 3!')
    elif board[int(coords_[0]) - 1][int(coords_[2]) - 1] != ' ':
        print('This cell is occupied! Choose another one!')
    else:
        return True


def return_x_or_o(b:list):
    x_count, o_count = 0, 0

    for row in b:
        for elem in row:
            if elem == 'X': x_count += 1
            elif elem == 'O': o_count += 1

    if x_count == o_count:
        return 'X'
    elif x_count > o_count:
        return 'O'


def check_win(b:list): # returns the mark that won, or None
    winner = None
    # rows, columns
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] == 'X':
            winner = 'X'
        elif b[i][0] == b[i][1] == b[i][2] == 'O':
            winner = 'O'
    for j in range(3):
        if b[0][j] == b[1][j] == b[2][j] == 'X':
            winner = 'X'
        elif b[0][j] == b[1][j] == b[2][j] == 'O':
            winner = 'O'
    # diagonals
    if (b[0][0] == b[1][1] == b[2][2] == 'X') or (b[0][2] == b[1][1] == b[2][0] == 'X'):
        winner = 'X'
    elif (b[0][0] == b[1][1] == b[2][2] == 'O') or (b[0][2] == b[1][1] == b[2][0] == 'O'):
        winner = 'O'
    return winner


def check_empty(b:list): # return true if
    empty = False
    for row in b:
        for elem in row:
            if elem == ' ': empty = True
    return empty


def check_game_state():
    if not check_win(board) and check_empty(board):
        return 'Game not finished'
    elif not check_win(board) and not check_empty(board):
        return 'Draw'
    elif check_win(board):
        return f'{check_win(board)} wins'


ask_move(return_x_or_o(board))
print(check_game_state())