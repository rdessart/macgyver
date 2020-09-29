#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Handling drawable object"""


class Drawable():
    """Abastract class to reprensent a drawable object"""

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
        Set the new position, new_position should be a list of lenght 2,
        with both X and Y as positive integer.
        """
        if len(new_position) != 2:
            raise ValueError("Position is invalid: should be of size 2 (x, y)")
        if new_position[0] < 0:
            raise ValueError("the X value should be positive")
        if new_position[1] < 0:
            raise ValueError("the Y value should be positive")

        self.position[1], self.position[0] = new_position
