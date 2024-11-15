import numpy as np
import random

def initialize_board():
    board = np.zeros((4, 4), dtype=int)
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    empty_positions = list(zip(*np.where(board == 0)))
    if empty_positions:
        x, y = random.choice(empty_positions)
        board[x][y] = 2 if random.random() < 0.9 else 4

# Initialize the board and print it
board = initialize_board()
print(board)

def compress(board):
    new_board = np.zeros_like(board)
    for i in range(4):
        row = board[i][board[i] != 0]  # remove all zeros
        new_board[i][:len(row)] = row  # move all tiles to the left
    return new_board

def merge(board):
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j+1] and board[i][j] != 0:
                board[i][j] *= 2
                board[i][j+1] = 0
    return board

def move_left(board):
    board = compress(board)
    board = merge(board)
    board = compress(board)
    return board

def move_right(board):
    return np.fliplr(move_left(np.fliplr(board)))

def move_up(board):
    return np.rot90(move_left(np.rot90(board, -1)), 1)

def move_down(board):
    return np.rot90(move_left(np.rot90(board, 1)), -1)






import tkinter as tk

class Game2048(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('2048 Game')
        self.board = initialize_board()
        self.grid_cells = []
        self.init_grid()
        self.update_grid_cells()
        self.master.bind("<Key>", self.key_down)

    def init_grid(self):
        background = tk.Frame(self, bg="gray", width=400, height=400)
        background.grid()

        for i in range(4):
            grid_row = []
            for j in range(4):
                cell = tk.Frame(background, bg="lightgray", width=100, height=100)
                cell.grid(row=i, column=j, padx=5, pady=5)
                t = tk.Label(master=cell, text="", bg="lightgray", font=("Helvetica", 24), width=4, height=2)
                t.grid()
                grid_row.append(t)
            self.grid_cells.append(grid_row)

    def update_grid_cells(self):
        for i in range(4):
            for j in range(4):
                new_number = self.board[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg="lightgray")
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg="orange")
        self.update_idletasks()

    def key_down(self, event):
        key = event.keysym
        if key == 'Down':
            self.board = move_up(self.board)
        elif key == 'Up':
            self.board = move_down(self.board)
        elif key == 'Left':
            self.board = move_left(self.board)
        elif key == 'Right':
            self.board = move_right(self.board)
        
        add_new_tile(self.board)
        self.update_grid_cells()

        if self.game_over():
            self.game_over_popup()

    def get_color(self, number):
    # Define colors for different numbers
        colors = {
            0: "lightgray",  # Empty tile
            2: "#f9f9f9",    # Almost white
            4: "#f2f2f2",    # Light gray
            8: "#e6d8ab",    # Beige
            16: "#e6b27e",   # Light brown
            32: "#f59563",   # Coral
            64: "#f67c5f",   # Tomato
            128: "#f65e3b",  # Dark tomato
            256: "#edcf72",  # Mustard
            512: "#edcc61",  # Yellowish
            1024: "#edc850", # Golden yellow
            2048: "#edc22e"  # Deep yellow
        }
        # Return the corresponding color, or black for numbers greater than 2048
        return colors.get(number, "#edc22e")


    def update_grid_cells(self):
        for i in range(4):
            for j in range(4):
                new_number = self.board[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg="lightgray")
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=self.get_color(new_number))
        self.update_idletasks()
        
    def game_over(self):
    # Create copies of the board to simulate the moves without altering the actual board
        if np.any(self.board == 0):  # Check if there are empty tiles (possible moves)
            return False
        if (not np.array_equal(self.move_left(self.board.copy()), self.board) or
            not np.array_equal(self.move_right(self.board.copy()), self.board) or
            not np.array_equal(self.move_up(self.board.copy()), self.board) or
            not np.array_equal(self.move_down(self.board.copy()), self.board)):
            return False
        return True
    
    


    def game_over_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Game Over")
        label = tk.Label(popup, text="Game Over!", font=("Helvetica", 20))
        label.pack(pady=10)
        button = tk.Button(popup, text="OK", command=self.master.quit)
        button.pack(pady=5)

# Run the Game
game = Game2048()
game.mainloop()
