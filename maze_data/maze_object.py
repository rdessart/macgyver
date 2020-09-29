#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Module to handle the Maze cells"""

from .drawable import Drawable

MAZE_OBJECT_TYPE = {
        0 : "Empty",
        1 : "Wall",
        2 : "Guard",
        3 : "Needle",
        4 : "Plastic Tube",
        5 : "Ether",
        9 : "MacGyver"}

class MazeObject(Drawable):
    """Reprensent a case in the maze"""

    def __init__(self, value: int, position: list):
        """
        Create a new MazeObject.
        Value should be an integer reprenstig the type of case, value should
        be as in MAZE_OBJECT_TYPE.
        """
        super().__init__(position)
        self._value = value

    def __repr__(self) -> str:
        """Return repr(self)."""
        return "MazeObject({}, [{}, {}])".format(self._value,
                                                 self.position[0],
                                                 self.position[1])

    def __str__(self)-> str:
        """Return str(self)."""
        output_string = "{} at position {} - {}"
        return output_string.format(MAZE_OBJECT_TYPE[self._value],
                                    self.position[0],
                                    self.position[1])

    @property
    def value(self):
        """Return the value of the case."""
        return self._value

    @value.setter
    def value(self, value: int):
        """
        Update the value of the case, value should be contained in
        MAZE_OBJECT_TYPE.
        """
        if value not in MAZE_OBJECT_TYPE.keys():
            raise ValueError("Value is not contained in the MAZE_OBJECT_TYPE")
        self._value = value

    def is_blocking(self) -> bool:
        """Return true if player can't go through the object."""
        return self._value == 1
