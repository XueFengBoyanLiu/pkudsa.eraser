import numpy as np
import random
from eraserconfig import *

class Board:
    def __init__(self, size=BOARD_SIZE, board_num=N_ROWS//BOARD_SIZE,
            colors=np.array(list(COLORS.keys()))):
        '''
        Initialize board instance.

        Parameters:
        size(int): Size of each sub-board
        board_num(int): Number of sub-boards in the main board
        colors(np.array): Array of available colors
        '''
        self.size = size
        self.board_num = board_num
        self.colors = colors
        self.board = np.concatenate([self.generate_board() for i in np.arange(board_num)])
        self.move_dict = {}

        # Use numpy.indices to create a matrix of row/column indices for each cell
        a = np.indices((self.size * board_num, self.size))
        # Use numpy.apply_along_axis function to generate unique IDs for cells using row/column indices
        self.id_matrix = np.apply_along_axis(lambda x: f'r{x[0]:04d}c{x[1]:04d}', 0, a)

        # Add ID matrix to the main board
        self.board = np.dstack((self.board, self.id_matrix))
        # Extract the first sub-board to use as the main board.
        self.mainboard = self.board[:self.size, :self.size, 0]

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
        a = np.vstack([np.full((self.size, self.size // len(self.colors) + remain[i]),
            self.colors[idx[i]]) for i in range(len(self.colors))]).reshape(
            (self.size ** 2, 1))
        np.random.shuffle(a)  # Shuffle the order of color blocks.

        # Reshape sub-board array using the shuffled colors.
        new_array = a.reshape(self.size, self.size)

        # If there are three adjacent cells with the same color, randomly choose a different color for one of them
        while self.check(new_array):
            for i, j in self.check(new_array):
                new_array[i][j] = new_array[i - random.randint(1, self.size - 1)][j - random.randint(1, self.size - 1)]

        # Return the generated sub-board.
        return new_array

    def check(self, array):
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
        for i in np.arange(1, self.size - 1):
            for j in np.arange(self.size):
                a = array[i - 1:i + 2, j]
                b = (a == array[i, j])
                if np.sum(b) == 3:
                    repeats.add((i, j))

        # Traverse the columns
        for i in np.arange(1, self.size - 1):
            for j in np.arange(self.size):
                a = array[j, i - 1:i + 2]
                b = (a == array[j, i])
                if np.sum(b) == 3:
                    repeats.add((j, i))

        # Return a set of tuple(s) which contain the location(s) of cells whose neighbors share the same color.
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
        return self.board[:self.size + 2, :self.size, :]

    def get_info(self):
        '''
        Get information about the current sub-board and possible operations to transform it into a valid sub-board.

        Returns:
        list: A list consisting of two elements. The first element is the current sub-board array without any color
              information. The second element is a list of all possible operations that can be performed on the
              sub-board to make it valid.
        '''
        operations = []
        for i in range(self.size - 1):
            for j in range(self.size):
                self.mainboard[i, j], self.mainboard[i + 1, j] = self.mainboard[i + 1, j], self.mainboard[i, j]
                if self.check(self.mainboard):
                    operations.append([(i, j), (i + 1, j)])
                self.mainboard[i, j], self.mainboard[i + 1, j] = self.mainboard[i + 1, j], self.mainboard[i, j]
        for j in range(self.size - 1):
            for i in range(self.size):
                self.mainboard[i, j], self.mainboard[i, j + 1] = self.mainboard[i, j + 1], self.mainboard[i, j]
                if self.check(self.mainboard):
                    operations.append([(i, j), (i, j + 1)])
                self.mainboard[i, j], self.mainboard[i, j + 1] = self.mainboard[i, j + 1], self.mainboard[i, j]
        return [self.board[:, :, 0], operations]
    
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

    def scan_for_connected(self):
        '''
        Scan the mainboard for connected elements.

        Returns:
        list: A list of connected elements groups. Each group consists of elements with the same color that are
              connected in a row or column and has three or more elements.
        '''
        matrix = self.board[:, :, 0]
        visited = set()
        res = []
        for i in range(self.size):
            for j in range(self.size):
                if matrix[i, j] not in self.colors:
                    visited.add((i, j))
                    continue
                if (i, j) not in visited:
                    visited.add((i, j))
                    temp = []
                    queue = [(i, j)]
                    while queue:
                        x, y = queue.pop(0)
                        temp.append((x, y))
                        if x + 1 < self.size and (x + 1, y) not in visited and matrix[x + 1][y] == matrix[x][y]:
                            queue.append((x + 1, y))
                            visited.add((x + 1, y))
                        if x - 1 >= 0 and (x - 1, y) not in visited and matrix[x - 1][y] == matrix[x][y]:
                            queue.append((x - 1, y))
                            visited.add((x - 1, y))
                        if y + 1 < self.size and (x, y + 1) not in visited and matrix[x][y + 1] == matrix[x][y]:
                            queue.append((x, y + 1))
                            visited.add((x, y + 1))
                        if y - 1 >= 0 and (x, y - 1) not in visited and matrix[x][y - 1] == matrix[x][y]:
                            queue.append((x, y - 1))
                            visited.add((x, y - 1))
                    res.append(temp)
        # Iterate through every element on the mainboard and perform a breadth-first search for connected elements.
        # Store each group of connected elements in the res list.
        list_of_connected_elements = []
        for sublst in res:
            lx=sorted(sorted(sublst, key=lambda x: x[1]), key=lambda x: x[0])
            ly=sorted(sorted(sublst, key=lambda x: x[0]), key=lambda x: x[1])
            for i in range(len(sublst)-2):
                if sublst not in list_of_connected_elements and lx[i][0]==lx[i+1][0]==lx[i+2][0] and lx[i][1]+2==lx[i+1][1]+1==lx[i+2][1]:
                    list_of_connected_elements.append(sublst)
                    break
            for j in range(len(sublst)-2):
                if sublst not in list_of_connected_elements and ly[j][1]==ly[j+1][1]==ly[j+2][1] and ly[j][0]+2==ly[j+1][0]+1==ly[j+2][0]:
                    list_of_connected_elements.append(sublst)
                    break
        # Filter out groups that have three or more connected elements in a row or column and return the list.
        return list_of_connected_elements

    def eliminate(self, func=lambda x: (len(x) - 2) ** 2):
        '''
        Eliminates connected elements from the mainboard and calculates the score.

        Args:
        func (function): A function that takes in a group of connected elements and returns a score.

        Returns:
        tuple: A tuple that contains the total score (int) and the number of columns eliminated (array).
        '''
        # Scan the board for connected elements
        list_of_connected_elements = self.scan_for_connected()

        # Calculate the score for each connected element
        scorelist = list(map(func, list_of_connected_elements))

        # Calculate the total score
        score = sum(scorelist)

        # Mark the connected elements as changed
        changed = np.zeros((self.size, self.size), bool)
        for sublst in list_of_connected_elements:
            for cordinates in sublst:
                changed[cordinates] = True

        # Eliminate the columns with connected elements
        columns_eliminated = np.sum(changed, axis=0)
        for i in range(self.size):
            col = self.board[0:self.size, i, :]
            indices = np.where(changed[:, i] == False)[0]
            if len(indices) != self.size:
                self.board[:, i, :] = np.concatenate(
                    (col[indices, :], self.board[self.size:, i, :],
                     np.full((columns_eliminated[i], 2), np.nan)), axis=0)

        # Return the total score and the number of columns eliminated
        return score, columns_eliminated

