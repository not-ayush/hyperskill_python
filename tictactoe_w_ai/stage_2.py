import random

'''
stage 2
make the game playable (user vs comp), easy mode, computer makes random moves
loop:
    X is user (starts), O is comp
    make user move, display
    check game state,exit program if someone wins or draw
    say making move, and make the comp's move
        check make a tuple of empty indices on the board
        make random choice
        move 
    display
    check game state, exit program if someone wins or draw
'''

board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']]


def print_board():
    print(f'''
---------
| {board[0][0]} {board[0][1]} {board[0][2]} |
| {board[1][0]} {board[1][1]} {board[1][2]} |
| {board[2][0]} {board[2][1]} {board[2][2]} |
---------''')


print_board()


def make_users_move():  # asks what move, check correct move, print board, makes user's move
    coord_inp = input('Enter the coordinates: ')
    while not check_vaild_move(coord_inp):
        coord_inp = input('Enter the coordinates: ')
    coords = coord_inp.split(' ')
    board[int(coords[0]) - 1][int(coords[1]) - 1] = "X"
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


def check_win(b: list):  # returns the mark that won, or None
    winner = None
    # rows, columns
    for r in range(3):
        if b[r][0] == b[r][1] == b[r][2] == 'X':
            winner = 'X'
        elif b[r][0] == b[r][1] == b[r][2] == 'O':
            winner = 'O'
    for c in range(3):
        if b[0][c] == b[1][c] == b[2][c] == 'X':
            winner = 'X'
        elif b[0][c] == b[1][c] == b[2][c] == 'O':
            winner = 'O'
    # diagonals
    if (b[0][0] == b[1][1] == b[2][2] == 'X') or (b[0][2] == b[1][1] == b[2][0] == 'X'):
        winner = 'X'
    elif (b[0][0] == b[1][1] == b[2][2] == 'O') or (b[0][2] == b[1][1] == b[2][0] == 'O'):
        winner = 'O'
    return winner


def check_empty(b: list):  # return true if
    empty = False
    for row in b:
        for elem in row:
            if elem == ' ':
                empty = True
    return empty


def check_game_state():
    # if not check_win(board) and check_empty(board):
    #     return 'Game not finished'
    if not check_win(board) and not check_empty(board):
        return 'Draw'
    elif check_win(board):
        return f'{check_win(board)} wins'


def return_empty_places():
    empty_indices = []
    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                empty_indices.append((r, c))
    return empty_indices


for i in range(9):  # start game
    if i % 2 == 0:  # user's turn
        make_users_move()
        game_state = check_game_state()
        if game_state:
            print(game_state)
            break
    else:  # computer's turn
        comp_choice = random.choice(return_empty_places())
        print('Making move level "easy"')
        board[comp_choice[0]][comp_choice[1]] = 'O'
        print_board()
        game_state = check_game_state()
        if game_state:
            print(game_state)
            break
