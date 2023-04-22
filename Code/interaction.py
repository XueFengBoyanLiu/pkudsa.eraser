## the game interaction
from Board import *
from exception_manager import *

#from player1 import Robot as P1
#from player2 import Robot as P2
## player class: Robot
## method: move(np.array: current_board) -> tuple: 2 blocks to move
#player_safe_1 = Player(P1)
#player_safe_2 = Player(P2)

import threading, time, traceback
from __future__ import annotations
import numpy as np

class Invalid_move(Exception):
    pass

class Game_play():
    def __init__(self, player_1, player_2):
        self.players = (player_1, player_2)
        # the players are wrapped by exception_manager.py
        self.board = Board()
        self.turn = 0
        self.replay = {}
        self.terminated = False
        self.winner = None
        self.points = (0, 0)

    def next_turn(self):
        '''
        Perform one game turn
        '''
        self.turn += 1
        current_player = self.players[self.turn % 2]
        self.replay[self.turn] = {'current_player': self.turn % 2}
        mv = self.ask_for_move(current_player)
        if self.is_invalid_move(mv):
            self.terminated = True
            self.winner = self.players[(self.turn + 1) % 2]
            return
        self.make_move(mv)

    def ask_for_move(self, player):
        '''
        Given current board, get a move from the current player
        '''
        player('move', self.board.current_board())
        return player.output

    def is_invalid_move(self, move) -> bool:
        '''
        This function will check the following:
        - move is a (2, 2) array-like object
        - the two points are adjacent
        - the points lie inside the board
        '''
        try:
            blocks = np.array(move)
            if blocks.shape != (2, 2):
                raise Invalid_move
            distance = np.sum(np.abs(blocks[0] - blocks[1]))
            if distance != 1:
                raise Invalid_move
            if not ((blocks>=0) & (blocks<self.board.size)).all():
                raise Invalid_move
            return True
        except Exception as exception:
            self.handle_invalid_move(exception)
            return False

    def handle_invalid_move(self, exception):
        ##TODO
        pass

    def make_move(self, move) -> replay dict:
        ##TODO
        '''
        Perform a valid move, and return a dictionary for replay
        '''
        log_data = self.board.move(*move)
        log_dict = {'changed_blocks': None}
        return log_dict
