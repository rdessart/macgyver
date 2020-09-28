"""Storing all the non GUI data type"""

import logging as log

class Drawable():
    """Reprensting any displayed element"""

    def __init__(self, position: list):
        """Create a new drawable object, to be place at the given position."""
        self._position = position

    @property
    def position(self)->tuple:
        """Return the positon as tuple."""
        return (self._position[0], self._position[1])

    @position.setter
    def position(self, new_position: list):
        """
        Set the new position, new_position should be a list of lenght 2,
        with both X and Y as positive integer.
        """
        if len(new_position) != 2:
            raise ValueError("Position is invalid: should be of size 2 (x, y)")
        if new_position[0] < 0:
            raise ValueError("the X value should be positive")
        if new_position[1] < 0:
            raise ValueError("the Y value should be positive")

        self._position = new_position


class MazeObject(Drawable):
    """Reprensent a case in the maze"""
    MAZE_OBJECT_TYPE = {
        0 : "Empty",
        1 : "Wall",
        2 : "Exit",
        3 : "Start",
        4 : "Needle",
        5 : "Plastic Tube",
        6 : "Ether",
        7 : "Guard"
    }

    def __init__(self, value: int, position: list):
        """
        Create a new MazeObject.
        Value should be an integer reprenstig the type of case, value should
        be as in MAZE_OBJECT_TYPE.
        """
        super().__init__(position)
        self._value = value

    def __repr__(self) -> str:
        """Return repr(self)."""
        return "MazeObject({}, [{}, {}])".format(self._value,
                                                 self.position[0],
                                                 self.position[1])

    def __str__(self)-> str:
        """Return str(self)."""
        output_string = "{} at position {} - {}"
        return output_string.format(self.MAZE_OBJECT_TYPE[self._value],
                                    self.position[0],
                                    self.position[1])

    @property
    def value(self):
        """Return the value of the case."""
        return self._value

    @value.setter
    def value(self, value: int):
        """
        Update the value of the case, value should be contained in
        MAZE_OBJECT_TYPE.
        """
        if value not in self.MAZE_OBJECT_TYPE.keys():
            raise ValueError("Value is not contained in the MAZE_OBJECT_TYPE")
        self._value = value

    def is_blocking(self) -> bool:
        """Return true if player can't go through the object."""
        return self._value == 1


class Maze():
    """Reprensente the whole maze"""
    #special methods
    def __init__(self):
        """Constructor"""
        self.maze_data = []
        self._iteratorPos = [0, -1]

    def __str__(self):
        """Implement str()"""
        output_string = ""
        for row in self.maze_data:
            for case in row:
                output_string += "{} ".format(case.value)
            output_string.split(' ')
            output_string += '\n'
        return output_string
    
    def __getitem__(self, position):
        """Implement [y, x]"""
        return self.maze_data[position[0]][position[1]]
    
    def __iter__(self):
        """Implement this class as an iterable"""
        return self
    
    def __next__(self):
        """Implement an iterator to go throught all the maze"""
        self._iteratorPos[1] += 1
        if self._iteratorPos[1] >= len(self.maze_data[self._iteratorPos[0]]):
            self._iteratorPos[0] += 1
            self._iteratorPos[1] = 0
        
        if self._iteratorPos[0] >= len(self.maze_data):
            raise StopIteration
        return self.maze_data[self._iteratorPos[0]][self._iteratorPos[1]]

    #protected methods:
    def _parse_line(self, line_data: tuple):
        """[Protected] Parse a line of the maze, input is (line_num, line)"""
        line_value = (char for char in line_data[1] if char != '\n')
        maze_line = []
        for row_data in enumerate(line_value):
            if not row_data[1].isnumeric():
                continue
            maze_line.append(MazeObject(int(row_data[1]),
                                        [row_data[0],
                                        line_data[0]]))
        self.maze_data.append(maze_line)

    #public mehtods: 
    def load_from_file(self, filepath: str):
        """Load the maze for a level file."""
        try:
            with open(filepath, 'r') as file_in:
                log.debug("File %s loaded sucessfully!", filepath)
                for line_data in enumerate(file_in):
                    self._parse_line(line_data)
        except FileNotFoundError as exception:
            log.critical("Specified file not found!\n%s", exception)
            return
        

if __name__ == "__main__":
    from os import path
    log.basicConfig(level=log.DEBUG)
    maze = Maze()
    maze.load_from_file(path.join(path.dirname(__file__),
                                  "resources\\levels\\level0.lvl"))
    for i in maze:
        print(i)
    