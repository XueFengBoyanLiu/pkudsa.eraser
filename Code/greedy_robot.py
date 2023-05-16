import numpy as np
from eraserconfig import *

action_space = [((i, j), (i, j + 1)) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE - 1)] + \
               [((i + 1, j), (i, j)) for i in range(BOARD_SIZE - 1) for j in range(BOARD_SIZE)]


class MyBoard:
    def __init__(self, board):
        '''
        Initialize board instance.
        Parameters:
        size(int): Size of each sub-board
        board_num(int): Number of sub-boards in the main board
        colors(np.array): Array of available colors
        '''
        self.size = board.shape[0]
        self.board = board

    def change(self, loc1, loc2):
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
        temp1 = self.board[x1, y1].copy()
        temp2 = self.board[x2, y2].copy()
        self.board[x1, y1], self.board[x2, y2] = temp2, temp1

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

        '''
        for i in range(self.size):
            for j in range(self.size):
                if arr[i, j] == 'nan':
                    continue
                if i <= self.size - 3 and (arr[i+1:i+3, j] == arr[i, j]).all():
                    to_visit.append([i+1, j])
                if j <= self.size - 3 and (arr[i, j+1:j+3] == arr[i, j]).all():
                    to_visit.append([i, j+1])
        '''
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
            self.board[i, N_ROWS-col_eliminated[i]:] = np.nan

        # Return the total score and the number of columns eliminated
        return score, col_eliminated

    @property
    def mainboard(self):
        return self.board[:self.size, :self.size]


# 贪心策略
class Best:
    def __init__(self, board):
        self.board = board

    # 在棋盘上进行一次操作
    def move(self, action):
        (x1, y1), (x2, y2) = action
        new_board = MyBoard(self.board.board.copy())
        new_board.change((x1, y1), (x2, y2))
        total_score, columns_eliminated = new_board.eliminate()
        score = total_score
        while score != 0 and not (new_board.board[:BOARD_SIZE, :BOARD_SIZE] == 'nan').any():
            score, columns_eliminated = new_board.eliminate()
            total_score += score
        return new_board, total_score

    # 直接挑选最优解
    def select(self):
        value = 0
        choice = None
        for action in action_space:
            new_board, total_score = self.move(action)
            if total_score > value:
                value = total_score
                choice = action
        if choice is not None:
            return choice
        return action_space[np.random.randint(0, len(action_space))]


class Plaser:
    def __init__(self, *args):
        pass

    @ staticmethod
    def move(current_board, valid_movements, *args):
        board = MyBoard(board=current_board)
        root = Best(board=board)
        return root.select()
