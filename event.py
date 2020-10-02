#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Events handling"""


class KeyPressedEvent():
    """Action"""

    def __init__(self, target, value: tuple):
        """ constructor"""
        self.value = value
        self.target = target

    def execute(self):
        """Execute the target command"""
        self.target(self.value)
