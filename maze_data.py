#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Handle all the maze, the blitable item as MazeObject and Player"""

from random import choice
import logging as log
from copy import copy
from os import path

import pygame

import const

pygame.init()


class Drawable():
    """Class to reprensent any drawable object on the maze"""

    def __init__(self, position: list = []):
        """Create a new drawable object, to be place at the given position."""
        super().__init__()
        self._position = position
        self.image = None
        self.rect = []
        self.value = ''

    def __repr__(self):
        """ Implement repr()"""
        return "Drawable({})".format(self._position)

    def __str__(self):
        """Implement str()"""
        return str(self.value)

    @property
    def position(self) -> tuple:
        """Return the position of the object as a tuple"""
        return self._position

    @position.setter
    def position(self, position: list):
        """Set the position of the object as well as the rect of the image"""
        if self.rect is not None:
            self.rect.x = position[1] * const.SPRITE_SIZE[0]
            self.rect.y = position[0] * const.SPRITE_SIZE[1]
        self._position = position

    def set_colorkey(self, color: pygame.Color):
        """Set the alpha color of the image"""
        self.image.set_colorkey(color)
        self.image = self.image.convert_alpha()

    def scale(self, new_res: tuple):
        """ Rescale image to the new resolution"""
        self.image = pygame.transform.smoothscale(self.image, new_res)

    def overlay(self, color: tuple, flags=pygame.BLEND_MULT):
        """ Add a color overlay to the image"""
        self.image.fill(color, special_flags=flags)

    def load_from_file(self, file_path: str, color_key=None) -> bool:
        """
        Load image from a file.
        If colory_key is -1, the alpha pixel is loaded from the pixel at 0-0
        """
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
                color_key = self._image.get_at((0, 0))
            self._image.set_colorkey(color_key)
        self.rect = self._image.get_rect()
        self.image = self._image
        return True

    def crop(self, width: int, height: int, left: int, top: int):
        """Cut the image to fit a width * height rectangle from the data
        starting a top & left"""
        self.image = pygame.Surface([width, height])
        self.image.blit(self._image, (0, 0), (top, left, width, height))
        self.rect = self.image.get_rect()


class MazeObject(Drawable):
    """Reprensent a case in the maze"""

    def __init__(self, value: int, position: list = []):
        """
        Create a new MazeObject.
        - Value should be an integer reprenstig the type of case, value should
        be as in MAZE_OBJECT_TYPE.
        - Position should be a list of 2 integer representing the position as
        Row -> Column or None if not yet set.

        The image file, or any cropping data are loaded from "const.py"
        """
        super().__init__(position)
        self._value = value
        object_data = const.MAZE_OBJ[value]
        if object_data[1] is not None:
            self.load_from_file(path.join(const.IMG_FOLDER, object_data[1]))
            if len(object_data) > 2 and object_data[2] is not None:
                self.crop(object_data[2][0],
                          object_data[2][1],
                          object_data[2][2],
                          object_data[2][3])
                self.scale(const.SPRITE_SIZE)
            if len(object_data) > 3 and object_data[3] is not None:
                self.set_colorkey(object_data[3])
        else:
            self.image = pygame.Surface(const.SPRITE_SIZE)
            self.image.fill((255, 255, 255))
            self.rect = self.image.get_rect()

    def __repr__(self) -> str:
        """Return repr(self)."""
        return "MazeObject({}, {})".format(self._value, self.position)

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
        self._position = None
        self.own_object = []
        self.load_from_file(path.join(const.IMG_FOLDER, const.MAZE_OBJ[6][1]))
        self.value = 'X'  # DEBUG

    def pickup(self, maze_object: MazeObject):
        """
        Add the item under the player to our backpack, and reset the cell
        to it's empty value (value = 0).
        As object get also edited in the game loop we proceed to a full copy
        instead of a reference copy.
        """
        self.own_object.append(copy(maze_object))

    def place(self, new_pos: list) -> None:
        """
        Position the player onto the new_pos value.
        The function will return the value of the cell under the player,
        if the displacement is impossible, the function return None
        """
        self.position = new_pos


class Text(Drawable):
    """
    Handle Text
    """
    def __init__(self, position: tuple = None):
        """ Initalise new text drawer"""
        super().__init__(None)
        self.rect = None
        self.font = None
        self.anti_aliasing = True
        self.foreground_color = (255, 255, 255)
        self.background_color = (0, 0, 0, 0)
        self.position = position

    @staticmethod
    def get_sys_font():
        """Return all installed font"""
        return pygame.font.get_fonts()

    def load_font_from_sys(self, font_name: str, size: int):
        """Load a font from the default system fonts"""
        path_font = pygame.font.match_font(font_name)
        self.font = pygame.font.Font(path_font, size)

    def write(self, text: str):
        """Write text on the surface"""
        self.image = self.font.render(text,
                                      self.anti_aliasing,
                                      self.foreground_color,
                                      self.background_color)
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]


class Maze():
    """Reprensente the whole maze as a 2D array"""
    # Special methods:
    def __init__(self):
        """Constructor"""
        self.maze_data = []
        self._iterator_pos = [0, -1]
        self.drawables = []

    def __str__(self):
        """Implement str()"""
        output_string = ""
        for row in self.maze_data:
            for case in row:
                output_string += "{} ".format(case)
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
            maze_obj = MazeObject(int(column_data[1]),
                                  [row_data[0], column_data[0]])
            maze_line.append(maze_obj)
            maze_obj.rect.x = column_data[0] * const.SPRITE_SIZE[0]
            maze_obj.rect.y = row_data[0] * const.SPRITE_SIZE[1]
            self.drawables.append(maze_obj)
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
            position = self.pickup_empty_space().position
            obj.position = position
            self[position] = obj
            self.drawables.append(obj)

    def pickup_empty_space(self) -> MazeObject:
        """Return a free (value = 0) cell"""
        selected_block = choice(self)
        while selected_block.value != 0:
            selected_block = choice(self)
        return selected_block
