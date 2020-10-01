#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""main file"""

import os
import sys
# DEBUG
from collections import Counter
import linecache
import os
import tracemalloc

from event import KeyPressedEvent
import game


def main(args: list) -> int:
    """Program entry point"""
    filepath = "./resources/levels/level0.lvl"  # Default value
    if len(args) > 1:
        filepath = os.path.join(os.path.dirname(__file__),
                                args[1])

    the_game = game.Game(filepath)
    target_action = the_game.player_one.move
    the_game.bind_action('Z', KeyPressedEvent(target_action, (0, 1)))
    the_game.bind_action('S', KeyPressedEvent(target_action, (0, -1)))
    the_game.bind_action('Q', KeyPressedEvent(target_action, (-1, 0)))
    the_game.bind_action('D', KeyPressedEvent(target_action, (1, 0)))
    the_game.game_loop()
    # start_position = my_maze.pickup_empty_space().position
    # case_value = mac_gyver.place(start_position)
    # display(mac_gyver, my_maze)

    # case_value = mac_gyver.move(movement[0], movement[1])

    # # if we land on a special object, we pick it up
    # if case_value is not None and case_value.value in [3, 4, 5]:
    #     mac_gyver.pickup()
    # # refresh the screen
    # display(mac_gyver, my_maze)
    # # End of the game.
    # clear_cmd_screen()
    # mac_gyver.own_object.sort()
    # if mac_gyver.own_object == [3, 4, 5]:  # we have all the items
    #     print("YOU WIN !!!!")
    # else:
    #     print("YOU LOOSE :( ")
    # return 0


def display_top(snapshot, key_type='lineno', limit=3):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB"
              % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))


if __name__ == "__main__":
    tracemalloc.start()
    main(sys.argv)
    snapshot = tracemalloc.take_snapshot()
    display_top(snapshot)
