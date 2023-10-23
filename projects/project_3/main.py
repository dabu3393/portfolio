import os
import random


class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_board(self):
        for i, row in enumerate(self.board):
            print(" | ".join(row))
            if i < 2:
                print("---------")

    def take_turn(self):
        while True:
            try:
                row = int(input("Enter the row (0, 1, or 2): "))
                col = int(input("Enter the column (0, 1, or 2): "))
                if 0 <= row <= 2 and 0 <= col <= 2 and self.board[row][col] == ' ':
                    self.board[row][col] = self.current_player
                    break
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Enter numbers between 0 and 2.")

    def toggle_player(self):
        # Toggle the current player
        self.current_player = 'X' if self.current_player == 'O' else 'O'

    def block_player_win(self):
        # Check for potential winning moves by the player and block them
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    # Simulate a move for the player
                    self.board[row][col] = 'X'
                    # Check if this move results in a win for the player
                    if self.check_winner():
                        # Block the move
                        self.board[row][col] = 'O'
                        return True
                    else:
                        self.board[row][col] = ' '

    def computer_turn(self):
        # First, block the player's potential winning moves

        # Next, check if the computer can win and make a winning move
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ':
                    # Simulate a move for the computer
                    self.board[row][col] = 'O'
                    # Check if this move results in a win for the computer
                    if self.check_winner():
                        self.board[row][col] = 'O'
                        return
                    else:
                        self.board[row][col] = ' '

        if self.block_player_win():
            return
        else:
            while True:
                row = random.randint(0, 2)
                col = random.randint(0, 2)
                if self.board[row][col] == ' ':
                    self.board[row][col] = self.current_player
                    break

    def check_winner(self):
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return True

        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return True

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return True

        return False

    def check_tie(self):
        for row in self.board:
            if ' ' in row:
                return False
        return not self.check_winner()

    def play_game(self):
        while True:
            self.display_board()

            if self.current_player == 'X':
                self.take_turn()
                if self.check_winner():
                    self.clear_screen()
                    self.display_board()
                    print(f"Player {self.current_player} wins!")
                    break
                self.toggle_player()
            else:
                self.computer_turn()
                if self.check_winner():
                    self.clear_screen()
                    self.display_board()
                    print(f"Player {self.current_player} wins!")
                    break
                self.toggle_player()

            if self.check_tie():
                self.clear_screen()
                self.display_board()
                print("It's a tie!")
                break

            self.clear_screen()


if __name__ == "__main__":
    while True:
        game = TicTacToe()
        game.play_game()

        play_again = input("Do you want to play again? (yes or no): ").lower()
        game.clear_screen()
        if play_again != 'yes':
            break
