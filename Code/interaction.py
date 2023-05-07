## the game interaction
#from __future__ import annotations
from board import *
from exception_manager import *
from eraserconfig import *

import threading
import time
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
    def __init__(self, player_1, player_2, board=None):
        '''
        Parameters
        ----------
        player_1, player_2: imported from player's code
        '''
        self.players = (Player_safe(player_1), Player_safe(player_2))
        self.terminated = False
        # the players are wrapped by exception_manager.py
        self.board = Board() if board is None else board
        self.remained_blocks = [N_ROWS - BOARD_SIZE for _ in range(BOARD_SIZE)]

        self.turn = 0
        self.replay = {'totalFrames': 0,
                'totalRemains': (N_ROWS - BOARD_SIZE),
                'scores': {},
                'exitStatus': 0,
                'errorMessage': '',
                'winner': -1,
                'frames': []}

        self.scores_history = []
        self.score = [0, 0]
        self.high_combo = [0, 0]
        self.current_combo = [0, 0]

        self.record_frame()

    def _get_side_status(self, side=0):
        a = 1 if self.score[side] >= self.score[1 - side] else 0
        b = -1 if self.score[side] <= self.score[1 - side] else 0
        data = {'totalScores': self.score[side],
                'highestCombo': self.high_combo[side],
                'currentCombo': self.current_combo[side],
                'status': a + b}
        return data

    @property
    def status(self):
        return {'left': self._get_side_status(0),
                'right': self._get_side_status(1)}

    def perform_turn(self):
        '''
        Perform one game turn
        '''
        if self.terminated:
            self.end_game()
            return
        if self.turn >= MAX_TURN * 2:
            self.terminated = True
            return
        if (self.board.peek_board()[:BOARD_SIZE, :BOARD_SIZE] == 'nan').any():
            self.terminated = True

        # update turn data
        self.turn += 1
        side = self.turn & 1
        current_player = self.players[side]
        self.scores_history.append(self.score.copy())
        self.current_combo[side] = 0
        print(f'perform turn {self.turn}, current player {side}')

        # make a move for the current player
        mv = self.ask_for_move(current_player)
        if current_player.error is not None:
            self.terminated = True
            self.replay['winner'] = 1 - side
            self.replay['exitStatus'] = 1
            self.replay['errorMessage'] = current_player.error
            return

        self.board.change(*mv)
        self.record_frame()

        # eliminating blocks
        while True:
            pts, columns_eliminated = self.board.eliminate()
            if columns_eliminated.sum() == 0:
                break
            self.remained_blocks = self.remained_blocks - columns_eliminated
            self.score[side] += pts
            self.current_combo[side] += columns_eliminated.sum()
            #print(self.current_combo)
            self.high_combo[side] = max(self.high_combo[side],
                    self.current_combo[side])

            self.record_frame()

    def ask_for_move(self, player):
        '''
        Given current board, get a move from the current player
        Returns: ((x1, y1), (x2, y2))
        '''
        #if self.board.get_info()[1] == []:
            #print('no moves available')
        return player('move', *self.board.get_info())

    def record_frame(self):
        '''
        Generate a frame for replay
        '''
        self.replay['totalFrames'] += 1
        board_status = self.board.peek_board()
        frame = {'turnNumber': self.turn,
                'currentPlayer': self.turn & 1,
                'remainedBarStatus': self.remained_blocks}
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
        print('Game starts')
        while not self.terminated:
            self.perform_turn()
        self.end_game()

    def end_game(self):
        '''End the game and format the replay as .json file'''
        self.terminated = True

        if not self.replay['exitStatus']:
            self.replay['winner'] = np.argmax(self.score)

        history = np.vstack(self.scores_history)
        self.replay['scores'] = {'left': history[:, 0],
                                'right': history[:, 1],
                                'relative': history[:, 0] - history[:, 1]}
        print('Game ends')

    def save_log(self, path):
        with open(path, 'w') as f:
            json.dump(self.replay, f, default = serialize_np)
        return

    @property
    def log_data(self):
        '''Return the log data to server'''
        log = {'winner': self.replay['winner'],
                'errorMessage': '',
                'errorStatus': self.replay['exitStatus'] - 1,
                'length': self.turn,
                'score': 1000,
                'reason': None}
        if not self.replay['exitStatus']:
            log['score'] = abs(self.score[0] - self.score[1])
            if self.turn < 2 * MAX_TURN:
                log['reason'] = 'Run out of blocks'
            else:
                log['reason'] = 'Reach turn limit'
        else:
            log['reason'] = 'An error occurred during the game, see error message for details'
            log['errorMessage'] = self.replay['errorMessage'].split('\n')[-2]
        return log

class Game_runner():
    def __init__(self, p1, p2):
        self.board1 = Board()
        self.board2 = Board()
        self.p1 = p1
        self.p2 = p2

    def start_games(self):
        self.game1 = Game_play(self.p1, self.p2, board=self.board1)
        self.game1.start_game()
        self.game2 = Game_play(self.p2, self.p1, board=self.board2)
        self.game2.start_game()
        log1, log2 = self.game1.log_data, self.game2.log_data
        log2['winner'] = 1 - log2['winner']
        return log1, log2

    def save_game_log(self, path1, path2):
        self.game1.save_log(path1)
        self.game2.save_log(path2)

if __name__ == '__main__':
    import test_bot
    tp = test_bot.Robot()
    import failed_test_bot as fb
    bots = [fb.FailedRobot1(), fb.FailedRobot2(), fb.FailedRobot3(),
            fb.FailedRobot4(), fb.FailedRobot5()]
    game = Game_runner(tp, tp)
    print(game.start_games())
    game.save_game_log('r1.json', 'r2.json')
