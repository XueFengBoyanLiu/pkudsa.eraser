import numpy as np
import random
np.set_printoptions(threshold=np.inf)

class Board:
    # 初始化棋盘大小、颜色和棋盘数量
    def __init__(self, size=8, num=100, colors=np.array(['R', 'G', 'B', 'Y'])):
        '''
        初始化棋盘
        size: 棋盘大小，默认值为8
        num: 一个测试中生成的子棋盘数量，默认值为100
        colors: 可用颜色列表， 默认为 ['R', 'G', 'B', 'Y']
        '''
        self.size = size
        self.colors = colors  # 可选颜色数组
        self.board = np.concatenate([self.generate_board() for i in range(num)]).T # 连接多个棋盘
        #！！！注意！！！这里把棋盘转置了一下（不会写移到列底，只会写移到行末）
        self.move_dict = {}  # 记录每一步移动
        self.round = 0  # 当前回合数

    # 生成一个新棋盘，并保证该棋盘不存在连续三个相邻相同的颜色方块
    def generate_board(self):
        '''
        生成一个新的随机子棋盘，并且保证没有任何相邻元素的颜色相同。

        返回值：
        np.array：返回新生成的矩阵；
        '''
        a = np.concatenate([np.full((self.size // 2, self.size // 2), self.colors[i])
            for i in range(4)]).reshape(self.size ** 2, 1)

        np.random.shuffle(a)  # 打乱颜色块的顺序
        new_array = a.reshape(self.size, self.size)

        while self.check(new_array):  # 检查是否存在连续三个相邻元素
            for i, j in self.check(new_array):
                # 随机替换掉其中一个同色元素
                new_array[i][j] = new_array[i - np.random.randint(1,self.size-1)][j - np.random.randint(1,self.size-1)]

        return new_array

    def current_board(self):
        '''
        返回当前棋盘的状态副本。

        返回值：
        np.array：返回当前棋盘的状态副本矩阵；
        '''
        return self.board.copy()

    # 获取主要棋盘（size*size）
    def main_board(self):
        '''
        返回当前棋盘的主要区域（正方形区域），长度为size的二维numpy数组。

        返回值：
        np.array: 返回当前棋盘状态下的主要区域。
        '''
        return self.board[:self.size, :self.size]

    # 检查棋盘是否存在连续三个相邻的同色元素
    def check(self, array):
        '''
        返回在电路中重复的位置。

        参数：
        array: 以二维数组形式输入的元素列表；

        返回值：
        set: （i，j）位置集合，即 (i, j) 是重复位置。
        '''
        repeats = set()
        for i in range(1, self.size - 1):  # 遍历行
            for j in np.arange(self.size):
                a = array[i - 1:i + 2, j]
                b = (a == array[i, j])
                if np.sum(b) == 3:
                    repeats.add((i, j))
        for i in range(1, self.size - 1):  # 遍历列
            for j in np.arange(self.size):
                a = array[j, i - 1:i + 2]
                b = (a == array[j, i])
                if np.sum(b) == 3:
                    repeats.add((j, i))
        return repeats

    def move(self, row1, col1, row2, col2):
        '''
        在棋盘上移动两个颜色方块，并存储每一步操作。

        参数：
        row1, col1: 第一块方块的行和列索引
        row2, col2: 第二块方块的行和列索引

        返回值：
        list: 包含下面 4 个元素的切片列表
            - 当前棋盘状态
            - 第一块方块的坐标和颜色信息
            - 第二块方块的坐标和颜色信息
            - 移动后的新棋盘状态
       '''
        self.round += 1                                            # 当前回合数+1
        self.move_dict[self.round] = [self.current_board(), (row1, col1, self.board[row1, col1]),
                                      (row2, col2, self.board[row2, col2])]  # 记录此次操作前的棋盘和两个方块的信息
        self.board[row1, col1], self.board[row2, col2] = self.board[row2, col2], self.board[row1, col1]   # 调换两个棋子
        self.move_dict[self.round].append(self.current_board())     # 记录此次操作后的棋盘矩阵
        return self.move_dict[self.round]                           # 返回当前操作的所有步骤，供后续检查和分析使用

    def scan_for_connected(self):
        matrix=self.board
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
        #用广搜获得所有主盘面上联通的元素，以[[(x11,y11),...,(x1n,y1n)],...,[(xn1,yn1),...,(xnn,ynn)]]的形式储存所有联通的瞳色元素
        list_of_connected_elements = [sublst for sublst in res if any(len(set([coord[0] for coord in sublst[i:i + 3]])) == 1 and len(
            set([coord[1] for coord in sublst[i:i + 3]])) == 3 or len(
            set([coord[0] for coord in sublst[i:i + 3]])) == 3 and len(
            set([coord[1] for coord in sublst[i:i + 3]])) == 1 for i in range(len(sublst) - 2))]
        #筛选出所有在同一行（或列）有三个及以上连续元素的的联通元素组
        return list_of_connected_elements

    def eliminate_and_score(self):
        list_of_connected_elements=self.scan_for_connected()
        scorelist = list(map(lambda x: (len(x) - 2) ** 2, list_of_connected_elements))
        score=sum(scorelist)
        #为了避免多次调用，在这里也顺便把分算了 score:int 总得分
        for sublst in list_of_connected_elements:
            for cordinates in sublst:
                self.board[cordinates]="Q"
        #把所有的连续同色元素替换成“Q”
        for i in range(self.board.shape[0]):
            row = self.board[i]
            Q_indices = np.where(row == 'Q')[0]
            if len(Q_indices) > 0:
                row = np.concatenate((row[row != 'Q'], row[Q_indices]))
                self.board[i] = row
        #将所有的“Q”移到最上(其实是右）方





