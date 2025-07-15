import random

# Constants
EMPTY = 1
PLAYER_X = 2
PLAYER_O = 3

def prod(x):
    'Multiplies the elements of a list'
    i = 1
    for j in x:
        i *= j
    return i

def transp(x):
    'Transposes a 3x3 matrix'
    return [[x[i][j] for i in range(3)] for j in range(3)]

def diag1(x):
    'Takes the 1st diagonal of a 3x3 matrix'
    return [x[i][i] for i in range(3)]

def diag2(x):
    'Takes the 2nd diagonal of a 3x3 matrix'
    return [x[i][2 - i] for i in range(3)]

def switch(pl):
    'Maps (1,2) to (2,1) for switching the player'
    return pl % 2 + 1

class Tic:
    'The class of Tic-Tac-Toe boards'

    def __init__(self):
        'Initiates with an empty board and 1st player'
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.player = 1  # takes values 1 or 2

    def __str__(self):
        'Prints the board and whose turn it is'
        dct = {
            EMPTY: " . ",
            PLAYER_X: " X ",
            PLAYER_O: " O "
        }
        dct2 = {
            1: "1 (X)",
            2: "2 (O)"
        }
        return f"""
             1   2   3         
             
         1  {dct[self.board[0][0]]}|{dct[self.board[0][1]]}|{dct[self.board[0][2]]}
            ---+---+---
         2  {dct[self.board[1][0]]}|{dct[self.board[1][1]]}|{dct[self.board[1][2]]}
            ---+---+---
         3  {dct[self.board[2][0]]}|{dct[self.board[2][1]]}|{dct[self.board[2][2]]}
                    Player: {dct2[self.player]}
        """

    def play(self, x, y):
        'A valid move is played with this command'
        self.board[x][y] = self.player + 1
        self.player = switch(self.player)

    def unplay(self, x, y):
        'A move is reversed with this command'
        self.board[x][y] = EMPTY
        self.player = switch(self.player)

    def control(self, x, y):
        'Checks if a proposed move is valid'
        return 0 <= x < 3 and 0 <= y < 3 and self.board[x][y] == EMPTY

    def reset_board(self):
        'Resets the board'
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.player = 1

    def get_player_input(self):
        'Gets input from a human player'
        while True:
            a = input("First coordinate (1-3): ")
            b = input("Second coordinate (1-3): ")
            if a.isdigit() and b.isdigit():
                x = int(a) - 1
                y = int(b) - 1
                if self.control(x, y):
                    self.play(x, y)
                    break
            print("Invalid move. Try again.")

    def win(self):
        'Checks if the game is won/lost'
        check_row_aux = set(map(prod, self.board))
        check_row = 27 in check_row_aux or 8 in check_row_aux
        check_col_aux = set(map(prod, transp(self.board)))
        check_col = 27 in check_col_aux or 8 in check_col_aux
        check_diags = prod(diag1(self.board)) in {27, 8} or prod(diag2(self.board)) in {27, 8}
        return (check_diags or check_row or check_col), switch(self.player)

    def tie(self):
        'Checks if the game is over with a tie'
        return not self.possible_moves() and not self.win()[0]

    def possible_moves(self):
        'Lists the possible moves available'
        return [[i, j] for i in range(3) for j in range(3) if self.board[i][j] == EMPTY]

    def minimax(self, maxpl):
        'Uses the minimax algorithm to decide on the optimal move for the AI with infinite depth and varied symmetry'
        if self.win()[0]:
            return 1 - 2 * maxpl, [-1, -1]
        if self.tie():
            return 0, [-1, -1]

        best_value = -10 if maxpl else 10
        best_moves = []

        for pos_move in self.possible_moves():
            self.play(*pos_move)
            value, _ = self.minimax(not maxpl)
            self.unplay(*pos_move)

            if maxpl:
                if value > best_value:
                    best_value = value
                    best_moves = [pos_move]
                elif value == best_value:
                    best_moves.append(pos_move)
            else:
                if value < best_value:
                    best_value = value
                    best_moves = [pos_move]
                elif value == best_value:
                    best_moves.append(pos_move)

        return best_value, random.choice(best_moves)

    def loop(self):
        'Runs the turns of the game in a loop'
        while True:
            is_win, winner = self.win()
            if is_win or self.tie():
                break
            print(self)
            human_plays = (
                self.mode == "1" or
                (self.mode == "2" and self.player == 1) or
                (self.mode == "3" and self.player == 2)
            )
            if human_plays:
                self.get_player_input()
            else:
                _, move = self.minimax(True)
                self.play(*move)
        print(self)
        is_win, winner = self.win()
        if is_win:
            print("Game over! Player " + str(winner) + " won.")
        else:
            print("Game over! It's a tie.")

    def select_game_mode(self):
        'Asks about the game mode'
        print("""Choose the mode of play:""")
        print("""1 : human vs human""")
        print("""2 : human vs AI""")
        print("""3 : AI vs human""")
        print("""4 : AI vs AI""")
        a = input(" ")
        self.mode = a

    def start(self):
        'Launches the game'
        print("\nWelcome to Tic-Tac-Toe, designed by Yigit Yargic and Ekin Igdir! Reworked by @murscht.")
        self.select_game_mode()
        print("""Enjoy the game!""")
        self.loop()
        restart = input("Do you want to play again? (Y/N): ")
        if restart.strip().lower() in {"y", "1", "yes"}:
            self.reset_board()
            self.start()

if __name__ == '__main__':
    a = Tic()
    a.start()

