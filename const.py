# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""Program constant"""

from maze_data.maze_object import MAZE_DEFAULT_OBJ, MazeObject


DEFAULT_MAZE_FILE = "./resources/levels/level0.lvl"
OBJECTS = [MazeObject(MAZE_DEFAULT_OBJ.index("Ether"), None),
           MazeObject(MAZE_DEFAULT_OBJ.index("Needle"), None),
           MazeObject(MAZE_DEFAULT_OBJ.index("Plastic Tube"), None)]
