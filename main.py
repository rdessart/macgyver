"""main file"""

from os import path
import argparse
import logging as log

import data

log.basicConfig(level=log.DEBUG)

def parse_cmd_line_arguments():
    """ parse the arguments and return them"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",help="the path to"
                        " the level file to be loaded")
    return parser.parse_args()

def main():
    """program entry point"""
    args = parse_cmd_line_arguments()
    if args.input is None:
        return
    filepath = path.join(path.dirname(__file__), args.input)
    maze = data.Maze()
    maze.load_from_file(filepath)
    print(maze)

if __name__ == "__main__":
    main()
