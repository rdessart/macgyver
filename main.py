#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""main file"""

import os
import sys

from event import KeyPressedEvent
import game


def main(args: list) -> int:
    """Program entry point"""
    filepath = "./resources/levels/level0.lvl"  # Default value
    if len(args) > 1:
        filepath = os.path.join(os.path.dirname(__file__),
                                args[1])

    the_game = game.Game(filepath)
    target_action = the_game.player_one.move
    the_game.bind_action('Z', KeyPressedEvent(target_action, (0, 1)))
    the_game.bind_action('S', KeyPressedEvent(target_action, (0, -1)))
    the_game.bind_action('Q', KeyPressedEvent(target_action, (-1, 0)))
    the_game.bind_action('D', KeyPressedEvent(target_action, (1, 0)))
    the_game.game_loop()
    # start_position = my_maze.pickup_empty_space().position
    # case_value = mac_gyver.place(start_position)
    # display(mac_gyver, my_maze)

    # case_value = mac_gyver.move(movement[0], movement[1])

    # # if we land on a special object, we pick it up
    # if case_value is not None and case_value.value in [3, 4, 5]:
    #     mac_gyver.pickup()
    # # refresh the screen
    # display(mac_gyver, my_maze)
    # # End of the game.
    # clear_cmd_screen()
    # mac_gyver.own_object.sort()
    # if mac_gyver.own_object == [3, 4, 5]:  # we have all the items
    #     print("YOU WIN !!!!")
    # else:
    #     print("YOU LOOSE :( ")
    # return 0


if __name__ == "__main__":
    main(sys.argv)
