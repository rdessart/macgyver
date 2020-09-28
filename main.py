#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""main file"""

from os import path
from os import system
import argparse
import logging as log

import maze_data.maze as maze
import maze_data.maze_object as maze_obj
import player

log.basicConfig(level=log.DEBUG)

def parse_cmd_line_arguments():
    """ parse the arguments and return them"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",help="the path to"
                        " the level file to be loaded")
    return parser.parse_args()

def main()-> int:
    """program entry point"""
    args = parse_cmd_line_arguments()
    filepath = ""
    if args.input is None:
        filepath = "./resources/levels/level1.lvl"
    else:
        filepath = path.join(path.dirname(__file__), args.input)
    my_maze = maze.Maze()
    if not my_maze.load_from_file(filepath):
        return 1
    my_maze.place_random_object([3, 4, 5])
    mac_gyver = player.Player()
    mac_gyver.bind_maze(my_maze)
    start_block = my_maze.pickup_empty_space()
    start_pos = start_block.position
    res = mac_gyver.place(start_pos)
    system('cls') #windows Powershell ONLY - linux/mac replace with clr
    print("Owned items : {}".format(mac_gyver.own_object))
    print(my_maze)
    touche = ''
    while touche != 'R' and (res is None or res.value != 2):
        touche = input("[Z/S] - [Q/D] : ")
        system('cls') #windows Powershell ONLY - linux/mac replace with clr
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
        print(mac_gyver.own_object)
        print(my_maze)
    system('cls')
    mac_gyver.own_object.sort()
    if mac_gyver.own_object == [3, 4, 5]:
        print("YOU WIN !!!!")
    else :
        print("YOU LOOSE :( ")

    return 0

if __name__ == "__main__":
    main()
