import random


class Board:
    grid = [[' ', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']]

    def __int__(self):
        self.grid = [[' ', ' ', ' '],
                     [' ', ' ', ' '],
                     [' ', ' ', ' ']]

    def print_board(self):
        print(f'''
    ---------
    | {self.grid[0][0]} {self.grid[0][1]} {self.grid[0][2]} |
    | {self.grid[1][0]} {self.grid[1][1]} {self.grid[1][2]} |
    | {self.grid[2][0]} {self.grid[2][1]} {self.grid[2][2]} |
    ---------''')

    def check_win(self):  # returns the mark that won, or None
        # rows, columns
        for r in range(3):
            if self.grid[r][0] == self.grid[r][1] == self.grid[r][2] == 'X':
                return 'X'
            elif self.grid[r][0] == self.grid[r][1] == self.grid[r][2] == 'O':
                return 'O'
        for c in range(3):
            if self.grid[0][c] == self.grid[1][c] == self.grid[2][c] == 'X':
                return 'X'
            elif self.grid[0][c] == self.grid[1][c] == self.grid[2][c] == 'O':
                return 'O'
        # diagonals
        if (self.grid[0][0] == self.grid[1][1] == self.grid[2][2] == 'X') or (
                self.grid[0][2] == self.grid[1][1] == self.grid[2][0] == 'X'):
            return 'X'
        elif (self.grid[0][0] == self.grid[1][1] == self.grid[2][2] == 'O') or (
                self.grid[0][2] == self.grid[1][1] == self.grid[2][0] == 'O'):
            return 'O'

    def check_empty(self):  # return true if
        empty = False
        for row in self.grid:
            for elem in row:
                if elem == ' ':
                    empty = True
        return empty

    def check_game_state(self):
        if not self.check_win() and not self.check_empty():
            return 'Draw'
        elif self.check_win():
            return f'{self.check_win()} wins'

    def return_empty_places(self):
        empty_indices = []
        for r in range(3):
            for c in range(3):
                if self.grid[r][c] == ' ':
                    empty_indices.append((r, c))
        return empty_indices


def make_users_move(mark: str):  # asks what move, check correct move, makes user's move
    coord_inp = input('Enter the coordinates: ')
    while not check_valid_move(coord_inp):
        coord_inp = input('Enter the coordinates: ')
    index = coord_inp.split(' ')
    board.grid[int(index[0]) - 1][int(index[1]) - 1] = mark


def make_easy_move(mark: str):
    comp_choice = random.choice(board.return_empty_places())
    print('Making move level "easy"')
    board.grid[comp_choice[0]][comp_choice[1]] = mark


def make_med_move(mark: str):
    columns = [[board.grid[0][r], board.grid[1][r], board.grid[2][r]] for r in range(3)]
    rows_check = [row.count('X') == 2 or row.count('O') == 2 for row in board.grid]
    columns_check = [column.count('X') == 2 or column.count('O') == 2 for column in columns]
    d1 = [board.grid[0][0], board.grid[1][1], board.grid[2][2]]
    d2 = [board.grid[0][2], board.grid[1][1], board.grid[2][0]]

    print('Making move level "medium"')
    if any(rows_check) and ' ' in set(board.grid[rows_check.index(True)]):
        r = rows_check.index(True)
        c = board.grid[r].index(' ')
        board.grid[r][c] = mark
    elif any(columns_check) and (' ' in set(columns[columns_check.index(True)])):
        c = columns_check.index(True)
        r = columns[c].index(' ')
        board.grid[r][c] = mark
    elif (d1.count('X') == 2 or d1.count('O') == 2) and ' ' in set(d1):
        n = d1.index(' ')
        board.grid[n][n] = mark
    elif (d2.count('X') == 2 or d2.count('O') == 2) and ' ' in set(d2):
        d2_moves = {0: (0, 2), 1: (1, 1), 2: (2, 0)}
        n = d2.index(' ')
        board.grid[d2_moves[n][0]][d2_moves[n][1]] = mark
    else:
        comp_choice = random.choice(board.return_empty_places())
        board.grid[comp_choice[0]][comp_choice[1]] = mark


move_funcs = {'user': make_users_move, 'easy': make_easy_move, 'medium': make_med_move}


def check_valid_move(index_: str):
    if len(index_) != 3 or (not index_[0].isdigit() and not index_[2].isdigit()):
        print('You should enter numbers!')
    elif index_[0] not in '123' or index_[2] not in '123':
        print('Coordinates should be from 1 to 3!')
    elif board.grid[int(index_[0]) - 1][int(index_[2]) - 1] != ' ':
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
    valid_player = ['user', 'easy', 'medium']
    if command[0] != 'exit' and len(command) != 3:
        return False
    elif command[0] == 'exit':
        return True
    elif (command[0] == 'start') and (command[1] in valid_player and command[2] in valid_player):
        return True


inp_comm = ''

board = Board()

while inp_comm != 'exit':
    player_1 = ''
    player_2 = ''
    inp_comm = input("Input command: ")
    while not check_valid_param():
        print('Bad parameters!')
        inp_comm = input("Input command: ")
    if inp_comm == 'exit':
        break
    player_mode_check()
    # start game
    board.print_board()
    for i in range(9):
        if i % 2 == 0:  # player 1 turn 'X'
            move_funcs[player_1]('X')
            print('X')
            board.print_board()
            game_state = board.check_game_state()
            if game_state:
                print(game_state)
                break
        else:  # player 2 turn  'O'
            move_funcs[player_2]('O')
            print('O')
            board.print_board()
            game_state = board.check_game_state()
            if game_state:
                print(game_state)
                break

'''
STAGE 4 ------------
what needed:
check if two consecutive elements in the grid in any arrangement are same
    checking rows
    checking columns
    checking diagonals
for this I think I'll need to create dictionary and check
so order doesn't matter, but number of things matters
-------
checking diagonals, rows, columns.
changing the appropriate mark
[[' ', 'X', ' '], [' ', 'X', ' '], [' ', 'X', ' ']]

columns = [board.grid[0][r], board.grid[1][r], board.grid[2][r]] for r in range(3)
rows_check = [row.count('X') == 2 or row.count('O') == 2 for row in board.grid]
columns_check = column.count('X') == 2 or column.count('O') == 2 for column in columns
any(rows_check)
any(columnds_check)

[board.grid[0][2], board.grid[1][1], board.grid[2][0]]
[board.grid[0][0], board.grid[1][1], board.grid[2][2]]

so use the any conditions for finding if two are lined
To find where to put the mark
    use the "any" statement list returned true to find what row/column it is in.
    then write a put the mark in place of the

so the final algorithm is:
for rows, columns, first just make a nested list of the rows, columns.
then check using any statemnt if two X or Os are present in any elements of that nested list
if there are, and ' ' is also an element of that element, then put the mark in place of that ' '
    to find the ' ', use the any statement boolean list and the index function
'''
