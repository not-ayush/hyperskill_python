import random


class Board:
    grid = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    def __int__(self):
        self.grid = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    def print_board(self):
        print(f'''
    ---------
    | {self.grid[0][0]} {self.grid[0][1]} {self.grid[0][2]} |
    | {self.grid[1][0]} {self.grid[1][1]} {self.grid[1][2]} |
    | {self.grid[2][0]} {self.grid[2][1]} {self.grid[2][2]} |
    ---------''')

    def check_win(self):  # returns the mark that won, or None
        winner = None
        # rows, columns
        for r in range(3):
            if self.grid[r][0] == self.grid[r][1] == self.grid[r][2] == 'X':
                winner = 'X'
            elif self.grid[r][0] == self.grid[r][1] == self.grid[r][2] == 'O':
                winner = 'O'
        for c in range(3):
            if self.grid[0][c] == self.grid[1][c] == self.grid[2][c] == 'X':
                winner = 'X'
            elif self.grid[0][c] == self.grid[1][c] == self.grid[2][c] == 'O':
                winner = 'O'
        # diagonals
        if (self.grid[0][0] == self.grid[1][1] == self.grid[2][2] == 'X') or (
                self.grid[0][2] == self.grid[1][1] == self.grid[2][0] == 'X'):
            winner = 'X'
        elif (self.grid[0][0] == self.grid[1][1] == self.grid[2][2] == 'O') or (
                self.grid[0][2] == self.grid[1][1] == self.grid[2][0] == 'O'):
            winner = 'O'
        return winner

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


board = Board()


def make_users_move(mark: str):  # asks what move, check correct move, makes user's move
    coord_inp = input('Enter the coordinates: ')
    while not check_valid_move(coord_inp):
        coord_inp = input('Enter the coordinates: ')
    coords = coord_inp.split(' ')
    board.grid[int(coords[0]) - 1][int(coords[1]) - 1] = mark


def make_easy_move(mark: str):
    comp_choice = random.choice(board.return_empty_places())
    print('Making move level "easy"')
    board.grid[comp_choice[0]][comp_choice[1]] = mark


move_funcs = {'user': make_users_move, 'easy': make_easy_move}


def check_valid_move(coords_: str):
    if len(coords_) != 3 or (not coords_[0].isdigit() and not coords_[2].isdigit()):
        print('You should enter numbers!')
    elif coords_[0] not in '123' or coords_[2] not in '123':
        print('Coordinates should be from 1 to 3!')
    elif board.grid[int(coords_[0]) - 1][int(coords_[2]) - 1] != ' ':
        print('This cell is occupied! Choose another one!')
    else:
        return True


def player_mode_check():  # check players and update variables
    global player_1, player_2, inp_comm
    command = inp_comm.split(' ')
    player_1 = 'user' if command[1] == 'user' else 'easy'
    player_2 = 'user' if command[2] == 'user' else 'easy'


def check_valid_param():
    global inp_comm
    command = inp_comm.split(' ')
    valid_player = ['user', 'easy']
    if command[0] != 'exit' and len(command) != 3:
        return False
    elif command[0] == 'exit':
        return True
    elif (command[0] == 'start') and (command[1] in valid_player and command[1] in valid_player):
        return True


inp_comm = ''

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
            # make_users_move()
            move_funcs[player_1]('X')
            board.print_board()
            game_state = board.check_game_state()
            if game_state:
                print(game_state)
                break
        else:  # player 2 turn  'O'
            move_funcs[player_2]('O')
            board.print_board()
            game_state = board.check_game_state()
            if game_state:
                print(game_state)
                break
'''
Stage 3
Menu
    while loop for one game each
Choose who plays who
    there are options, who plays X, who plays O, user user; user AI; AI AI
    
exit
'''