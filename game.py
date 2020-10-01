# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""Handle the game"""

import os

from maze_data import drawable, maze_object, maze, player
import const


class Game():
    """Handle the game data"""

    def __init__(self, maze_file: str):
        """Initalisze"""
        self.main_maze = None
        self._initalise_maze(maze_file)
        self.player_one = player.Player()

    def _initalise_maze(self, maze_file: str) -> None:
        """Instanciate the maze and load it from a file"""
        self.main_maze = maze.Maze()
        self.main_maze.load_from_file(maze_file)
        if not self.main_maze.load_from_file(maze_file):
            raise FileNotFoundError()

    def game_loop(self) -> bool:
        """The game loop, return True if player won, else False"""

    def _input_command(self) -> tuple:
        """Ask user witch direction to go"""
        command = input("[Z/S] - [Q/D] : ")
        movement = (0, 0)
        if command.upper() == 'Z':
            movement = (0, -1)
        elif command.upper() == 'S':
            movement = (0, 1)
        elif command.upper() == 'Q':
            movement = (-1, 0)
        elif command.upper() == 'D':
            movement = (1, 0)
        return movement

    def _clear_screen(self) -> None:
        """Clear the screen"""
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:
            os.system('clear')

    def _draw(self) -> None:
        """Clear the screen, display the owned items and the maze"""
        self._clear_screen()
        print(self.player_one.display_owned_items())
        print(self.main_maze)
