import numpy as np
import random

BOARD_SIZE = 6
N_ROWS = 1200
COLORS = {'R': '0', 'B': '1', 'G': '2', 'Y': '3', 'P': '4'}
action_space = [((i, j), (i, j + 1)) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE - 1)] + \
               [((i + 1, j), (i, j)) for i in range(BOARD_SIZE - 1) for j in range(BOARD_SIZE)]


class MyBoard:
    def __init__(self, board, colors):
        self.size = board.shape[0]
        self.board = board.copy()
        self.colors = colors

    def change(self, loc1, loc2):
        x1, y1 = loc1
        x2, y2 = loc2
        temp1 = self.board[x1, y1].copy()
        temp2 = self.board[x2, y2].copy()
        self.board[x1, y1], self.board[x2, y2] = temp2, temp1

    @staticmethod
    def check(arr):
        repeats = set()
        for i in range(0, BOARD_SIZE - 2):
            for j in range(BOARD_SIZE):
                if arr[i, j] != 'nan' and (arr[i+1:i+3, j] == arr[i, j]).all():
                    repeats.add((i+1, j))
                if arr[j, i] != 'nan' and (arr[j, i+1:i+3] == arr[j, i]).all():
                    repeats.add((j, i+1))
        return repeats

    def eliminate(self, func=lambda x: (x - 2) ** 2):
        arr = self.board
        to_eliminate = np.zeros((self.size, self.size), dtype=int)
        directions = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
        to_visit = self.check(arr)
        score = 0

        for coord in to_visit:
            if to_eliminate[coord[0], coord[1]] == 1:
                continue
            head = 0
            connected = np.array([coord])
            while head < len(connected):
                current = connected[head]
                to_eliminate[current[0], current[1]] = 1
                for d in directions:
                    neighbor = current + d
                    if (neighbor < 0).any() or (neighbor >= self.size).any():
                        continue

                    if (arr[neighbor[0], neighbor[1]] == arr[current[0], current[1]]
                        and to_eliminate[neighbor[0], neighbor[1]] == 0) and not (connected == [neighbor]).all(1).any():
                        connected = np.concatenate((connected, [neighbor]))
                head += 1
            score += func(len(connected))

        col_eliminated = np.sum(to_eliminate, axis=1)
        col_remained = self.size - col_eliminated
        for i in range(self.size):
            if col_eliminated[i] == 0:
                continue
            col = self.board[i]
            self.board[i, :col_remained[i]] = col[:self.size][to_eliminate[i] == 0]
            self.board[i, col_remained[i]:N_ROWS - col_eliminated[i]] = col[self.size:]
            self.board[i, N_ROWS - col_eliminated[i]:] = 'nan'

        return score, col_eliminated


# 贪心策略
class Best:
    def __init__(self, board):
        self.board = board

    # 直接挑选最优解
    def select(self, valid_movements):
        value = 0
        choice = None
        for action in valid_movements:
            (x1, y1), (x2, y2) = action
            new_board = MyBoard(board=self.board.board, colors=self.board.colors)
            new_board.change((x1, y1), (x2, y2))
            total_score, columns_eliminated = new_board.eliminate()
            while columns_eliminated.sum() and not (new_board.board[:BOARD_SIZE, :BOARD_SIZE] == 'nan').any():
                score, columns_eliminated = new_board.eliminate()
                total_score += score
            if total_score > value:
                value = total_score
                choice = action
        if choice is not None:
            return choice
        return random.choice(action_space)


class Plaser:
    def __init__(self, is_First):
        pass

    def move(self, board, operations, scores, turn_number, **kwargs):
        board = MyBoard(board=board, colors=np.array(list(COLORS.keys())))
        root = Best(board=board)
        return root.select(valid_movements=operations)
