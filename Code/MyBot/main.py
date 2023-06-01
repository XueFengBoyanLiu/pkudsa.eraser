# -*- coding: utf-8 -*-
"""
Created on Mon May 22 13:33:44 2023

@author: admin
"""

# ??? 1200*6 -> 60

# 먼저 보드판을 읽어서 가능한 수를 모두 표시하고 각각의 결과 반을 반환하는 함수
# 최대한 ctypes 쓰면서


#                                   heuristic
# meacure(labeling) -> labeled as array -> find_clustered, d(score) -> return all_possible


import parent
from board import Board

from boardmanager import BoardManager



boardmanager = BoardManager()
board = Board()



print(f"\n  {boardmanager.move(*board.get_info(),0,0) = }\n")



# for k, val in enumerate( boardmanager.scoreboards ):
#     print(f"\n\n\n\nLevel {k} ----------")
#     for v in val:
#         print(f"\n{v}")

