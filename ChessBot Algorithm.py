import os
import chess
import tkinter as tk
from threading import Thread

class ChessEngine:
    def __init__(self):
        self.board = chess.Board()
        self.history = []
        self.move_in_progress = False

    def evaluate_board(self):
        score = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                x, y = divmod(square, 8)
                if piece.color == chess.WHITE:
                    score += self.get_piece_value(piece, x, y)
                else:
                    score -= self.get_piece_value(piece, x, y)
        return score

    def get_piece_value(self, piece, x, y):
        piece_values_with_position = {
            chess.PAWN: [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [50, 50, 50, 50, 50, 50, 50, 50],
                [10, 10, 20, 30, 30, 20, 10, 10],
                [5, 5, 10, 25, 25, 10, 5, 5],
                [0, 0, 0, 20, 20, 0, 0, 0],
                [5, -5, -10, 0, 0, -10, -5, 5],
                [5, 10, 10, -20, -20, 10, 10, 5],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            chess.KNIGHT: [
                [-50, -40, -30, -30, -30, -30, -40, -50],
                [-40, -20, 0, 0, 0, 0, -20, -40],
                [-30, 0, 10, 15, 15, 10, 0, -30],
                [-30, 5, 15, 20, 20, 15, 5, -30],
                [-30, 0, 15, 20, 20, 15, 0, -30],
                [-30, 5, 10, 15, 15, 10, 5, -30],
                [-40, -20, 0, 5, 5, 0, -20, -40],
                [-50, -40, -30, -30, -30, -30, -40, -50]
            ],
            chess.BISHOP: [
                [-20, -10, -10, -10, -10, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 10, 10, 5, 0, -10],
                [-10, 5, 5, 10, 10, 5, 5, -10],
                [-10, 0, 10, 10, 10, 10, 0, -10],
                [-10, 10, 10, 10, 10, 10, 10, -10],
                [-10, 5, 0, 0, 0, 0, 5, -10],
                [-20, -10, -10, -10, -10, -10, -10, -20]
            ],
            chess.ROOK: [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [5, 10, 10, 10, 10, 10, 10, 5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [0, 0, 0, 5, 5, 0, 0, 0]
            ],
            chess.QUEEN: [
                [-20, -10, -10, -5, -5, -10, -10, -20],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-10, 0, 5, 5, 5, 5, 0, -10],
                [-5, 0, 5, 5, 5, 5, 0, -5],
                [0, 0, 5, 5, 5, 5, 0, -5],
                [-10, 5, 5, 5, 5, 5, 0, -10],
                [-10, 0, 5, 0, 0, 0, 0, -10],
                [-20, -10, -10, -10, -5, -5, -5, -5, -10, -20]
            ],
            chess.KING: [
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-30, -40, -40, -50, -50, -40, -40, -30],
                [-20, -30, -30, -30, -40, -40, -30, -20],
                [-10, -20, -20,-20, -20, -20, -20, -20, -20, -20, -10],
                [20, 20, 0, 0, 0, 0, 20, 20],
                [20, 30, 10, 0, 0, 10, 30, 20]
            ]
        }
        piece_type = piece.piece_type
        position_value = piece_values_with_position[piece_type][x][y]
        base_value = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }.get(piece_type, 0)
        return base_value + position_value

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_board()

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, alpha, beta, False)
                self.board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.board.legal_moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self, depth):
        best_move = None
        max_eval = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            eval = self.minimax(depth - 1, alpha, beta, False)
            self.board.pop()
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
        return best_move

    def make_move(self, move):
        self.history.append(str(self.board.fen()))
        self.board.push(move)

    def undo_move(self):
        if len(self.history) > 0:
            self.board.set_fen(self.history.pop())

    def is_legal_move(self, move):
        return move in self.board.legal_moves

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ChessBot")
        self.root.resizable(False, False)
        self.engine = ChessEngine()
        self.player_color = chess.WHITE
        self.square_size = 75
        self.canvas = tk.Canvas(root, width=8 * self.square_size, height=8 * self.square_size)
        self.canvas.pack()
        self.selected_square = None
        self.images = {}
        self.load_images()
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_square_click)
        self.turn_label = tk.Label(root, text="White's turn")
        self.turn_label.pack()
        self.color_frame = tk.Frame(root)
        self.color_frame.pack()
        self.white_button = tk.Button(self.color_frame, text="Play as White", command=self.play_as_white)
        self.white_button.pack(side=tk.LEFT)
        self.black_button = tk.Button(self.color_frame, text="Play as Black", command=self.play_as_black)
        self.black_button.pack(side=tk.RIGHT)

    def play_as_white(self):
        self.player_color = chess.WHITE
        self.engine.board.reset()
        self.draw_board()
        self.turn_label.config(text="White's turn")

    def play_as_black(self):
        self.player_color = chess.BLACK
        self.engine.board.reset()
        self.draw_board()
        self.turn_label.config(text="Black's turn")
        self.make_ai_move()

    def load_images(self):
        pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'pawn']
        colors = ['white', 'black']
        for color in colors:
            for piece in pieces:
                file_path = os.path.join('ChessPieces', f'{color}_{piece}.png')
                self.images[f'{color}_{piece}'] = tk.PhotoImage(file=file_path)

    def draw_board(self):
        self.canvas.delete("all")
        color = ["#f0d9b5", "#b58863"]
        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color[(row + col) % 2])
                piece = self.engine.board.piece_at(chess.square(col, 7 - row))
                if piece:
                    piece_color = 'white' if piece.color == chess.WHITE else 'black'
                    piece_type = chess.piece_name(piece.piece_type)
                    image_key = f"{piece_color}_{piece_type}"
                    if image_key in self.images:
                        self.canvas.create_image(x1 + self.square_size // 2, y1 + self.square_size // 2, image=self.images[image_key])

        self.add_board_labels_to_canvas()

    def add_board_labels_to_canvas(self):
        for i in range(8):
            x = i * self.square_size + self.square_size // 2
            y1 = 8 * self.square_size + 10
            y2 = -10
            self.canvas.create_text(x, y1, text=chr(ord('a') + i), font=("Arial", 12))
            self.canvas.create_text(x, y2, text=chr(ord('a') + i), font=("Arial", 12))

        for i in range(8):
            y = (7 - i) * self.square_size + self.square_size // 2
            x1 = 8 * self.square_size + 10
            x2 = -10
            self.canvas.create_text(x1, y, text=str(i + 1), font=("Arial", 12))
            self.canvas.create_text(x2, y, text=str(i + 1), font=("Arial", 12))

    def on_square_click(self, event):
        if self.engine.move_in_progress:
            print("Move in progress, ignoring click")
            return

        col = int(event.x / self.square_size)
        row = int((self.canvas.winfo_height() - event.y) / self.square_size)
        square = chess.square(col, row)
        print("Clicked square:", square)

        if self.engine.board.turn != self.player_color:
            print("Not player's turn")
            return

        if self.selected_square is None:
            self.selected_square = square
            print("Selected square:", self.selected_square)
        else:
            move = chess.Move(self.selected_square, square)
            print("Move attempted:", move)

            if self.engine.is_legal_move(move):
                print("Move is legal")
                self.engine.make_move(move)
                self.draw_board()
                self.check_game_status()
                self.make_ai_move()
            else:
                print("Move is illegal")

            self.engine.move_in_progress = True
            self.selected_square = None

            self.root.after(200, self.reset_move_in_progress)

    def reset_move_in_progress(self):
        self.engine.move_in_progress = False

    def make_ai_move(self):
        if self.engine.board.turn != self.player_color:
            thread = Thread(target=self.calculate_ai_move)
            thread.start()

    def calculate_ai_move(self):
        best_move = self.engine.get_best_move(depth=4)
        if best_move:
            self.engine.make_move(best_move)
            self.draw_board()
            self.check_game_status()

            self.reset_move_in_progress()

    def check_game_status(self):
        if self.engine.board.is_checkmate():
            self.display_end_message("Checkmate!")
        elif self.engine.board.is_stalemate():
            self.display_end_message("Stalemate!")
        elif self.engine.board.is_insufficient_material():
            self.display_end_message("Insufficient material!")
        elif self.engine.board.is_seventyfive_moves():
            self.display_end_message("75-move rule!")
        elif self.engine.board.is_fivefold_repetition():
            self.display_end_message("Fivefold repetition!")
        elif self.engine.board.is_check():
            self.turn_label.config(text="Check!")
        else:
            turn = "White's turn" if self.engine.board.turn == chess.WHITE else "Black's turn"
            self.turn_label.config(text=turn)

    def display_end_message(self):
        self.engine.board.reset()
        self.draw_board()
        self.turn_label.config(text="White's turn")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("650x680")
    root.minsize(650, 680)
    gui = ChessGUI(root)
    root.mainloop()

