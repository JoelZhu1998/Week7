import logging
import random  # Import the random module
from logic import make_empty_board, get_winner, other_player
import csv
from datetime import datetime
logging.basicConfig(
    filename='logs/happyjoel_game_log.log',
    level=logging.INFO
)

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self, board):
        raise NotImplementedError("Subclasses must implement the make_move method.")

class HumanPlayer(Player):
    def make_move(self, board):
        row = int(input("Enter the row (0, 1, 2): "))
        col = int(input("Enter the column (0, 1, 2): "))
        return row, col

class BotPlayer(Player):
    def make_move(self, board):
        available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] is None]
        return random.choice(available_moves) if available_moves else None

class TicTacToeGame:
    def __init__(self, player1, player2):
        self.board = make_empty_board()
        self.players = [player1, player2]
        self.current_player_index = 0
        self.winner = None
        self.move_history = {'X': [], 'O': []}  # To track moves of each player
        self.total_moves = 0

    def switch_player(self):
        self.current_player_index = (self.current_player_index + 1) % 2

    def print_board(self):
        for i in range(3):
            for j in range(3):
                print(" " if self.board[i][j] is None else self.board[i][j], end="")
                if j < 2:
                    print(" | ", end="")
            print()
            if i < 2:
                print("-" * 9)

    def play_round(self):
        player = self.players[self.current_player_index]
        self.print_board()  # Corrected line
        print(f"Player {player.symbol}'s turn:")

        move = player.make_move(self.board)

        if move is not None:
            row, col = move
            if self.board[row][col] is None:
                self.board[row][col] = player.symbol
                self.winner = get_winner(self.board)
                self.move_history[player.symbol].append((row, col))  # Record the move
                self.total_moves += 1
            else:
                print("Invalid move. That position is already occupied. Try again.")
        else:
            print("Invalid move. No available moves. Try again.")

        self.switch_player()
    
    def record_game_details(self):
        with open('logs/game_results.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            winner = self.winner if self.winner else 'Draw'
            moves_x = len(self.move_history['X'])
            moves_o = len(self.move_history['O'])
            writer.writerow([timestamp, winner, self.total_moves, moves_x, moves_o])

    def play_game(self):
        while self.winner is None:
            self.play_round()

        self.print_board()

        if self.winner:
            print(f"Player {self.winner} wins!")
            logging.info(f'Player {self.winner} wins!')
        else:
            print("It's a draw!")
            logging.info("It's a draw!")

        self.record_game_details()  # Add this line to record the game outcome

if __name__ == '__main__':
    player1_symbol = 'X'
    player2_symbol = 'O'

    player1 = HumanPlayer(player1_symbol)
    player2 = BotPlayer(player2_symbol)

    game = TicTacToeGame(player1, player2)
    game.play_game()
