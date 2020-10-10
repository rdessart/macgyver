# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""Handle the game"""

import copy

import pygame

from maze_data import Maze, MazeObject, Player, Text
from const import MAZE_PLACABLE, RESOLUTION, SPRITE_SIZE, MAZE_BLOCKING,\
                  INTRO_TEXT


class Game():
    """Handle the graphics, the game logic and the data loading"""

    def __init__(self, maze_file: str):
        """
        Constructor : Set all class variable, load the maze from the file
        Initialize pygame
        Initialize the player
        """
        self.main_maze = None
        self.player_one = None
        self.old_pos = None
        self._action = {}
        self.game_status = 0
        self.run = True
        self.window = pygame.display.set_mode(RESOLUTION)
        self._initialise_maze(maze_file)
        self._initialise_player()
        self.win = False

    def _initialise_maze(self, maze_file: str) -> None:
        """[PROTECTED] Instanciate the maze and load it from a file"""
        self.main_maze = Maze()
        if not self.main_maze.load_from_file(maze_file):
            raise FileNotFoundError()

        objects = []
        for pos, obj in enumerate(MAZE_PLACABLE):
            maze_obj = MazeObject(obj, None)
            maze_obj.scale(SPRITE_SIZE)
            objects.append(maze_obj)

        self.main_maze.place_random_object(objects)

    def _initialise_player(self) -> None:
        """[PROTECTED] Find an empty spot in the maze, save the data and then
        place the player on the free spot.
        """
        self.player_one = Player()
        player_pos = self.main_maze.pickup_empty_space()
        self.player_one.position = player_pos.position
        self.player_one.scale(SPRITE_SIZE)
        self.main_maze.drawables.append(self.player_one)  # TODO - Groups
        self.old_pos = copy.copy(self.main_maze[self.player_one.position])
        self.main_maze[self.player_one.position] = self.player_one

        item_text = Text((0, len(self.main_maze.maze_data) * SPRITE_SIZE[1]))
        item_text.load_font_from_sys(Text.get_sys_font()[0], 20)
        item_text.write("Found Items : ")
        self.main_maze.drawables.append(item_text)

    def _handle_user_input(self) -> list:
        """
        [PROTECTED] Handle user inputs, return the expected new position
        of the player
        """
        future_pos = copy.copy(self.player_one.position)
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                future_pos[0] -= 1
            elif event.key == pygame.K_DOWN:
                future_pos[0] += 1
            elif event.key == pygame.K_LEFT:
                future_pos[1] -= 1
            elif event.key == pygame.K_RIGHT:
                future_pos[1] += 1
        return future_pos

    def _update(self, future_pos: list) -> None:
        """
        [PROTECTED] Wait for inputs, move player, if any pickup object
        on the ground
        future_pos: the expected future position of the player
        """
        if self.main_maze[future_pos].value in MAZE_BLOCKING:
            return

        if self.main_maze[future_pos].value in MAZE_PLACABLE:
            self.player_one.pickup(self.main_maze[future_pos])
            self.main_maze.drawables.remove(self.main_maze[future_pos])
            self.main_maze[future_pos].value = 0

        elif self.main_maze[future_pos].value == 2:
            self.run = False

        self.main_maze[self.old_pos.position] = self.old_pos
        self.old_pos = copy.copy(self.main_maze[future_pos])
        self.player_one.position = future_pos
        self.main_maze[self.player_one.position] = self.player_one

    def _draw(self, debug: bool = False) -> None:
        """
        [PROTECTED]
        - Clear the screen
        - display the maze and the player
        - display the player's owned items
        - display the syringe in green if we pick-up all the items, else in red
        If 'debug' is set to true, the console output the display of the maze
        """
        # Display the maze
        self.window.fill((0, 0, 0))
        for item in self.main_maze.drawables:
            self.window.blit(item.image, item.rect)
        # Display player's owned items
        for pos, obj_value in enumerate(self.player_one.own_object):
            obj = MazeObject(obj_value.value, [16, pos])
            obj.scale(SPRITE_SIZE)
            self.window.blit(obj.image, (120 + (pos * SPRITE_SIZE[0]),
                                         RESOLUTION[1] - SPRITE_SIZE[1] * 1.5))
        if not self.win:
            # Order the items
            objects = [obj.value for obj in self.player_one.own_object]
            objects.sort()
            self.win = objects == MAZE_PLACABLE
        # Load the syringe
        pos = len(MAZE_PLACABLE)
        syringe = MazeObject(7, [16, pos + 1])
        syringe.scale(SPRITE_SIZE)
        # Display the syringe in green if we have all the object else in red
        if self.win:
            syringe.overlay((0, 255, 0, 75))
        else:
            syringe.overlay((255, 0, 0, 75))

        self.window.blit(syringe.image, (120 + ((pos + 2) * SPRITE_SIZE[0]),
                                         RESOLUTION[1] - SPRITE_SIZE[1] * 1.5))
        pygame.display.flip()
        if debug:
            print(self.main_maze)

    def start_screen(self):
        """Show startup screen"""
        self.window.fill((0, 0, 0))

        for pos, lines in enumerate(INTRO_TEXT):
            text = Text((0, 0))
            text.load_font_from_sys(Text.get_sys_font()[0], lines[1])
            text.write(lines[0])
            text.rect.y = lines[2]
            text.rect.x = (RESOLUTION[0] / 2) - (text.rect.width / 2)
            self.window.blit(text.image, text.rect)
        pygame.display.flip()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return True
            elif event.type == pygame.QUIT:
                exit()

    def close_screen(self):
        """
        Display the exit message and return a boolean in respect with user
        input
        - If the ENTRY key is pressed the fuction return True
        - If the ESC key is pressed the function return False
        """
        self.window.fill((0, 0, 0))
        text = Text((0, 0))
        text.load_font_from_sys(Text.get_sys_font()[0], 40)
        if self.win:
            text.foreground_color = (0, 255, 0)
            text.write("You win !")
        else:
            text.foreground_color = (255, 0, 0)
            text.write("You loose !")

        text.rect.x = (RESOLUTION[0] / 2) - (text.rect.width / 2)
        text.rect.y = (RESOLUTION[1] / 2) - 100
        self.window.blit(text.image, text.rect)
        prev_pos = text.rect.y
        text.write("Press ENTER to Replay...")
        text.rect.y = prev_pos + 60
        text.rect.x = (RESOLUTION[0] / 2) - (text.rect.width / 2)
        self.window.blit(text.image, text.rect)
        prev_pos = text.rect.y
        self.window.blit(text.image, text.rect)
        prev_pos = text.rect.y
        text.write("Press ESC to quit...")
        text.rect.y = prev_pos + 60
        text.rect.x = (RESOLUTION[0] / 2) - (text.rect.width / 2)
        self.window.blit(text.image, text.rect)
        pygame.display.flip()

        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            elif event.type == pygame.QUIT:
                exit()

    def game_loop(self, debug: bool = False) -> bool:
        """
        The game loop : run until self.run is set to false by the "_update"
        method.
        - debug : display the maze data in the console
        Each run, the loop display the maze and wait for user input.
        This will return a boolean:
            - True: if all the const.OBJECT are pickup,
            - False: Otherwise
        """
        self.start_screen()
        self.run = True
        while self.run:
            self._draw(debug)
            new_pos = self._handle_user_input()
            self._update(new_pos)
        return self.close_screen()
