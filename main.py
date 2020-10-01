#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""main file"""

import os
import sys


from event import KeyPressedEvent
import game


def main(args: list):
    """Program entry point"""
    filepath = "./resources/levels/level0.lvl"  # Default value
    if len(args) > 1:
        filepath = os.path.join(os.path.dirname(__file__),
                                args[1])

    the_game = game.Game(filepath)
    # Binding controls:
    target_action = the_game.player_one.move
    the_game.bind_action('Z', KeyPressedEvent(target_action, (0, -1)))
    the_game.bind_action('S', KeyPressedEvent(target_action, (0, 1)))
    the_game.bind_action('Q', KeyPressedEvent(target_action, (-1, 0)))
    the_game.bind_action('D', KeyPressedEvent(target_action, (1, 0)))

    if the_game.game_loop():
        print("YOU WIN !!!!")
    else:
        print("YOU LOOSE :( ")


if __name__ == "__main__":
    main(sys.argv)
