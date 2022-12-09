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


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def equals(self, other: "Position") -> bool:
        return self.x == other.x and self.y == other.y


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
        self._positions: list[Position, ...] = [self._position]

    def _add_position(self, position: Position) -> None:
        if position not in self._positions:
            self._positions.append(position)

    def count_positions(self) -> int:
        return len(self._positions)

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
                self._position.y += 1
                self._position -= 1
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

        self._add_position(self._position)

        return self._position

    def move_position(self, position: Position) -> None:
        if self._position.equals(position):
            self._add_position(position)
            return


def parse(lines: list[str, ...]) -> list[Instruction, ...]:
    instruction = list()

    for line in lines:
        direction, size = line.split(" ")
        instruction.append(Instruction(Direction(direction), int(size)))

    return instruction


def move_elements(instruction: list[Instruction, ...], head: Rope, tail: Rope) -> tuple[Rope, Rope]:
    for element in instruction:
        for i in range(element.get_size()):
            new_pos = head.move_instruction(element)
            tail.move_position(new_pos)

    return head, tail


def d_09_main() -> None:
    with open("day_09/raw_input_09.txt", "r") as file:
        lines = file.readlines()
        instruction = parse(lines)
        print(instruction)
        head, tail = move_elements(instruction, Rope(), Rope())
