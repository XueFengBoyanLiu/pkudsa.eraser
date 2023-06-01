# -*- coding: utf-8 -*-
"""
Created on Tue May 30 16:08:47 2023

@author: admin
"""

class ScoredBoard:
    def __init__(self, select_hist, score_hist, score, board, operation):
        self.select_hist = select_hist
        self.score_hist = score_hist
        self.score = score
        self.board = board
        self.operation = operation
    def __repr__(self):
        return f"ScoreBoard(\nselect_hist={self.select_hist}, \nscore_hist={self.score_hist}, \nscore={self.score}, \nboard=\n{self.board}, \noperation=\n{self.operation}\n)"