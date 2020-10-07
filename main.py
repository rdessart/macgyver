#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""main file"""

import os
import sys

import game


def main(args: list):
    """Program entry point"""
    filepath = "./resources/levels/level0.lvl"  # Default value
    if len(args) > 1:
        filepath = os.path.join(os.path.dirname(__file__),
                                args[1])

    the_game = game.Game(filepath)
    if the_game.game_loop():
        print("YOU WIN !!!!")
    else:
        print("YOU LOOSE :( ")


if __name__ == "__main__":
    main(sys.argv)
