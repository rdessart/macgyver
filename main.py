#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""main file"""

import os
import sys

import maze_data.maze as maze
import player


def clear_cmd_screen():
    """Clear the screen of the console"""
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:
        os.system('clear')


def display(the_player: player.Player, the_maze: maze.Maze):
    """Clear the screen, display the owned items and the maze"""
    clear_cmd_screen()
    print(the_player.display_owned_items())
    print(the_maze)


def main(args) -> int:
    """Program entry point"""
    filepath = "./resources/levels/level0.lvl"
    if len(args) > 1:
        filepath = os.path.join(os.path.dirname(__file__),
                                args[1])
    my_maze = maze.Maze()
    if not my_maze.load_from_file(filepath):
        return 1
    my_maze.place_random_object([3, 4, 5])
    mac_gyver = player.Player()
    mac_gyver.bind_maze(my_maze)
    res = mac_gyver.place(my_maze.pickup_empty_space().position)
    display(mac_gyver, my_maze)
    touche = ''
    while touche != 'R' and (res is None or res.value != 2):
        touche = input("[Z/S] - [Q/D] : ")
        clear_cmd_screen()
        if touche.upper() == 'Z':
            res = mac_gyver.move(0, -1)
        elif touche.upper() == 'S':
            res = mac_gyver.move(0, 1)
        elif touche.upper() == 'Q':
            res = mac_gyver.move(-1, 0)
        elif touche.upper() == 'D':
            res = mac_gyver.move(1, 0)
        if res is not None and res.value in [3, 4, 5]:
            mac_gyver.pickup()
        display(mac_gyver, my_maze)
    clear_cmd_screen()
    mac_gyver.own_object.sort()
    if mac_gyver.own_object == [3, 4, 5]:
        print("YOU WIN !!!!")
    else:
        print("YOU LOOSE :( ")
    return 0


if __name__ == "__main__":
    main(sys.argv)
