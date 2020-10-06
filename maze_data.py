#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Handle all the maze, the blitable item as MazeObject and Player"""

from random import choice
import logging as log
from copy import copy
from os import path

import pygame

import const


class Drawable(pygame.sprite.Sprite):
    """Class to reprensent any drawable object on the maze"""

    def __init__(self, image_path: str, position: list = []):
        """Create a new drawable object, to be place at the given position."""
        super().__init__()
        self.position = position
        self.image = None

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
        if self.position is not None:
            return (self.position[1], self.position[0])
        return None

    @position_xy.setter
    def position_xy(self, new_position: list):
        """
        Set the new position.
        """
        if self.position is None:
            self.position = [new_position[0], new_position[1]]
        else:
            self.position[1], self.position[0] = new_position

    def set_colorkey(self, color: pygame.Color):
        """Set the alpha color of the image"""
        self.image.set_colorkey(color)

    def scale(self, new_res: tuple):
        """ Rescale image to the new resolution"""
        self.image = pygame.transform.smoothscale(self.image, new_res)

    def overlay(self, color: tuple, flags=pygame.BLEND_MULT):
        """ Add a color overlay to the image"""
        self.image.fill(color, special_flags=flags)

    def load_from_file(self, file_path: str, color_key=None) -> bool:
        """Load image from a file"""
        fullpath = path.join(path.dirname(__file__), file_path)
        try:
            image = pygame.image.load(file_path)
        except FileNotFoundError as exception:
            log.warning("Unable to load image from %s\n%s"
                        % (fullpath, exception))
            return False
        self._image = image.convert()
        if color_key is not None:
            if color_key == -1:
                color_key = self._image.get_at((10, 10))
            self._image.set_colorkey(color_key)
        self._image_rect = self._image.get_rect()
        self.image = self._image
        return True

    def crop(self, width: int, height: int, left: int, top: int):
        self.image = pygame.Surface([width, height])
        self.image.blit(self._image, (0, 0), (top, left, width, height))
        self._image_rect = self.image.get_rect()


class MazeObject(Drawable):
    """Reprensent a case in the maze"""

    def __init__(self, value: int, position: list):
        """
        Create a new MazeObject.
        Value should be an integer reprenstig the type of case, value should
        be as in MAZE_OBJECT_TYPE.
        Position should be a list of 2 integer representing the position as
        Row -> Column
        """
        super().__init__(position)
        self._value = value
        object_data = const.MAZE_OBJ[value]
        if object_data[1] is not None:
            self.load_from_file(path.join(const.IMG_FOLDER, object_data[1]))
            if len(object_data) > 2:
                self.crop(object_data[2][0],
                          object_data[2][1],
                          object_data[2][2],
                          object_data[2][3])
        else:
            self.image = pygame.Surface(const.SPRITE_SIZE)
            self.image.fill((255, 255, 255))

    def __repr__(self) -> str:
        """Return repr(self)."""
        return "MazeObject({}, {})".format(self._value, self.position)

    def __str__(self) -> str:
        """Return str(self)."""
        output_string = "{} at position {} - {}"
        return output_string.format(self._value,
                                    self.position[0],
                                    self.position[1])

    @property
    def value(self):
        """Return the value of the case."""
        return self._value

    @value.setter
    def value(self, value: int):
        """
        Update the value of the case
        """
        self._value = value

    def is_blocking(self) -> bool:
        """Return true if player can't go through the object."""
        return self._value == 1


class Player(Drawable):
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

    def pickup(self, maze_object: MazeObject):
        """
        Add the item under the player to our backpack, and reset the cell
        to it's empty value (value = 0)
        """
        # To avoid a reference copy we explicitly ask python to copy the value
        self.own_object.append(copy(maze_object))

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
            output_string += "{} ".format(const.MAZE_OBJ[obj.value])
        return output_string


class Maze():
    """Reprensente the whole maze as a 2D array"""
    # Special methods:
    def __init__(self):
        """Constructor"""
        self.maze_data = []
        self._iterator_pos = [0, -1]

    def __str__(self):
        """Implement str()"""
        output_string = ""
        for row in self.maze_data:
            for case in row:
                output_string += "{} ".format(case.value)
            output_string.split(' ')
            output_string += '\n'
        return output_string

    def __getitem__(self, position) -> MazeObject:
        """
        Implement getitem(x, y) and getitem(pos):
        If getitem is a list, we return [y][x]
        If getitem is a integer, we calulate the position in the 2D array
        """
        if not isinstance(position, (list, tuple)):
            row = position // len(self.maze_data)
            column = position % len(self.maze_data[row])
        else:
            row, column = position
        return self.maze_data[row][column]

    def __setitem__(self, position, value):
        """Implement setitem(x, y) and setitem(pos)"""
        if not isinstance(position, (list, tuple)):
            row = position // len(self.maze_data)
            column = position % len(self.maze_data[row])
        else:
            row, column = position
        self.maze_data[row][column] = value

    def __iter__(self):
        """Implement this class as an iterable"""
        return self

    def __next__(self):
        """
        Implement an iterator to go throught all the maze
        Iteration is made row by row : [0][1] .. [0][n], [1][0] .. [1][n],..
        """
        self._iterator_pos[1] += 1
        if self._iterator_pos[1] >= len(self.maze_data[self._iterator_pos[0]]):
            self._iterator_pos[0] += 1
            self._iterator_pos[1] = 0

        if self._iterator_pos[0] >= len(self.maze_data):
            raise StopIteration
        return self.maze_data[self._iterator_pos[0]][self._iterator_pos[1]]

    def __len__(self) -> int:
        """
        Implement len()
        Caution : Not to be used if maze is not a rectangle or a square.
        """
        return len(self.maze_data) * len(self.maze_data[0])

    # Protected methods:
    def _parse_row(self, row_data: tuple):
        """[Protected] Parse a row of the maze, input is (row_num, row_data)"""
        column_value = (char for char in row_data[1] if char != '\n')
        maze_line = []
        for column_data in enumerate(column_value):
            if not column_data[1].isnumeric():
                continue
            maze_line.append(MazeObject(int(column_data[1]),
                                        [row_data[0], column_data[0]]))
        self.maze_data.append(maze_line)

    # Public mehtods:
    def load_from_file(self, filepath: str) -> bool:
        """
        Load the maze for a level file.
        The function return True if the file is found and readable,
        else : return False
        """
        try:
            with open(filepath, 'r') as file_in:
                log.debug("File %s loaded sucessfully!", filepath)
                for row_data in enumerate(file_in):
                    self._parse_row(row_data)
            return True
        except FileNotFoundError as exception:
            log.critical("Specified file not found!\n%s", exception)
            return False

    def place_random_object(self, objects_list: list) -> list:
        """
        Function take a list of object and place them randomely in the maze.
        Object can only be placed over an empty (value = 0) cell
        """
        for obj in objects_list:
            self.pickup_empty_space().value = obj.value

    def pickup_empty_space(self) -> MazeObject:
        """Return a free (value = 0) cell"""
        selected_block = choice(self)
        while selected_block.value != 0:
            selected_block = choice(self)
        return selected_block
