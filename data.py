"""Storing all the non GUI data type"""

import logging as log

class Maze():
    """
    Represente the maze
    """
    def __init__(self):
        """default constructor"""
        self.maze_array = []

    def load_from_file(self, filepath):
        """load the maze from a file"""
        try :
            with open(filepath, 'r') as file_in:
                self.maze_array = file_in.readlines()
                log.debug("file loaded with a %d x %d",
                        len(self.maze_array [0]), len(self.maze_array))
        except FileNotFoundError as exception:
            log.critical("File %s : not found !\n %s", filepath, exception)
