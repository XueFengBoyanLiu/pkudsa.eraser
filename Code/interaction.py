## the game interaction
from Board import *

#from player1 import Player as P1
#from player2 import Player as P2
## player class: Player
## method: move(np.array: current_board) -> tuple: 2 blocks to move

import threading, time, traceback
from __future__ import annotations
import numpy as np

class Player_wrapped():
    def __init__(self, player):
        self.core = player
        self.pts = 0  # record the points gained by him
        self.time = 0
        self.error = None

class Game_play():
    def __init__(self, player_1, player_2):
        self.players = (player_1, player_2)
        self.board = Board()
        self.turn = 0
        self.replay = {}

    def next_turn(self):
        self.turn += 1
        current_player = self.players[self.turn % 2]
        self.replay[self.turn] = {'current_player': self.turn % 2}
        mv = self.ask_for_move(self.borad.current_board(), current_player)
        self.make_move(mv)

    @classmethod
    def ask_for_move(cls, board, plr):
        return plr.move(board)

    def make_move(self, move):
        log_data = self.board.move(*move)
        log_dict = {}
        return log_dict
