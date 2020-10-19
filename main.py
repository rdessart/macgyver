#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""main file"""

import sys

import game


def main(args: list) -> None:
    """Program entry point"""
    debug = False  # display the maze representation in the console
    play = True
    while play:
        the_game = game.Game(args)
        play = the_game.game_loop(debug)


if __name__ == "__main__":
    main(sys.argv)
