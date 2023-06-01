# -*- coding: utf-8 -*-
"""
Created on Tue May 30 17:43:06 2023

@author: admin
"""

from .config import (
    vec2, 
)


def direction(boardshape: vec2, pos: vec2):
    base = {
        vec2( 1,  0), 
        vec2(-1,  0), 
        vec2( 0,  1), 
        vec2( 0, -1), 
    }
    if ( pos.x + 1 ) == boardshape.x:
        base.remove(
            vec2(1, 0)
        )
    if ( pos.y + 1 ) == boardshape.y:
        base.remove(
            vec2(0, 1)
        )
    if pos.x == 0:
        base.remove(
            vec2(-1, 0)
        )
    if pos.y == 0:
        base.remove(
            vec2(0, -1)
        )
    return base