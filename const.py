# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""Program constant"""


MAZE_OBJ = ["Empty", "Wall", "Guard", "Needle", "Plastic Tube",
            "Ether", "MacGyver"]

MAZE_PLACABLE = [MAZE_OBJ.index("Needle"),
                 MAZE_OBJ.index("Plastic Tube"),
                 MAZE_OBJ.index("Ether")]

DEFAULT_MAZE_FILE = "./resources/levels/level0.lvl"

DEFAULT_INPUT_MSG = "Select your action [Z/S/Q/D]: "
