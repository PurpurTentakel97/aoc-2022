#
# Purpur Tentakel
# 05.12.2022
#

from enum import Enum


class Direction(Enum):
    UP = "U"
    UP_RIGHT = "UR"
    RIGHT = "R"
    DOWN_RIGHT = "DR"
    DOWN = "D"
    DOWN_LEFT = "DL"
    LEFT = "L"
    UP_LEFT = "UL"
    NONE = "N"


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def subtract(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)

    def equals(self, other: "Position") -> bool:
        return self.x == other.x and self.y == other.y

    @staticmethod
    def is_in_list(positions: list["Position,..."], other: "Position") -> bool:

        for position in positions:
            if position.equals(other):
                return True
        return False

    def is_next_to(self, other: "Position") -> bool:
        subtracted = self.subtract(other)

        if subtracted.x == 0 and subtracted.y == 0:
            return False

        if -1 <= subtracted.x <= 1 and -1 <= subtracted.y <= 1:
            return True

        return False

    def get_direction_to_move(self, other: "Position") -> Direction:
        subtracted = self.subtract(other)

        if subtracted.y < 0:
            if subtracted.x < 0:
                return Direction.UP_RIGHT
            if subtracted.x == 0:
                return Direction.UP
            if subtracted.x > 0:
                return Direction.UP_LEFT
        if subtracted.y == 0:
            if subtracted.x < 0:
                return Direction.RIGHT
            if subtracted.x == 0:
                return Direction.NONE
            if subtracted.x > 0:
                return Direction.LEFT

        if subtracted.y > 0:
            if subtracted.x < 0:
                return Direction.DOWN_RIGHT
            if subtracted.x == 0:
                return Direction.DOWN
            if subtracted.x > 0:
                return Direction.DOWN_LEFT

        return Direction.NONE

    def __str__(self) -> str:
        return f"{self.x}, {self.y}"

    def __repr__(self) -> str:
        return self.__str__()


class Instruction:
    def __init__(self, direction, size) -> None:
        self._direction = direction
        self._size = size

    def get_direction(self) -> Direction:
        return self._direction

    def get_size(self) -> int:
        return self._size

    def __str__(self) -> str:
        return f"//{self._direction}, {self._size}//"

    def __repr__(self) -> str:
        return self.__str__()


class Rope:
    def __init__(self):
        self._position = Position(0, 0)
        self._positions: list[Position, ...] = [Position(0, 0)]

    def _add_position(self, ) -> None:
        self._positions.append(Position(self._position.x, self._position.y))

    def get_positions(self) -> list:
        return self._positions

    def get_single_positions(self) -> list:
        to_return = list()

        for position in self._positions:
            if not Position.is_in_list(to_return, position):
                to_return.append(position)

        return to_return

    def move_instruction(self, instruction: Instruction) -> Position:
        return self.move_direction(instruction.get_direction())

    def move_direction(self, direction: Direction) -> Position:
        match direction:
            case Direction.UP:
                # no x
                self._position.y += 1
            case Direction.UP_RIGHT:
                self._position.x += 1
                self._position.y += 1
            case Direction.RIGHT:
                self._position.x += 1
                # no y
            case Direction.DOWN_RIGHT:
                self._position.x += 1
                self._position.y -= 1
            case Direction.DOWN:
                # no x
                self._position.y -= 1
            case Direction.DOWN_LEFT:
                self._position.x -= 1
                self._position.y -= 1
            case Direction.LEFT:
                self._position.x -= 1
                # no y
            case Direction.UP_LEFT:
                self._position.x -= 1
                self._position.y += 1

        self._add_position()

        return self._position

    def move_position(self, position: Position) -> Position:

        if self._position.equals(position):
            self._add_position()
            return self._position

        if self._position.is_next_to(position):
            self._add_position()
            return self._position

        direction = self._position.get_direction_to_move(position)
        self.move_direction(direction)
        return self._position

    def __str__(self) -> str:
        to_print = ""
        for entry in self._positions:
            to_print += f"{entry} / "

        return to_print

    def __repr__(self) -> str:
        return self.__str__()


def parse(lines: list[str, ...]) -> list[Instruction, ...]:
    instruction = list()

    for line in lines:
        direction, size = line.split(" ")
        instruction.append(Instruction(Direction(direction), int(size)))

    return instruction


def move_elements(instruction: list[Instruction, ...], count: int) -> list:
    rope_elements: list = [Rope() for x in range(count)]

    for element in instruction:
        for i in range(element.get_size()):
            new_pos = rope_elements[0].move_instruction(element)

            for index, rope in enumerate(rope_elements):
                if index == 0:
                    continue

                new_pos = rope.move_position(new_pos)

    return rope_elements


def d_09_main() -> None:
    with open("day_09/input_09_2.txt", "r") as file:
        lines = file.readlines()

        rope_length: int = 10

        instruction = parse(lines)
        rope_elements = move_elements(instruction, rope_length)

        print(f"head visited {len(rope_elements[0].get_single_positions())} once.")
        print(f"tail visited {len(rope_elements[-1].get_single_positions())} once.")
