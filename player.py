#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Player management"""

import copy

import maze_data.maze_object as maze_obj
import maze_data.maze as maze
import maze_data.drawable as drawable

class Player(drawable.Drawable):
    """
    Represent our player
    """
    def __init__(self):
        """Constructor"""
        super().__init__([0, 0])
        self._position = [None, None]
        self.own_object = []
        self._maze = None
        self._old_pos = None

    def pickup(self):
        """
        Add the item under the player to our backpack, and reset the cell
        to being empty (value = 0)
        """
        self.own_object.append(copy.copy(self._old_pos[1].value))
        title = "Special Object Collected : {}"
        print(title.format(self._old_pos[1]))
        self._old_pos[1].value = 0

    def _is_position_valid(self, position: list) -> bool:
        """Check if the position is valid"""
        if self._maze is None:
            raise ValueError("The maze was not assign")
        # if self._maze[position].value == 1:
        #     return False
        # return True
        return self._maze[position].is_blocking

    def _draw(self):
        """
        [PROTECTED] position the player on the maze and return the previous
        cell to it initial value
        """
        if self._old_pos:
            self._maze[self._old_pos[0]] = self._old_pos[1]
        self._old_pos = (self.position, self._maze[self.position])
        self._maze[self.position] = maze.MazeObject(9, self.position)

    def move(self, val_x: int, val_y: int) -> list:
        """
        displace the player of val_x and val_x case respectivly toward
        the right and the bottom.
        The function will return the value of the cell under the player,
        if the displacement is impossible, the function return None
        """
        new_pos = [self.position[0] + val_y, self.position[1] + val_x]
        if self._is_position_valid(new_pos):
            self.position = new_pos
            self._draw()
            return self._old_pos[1]
        return None

    def place(self, new_pos: list) -> list:
        """
        Position the player onto the new_pos value.
        The function will return the value of the cell under the player,
        if the displacement is impossible, the function return None
        """
        if self._is_position_valid(new_pos):
            self.position = new_pos
            self._draw()
            return self._old_pos[1]
        return None

    def bind_maze(self, master_maze: maze.Maze):
        """Set a reference toward the maze."""
        self._maze = master_maze
    
    def display_owned_items(self)-> str:
        """Return a string with the formated owned items"""
        output_string = "Owned Item : "
        for obj in self.own_object:
            output_string += "{} ".format(maze_obj.MAZE_OBJECT_TYPE[obj])
        return output_string
        
