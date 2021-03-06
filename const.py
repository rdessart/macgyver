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
            3: ("Needle", "aiguille.png", None, (0, 0, 0)),
            4: ("Plastic Tube", "tube_plastique.png", None, (255, 255, 255)),
            5: ("Ether", "ether.png", None, (1, 1, 1)),
            6: ("MacGyver", "MacGyver.png"),
            7: ("Syringe", "seringue.png")}

MAZE_PLACABLE = [3, 4, 5]

MAZE_BLOCKING = [1]

DEFAULT_MAZE_FILE = "./resources/levels/level0.lvl"

SPRITE_SIZE = (30, 30)

RESOLUTION = (450, 510)

INTRO_TEXT = [("MacGyver: The game!", 35, 0),
              ("Oh no, MacGyver is in trouble!", 20, 45),
              ("Help him by finding the exit.", 20, 70),
              ("But wait, there is a guard...", 20, 95),
              ("Fortunately some items are hidden in the maze:", 20, 120),
              ("- A plastic tube", 20, 145),
              ("- A bit of ether", 20, 165),
              ("- A needle", 20, 185),
              ("You need to find them order to craft a syringe.", 20, 215),
              ("This will allow McGyver to knock out the guard", 20, 235),
              ("Press ENTER to start ! ", 30, 255)]
