#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Player management"""

import copy


import maze_data.drawable as drawable
import maze_data.maze_object as maze_obj
from .const import MAZE_DEFAULT_OBJ


class Player(drawable.Drawable):
    """
    Represent our player
    """
    def __init__(self):
        """
        Constructor.
        If a maze is available we save his reference.
        """
        super().__init__([0, 0])
        self._position = [None, None]
        self.own_object = []
        self.value = 'X'

    def pickup(self, maze_object: maze_obj):
        """
        Add the item under the player to our backpack, and reset the cell
        to it's empty value (value = 0)
        """
        # To avoid a reference copy we explicitly ask python to copy the value
        self.own_object.append(copy.copy(maze_object))

    def move(self, value_xy: tuple) -> None:
        """
        displace the player of val_x and val_x case respectivly toward
        the right and the bottom.
        The function will return the value of the cell under the player,
        if the displacement is impossible, the function return None
        """
        self.position[0] += value_xy[1]
        self.position[1] += value_xy[0]

    def place(self, new_pos: list) -> None:
        """
        Position the player onto the new_pos value.
        The function will return the value of the cell under the player,
        if the displacement is impossible, the function return None
        """
        self.position = new_pos

    def display_owned_items(self) -> str:
        """Return a formated string with the items in our backpack"""
        output_string = "Owned Item : "
        for obj in self.own_object:
            output_string += "{} ".format(MAZE_DEFAULT_OBJ[obj.value])
        return output_string
