import numpy as np
import random

class Custom2048Env:
    def __init__(self):
        self.board = np.zeros((4, 4), dtype=np.int32)
        self.reset()

    def reset(self):
        """Reset the environment to start a new game."""
        self.board = np.zeros((4, 4), dtype=np.int32)
        self.add_new_tile()
        self.add_new_tile()
        return self.board

    def add_new_tile(self):
        """Add a new tile to the game board at a random empty position."""
        empty_positions = list(zip(*np.where(self.board == 0)))
        if empty_positions:
            x, y = random.choice(empty_positions)
            self.board[x][y] = 2 if random.random() < 0.9 else 4

    def step(self, action):
        """Take an action in the environment."""
        old_board = self.board.copy()
        reward = 0

        # Perform the action (up, down, left, right)
        if action == 0:  # Up
            self.board = self.move_up(self.board)
        elif action == 1:  # Down
            self.board = self.move_down(self.board)
        elif action == 2:  # Left
            self.board = self.move_left(self.board)
        elif action == 3:  # Right
            self.board = self.move_right(self.board)

        reward = np.sum(self.board) - np.sum(old_board)
        done = not self.is_move_possible()
        if not done:
            self.add_new_tile()
        return self.board, reward, done

    def move_left(self, board):
        """Move the tiles left."""
        new_board = np.zeros_like(board)
        for i in range(4):
            row = board[i][board[i] != 0]
            merged_row = []
            skip = False
            for j in range(len(row)):
                if skip:
                    skip = False
                    continue
                if j != len(row) - 1 and row[j] == row[j + 1]:
                    merged_row.append(row[j] * 2)
                    skip = True
                else:
                    merged_row.append(row[j])
            new_board[i, :len(merged_row)] = merged_row
        return new_board

    def move_right(self, board):
        return np.fliplr(self.move_left(np.fliplr(board)))

    def move_up(self, board):
        return np.rot90(self.move_left(np.rot90(board, -1)), 1)

    def move_down(self, board):
        return np.rot90(self.move_left(np.rot90(board, 1)), -1)

    def is_move_possible(self):
        if np.any(self.board == 0):
            return True
        for move_func in [self.move_left, self.move_right, self.move_up, self.move_down]:
            if not np.array_equal(self.board, move_func(self.board.copy())):
                return True
        return False

    def render(self):
        print(self.board)

import numpy as np
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory




env = Custom2048Env()

# Build a simple neural network model for the DQN agent
model = Sequential()
model.add(Flatten(input_shape=(1, 4, 4)))
model.add(Dense(24, activation='relu'))
model.add(Dense(24, activation='relu'))
model.add(Dense(4, activation='linear'))  # 4 actions (up, down, left, right)

# Configure and compile the agent
policy = EpsGreedyQPolicy()
memory = SequentialMemory(limit=50000, window_length=1)
dqn = DQNAgent(model=model, nb_actions=4, memory=memory, nb_steps_warmup=10, target_model_update=1e-2, policy=policy)
dqn.compile(optimizer='adam', metrics=['mae'])

# Train the agent
dqn.fit(env, nb_steps=10000, visualize=False, verbose=2)

# Test the agent
dqn.test(env, nb_episodes=5, visualize=False)
