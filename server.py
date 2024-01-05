import socket
import threading

class TicTacToeServer:
    def init(self):
        self.host = '127.0.0.1'
        self.port = 55555
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.players = []
        self.current_player_index = 0
        self.game_started = False
        self.game_over = False
        self.board = [["" for _ in range(3)] for _ in range(3)]

    def broadcast(self, message):
        for player in self.players:
            player.send(message)

    def handle_client(self, player):
        # Get the player's name
        name = player.recv(1024).decode()
        player_name = f"Player {len(self.players) + 1}"
        player.send(player_name.encode())

        # Add the player to the list
        self.players.append(player)

        # Wait for both players to join
        if len(self.players) < 2:
            return

        # Start the game
        self.game_started = True
        self.broadcast("Game started!".encode())

        while not self.game_over:
            # Get the current player
            current_player = self.players[self.current_player_index]

            # Send the board to the current player
            current_player.send(str(self.board).encode())

            # Wait for the current player to make a move
            move = current_player.recv(1024).decode()
            x, y = map(int, move.split(","))

            # Make the move
            if self.board[x][y] == "":
                self.board[x][y] = current_player.symbol
                self.broadcast(str(self.board).encode())

                # Check for a winner
                winner = self.check_winner()
                if winner:
                    self.broadcast(f"{winner.name} wins!".encode())
                    self.game_over = True
                    break

                # Check for a tie
                if self.is_board_full():
                    self.broadcast("Tie game!".encode())
                    self.game_over = True
                    break

                # Switch to the next player
                self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def check_winner(self):
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return self.get_player_by_symbol(self.board[i][0])
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return self.get_player_by_symbol(self.board[0][i])
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return self.get_player_by_symbol(self.board[0][0])
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return self.get_player_by_symbol(self.board[0][2])
        return None

    def get_player_by_symbol(self, symbol):
        for player in self.players:
            if player.symbol == symbol:
                return player
        return None

    def is_board_full(self):
        return all(all(cell != "" for cell in row) for row in self.board)

    def start(self):
        print("Server is listening...")
        while True:
            player_socket, address = self.server.accept()
            print(f"New connection from {address}")
            player_thread = threading.Thread(target=self.handle_client, args=(player_socket,))
            player_thread.start()

server = TicTacToeServer()
server.start()