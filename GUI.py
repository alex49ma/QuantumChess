import tkinter as tk
from tkinter import font
from tkinter import messagebox
import random
import Game
import re

rules = "Quantum Chess is a variant of the classical chess game adding some Quantum propperties. In the game, sometimes pieces can be two places at once, the known as quantum superposition. This happens when you make a quantum move. Quantum moves are the result of two classical moves at once, so we no longer know the precise position of this piece. Piece's position is defined when an observation happens. In this case, when someone captures a quantum piece or when a quantum piece captures another. Then we have 50% chance to be on each different position. This allows quantum entanglement. If a quantum piece has a certain probability to be at one place, means that there is a probability that it is not there and I can pass through it with a slide move. In this case the piece may have done the movement or not, it depends on the final position of the previous quantum piece. It is entangled.To win, you must capture the enemy king."
piece_mapping = {
    "K": "♔", "Q": "♕", "R": "♖", "N": "♘", "B": "♗", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜", "n": "♞", "b": "♝", "p": "♟"
}
pattern = r'^[a-h][1-8][a-h][1-8][qrbn]?$'
patternQ = r'^[a-h][1-8][a-h][1-8], [a-h][1-8][a-h][1-8][qrbn]?$'

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

        self.canvas = tk.Canvas(root, width=800, height=750)
        self.canvas.pack(side=tk.LEFT)

        self.board_size = 8
        self.square_size = 90
        self.pieces = {}  # Store piece IDs and their positions

        self.draw_board()
        self.draw_pieces()

        self.dragged_piece = None
        self.drag_data = {"x": 0, "y": 0}


        # Add menu buttons
        self.menu_frame = tk.Frame(root, width=200, height=400)

        self.color_sel_menu_frame = tk.Frame(root, width=200, height=400)
        #self.menu_frame.pack(side=tk.RIGHT, padx=10)
        
        self.button_turn = tk.Button(self.menu_frame, text="♔", state=tk.DISABLED, font=font.Font(size=30), height= 1, width= 10, bg= "white")
        self.button_turn.pack(pady=10)

        self.button_end = tk.Button(self.menu_frame, text="Finish Game", command=self.end_game, font=font.Font(size=16), height= 2, width= 18, bg= "white")
        self.button_end.pack(pady=10)
        
        self.button_rules = tk.Button(self.menu_frame, text="Rules", command=self.display_rules, font=font.Font(size=16), height= 2, width= 18, bg= "white")
        self.button_rules.pack(pady=10)
        
        self.button_hint = tk.Button(self.menu_frame, text="Hint", command=self.display_hint, font=font.Font(size=16), height= 2, width= 18, bg= "white")
        self.button_hint.pack(pady=10)
                
        self.button_quantum = tk.Button(self.menu_frame, text="Enter Quantum Mode", command=self.enter_quantum_mode, font=font.Font(size=16), height= 2, width= 18, bg= "white")
        self.button_quantum.pack(pady=10)

        self.main_menu_frame = tk.Frame(root, width=200, height=400)
        self.main_menu_frame.pack(side=tk.RIGHT, padx=10)

        self.button_start = tk.Button(self.main_menu_frame, text="Play against Stockfish", command=self.sel_color, font=font.Font(size=16), height= 2, width= 18, bg= "white")
        self.button_start.pack(pady=10)

        self.button_start = tk.Button(self.main_menu_frame, text="Play with a friend", command=lambda: self.start_game(None), font=font.Font(size=16), height= 2, width= 18, bg= "white")
        self.button_start.pack(pady=10)
        
        self.button_start = tk.Button(self.main_menu_frame, text="Exit", command=self.root.destroy, font=font.Font(size=16), height= 2, width= 18, bg= "white")
        self.button_start.pack(pady=10)

        #self.menu_frame.pack_forget()
        self.in_game = False

    def game(self):
        return Game.Game()

    def sel_color(self):
        self.main_menu_frame.pack_forget()

        self.color_sel_menu_frame.pack(side=tk.RIGHT, padx=10)
        
        self.title_label = tk.Label(self.color_sel_menu_frame, text="Choose a color", font=("Helvetica", 20))
        self.title_label.pack(pady=20)

        self.button_start = tk.Button(self.color_sel_menu_frame, text="White", command=lambda: self.start_game("w"), font=font.Font(size=16), height= 2, width= 18, bg= "white")
        self.button_start.pack(pady=10)

        self.button_start = tk.Button(self.color_sel_menu_frame, text="Black", command=lambda: self.start_game("b"), font=font.Font(size=16), height= 2, width= 18, bg= "white")
        self.button_start.pack(pady=10)
        
        self.button_start = tk.Button(self.color_sel_menu_frame, text="Random", command=lambda: self.start_game(random.choice(["w", "b"])), font=font.Font(size=16), height= 2, width= 18, bg= "white")
        self.button_start.pack(pady=10)

    def start_game(self, oponent):
        self.game = Game.Game()
        self.in_game = True
        self.menu_frame.pack(side=tk.RIGHT, padx=10)
        self.color_sel_menu_frame.pack_forget()
        self.main_menu_frame.pack_forget()  # Hide the menu frame
        self.canvas.pack(side=tk.LEFT)
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.loop(oponent)

    def loop(self, oponent):
        pass

    def end_game(self):
        confirm = messagebox.askokcancel("End Game", "Are you sure you want to end the game here?")
        if confirm:
            self.game = Game.Game()
            self.quantum_mode = False
            self.quantum_piece = None
            self.quantum_squares = []
            self.original_colors = {}
            self.sel_square = ""

            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")


            self.main_menu_frame.pack(side=tk.RIGHT, padx=10)
            self.color_sel_menu_frame.pack_forget()
            self.menu_frame.pack_forget()  # Hide the menu frame
            self.canvas.pack(side=tk.LEFT)

            self.draw_board()
            self.draw_pieces()
            

    def display_rules(self):
        messagebox.showinfo("Rules", rules)

    def display_hint(self):
        hint = self.game.moveHint()
        moveList = ""
        counter = 0
        for recom in hint:
            moves = recom[0].split(", ")
            for move in moves:
                sq = move[0:2]
                piece = self.game.position.getWhatIsOnSquare(sq)
                unicod = piece_mapping.get(piece.pieceClass)
                moveList += unicod+ " " +  move[2:4] + " "
            moveList += "\n"
            counter += 1
            if counter == 3: break
        messagebox.showinfo("Hints", moveList)

    def enter_quantum_mode(self):
        self.quantum_mode = not self.quantum_mode
        if self.quantum_mode:
            self.button_quantum.config(text="Exit Quantum Mode", bg= "BlueViolet")
            self.sel_square = ""
            self.draw_board()
            self.draw_pieces()
        else:
            self.quantum_piece = None
            self.button_quantum.config(text="Enter Quantum Mode", bg= "white")
            self.quantum_squares = []
            self.draw_board()
            self.draw_pieces()

    def draw_board(self):
        for col in range(self.board_size):
            for row in range(self.board_size):
                color = "white" if (row + col) % 2 == 0 else "grey"
                frame_width = self.square_size/8
                x0 = col * self.square_size
                y0 = row * self.square_size
                x1 = x0 + self.square_size
                y1 = y0 + self.square_size
                if str(row) + str(col) in self.quantum_squares:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="BlueViolet")
                elif str(row) + str(col) in self.sel_square:
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="green")
                else:
                    self.original_colors[(row, col)] = color
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
                sq = chr(col + ord('a')) + str(8 - row)
                piece = self.game.position.getWhatIsOnSquare(sq)
                if piece:
                    if piece.quantic:
                        self.canvas.create_rectangle(x0, y0, x1, y1, fill="BlueViolet")
                        if str(row) + str(col) in self.sel_square:
                            color = "green"
                        self.canvas.create_rectangle(x0 + frame_width, y0 + frame_width, x1 - frame_width, y1 - frame_width, fill=color)
                        if str(row) + str(col) in self.quantum_squares:
                            self.canvas.create_rectangle(x0 + frame_width * 1.5, y0 + frame_width * 1.5, x1 - frame_width * 1.5, y1 - frame_width * 1.5, fill="BlueViolet")
        
            x0 = self.square_size * col
            y0 = self.square_size * 8
            x1 = x0 + self.square_size
            y1 = y0 + self.square_size/3
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")
            self.canvas.create_text(x0 + (1/2 * self.square_size), y0 + (1/7 * self.square_size), text=chr(ord('a') + col), font=("Helvetica", 20), tags=("label",))
        for row in range(self.board_size):
            x0 = self.square_size * 8
            y0 = self.square_size * row
            x1 = x0 + self.square_size/3
            y1 = y0 + self.square_size
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")
            self.canvas.create_text(x0 + (1/6 * self.square_size), y0 + (1/2 * self.square_size), text=str(8 - row), font=("Helvetica", 20), tags=("label",))

        self.canvas.create_rectangle(self.square_size * 8, self.square_size * 8, self.square_size * 8 + self.square_size/3, self.square_size * 8 + self.square_size/3, fill="white")

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
                    text = piece_mapping.get(piece.pieceClass, "")
                    piece_id = self.canvas.create_text(x, y, text=text, font=("Helvetica", 24), tags=("piece",))
                    self.pieces[piece_id] = (piece, row, col)

    def select_square(self, row, col):
        sq = chr(col + ord('a')) + str(8 - row)
        if str(row) + str(col) == self.sel_square:
            self.sel_square = ""
        elif self.sel_square == "":
            self.sel_square = str(row) + str(col)
        else:
            selected = chr(int(self.sel_square[1]) + ord('a')) + str(8 - int(self.sel_square[0]))
            self.perform_move(selected, sq)

    def select_quantum(self, row, col):
        key = 1
        sq = chr(col + ord('a')) + str(8 - row)
        if len(self.quantum_squares) == 0:
            self.quantum_squares.append(str(row) + str(col))
        elif str(row) + str(col) == self.quantum_squares[-1]:
            self.quantum_squares.pop()
        elif len(self.quantum_squares) == 1:
            self.quantum_squares.append(str(row) + str(col))
        elif str(row) + str(col) in self.quantum_squares:
            key = 0
            self.quantum_squares = []
        else:
            key = 0
            selected = []
            selected.append(chr(int(self.quantum_squares[0][1]) + ord('a')) + str(8 - int(self.quantum_squares[0][0])))
            selected.append(chr(int(self.quantum_squares[1][1]) + ord('a')) + str(8 - int(self.quantum_squares[1][0])))
            selected.append(sq)
            self.perform_quantum_move(selected)

        if key:
            x = col * self.square_size + self.square_size // 2
            y = row * self.square_size + self.square_size // 2
            piece = self.game.position.getWhatIsOnSquare(sq)
            if piece is not None:
                figure = piece_mapping.get(piece.pieceClass, "")
                self.canvas.create_text(x, y, text=figure, font=("Helvetica", 24), tags=("piece",))

    def on_click(self, event):
        col = event.x // self.square_size
        row = event.y // self.square_size
        if self.quantum_mode:
            self.select_quantum(row, col)
        else:
            self.select_square(row, col)

    def on_drag(self, event):
        pass

    def on_release(self, event):
        self.draw_board()
        self.draw_pieces()
        if self.game.over:
            messagebox.showinfo("Game over", str(self.game.over))
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")


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
            if self.game.move(origin + destination):
                if self.game.flagList[0] == "w":
                    self.button_turn.config(text="♚", bg= "white")   
                else:
                    self.button_turn.config(text="♔", bg= "black")
            self.sel_square = ""
            #self.draw_board()
            #self.draw_pieces()
            



    def perform_quantum_move(self, selected):
        qmove1 = selected[0] + selected[1]
        qmove2 = selected[0] + selected[2]
        if re.search(patternQ, qmove1  + ", " + qmove2) is not None:
            if self.game.qMove(qmove1, qmove2):
                self.quantum_mode = False
                self.button_quantum.config(text="Enter Quantum Mode", bg= "white")
                if self.game.flagList[0] == "w":
                    self.button_turn.config(text="♚", bg= "white")   
                else:
                    self.button_turn.config(text="♔", bg= "black")
            self.quantum_squares = []
            #self.draw_board()
            #self.draw_pieces()

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
