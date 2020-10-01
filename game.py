# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""Handle the game"""

import os
import copy

from maze_data import drawable, maze_object, maze, player
from event import KeyPressedEvent
import const


class Game():
    """Handle the game data"""

    def __init__(self, maze_file: str):
        """Initalisze"""
        self.main_maze = None
        self.player_one = None
        self._action = {}
        self.run = True
        self._initialise_maze(maze_file)
        self._initialise_player()

    def _initialise_maze(self, maze_file: str) -> None:
        """Instanciate the maze and load it from a file"""
        self.main_maze = maze.Maze()
        if not self.main_maze.load_from_file(maze_file):
            raise FileNotFoundError()
        self.main_maze.place_random_object(const.OBJECTS)
        print(self.main_maze)

    def _initialise_player(self) -> None:
        """Initalise the player"""
        self.player_one = player.Player()
        player_pos = self.main_maze.pickup_empty_space()
        self.player_one.place(player_pos.position)

    def game_loop(self) -> bool:
        """The game loop, return True if player won, else False"""
        while self.run:
            # self._clear_screen()
            self._draw()
            self._input_command(const.DEFAULT_INPUT_MSG)

    def _input_command(self, message: str) -> tuple:
        """Ask user witch direction to go"""
        command = input(message).upper()
        if(command in self._action):
            self._action[command].execute()
        elif command == 'R':
            self.run = False

    def bind_action(self, key: str, event: KeyPressedEvent) -> None:
        """Bind action"""
        self._action[key] = event

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
        background = copy.deepcopy(self.main_maze)
        background[self.player_one.position] = self.player_one
        print(background)
