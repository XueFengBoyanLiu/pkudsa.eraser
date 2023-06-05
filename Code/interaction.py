## the game interaction
from board import *
from exception_manager import *
from eraserconfig import *

import traceback
import numpy as np
import json

def serialize_np(obj):
    if isinstance(obj, (np.int64, np.int32)):
        return int(obj)
    if isinstance(obj, np.ndarray):
        return list(obj)
    raise TypeError ("Type %s is not serializable" % type(obj))

class Game_play():
    def __init__(self, player_1, player_2, board=None, order=0, seed=None):
        '''
        Parameters
        ----------
        player_1, player_2: the player's code
        '''
        self.players = (Player_safe(player_1.Plaser, False),
                Player_safe(player_2.Plaser, True))
        self.terminated = False

        # the players are wrapped by exception_manager.py
        self.board = Board(seed=seed) if board is None else board
        self.remained_blocks = np.full(BOARD_SIZE, N_ROWS - BOARD_SIZE - 2)

        self.turn = 0
        self.replay = {'totalFrames': 0,
                'totalRemains': (N_ROWS - BOARD_SIZE - 2),
                'scores': {},
                'errorStatus': -1,
                'errorMessage': '',
                'winner': -1,
                'frames': [],
                'extra': '',
                'order': order,
                'players': (player_1.__name__, player_2.__name__)}

        self.scores_history = []
        self.score = [0, 0]
        self.high_combo = [0, 0]
        self.current_combo = [0, 0]

        if not self.players[0].error:
            self.players[0].core.move_history = []
            self.players[0].core.used_time = [0, 0]
        else:
            self.replay['winner'] = 1
            self.replay['errorStatus'] = 0
            self.replay['errorMessage'] = self.players[0].error
            self.terminated = True
        if not self.players[1].error:
            self.players[1].core.move_history = []
            self.players[1].core.used_time = [0, 0]
        else:
            self.replay['winner'] = 0
            self.replay['errorStatus'] = 1
            self.replay['errorMessage'] = self.players[1].error
            self.terminated = True
        self.record_frame()

    def _get_side_status(self, side=0):
        a = 1 if self.score[side] >= self.score[1 - side] else 0
        b = -1 if self.score[side] <= self.score[1 - side] else 0
        data = {'totalScores': self.score[side],
                'highestCombo': self.high_combo[side],
                'currentCombo': self.current_combo[side],
                'status': a + b,
                'totalTime': self.players[side].time}
        return data

    @property
    def status(self):
        return {'left': self._get_side_status(0),
                'right': self._get_side_status(1)}

    def perform_turn(self):
        '''
        Perform one game turn
        '''
        self.scores_history.append(self.score.copy())
        if self.terminated:
            self.end_game()
            return
        if self.turn >= MAX_TURN * 2:
            self.terminated = True
            return
        if (self.board.mainboard == 'nan').any():
            self.terminated = True
        info = self.board.get_info()
        if not info[1]:
            self.terminated = True
            return

        # update turn data
        self.turn += 1
        side = self.turn & 1
        current_player = self.players[side]
        # self.scores_history.append(self.score.copy())
        self.current_combo[side] = 0

        # make a move for the current player
        mv = self.ask_for_move(current_player, info)
        if current_player.error is not None:
            self.terminated = True
            self.replay['winner'] = 1 - side
            self.replay['errorStatus'] = side
            self.replay['errorMessage'] = current_player.error
            return

        self.board.change(*mv)
        self.players[0].core.move_history.append(mv)
        self.players[1].core.move_history.append(mv)
        self.players[0].core.used_time[side] = self.players[1].core.used_time[1-side] = self.players[side].time
        self.record_frame()

        # eliminating blocks
        while True:
            pts, columns_eliminated = self.board.eliminate()
            if pts == 0:
                break
            self.remained_blocks = self.remained_blocks - columns_eliminated
            self.score[side] += pts
            self.current_combo[side] += columns_eliminated.sum()
            self.high_combo[side] = max(self.high_combo[side],
                    self.current_combo[side])

            self.record_frame()

    def ask_for_move(self, player, info):
        '''
        Given current board, get a move from the current player
        Returns: ((x1, y1), (x2, y2))
        '''
        score = self.score if self.turn % 2 == 0 else self.score[::-1]
        return player('move', *info, score.copy(), (self.turn+1)//2)

    def record_frame(self):
        '''
        Generate a frame for replay
        '''
        self.replay['totalFrames'] += 1
        board_status = self.board.peek_board()
        frame = {'turnNumber': self.turn,
                'currentPlayer': self.turn & 1,
                'remainedBarStatus': self.remained_blocks.clip(0, None)}
        board_status = {'nan' if board_status[i, j, 0] == 'nan'
                        else board_status[i, j, 1] + 'b' +
                        COLORS[board_status[i, j, 0]]: [i, j]
                            for i in range(board_status.shape[0])
                                for j in range (board_status.shape[1])}
        frame['boardStatus'] = {}
        for k, v in board_status.items():
            if k != 'nan':
                frame['boardStatus'][k] = v
        frame['sideBarStatus'] = self.status
        self.replay['frames'].append(frame)
        return

    def start_game(self):
        while not self.terminated:
            self.perform_turn()
        self.record_frame()
        self.end_game()
        return self.replay

    def end_game(self):
        '''End the game and format the replay as .json file'''
        if self.replay['errorStatus'] == -1:
            self.replay['winner'] = np.argmax(self.score)
            if self.score[0] == self.score[1]:
                self.replay['winner'] = 0 if self.players[0].time < self.players[1].time else 1

        if self.scores_history:
            history = np.vstack(self.scores_history)
        else:
            history = np.array([[0, 0]])
        self.replay['scores'] = {'left': history[:, 0],
                                'right': history[:, 1],
                                'relative': history[:, 1] - history[:, 0]}
        self.replay['length'] = self.turn
        self.replay['time'] = np.array([self.players[0].time, self.players[1].time])

        if self.replay['errorStatus'] == -1:
            self.replay['extra'] = abs(self.score[0] - self.score[1])
            if self.turn < 2 * MAX_TURN:
                if (self.board.mainboard == 'nan').any():
                    self.replay['reason'] = 'Run out of blocks'
                else:
                    self.replay['reason'] = 'No eraserable moves'
            else:
                self.replay['reason'] = 'Reach the maximum turn number'
        else:
            self.replay['extra'] = 1000
            self.replay['reason'] = 'An error occurred: '
            self.replay['reason'] += self.replay['errorMessage'].split('\n')[-2]

        if self.turn >= 6:
            self.replay['tag'] = self.tags

    def save_log(self, path):
        with open(path, 'w') as f:
            json.dump(self.replay, f, default = serialize_np)
        return

    @property
    def tags(self):
        tags = []
        relative = self.replay['scores']['relative']
        lead = np.sum(relative < 0) / self.turn
        if abs(self.score[0] - self.score[1]) < 15:
            tags.append(('险胜', 'red'))
        if abs(lead - 0.5) < 0.15 and abs(relative.mean()) < 100:
            tags.append(('有来有回', 'blue'))
        if abs(lead - 0.5) > 0.4 and abs(relative.mean()) > 150:
            tags.append(('压制', 'blue'))
        if self.replay['errorStatus'] == -1:
            if abs(self.score[0] - self.score[1]) > 250:
                tags.append(('遥遥领先', 'red'))
            if relative[-1] * relative[-2] < 0 or relative[-2] * relative[-3] < 0:
                tags.append(('绝杀', 'purple'))
            if (relative > 200).sum() >= 5 and self.replay['winner'] == 0:
                tags.append(('逆风翻盘', 'green'))
            if (relative < -200).sum() >= 5 and self.replay['winner'] == 1:
                tags.append(('逆风翻盘', 'green'))
            if self.replay['reason'] == 'No eraserable moves' and abs(relative[-1]) < 50 and self.turn % 2 == self.replay['winner']:
                tags.append(('不讲武德', 'orange'))
            if self.replay['reason'] == 'No eraserable moves' and self.turn % 2 != self.replay['winner']:
                tags.append(('申之一手', 'orange'))
            if self.replay['reason'] == 'Reach the maximum turn number':
                tags.append(('血战到底', 'orange'))
        else:
            if relative[-1] * (self.replay['winner'] - 0.5) < 0:
                tags.append(('是故意的', 'orange'))
        hc = max(self.high_combo[0], self.high_combo[1])
        tags.append(('{}连消'.format(hc), 'gray'))
        return tags

    @property
    def log_data(self):
        '''Return the log data to server'''
        log = {'winner': self.replay['winner'],
                'errorMessage': '',
                'errorStatus': self.replay['errorStatus'],
                'length': self.turn,
                'score': 500,
                'reason': None,
                'time': [self.players[0].time, self.players[1].time]}
        if self.replay['errorStatus'] == -1:
            log['score'] = abs(self.score[0] - self.score[1])
            log['reason'] = self.replay['reason']
        else:
            log['reason'] = ''
            log['errorMessage'] = self.replay['errorMessage'].split('\n')[-2]
            log['reason'] += log['errorMessage']
        if self.turn >= 6:
            log['tag'] = self.tags
        return log

if __name__ == '__main__':
    import test_bot
    import failed_test_bot as fb
    import greedy_robot
    game = Game_play(test_bot, fb)
    import time
    a = time.time()
    game.start_game()
    b = time.time()
    print(b - a)
    print(game.log_data)
    import matplotlib.pyplot as plt
    plt.plot(game.replay['scores']['relative'])
    plt.axis(True)
    plt.show()
    game.save_log('replay.json')
