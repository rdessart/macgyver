# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""Handle the game"""

import copy

import pygame

from maze_data import Maze, MazeObject, Player
from const import MAZE_PLACABLE, RESOLUTION, SPRITE_SIZE, MAZE_BLOCKING


class Game():
    """Handle the game data"""

    def __init__(self, maze_file: str):
        """Initalisze"""
        self.main_maze = None
        self.player_one = None
        self.old_pos = None
        self._action = {}
        self.group = pygame.sprite.Group()
        self.run = True
        self.window = pygame.display.set_mode(RESOLUTION)
        self._initialise_maze(maze_file)
        self._initialise_player()

    def _initialise_maze(self, maze_file: str) -> None:
        """[PROTECTED] Instanciate the maze and load it from a file"""
        self.main_maze = Maze()
        if not self.main_maze.load_from_file(maze_file):
            raise FileNotFoundError()

        objects = []
        for obj in MAZE_PLACABLE:
            maze_obj = MazeObject(obj, None)
            maze_obj.scale(SPRITE_SIZE)
            objects.append(maze_obj)

        self.main_maze.place_random_object(objects)

    def _initialise_player(self) -> None:
        """[PROTECTED] Initalise the player"""
        self.player_one = Player()
        player_pos = self.main_maze.pickup_empty_space()
        self.player_one.position = player_pos.position
        self.player_one.scale(SPRITE_SIZE)
        self.main_maze.drawables.append(self.player_one)
        self.main_maze[self.player_one.position] = self.player_one

    def _update(self) -> None:
        """
        [PROTECTED] Ask for user input, move player, if any pickup object
        on the ground
        """
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            self.run = False
        elif event.type == pygame.KEYDOWN:
            future_pos = copy.copy(self.player_one.position)
            if event.key == pygame.K_UP:
                future_pos[0] -= 1
            elif event.key == pygame.K_DOWN:
                future_pos[0] += 1
            elif event.key == pygame.K_LEFT:
                future_pos[1] -= 1
            elif event.key == pygame.K_RIGHT:
                future_pos[1] += 1
            if self.main_maze[future_pos].value not in MAZE_BLOCKING:
                self.player_one.position = future_pos
            if self.main_maze[future_pos].value in MAZE_PLACABLE:
                self.player_one.pickup(self.main_maze[future_pos])
                self.main_maze.drawables.remove(self.main_maze[future_pos])
                self.main_maze[future_pos].value = 0
            elif self.main_maze[future_pos].value == 2:
                self.run = False

    def _draw(self) -> None:
        """
        [PROTECTED]
        Call the function to clear the screen;
        Display the owned items and the maze
        """
        self.window.fill((0, 0, 0))
        for item in self.main_maze.drawables:
            self.window.blit(item.image, item.rect)
        pygame.display.flip()

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
