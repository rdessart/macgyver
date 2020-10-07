# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""Program constant"""

import os

IMG_FOLDER = os.path.join(os.path.dirname(__file__), "resources", "img")

# Item dictionnary key is the id of object.
# Value is a tuple of (Name, Image file | or None | Cropping data if require)
MAZE_OBJ = {0: ("Empty", None),
            1: ("Wall", "floor-tiles-20x20.png", (20, 20, 220, 0)),
            2: ("Guard", "Gardien.png"),
            3: ("Needle", "aiguille.png"),
            4: ("Plastic Tube", "tube_plastique.png"),
            5: ("Ether", "ether.png"),
            6: ("MacGyver", "MacGyver.png")}

MAZE_PLACABLE = [3, 4, 5]

MAZE_BLOCKING = [1]

DEFAULT_MAZE_FILE = "./resources/levels/level0.lvl"

SPRITE_SIZE = (30, 30)

MAZE_SIZE = (15, 15)

RESOLUTION = (MAZE_SIZE[0] * SPRITE_SIZE[0], MAZE_SIZE[1] * SPRITE_SIZE[1])
