# -*- coding: utf-8 -*-
"""
Created on Tue May 30 17:13:38 2023

@author: admin
"""

class Pattern:
    def __init__(self, pattern, operation):
        self.pattern = pattern
        self.operation = operation
    def __repr__(self):
        return f"Pattern(\npattern={self.pattern}, \noperation=\n{self.operation}\n)"
    def __getitem__(self, value):
        if value == 0:
            return self.pattern
        elif value == 1:
            return self.operation
        raise IndexError(f"Index '{value}' out of range")