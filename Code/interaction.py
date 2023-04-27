## the game interaction
from __future__ import annotations
from board import *
from exception_manager import *

#from player1 import Robot as P1
#from player2 import Robot as P2
## player class: Robot (the name may change)
## method: move(np.array: current_board) -> tuple: 2 blocks to move
## attribute: name(str)
#player_safe_1 = Player(P1)
#player_safe_2 = Player(P2)

import threading
import time
import traceback
import numpy as np
import pandas as pd
import json

from config import *

class Game_play():
    def __init__(self, player_1, player_2):
        '''
        Parameters
        ----------
        player_1, player_2: imported from player's code
        '''
        self.players = (Player_safe(player_1), Player_safe(player_2))
        self.terminated = False
        self.winner = None
        # the players are wrapped by exception_manager.py
        self.board = Board()
        self.remained_blocks = [N_ROWS - BOARD_SIZE for i in range(BOARD_SIZE)]

        self.turn = 0
        self.replay = {'totalFrames': 0,
                'totalRemains': BOARD_SIZE * (N_ROWS - BOARD_SIZE),
                'scores': {},
                'exitStatus': 0,
                'errorMessage': '',
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
            self.end_game()
            return

        # update turn data
        self.turn += 1
        side = self.turn & 1
        current_player = self.players[side]
        self.scores_history.append(self.score)
        self.current_combo[side] = 0

        # make a move for the current player
        mv = self.ask_for_move(current_player)
        if current_player.error is not None:
            self.terminated = True
            self.winner = self.players[1 - side]
            self.replay['exitStatus'] = side
            self.replay['errorMessage'] = current_player.error
            self.end_game()
            return

        if not self.is_invalid_move(mv):
            self.terminated = True
            self.winner = self.players[1 - side]
            self.end_game()
            return
        self.board.change(*mv)

        self.record_frame()

        # eliminating blocks
        while True:
            pts, columns_eliminated, is_end = self.board.eliminate()
            if columns_eliminated.sum() == 0:
                break
            self.remained_blocks = self.remained_blocks - columns_eliminated
            self.score[side] += pts
            self.current_combo[side] += columns_eliminated.sum()
            self.high_combo[side] = max(self.high_combo[side],
                    self.current_combo[side])
            self.record_frame()

    def ask_for_move(self, player):
        '''
        Given current board, get a move from the current player
        Returns: ((x1, y1), (x2, y2))
        '''
        return player('move', self.board.get_info())

    def record_frame(self):
        '''
        Generate a frame for replay
        '''
        self.replay['totalFrames'] += 1
        board_status = self.board.peek_board()
        frame = {'turnNumber': self.turn,
                'currentPlayer': self.turn & 1,
                'remainedBarStatus': self.remained_blocks}
        frame['boardStatus'] = {board_status[i, j]: [i, j]
                                    for i in range(n_rows)
                                        for j in range (n_cols)}
        frame['sideBarStatus'] = self.status
        self.replay['frames'].append(frame)
        return

    def end_game(self):
        '''End the game and format the replay as .json file'''
        history = np.vstack(self.scores_history)
        history = pd.DataFrame(history, columns=['left', 'right'])
        history['relative'] = history['left'] - history['right']
        self.replay['scores'] = history.to_dict('list')

        filename = 'replay.json'
        with open(filename, 'w') as f:
            json.dump(self.replay, f)
        return

if __name__ == '__main__':
    tp = None
    game = Game_play(tp, tp)
