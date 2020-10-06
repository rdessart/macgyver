# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""Program constant"""

import os

IMG_FOLDER = os.path.join(os.path.dirname(__file__), "resources", "img")

MAZE_OBJ = {0: ("Empty", None),
            1: ("Wall", "floor-tiles-20x20.png", (20, 20, 220, 0)),
            2: ("Guard", "Gardien.png"),
            3: ("Needle", "aiguille.png"),
            4: ("Plastic Tube","tube_plastique.png"),
            5: ("Ether", "ether.png"),
            6: ("MacGyver", "MacGyver.png")}

MAZE_PLACABLE = [3, 4, 5]

DEFAULT_MAZE_FILE = "./resources/levels/level0.lvl"

DEFAULT_INPUT_MSG = "Select your action [Z/S/Q/D]: "

RESOLUTION = [700, 1000]
