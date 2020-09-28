"""Storing all the non GUI data type"""

# import logging as log

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


if __name__ == "__main__":
    obj = MazeObject(0, [0, 0])
    obj.value = 1
    obj.position = (5, 4)
    obj.position = [2, 0]
    print(obj)
