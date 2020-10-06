# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""Program constant"""

IMG_FOLDER = "./resources/img"

MAZE_OBJ = [("Empty", None),
            ("Wall", "floor-tiles-20x20.png", (20, 20, 220, 0)),
            ("Guard", "Gardien.png"),
            ("Needle", "aiguille.png"),
            ("Plastic Tube", "tube_plastique.png"),
            ("Ether", "ether.png"),
            ("MacGyver", "MacGyver.png")]

MAZE_PLACABLE = [MAZE_OBJ.index("Needle"),
                 MAZE_OBJ.index("Plastic Tube"),
                 MAZE_OBJ.index("Ether")]

DEFAULT_MAZE_FILE = "./resources/levels/level0.lvl"

DEFAULT_INPUT_MSG = "Select your action [Z/S/Q/D]: "
