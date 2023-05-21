import numpy as np
import random
from eraserconfig import *
import time

class Board:

    def __init__(self, board_num=N_ROWS // BOARD_SIZE,
                 colors=np.array(list(COLORS.keys())), seed=None):
        '''
        Initialize board instance.

        Parameters:
        size(int): Size of each sub-board
        board_num(int): Number of sub-boards in the main board
        colors(np.array): Array of available colors
        '''
        self.size = BOARD_SIZE
        self.board_num = board_num
        self.colors = colors
        if seed:
            np.random.seed(seed)
        self.board = np.concatenate([self.generate_board() for i in np.arange(board_num)], axis=1)
        self.move_dict = {}

        # Use numpy.indices to create a matrix of row/column indices for each cell
        a = np.indices((self.size, self.size * board_num))
        # Use numpy.apply_along_axis function to generate unique IDs for cells using row/column indices
        self.id_matrix = np.apply_along_axis(lambda x: f'r{x[1]:04d}c{x[0]:04d}', 0, a)

        # Add ID matrix to the main board
        self.board = np.dstack((self.board, self.id_matrix))
        self.times = {'get_info':0, 'eliminate':0, 'falling':0, 'check':0}
        
        self.move_history = []

    @property
    def mainboard(self):
        return self.board[:self.size, :self.size, 0]

    def copy(self):
        newboard = self.board.copy()
        copied = Board()
        copied.board = newboard
        return copied

    def generate_board(self):
        '''
        Generate a new sub-board.

        Returns:
        np.array: A new sub-board generated using the given rules.
        '''
        # Concatenate four color blocks, each of which has size*size/4 cells filled with the corresponding color.

        idx = np.arange(len(self.colors))
        np.random.shuffle(idx)
        remain = [1,] * (self.size % len(self.colors)) + [0,] * (len(self.colors) - (self.size % len(self.colors)))
        new_array = np.concatenate([np.full((self.size, self.size // len(self.colors) + remain[i]),
            self.colors[idx[i]]) for i in range(len(self.colors))], axis=1)
        np.random.shuffle(new_array.ravel())  # Shuffle the order of color blocks.


        # If there are three adjacent cells with the same color, randomly choose a different color for one of them
        invalid_pos = self.check(new_array)
        while invalid_pos:
            for i, j in invalid_pos:
                new_array[i, j] = np.random.choice(self.colors)
            invalid_pos = self.check(new_array)

        # Return the generated sub-board.
        return new_array

    @staticmethod
    def check(arr):
        '''
        Check if there are three adjacent cells in a sub-board that are filled with the same color.

        Parameters:
        array(np.array): A square sub-board array to be checked for repetition of colors.

        Returns:
        set: A set of tuples containing row and column indices of all cells that have three adjacent cells with
             the same color.
        '''
        repeats = set()
        # Traverse the rows
        for i in range(0, BOARD_SIZE - 2):
            for j in range(BOARD_SIZE):
                if arr[i, j] != 'nan' and (arr[i+1:i+3, j] == arr[i, j]).all():
                    repeats.add((i+1,j))
                if arr[j, i] != 'nan' and(arr[j, i+1:i+3] == arr[j, i]).all():
                    repeats.add((j,i+1))

        return repeats

    def current_board(self):
        '''
        Create a copy of the current sub-board.

        Returns:
        np.array: A new sub-board array identical to the current sub-board.
        '''
        return self.board.copy()

    def peek_board(self):
        '''
        Return a slice of the mainboard that displays the top portion of the current sub-board.

        Returns:
        np.array: A slice of the mainboard that shows the top part of the current sub-board with a buffer space on top.
        '''
        return self.board[:, :self.size + 2, :].transpose((1, 0, 2))

    def get_info(self):
        '''
        Get information about the current sub-board and possible operations to transform it into a valid sub-board.

        Returns:
        list: A list consisting of two elements. The first element is the current sub-board array without any color
              information. The second element is a list of all possible operations that can be performed on the
              sub-board to make it valid.
        '''
        operations = []
        arr = self.mainboard
        arrt = self.mainboard.T
        for i in range(self.size - 1):
            for j in range(self.size):
                if i <= self.size - 4 and (arr[i, j] == arr[i+2:i+4, j]).all():
                    operations.append(((i, j), (i+1, j)))
                    continue
                if i >= 2 and (arr[i+1, j] == arr[i-2:i, j]).all():
                    operations.append(((i, j), (i+1, j)))
                    continue
                if j >= 2 and ((arr[i, j] == arr[i+1, j-2:j]).all() |
                        (arr[i+1, j] == arr[i, j-2:j]).all()):
                    operations.append(((i, j), (i+1, j)))
                    continue
                if j <= self.size - 3 and ((arr[i, j] == arr[i+1, j+1:j+3]).all() |
                        (arr[i+1, j] == arr[i, j+1:j+3]).all()):
                    operations.append(((i, j), (i+1, j)))
                    continue
                if j >= 1 and j <= self.size - 2 and ((arr[i, j] == arr[i+1, [j-1, j+1]]).all() |
                        (arr[i+1, j] == arr[i, [j-1, j+1]]).all()):
                    operations.append(((i, j), (i+1, j)))
                    continue
        for i in range(self.size - 1):
            for j in range(self.size):
                if i <= self.size - 4 and (arrt[i, j] == arrt[i+2:i+4, j]).all():
                    operations.append(((j, i), (j, i + 1)))
                    continue
                if i >= 2 and (arrt[i+1, j] == arrt[i-2:i, j]).all():
                    operations.append(((j, i), (j, i + 1)))
                    continue
                if j >= 2 and ((arrt[i, j] == arrt[i+1, j-2:j]).all() |
                        (arrt[i+1, j] == arrt[i, j-2:j]).all()):
                    operations.append(((j, i), (j, i + 1)))
                    continue
                if j <= self.size - 3 and ((arrt[i, j] == arrt[i+1, j+1:j+3]).all() |
                        (arrt[i+1, j] == arrt[i, j+1:j+3]).all()):
                    operations.append(((j, i), (j, i + 1)))
                    continue
                if j >= 1 and j <= self.size - 2 and ((arrt[i, j] == arrt[i+1, [j-1, j+1]]).all() |
                        (arrt[i+1, j] == arrt[i, [j-1, j+1]]).all()):
                    operations.append(((j, i), (j, i + 1)))
                    continue
        cb = self.board[:, :, 0].copy()
        return [cb, operations]

    def change(self, loc1, loc2, *args):
        '''
        Exchange the colors of two adjacent cells in the current sub-board.

        Parameters:
        loc1(tuple): The coordinate (x,y) of one cell to be swapped.
        loc2(tuple): The coordinate (x,y) of another cell to be swapped.
        args: Optional additional parameters that can be ignored.

        Returns:
        None
        '''
        x1, y1 = loc1
        x2, y2 = loc2
        temp1 = self.board[x1, y1, :].copy()
        temp2 = self.board[x2, y2, :].copy()
        self.board[x1, y1, :], self.board[x2, y2, :] = temp2, temp1
        self.move_history.append(((x1, y1), (x2, y2)))

    def eliminate(self, func=lambda x: (x - 2) ** 2):
        '''
        Eliminates connected elements from the mainboard and calculates the score.

        Args:
        func (function): A function that takes in a group of connected elements and returns a score.

        Returns:
        tuple: A tuple that contains the total score (int) and the number of columns eliminated (array).
        '''
        # Scan the board for connected elements
        arr = self.mainboard
        to_eliminate = np.zeros((self.size, self.size), dtype=int)
        directions = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
        to_visit = self.check(arr)
        score = 0

        # Check if it belongs to connected elements
        for coord in to_visit:
            if to_eliminate[coord[0], coord[1]] == 1:
                continue
            head = 0
            connected = [coord, ]
            while head < len(connected):
                current = connected[head]
                to_eliminate[current[0], current[1]] = 1
                for d in directions:
                    neighbor = current + d
                    if (neighbor < 0).any() or (neighbor >= self.size).any():
                        continue
                    if (arr[neighbor[0], neighbor[1]] == arr[current[0], current[1]]
                        and to_eliminate[neighbor[0], neighbor[1]] == 0):
                        connected.append(neighbor)
                head += 1
            score += func(len(connected))

        # Eliminate the columns with connected elements
        col_eliminated = np.sum(to_eliminate, axis=1)
        col_remained = self.size - col_eliminated
        for i in range(self.size):
            if col_eliminated[i] == 0:
                continue
            col = self.board[i]
            self.board[i, :col_remained[i]] = col[:self.size][to_eliminate[i] == 0]
            self.board[i, col_remained[i]:N_ROWS-col_eliminated[i]] = col[self.size:]
            self.board[i, N_ROWS-col_eliminated[i]:] = 'nan'

        # Return the total score and the number of columns eliminated
        return score, col_eliminated
