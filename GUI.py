import tkinter as tk
import random
import Game
import re

rules = "Quantum Chess is a variant of the classical chess game adding some Quantum propperties. \nIn the game, sometimes pieces can be two places at once, the known as quantum superposition. \nThis happens when you make a quantum move. Quantum moves are the result of two classical \nmoves at once, so we no longer know the precise position of this piece. Piece's position \nis defined when an observation happens. In this case, when someone captures a quantum \npiece or when a quantum piece captures another. Then we have 50% chance to be on each \ndifferent position. This allows quantum entanglement. If a quantum piece has a certain \nprobability to be at one place, means that there is a probability that it is not there and \nI can pass through it with a slide move. In this case the piece may have done the movement \nor not, it depends on the final position of the previous quantum piece. It is entangled.\nTo win, you must capture the enemy king."
piece_data = {
    "K": "♔", "Q": "♕", "R": "♖", "N": "♘", "B": "♗", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜", "n": "♞", "b": "♝", "p": "♟"
}
pattern = r'^[a-h][1-8][a-h][1-8][qrbn]?$'

class ChessGUI:

    def __init__(self, root):
        self.game = Game.Game()
        self.root = root
        self.quantum_mode = False
        self.quantum_piece = None
        self.quantum_squares = []
        self.root.title("Quantum Fish & Chess")
        self.original_colors = {}
        self.sel_square = ""

        self.canvas = tk.Canvas(root, width=450, height=400)
        self.canvas.pack(side=tk.LEFT)

        self.board_size = 8
        self.square_size = 50
        self.pieces = {}  # Store piece IDs and their positions

        self.draw_board()
        self.draw_pieces()

        self.dragged_piece = None
        self.drag_data = {"x": 0, "y": 0}


        # Add menu buttons
        self.menu_frame = tk.Frame(root, width=150, height=400)

        self.color_menu_frame = tk.Frame(root, width=150, height=400)
        #self.menu_frame.pack(side=tk.RIGHT, padx=10)
        
        self.button_end = tk.Button(self.menu_frame, text="Finish Game", command=self.end_game, height= 2, width= 15)
        self.button_end.pack(pady=10)
        
        self.button_rules = tk.Button(self.menu_frame, text="Rules", command=self.display_rules, height= 2, width= 15)
        self.button_rules.pack(pady=10)
        
        self.button_hint = tk.Button(self.menu_frame, text="Hint", command=self.display_hint, height= 2, width= 15)
        self.button_hint.pack(pady=10)
                
        self.button_quantum = tk.Button(self.menu_frame, text="Quantum Move", command=self.perform_q_move, height= 2, width= 15)
        self.button_quantum.pack(pady=10)

        self.main_menu_frame = tk.Frame(root, width=150, height=400)
        self.main_menu_frame.pack(side=tk.RIGHT, padx=10)

        self.button_start = tk.Button(self.main_menu_frame, text="Play against Stockfish", command=self.sel_color)
        self.button_start.pack(pady=10)

        self.button_start = tk.Button(self.main_menu_frame, text="Play with a friend", command=lambda: self.start_game(None))
        self.button_start.pack(pady=10)
        
        self.button_start = tk.Button(self.main_menu_frame, text="Exit", command=self.root.destroy)
        self.button_start.pack(pady=10)

        #self.menu_frame.pack_forget()
        self.in_game = False

    def game(self):
        return Game.Game()

    def sel_color(self):
        self.main_menu_frame.pack_forget()

        self.color_menu_frame.pack(side=tk.RIGHT, padx=10)
        
        self.title_label = tk.Label(self.color_menu_frame, text="Choose a color", font=("Helvetica", 20))
        self.title_label.pack(pady=20)

        self.button_start = tk.Button(self.color_menu_frame, text="White", command=lambda: self.start_game("w"))
        self.button_start.pack(pady=10)

        self.button_start = tk.Button(self.color_menu_frame, text="Black", command=lambda: self.start_game("b"))
        self.button_start.pack(pady=10)
        
        self.button_start = tk.Button(self.color_menu_frame, text="Random", command=lambda: self.start_game(random.choice(["w", "b"])))
        self.button_start.pack(pady=10)

    def start_game(self, oponent):
        self.game = Game.Game()
        self.in_game = True
        self.menu_frame.pack(side=tk.RIGHT, padx=10)
        self.color_menu_frame.pack_forget()
        self.main_menu_frame.pack_forget()  # Hide the menu frame
        self.canvas.pack(side=tk.LEFT)
        self.main_menu_frame.destroy()
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.loop(oponent)

    def loop(self, oponent):
        pass

    def end_game():
        pass
    def display_rules(self):
        tk.Tk(rules)
    def display_hint():
        pass
    def perform_q_move(self):
        self.quantum_mode = not self.quantum_mode
        if self.quantum_mode:
            self.button_quantum.config(text="Exit Quantum Mode")
        else:
            self.quantum_piece = None
            self.quantum_squares = []
            self.button_quantum.config(text="Quantum Move")

    def draw_board(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                color = "white" if (row + col) % 2 == 0 else "grey"
                x0 = col * self.square_size
                y0 = row * self.square_size
                x1 = x0 + self.square_size
                y1 = y0 + self.square_size
                self.original_colors[(row, col)] = color
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)

    def draw_pieces(self):
        for row in range(self.board_size):
            for col in range(self.board_size):
                sq = chr(col + ord('a')) + str(8 - row)
                piece = self.game.position.getWhatIsOnSquare(sq)

                """
                if row == 7:
                    piece = "RNBQKBNR"[col]
                elif row == 6:
                    piece = "P"
                elif row == 1:
                    piece = "p"
                elif row == 0:
                    piece = "rnbqkbnr"[col]
                """
                if piece:
                    x = col * self.square_size + self.square_size // 2
                    y = row * self.square_size + self.square_size // 2
                    text = piece_data.get(piece.pieceClass, "")
                    piece_id = self.canvas.create_text(x, y, text=text, font=("Helvetica", 24), tags=("piece",))
                    self.pieces[piece_id] = (piece, row, col)

    def select_square(self, row, col, color):
        x1 = col * self.square_size
        y1 = row * self.square_size
        x2 = x1 + self.square_size
        y2 = y1 + self.square_size
        key = 1
        sq = chr(col + ord('a')) + str(8 - row)
        if str(row) + str(col) == self.sel_square:
            new_color = self.original_colors[(row, col)]
            self.sel_square = ""
        elif self.sel_square == "":
            new_color = "green"
            self.sel_square = str(row) + str(col)
        else:
            key = 0 # Without a new color, you shall not try to paint. When moves performed, the square selected will come back to it's previous color
            selected = chr(int(self.sel_square[1]) + ord('a')) + str(8 - int(self.sel_square[0]))
            self.perform_move(selected, sq)

        if key:
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=new_color)
            x = col * self.square_size + self.square_size // 2
            y = row * self.square_size + self.square_size // 2
            piece = self.game.position.getWhatIsOnSquare(sq)
            if piece is not None:
                figure = piece_data.get(piece.pieceClass, "")
                self.canvas.create_text(x, y, text=figure, font=("Helvetica", 24), tags=("piece",))

    def on_click(self, event):
        col = event.x // self.square_size
        row = event.y // self.square_size
        self.select_square(row, col, "green")

    def on_drag(self, event):
        pass

    def on_release(self, event):
        pass

        """
        
    def on_click(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        tags = self.canvas.gettags(item)
        if "piece" in tags:
            if self.quantum_mode:
                if self.quantum_piece == None:
                    self.quantum_piece = item
                    self.quantum_squares = []
                elif len(self.quantum_squares) < 2:
                    self.quantum_squares.append((event.y // self.square_size, event.x // self.square_size))
                if len(self.quantum_squares) == 2:
                    self.quantum_piece = None
                    self.quantum_squares = []
            else:
                self.dragged_piece = item
                self.drag_data["x"] = event.x
                self.drag_data["y"] = event.y

    def on_drag(self, event):
        if self.dragged_piece:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            self.canvas.move(self.dragged_piece, dx, dy)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def on_release(self, event):
        if self.dragged_piece:
            row, col = event.y // self.square_size, event.x // self.square_size
            if 0 <= row < self.board_size and 0 <= col < self.board_size:
                new_x = col * self.square_size + self.square_size // 2
                new_y = row * self.square_size + self.square_size // 2
                self.canvas.coords(self.dragged_piece, new_x, new_y)
            else:
                self.reset_piece_position(self.dragged_piece)
            self.dragged_piece = None
        elif self.quantum_piece:
            if len(self.quantum_squares) < 2:
                self.quantum_squares.append((event.y // self.square_size, event.x // self.square_size))
                if len(self.quantum_squares) == 2:
                    self.perform_quantum_move()
        self.dragged_piece = None
        self.quantum_piece = None
        self.quantum_squares = []
        
        """

    def perform_move(self, origin, destination):
        if re.search(pattern, origin + destination) is not None:
            self.game.move(origin + destination)
            self.draw_board()
            self.draw_pieces()
            self.sel_square = ""
            



    def perform_quantum_move(self):
        pass

    def reset_piece_position(self, piece_id):
        if piece_id in self.pieces:
            piece, row, col = self.pieces[piece_id]
            new_x = col * self.square_size + self.square_size // 2
            new_y = row * self.square_size + self.square_size // 2
            self.canvas.coords(piece_id, new_x, new_y)

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()
