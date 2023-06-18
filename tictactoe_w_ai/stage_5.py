import random

board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]


def print_board(board_):
    print(f'''
---------
| {board_[0][0]} {board_[0][1]} {board_[0][2]} |
| {board_[1][0]} {board_[1][1]} {board_[1][2]} |
| {board_[2][0]} {board_[2][1]} {board_[2][2]} |
---------''')


def check_win(board_):  # returns the mark that won, or None
    winner = None
    for r in range(3):
        if board_[r][0] == board_[r][1] == board_[r][2] == 'X':
            winner = 'X'
        elif board_[r][0] == board_[r][1] == board_[r][2] == 'O':
            winner = 'O'
    for c in range(3):
        if board_[0][c] == board_[1][c] == board_[2][c] == 'X':
            winner = 'X'
        elif board_[0][c] == board_[1][c] == board_[2][c] == 'O':
            winner = 'O'
    # diagonals
    if (board_[0][0] == board_[1][1] == board_[2][2] == 'X') or (
            board_[0][2] == board_[1][1] == board_[2][0] == 'X'):
        winner = 'X'
    elif (board_[0][0] == board_[1][1] == board_[2][2] == 'O') or (
            board_[0][2] == board_[1][1] == board_[2][0] == 'O'):
        winner = 'O'
    return winner


def check_empty(board_):  # return true if
    empty = False
    for row in board_:
        for elem in row:
            if elem == ' ':
                empty = True
    return empty


def check_game_state(board_):
    win = check_win(board_)
    if not win and not check_empty(board_):
        return 'Draw'
    elif win:
        return f'{win} wins'


def return_empty_places(board_):
    empty_indices = []
    for r in range(3):
        for c in range(3):
            if board_[r][c] == ' ':
                empty_indices.append((r, c))
    return empty_indices


def player_to_move(board_):
    x_count, o_count = 0, 0
    for row in board_:
        for elem in row:
            if elem == "X":
                x_count += 1
            elif elem == "O":
                o_count += 1
    if x_count == o_count:
        return "X"
    elif x_count > o_count:
        return "O"


def make_users_move(mark: str):  # asks what move, check correct move, makes user's move
    coord_inp = input('Enter the coordinates: ')
    while not check_valid_move(coord_inp):
        coord_inp = input('Enter the coordinates: ')
    index = coord_inp.split()
    board[int(index[0]) - 1][int(index[1]) - 1] = mark


def make_easy_move(mark: str):
    comp_choice = random.choice(return_empty_places(board))
    print('Making move level "easy"')
    board[comp_choice[0]][comp_choice[1]] = mark


def make_med_move(mark: str):
    columns = [[board[0][r], board[1][r], board[2][r]] for r in range(3)]
    rows_check = [row.count('X') == 2 or row.count('O') == 2 for row in board]
    columns_check = [column.count('X') == 2 or column.count('O') == 2 for column in columns]
    d1 = [board[0][0], board[1][1], board[2][2]]
    d2 = [board[0][2], board[1][1], board[2][0]]

    print('Making move level "medium"')
    if any(rows_check) and ' ' in set(board[rows_check.index(True)]):
        r = rows_check.index(True)
        c = board[r].index(' ')
        board[r][c] = mark
    elif any(columns_check) and (' ' in set(columns[columns_check.index(True)])):
        c = columns_check.index(True)
        r = columns[c].index(' ')
        board[r][c] = mark
    elif (d1.count('X') == 2 or d1.count('O') == 2) and ' ' in set(d1):
        n = d1.index(' ')
        board[n][n] = mark
    elif (d2.count('X') == 2 or d2.count('O') == 2) and ' ' in set(d2):
        d2_moves = {0: (0, 2), 1: (1, 1), 2: (2, 0)}
        n = d2.index(' ')
        board[d2_moves[n][0]][d2_moves[n][1]] = mark
    else:
        comp_choice = random.choice(return_empty_places(board))
        board[comp_choice[0]][comp_choice[1]] = mark


