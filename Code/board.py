import numpy as np
import random
import pandas as pd


class Board:
    def __init__(self, size=8, board_num=1000, colors=np.array(['R', 'G', 'B', 'Y'])):
        self.size = size
        self.colors = colors  # 可选颜色数组
        self.board = np.concatenate([self.generate_board() for i in np.arange(board_num)])  # 连接多个棋盘
        self.move_dict = {}  # 记录每一步移动
        a = np.indices((self.size * board_num, self.size))
        self.id_matrix = np.apply_along_axis(lambda x: f'r{x[0]:04d}c{x[1]:04d}', 0, a)

    def generate_board(self):
        a = np.concatenate([np.full((self.size // 2, self.size // 2), self.colors[i]) for i in np.arange(4)]).reshape(
            (self.size ** 2, 1))
        np.random.shuffle(a)  # 打乱颜色块的顺序
        new_array = a.reshape(self.size, self.size)
        while self.check(new_array):  # 检查是否存在连续三个相邻元素
            for i, j in self.check(new_array):
                new_array[i][j] = new_array[i - random.randint(1, self.size - 1)][j - random.randint(1, self.size - 1)]
        return new_array

    def check(self, array):
        repeats = set()
        for i in np.arange(1, self.size - 1):  # 遍历行
            for j in np.arange(self.size):
                a = array[i - 1:i + 2, j]
                b = (a == array[i, j])
                if np.sum(b) == 3:
                    repeats.add((i, j))
        for i in np.arange(1, self.size - 1):  # 遍历列
            for j in np.arange(self.size):
                a = array[j, i - 1:i + 2]
                b = (a == array[j, i])
                if np.sum(b) == 3:
                    repeats.add((j, i))
        return repeats

    def current_board(self):
        return self.board.copy()

    def peek_board(self):
        return self.id_matrix

    def get_info(self):
        pass

    def change(self, x1, y1, x2, y2, *args):
        self.board[[x1, y1], [x2, y2]] = self.board[[x2, y2], [x1, y1]]
        self.id_matrix[[x1, y1], [x2, y2]] = self.id_matrix[[x2, y2], [x1, y1]]

    def scan_for_connected(self):
        matrix = self.board
        visited = set()
        res = []
        for i in range(self.size):
            for j in range(self.size):
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
        # 用广搜获得所有主盘面上联通的元素，以[[(x11,y11),...,(x1n,y1n)],...,[(xn1,yn1),...,(xnn,ynn)]]的形式储存所有联通的瞳色元素
        list_of_connected_elements = [sublst for sublst in res if
                                      any(len(set([coord[0] for coord in sublst[i:i + 3]])) == 1 and len(
                                          set([coord[1] for coord in sublst[i:i + 3]])) == 3 or len(
                                          set([coord[0] for coord in sublst[i:i + 3]])) == 3 and len(
                                          set([coord[1] for coord in sublst[i:i + 3]])) == 1 for i in
                                          range(len(sublst) - 2))]
        # 筛选出所有在同一行（或列）有三个及以上连续元素的的联通元素组
        return list_of_connected_elements

    def eliminate(self):
        list_of_connected_elements = self.scan_for_connected()
        scorelist = list(map(lambda x: (len(x) - 2) ** 2, list_of_connected_elements))
        score = sum(scorelist)
        # 为了避免多次调用，在这里也顺便把分算了 score:int 总得分
        changed = np.zeros((self.size, self.size), bool)

        for sublst in list_of_connected_elements:
            for cordinates in sublst:
                changed[cordinates] = True
        columns_eliminated = self.size * np.mean(changed, axis=0)

        # 把所有的连续同色元素替换成“Q”,并以columns_eliminated（numpy array）返回每一列被消除的元素个数
        for i in range(self.size):
            col = self.board[0:self.size, i]
            indices = np.where(changed[:, i] == False)[0]
            if len(indices) != self.size:
                self.board[0:self.size, i] = np.concatenate(
                    (col[indices], self.board[int(self.index[i]):int(self.index[i] + columns_eliminated[i]), i]))
        # 索引主棋盘以外的和被消除部分等长的部分顺次填补主棋盘的空缺
        return score, columns_eliminated

