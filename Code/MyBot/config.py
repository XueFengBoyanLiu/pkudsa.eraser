# -*- coding: utf-8 -*-
"""
Created on Tue May 30 13:58:33 2023

@author: admin
"""

from collections import namedtuple
from numpy import array

from .pattern import Pattern

vec2 = namedtuple("vec2", ("x", "y"))
Operation = namedtuple("Operation", ("pos1", "pos2"))

NA = 0
LEVEL = 1200//6
BOARDSIZE = vec2(6, 6*LEVEL)

PATTERNS: dict[vec2: set] = {
    vec2(3, 2): {
        # RIGHT
        Pattern(
            array((
                (1, 0), 
                (0, 1), 
                (0, 1), 
            )), 
            Operation(
                vec2(0, 0), 
                vec2(0, 1)
            )
        ), 
        Pattern(
            array((
                (0, 1), 
                (1, 0), 
                (0, 1), 
            )), 
            Operation(
                vec2(1, 0), 
                vec2(1, 1)
            )
        ), 
        Pattern(
            array((
                (0, 1), 
                (0, 1), 
                (1, 0), 
            )), 
            Operation(
                vec2(2, 0), 
                vec2(2, 1)
            )
        ), 
        # LEFT
        Pattern(
            array((
                (0, 1), 
                (1, 0), 
                (1, 0), 
            )), 
            Operation(
                vec2(0, 1), 
                vec2(0, 0)
            )
        ), 
        Pattern(
            array((
                (1, 0), 
                (0, 1), 
                (1, 0), 
            )), 
            Operation(
                vec2(1, 1), 
                vec2(1, 0)
            )
        ), 
        Pattern(
            array((
                (1, 0), 
                (1, 0), 
                (0, 1), 
            )), 
            Operation(
                vec2(2, 1), 
                vec2(2, 0)
            )
        ), 
    }, 
    vec2(1, 4): {
        # RIGHT
        Pattern(
            array((
                (1, 0, 1, 1), 
            )), 
            Operation(
                vec2(0, 0), 
                vec2(0, 1)
            )
        ), 
        # LEFT
        Pattern(
            array((
                (1, 1, 0, 1), 
            )), 
            Operation(
                vec2(0, 3), 
                vec2(0, 2)
            )
        ), 
    }, 
    vec2(2, 3): {
        # TOP
        Pattern(
            array((
                (0, 1, 1), 
                (1, 0, 0), 
            )), 
            Operation(
                vec2(1, 0), 
                vec2(0, 0)
            )
        ), 
        Pattern(
            array((
                (1, 0, 1), 
                (0, 1, 0), 
            )), 
            Operation(
                vec2(1, 1), 
                vec2(0, 1)
            )
        ), 
        Pattern(
            array((
                (1, 1, 0), 
                (0, 0, 1), 
            )), 
            Operation(
                vec2(1, 2), 
                vec2(0, 2)
            )
        ), 
        # BOTTOM
        Pattern(
            array((
                (1, 0, 0), 
                (0, 1, 1), 
            )), 
            Operation(
                vec2(0, 0), 
                vec2(1, 0)
            )
        ), 
        Pattern(
            array((
                (0, 1, 0), 
                (1, 0, 1), 
            )), 
            Operation(
                vec2(0, 1), 
                vec2(1, 1)
            )
        ), 
        Pattern(
            array((
                (0, 0, 1), 
                (1, 1, 0), 
            )), 
            Operation(
                vec2(0, 2), 
                vec2(1, 2)
            )
        ), 
    }, 
    vec2(4, 1): {
        # TOP
        Pattern(
            array((
                tuple((1, )), 
                tuple((1, )), 
                tuple((0, )), 
                tuple((1, )), 
            )), 
            Operation(
                vec2(3, 0), 
                vec2(2, 0)
            )
        ), 
        # BOTTOM
        Pattern(
            array((
                tuple((1, )), 
                tuple((0, )), 
                tuple((1, )), 
                tuple((1, )), 
            )), 
            Operation(
                vec2(0, 0), 
                vec2(1, 0)
            )
        ), 
    }, 
}


























































