#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Handling drawable object"""


class Drawable():
    """Class to reprensent any drawable object on the maze"""

    def __init__(self, position: list):
        """Create a new drawable object, to be place at the given position."""
        self.position = position

    def __repr__(self):
        """ Implement repr()"""
        return "Drawable({})".format(self.position)

    def __str__(self):
        """Implement str()"""
        ouput_string = "Drawable object at pos x : {} - y : {}"
        return ouput_string.format(self.position_xy[0], self.position_xy[1])

    @property
    def position_xy(self) -> tuple:
        """Return the positon as tuple."""
        return (self.position[1], self.position[0])

    @position_xy.setter
    def position_xy(self, new_position: list):
        """
        Set the new position.
        """
        self.position[1], self.position[0] = new_position
