import numpy as np
import random

class AI2048:
    def __init__(self, game):
        self.game = game  # Reference to the game object

    def get_best_move(self):
        # Evaluate all possible moves and return the best one based on score (sum of tiles)
        best_move = None
        best_score = -1
        
        moves = ['Up', 'Down', 'Left', 'Right']
        for move in moves:
            # Simulate the move
            simulated_board = self.simulate_move(move, self.game.board)
            if simulated_board is not None:
                score = self.evaluate_board(simulated_board)
                if score > best_score:
                    best_score = score
                    best_move = move
        
        return best_move

    def simulate_move(self, move, board):
        # Copy the board and simulate the move without affecting the actual game board
        board_copy = board.copy()
        
        if move == 'Up':
            new_board = self.game.move_up(board_copy)
        elif move == 'Down':
            new_board = self.game.move_down(board_copy)
        elif move == 'Left':
            new_board = self.game.move_left(board_copy)
        elif move == 'Right':
            new_board = self.game.move_right(board_copy)
        
        # Check if the move changes the board (otherwise it’s an invalid move)
        if np.array_equal(new_board, board_copy):
            return None  # Invalid move, board didn't change
        return new_board

    def evaluate_board(self, board):
        # Basic heuristic: sum of all tiles
        return np.sum(board)

import tkinter as tk
# Integrating AI with the game
class Game2048(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title('2048 Game')
        self.board = self.initialize_board()
        self.grid_cells = []
        self.init_grid()
        self.update_grid_cells()
        self.master.bind("<Key>", self.key_down)
        self.ai = AI2048(self)  # Initialize AI

    # (Other methods remain unchanged, like initialize_board, move_left, move_right, etc.)
    
    def key_down(self, event):
        key = event.keysym
        if key == 'Up':
            self.board = self.move_up(self.board)
        elif key == 'Down':
            self.board = self.move_down(self.board)
        elif key == 'Left':
            self.board = self.move_left(self.board)
        elif key == 'Right':
            self.board = self.move_right(self.board)
        
        self.add_new_tile(self.board)
        self.update_grid_cells()

        if not self.is_move_possible():
            self.game_over_popup()

    def ai_play(self):
        # AI plays the game
        while self.is_move_possible():
            best_move = self.ai.get_best_move()
            if best_move:
                if best_move == 'Up':
                    self.board = self.move_up(self.board)
                elif best_move == 'Down':
                    self.board = self.move_down(self.board)
                elif best_move == 'Left':
                    self.board = self.move_left(self.board)
                elif best_move == 'Right':
                    self.board = self.move_right(self.board)
                
                self.add_new_tile(self.board)
                self.update_grid_cells()
        
        self.game_over_popup()