def minimax(board_: list, is_maxing: bool = True, depth: int = 0):
    global max_player, min_player
    result = check_game_state(board_)
    if not result:
        best_score = -1000 if is_maxing else 1000
        s = 0
        moves = return_empty_places(board_)
        for m in moves:
            board_[m[0]][m[1]] = max_player if is_maxing else min_player
            s += minimax(board_, not is_maxing, depth + 1)
            if is_maxing:
                best_score = max(s, best_score)
            elif not is_maxing:
                best_score = min(s, best_score)
            board_[m[0]][m[1]] = ' '
        return best_score
    elif result[0] == max_player:
        return 10 - depth
    elif result[0] == min_player:
        return -10 + depth
    elif result == "Draw":
        return 0


def find_best_move(board_: list, player: str):
    moves = return_empty_places(board_)
    best_val = -100
    best_move = (None, None)
    for move in moves:
        board_[move[0]][move[1]] = player
        move_score = minimax(board_, False, 0)
        if move_score > best_val:
            best_val = move_score
            best_move = move
        board_[move[0]][move[1]] = " "
    return best_move


def make_hard_move(mark: str):  # minimax
    best_move = find_best_move(board, mark)
    board[best_move[0]][best_move[1]] = mark
    print('Making move level "hard"')


move_funcs = {'user': make_users_move,
              'easy': make_easy_move,
              'medium': make_med_move,
              'hard': make_hard_move
              }


def check_valid_move(index_: str):
    indices = index_.split()
    if not indices[0].isdigit() and not indices[1].isdigit():
        print('You should enter numbers!')
    elif indices[0] not in '123' or indices[1] not in '123':
        print('Coordinates should be from 1 to 3!')
    elif board[int(indices[0]) - 1][int(indices[1]) - 1] != ' ':
        print('This cell is occupied! Choose another one!')
    else:
        return True


def player_mode_check():  # check players and update variables
    global player_1, player_2, inp_comm
    command = inp_comm.split(' ')
    player_1 = command[1]
    player_2 = command[2]


def check_valid_param():
    global inp_comm
    command = inp_comm.split(' ')
    valid_player = ['user', 'easy', 'medium', 'hard']
    if command[0] != 'exit' and len(command) != 3:
        return False
    elif command[0] == 'exit':
        return True
    elif (command[0] == 'start') and (command[1] in valid_player and command[2] in valid_player):
        return True


inp_comm = ''
max_player, min_player = '', ''

while inp_comm != 'exit' and check_empty(board):
    player_1 = ''
    player_2 = ''
    inp_comm = input("Input command: ")
    players = inp_comm.split(' ')[1:]
    while not check_valid_param():
        print('Bad parameters!')
        inp_comm = input("Input command: ")
    if inp_comm == 'exit':
        break
    player_mode_check()
    # start game
    print_board(board)
    for i in range(9):
        if i % 2 == 0:  # player 1 turn 'X'
            if player_1 == 'hard':
                max_player, min_player = 'X', 'O'
            move_funcs[player_1]('X')
            print_board(board)
            game_state = check_game_state(board)
            if game_state:
                print(game_state)
                break
        else:  # player 2 turn  'O'
            if player_2 == 'hard':
                max_player, min_player = 'O', 'X'
            move_funcs[player_2]('O')
            print_board(board)
            game_state = check_game_state(board)
            if game_state:
                print(game_state)
                break

'''
find_best_move()
    best_move = None
    For each move on the board
        if current_move is better than best move
            return current move


minimax(board, depth, is_maxing)
    if ending:
        handle terminal case
    if maximizing player:
        best_score = -1000
        for each available move on the board:
            move_score = minimax(board, depth + 1, False)
            best_score = max(move_score, best_score)
        return best_score
    elif minimizing player:
        best_score = 1000
        for each available move on the board:
            move_score = minimax(board, depth + 1, True)
            best_score = min(move_score, best_score)
        return best_score
'''