# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""Handle the game"""

import os
import copy

import pygame

from maze_data import Maze, MazeObject, Player
from event import KeyPressedEvent
from const import MAZE_PLACABLE, DEFAULT_INPUT_MSG, RESOLUTION


class Game():
    """Handle the game data"""

    def __init__(self, maze_file: str):
        """Initalisze"""
        self.main_maze = None
        self.player_one = None
        self.old_pos = None
        self._action = {}
        self.run = True
        self.window = pygame.display.set_mode(RESOLUTION)
        self._initialise_maze(maze_file)
        self._initialise_player()

    def _initialise_maze(self, maze_file: str) -> None:
        """[PROTECTED] Instanciate the maze and load it from a file"""
        self.main_maze = Maze()
        if not self.main_maze.load_from_file(maze_file):
            raise FileNotFoundError()
        objects = [MazeObject(obj, None) for obj in MAZE_PLACABLE]
        self.main_maze.place_random_object(objects)

    def _initialise_player(self) -> None:
        """[PROTECTED] Initalise the player"""
        self.player_one = Player()
        player_pos = self.main_maze.pickup_empty_space()
        self.old_pos = player_pos
        self.player_one.place(player_pos.position)
        self.main_maze[self.player_one.position] = self.player_one

    def _update(self) -> None:
        """
        [PROTECTED] Ask for user input, move player, if any pickup object
        on the ground
        """
        self.main_maze[self.old_pos.position] = self.old_pos
        self._input_command(DEFAULT_INPUT_MSG)
        player_case = self.main_maze[self.player_one.position]
        if player_case.is_blocking:
            self.player_one.position = self.old_pos.position
        self.old_pos = copy.deepcopy(self.main_maze[self.player_one.position])
        if player_case.value in MAZE_PLACABLE:
            self.player_one.pickup(player_case)
            self.old_pos.value = 0
        self.run = (player_case.value != 2)
        self.main_maze[self.old_pos.position] = self.old_pos
        self.main_maze[self.player_one.position] = self.player_one

    def _input_command(self, message: str) -> tuple:
        """[PROTECTED] Manage user input"""
        command = input(message).upper()
        if(command in self._action):
            self._action[command].execute()
        elif command == 'R':
            self.run = False

    def _clear_screen(self) -> None:
        """[PROTECTED] Clear the screen"""
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:
            os.system('clear')

    def _draw(self) -> None:
        """
        [PROTECTED]
        Call the function to clear the screen;
        Display the owned items and the maze
        """
        self._clear_screen()
        print(self.player_one.display_owned_items())
        print(self.main_maze)

    def bind_action(self, key: str, event: KeyPressedEvent) -> None:
        """Bind an action to a key pressed on the keyboard"""
        self._action[key] = event

    def game_loop(self) -> bool:
        """
        The game loop : run until self.run is set to false by _update method
        Each run, the loop display the maze and wait for user input.
        This will return a boolean:
            - True if all the const.OBJECT are pickup,
            - False if not
        """
        while self.run:
            self._draw()
            self._update()
        objects = [obj.value for obj in self.player_one.own_object]
        objects.sort()
        return objects == MAZE_PLACABLE
