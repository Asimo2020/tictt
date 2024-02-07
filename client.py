import socket
import threading

class TicTacToeClient:
    def init(self):
        self.host = '127.0.0.1'
        self.port = 55555
        self.player_symbol = ""
        self.name = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.g

ame_over = False

def receive_message(self):
        while True:
            message = self.socket.recv(1024).decode()
            if message == "Game started!":
                print("Game started!")
            elif message.startswith("[["):
                # Update the board game
                self.board = eval(message)
                self.render_board()
            elif message.startswith("Player"):
                # Set the player's name and symbol
                self.name = message
                self.player_symbol = "X" if self.name == "Player 1" else "O"
                print(f"You are {self.name} ({self.player_symbol})")
            else:
                # Print the message
                print(message)

def render_board(self):
        print("   0 1 2")
        for i in range(3):
            row_str = f"{i}  "
            for j in range(3):
                row_str += f"{self.board[i][j]} "
            print(row_str)

def make_move(self):
        while not self.game_over:
            if self.name == f"Player {server.current_player_index + 1}":
                # Get the player's move
                move = input("Enter your move (row,column): ")
                x, y = map(int, move.split(","))

                # Send the move to the server
                self.socket.send(move.encode())

def start(self):
        # Get the player's name
        self.name = input("Enter your name: ")
        self.socket.send(self.name.encode())

        # Receive the player's name and symbol
        self.player_symbol = self.socket.recv(1024).decode()

        # Start the receive message thread
        receive_thread = threading.Thread(target=self.receive_message)
        receive_thread.start()

        # Make moves
        self.make_move()
#tictactoeclient
client = TicTacToeClient()
client.start()