#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""main file"""

import os
import sys

import maze_data.maze as maze
import maze_data.maze_object as maze_obj
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


def main(args: list) -> int:
    """Program entry point"""
    filepath = "./resources/levels/level0.lvl"  # Default value
    if len(args) > 1:
        filepath = os.path.join(os.path.dirname(__file__),
                                args[1])

    my_maze = maze.Maze()
    if not my_maze.load_from_file(filepath):
        return 1
    object_to_collect = [maze_obj.MazeObject(3, [0, 0]),  # Needle
                         maze_obj.MazeObject(4, [0, 0]),  # Tube
                         maze_obj.MazeObject(5, [0, 0])]  # Ether

    mac_gyver = player.Player(my_maze)  # we already bind the maze.
    start_position = my_maze.pickup_empty_space().position
    case_value = mac_gyver.place(start_position)
    display(mac_gyver, my_maze)
    command = ''
    while command != 'R' and (case_value is None or case_value.value != 2):
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
        case_value = mac_gyver.move(movement[0], movement[1])

        # if we land on a special object, we pick it up
        if case_value is not None and case_value.value in [3, 4, 5]:
            mac_gyver.pickup()
        # refresh the screen
        display(mac_gyver, my_maze)
    # End of the game.
    clear_cmd_screen()
    mac_gyver.own_object.sort()
    if mac_gyver.own_object == [3, 4, 5]:  # we have all the items
        print("YOU WIN !!!!")
    else:
        print("YOU LOOSE :( ")
    return 0


if __name__ == "__main__":
    main(sys.argv)
