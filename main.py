#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""main file"""

import os
import sys

import game


def main(args: list) -> None:
    """Program entry point"""
    filepath = "./resources/levels/level0.lvl"  # Default value
    if len(args) > 1:
        filepath = os.path.join(os.path.dirname(__file__), args[1])
    debug = True
    play = True
    while play:
        the_game = game.Game(filepath)
        play = the_game.game_loop(debug)


if __name__ == "__main__":
    main(sys.argv)
