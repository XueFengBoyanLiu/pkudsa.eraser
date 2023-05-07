import numpy as np

BOARD_SIZE = 6
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
        self.size = board.shape[1]
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

    def scan_for_connected(self):
        '''
        Scan the mainboard for connected elements.
        Returns:
        list: A list of connected elements groups. Each group consists of elements with the same color that are
              connected in a row or column and has three or more elements.
        '''
        matrix = self.board[:, :]
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
            col = self.board[0:self.size, i]
            indices = np.where(changed[:, i] == False)[0]
            if len(indices) != self.size:
                self.board[:, i] = np.concatenate(
                    (col[indices], self.board[self.size:, i],
                     np.full((columns_eliminated[i],), np.nan)), axis=0)

        # Return the total score and the number of columns eliminated
        return score, columns_eliminated


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
        while columns_eliminated.sum() != 0 and not (new_board.board[:BOARD_SIZE, :BOARD_SIZE] == 'nan').any():
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


class GreedyRobot:
    def __init__(self):
        pass

    @ staticmethod
    def move(current_board, valid_movements):
        board = MyBoard(board=current_board)
        root = Best(board=board)
        return root.select()
