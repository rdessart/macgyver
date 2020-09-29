#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Module to handle the maze"""

from random import choice
import logging as log

from .maze_object import MazeObject

class Maze():
    """Reprensente the whole maze"""
    #special methods
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

    def __getitem__(self, position)-> MazeObject:
        """
        Implement getitem(x, y) and getitem(pos):
        If getitem is a list, we return [y][x]
        If getitem is a integer, we calulate the position in the 2D array
        """
        if isinstance(position, (list, tuple)):
            return self.maze_data[position[0]][position[1]]
        row = position // len(self.maze_data)
        column = position % len(self.maze_data[row])
        return self.maze_data[row][column]

    def __setitem__(self, key, value):
        """Implement setitem(x, y) and setitem(pos)"""
        if isinstance(key, (list, tuple)):
            self.maze_data[key[0]][key[1]] = value
        else:
            row = key // len(self.maze_data)
            column = key % len(self.maze_data[row])
            self.maze_data[row][column] = value

    def __iter__(self):
        """Implement this class as an iterable"""
        return self

    def __next__(self):
        """Implement an iterator to go throught all the maze"""
        self._iterator_pos[1] += 1
        if self._iterator_pos[1] >= len(self.maze_data[self._iterator_pos[0]]):
            self._iterator_pos[0] += 1
            self._iterator_pos[1] = 0

        if self._iterator_pos[0] >= len(self.maze_data):
            raise StopIteration
        return self.maze_data[self._iterator_pos[0]][self._iterator_pos[1]]

    def __len__(self)-> int:
        """Implement len()"""
        return len(self.maze_data) * len(self.maze_data[0])

    #protected methods:
    def _parse_row(self, row_data: tuple):
        """[Protected] Parse a line of the maze, input is (line_num, line)"""
        column_value = (char for char in row_data[1] if char != '\n')
        maze_line = []
        for column_data in enumerate(column_value):
            if not column_data[1].isnumeric():
                continue
            maze_line.append(MazeObject(int(column_data[1]),
                                        [row_data[0],
                                         column_data[0]]))
        self.maze_data.append(maze_line)

    #public mehtods:
    def load_from_file(self, filepath: str)-> bool:
        """
        Load the maze for a level file.
        The function return True if the file is found and readable, else it
        return False
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

    def place_random_object(self, objects_list: list):
        """
        Function take a list of object and place them randomely in the maze.
        Object can only be placed over an empty (value = 0) cell
        """
        while objects_list:
            item = objects_list.pop(0)
            self.pickup_empty_space().value = item

    def pickup_empty_space(self) ->list:
        """Return a free (value = 0) cell"""
        selected_block = choice(self)
        while selected_block.value != 0:
            selected_block = choice(self)
        return selected_block