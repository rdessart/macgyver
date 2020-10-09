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
            6: ("MacGyver", "MacGyver.png"),
            7: ("Syringe", "seringue.png")}

MAZE_PLACABLE = [3, 4, 5]

MAZE_BLOCKING = [1]

DEFAULT_MAZE_FILE = "./resources/levels/level0.lvl"

SPRITE_SIZE = (30, 30)

RESOLUTION = (450, 510)

INTRO_TEXT = [("MacGyver: The game!", 35, 0),
              ("Oh no, MacGyver is in trouble!", 20, 40),
              ("Help him by finding the exit.", 20, 60),
              ("But wait, there is a guard...", 20, 80),
              ("Fortunately some items are hidden in the maze:", 20, 100),
              ("- A plastic tube", 20, 120),
              ("- A bit of ether", 20, 140),
              ("- A needle", 20, 160),
              ("You need to find them order to craft a syringe.", 20, 180),
              ("This will allow McGyver to knock out the guard", 20, 200),
              ("Press ENTER to start ! ", 30, 250)]
