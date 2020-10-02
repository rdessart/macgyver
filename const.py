# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""Program constant"""

from maze_data.maze_object import MazeObject


DEFAULT_MAZE_FILE = "./resources/levels/level0.lvl"

MAZE_DEFAULT_OBJ = ["Empty", "Wall", "Guard", "Needle", "Plastic Tube",
                    "Ether", "MacGyver"]

OBJECTS = [MazeObject(MAZE_DEFAULT_OBJ.index("Ether"), None),
           MazeObject(MAZE_DEFAULT_OBJ.index("Needle"), None),
           MazeObject(MAZE_DEFAULT_OBJ.index("Plastic Tube"), None)]

DEFAULT_INPUT_MSG = "Select your action [Z/S/Q/D]: "
