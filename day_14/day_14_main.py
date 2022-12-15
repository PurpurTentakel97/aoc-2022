#
# Purpur Tentakel
# 05.12.2022
#
import sys
from enum import Enum


class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Coordinate: {self.x}/{self.y}"

    def __repr__(self) -> str:
        return self.__str__()


class FieldType(Enum):
    START = 1
    NORMAL = 2
    SAND = 3
    WALL = 4
    FLOOR = 5


class Direction(Enum):
    DOWN = 1
    DOWN_LEFT = 2
    DOWN_RIGHT = 3
    NONE = 4


class Field:
    def __init__(self, field_type: FieldType, coordinates: Coordinate):
        self._coordinates: Coordinate = coordinates
        self._field_type = field_type

    def __str__(self) -> str:
        match self._field_type:
            case FieldType.START:
                return '+'
            case FieldType.NORMAL:
                return '.'
            case FieldType.SAND:
                return 'o'
            case FieldType.WALL:
                return 'X'
            case FieldType.FLOOR:
                return 'U'

    def get_coordinates(self) -> Coordinate:
        return self._coordinates

    def set_field_type(self, field_type: FieldType) -> None:
        self._field_type = field_type

    def get_field_type(self) -> FieldType:
        return self._field_type


class Cave:
    def __init__(self, edge_values: tuple[Coordinate, ...], coordinates: tuple[tuple[Coordinate, ...], ...],
                 sand_coordinate: Coordinate):
        self._coordinates: tuple[tuple[Coordinate, ...], ...] = coordinates
        self._edge_values: tuple[Coordinate, ...] = edge_values
        self._fields: list[list[Field]] = list()
        self._start_sand_coordinate: Coordinate = sand_coordinate

        self._rounds: int = 0

        self._initialize()

    def _initialize(self) -> None:
        self._validate_edge_values()
        self._initialize_cave()
        self._initialize_walls()
        self._initialize_sand_field()

    def _validate_edge_values(self) -> None:
        self._edge_values[0].y = min(self._start_sand_coordinate.y, self._edge_values[0].y)
        self._edge_values[1].y = min(self._start_sand_coordinate.y, self._edge_values[1].y)

        self._edge_values[2].y += 2
        self._edge_values[3].y += 2

        self._edge_values[1].x += 2
        self._edge_values[3].x += 2

    def _initialize_cave(self) -> None:

        self._fields.clear()

        for i in range(self._edge_values[0].y - 1, self._edge_values[2].y):
            single_fields: list[Field] = list()

            for j in range(self._edge_values[0].x - 1, self._edge_values[1].x):
                single_fields.append(Field(FieldType.NORMAL, Coordinate(j, i)))

            self._fields.append(single_fields)

        next_line: int = self._edge_values[3].y
        last_single_fields: list[Field] = list()
        for j in range(self._edge_values[0].x - 1, self._edge_values[1].x):
            last_single_fields.append(Field(FieldType.FLOOR, Coordinate(j, next_line)))

        self._fields.append(last_single_fields)

    def _initialize_walls(self) -> None:

        for line in self._coordinates:
            for i in range(1, len(line)):
                previous: Coordinate = line[i - 1]
                current: Coordinate = line[i]

                if previous.x != current.x:
                    if previous.x > current.x:
                        x_1 = current.x
                        x_2 = previous.x
                    else:
                        x_1 = previous.x
                        x_2 = current.x

                    for j in range(x_1, x_2 + 1):
                        index: tuple[int, int] = self._get_index_from_coordinate(Coordinate(j, current.y))
                        self._fields[index[1]][index[0]].set_field_type(FieldType.WALL)

                elif previous.y != current.y:
                    if previous.y > current.y:
                        y_1 = current.y
                        y_2 = previous.y
                    else:
                        y_1 = previous.y
                        y_2 = current.y

                    for j in range(y_1, y_2 + 1):
                        index: tuple[int, int] = self._get_index_from_coordinate(  # type: ignore
                            Coordinate(current.x, j))
                        self._fields[index[1]][index[0]].set_field_type(FieldType.WALL)

    def _initialize_sand_field(self) -> None:
        index: tuple[int, int] = self._get_index_from_coordinate(self._start_sand_coordinate)
        self._fields[index[1]][index[0]].set_field_type(FieldType.START)

    def _get_index_from_coordinate(self, coordinate: Coordinate) -> tuple[int, int]:

        assert len(self._fields) > 0
        assert len(self._fields[0]) > 0

        return coordinate.x - self._fields[0][0].get_coordinates().x, \
               coordinate.y - self._fields[0][0].get_coordinates().y

    def _get_next_direction(self, coordinates: Coordinate) -> Direction:

        index: tuple[int, int] = self._get_index_from_coordinate(coordinates)

        assert self._fields[index[1]][index[0]].get_field_type() in [FieldType.SAND, FieldType.START]

        if self._fields[index[1] + 1][index[0]].get_field_type() in [FieldType.NORMAL, FieldType.FLOOR]:
            return Direction.DOWN

        elif self._fields[index[1] + 1][index[0] - 1].get_field_type() in [FieldType.NORMAL, FieldType.FLOOR]:
            return Direction.DOWN_LEFT

        elif self._fields[index[1] + 1][index[0] + 1].get_field_type() in [FieldType.NORMAL, FieldType.FLOOR]:
            return Direction.DOWN_RIGHT

        return Direction.NONE

    def _get_next_field(self, coordinates: Coordinate, direction: Direction) -> Field:

        index: tuple[int, int] = self._get_index_from_coordinate(coordinates)

        match direction:
            case Direction.DOWN:
                return self._fields[index[1] + 1][index[0]]
            case Direction.DOWN_LEFT:
                return self._fields[index[1] + 1][index[0] - 1]
            case Direction.DOWN_RIGHT:
                return self._fields[index[1] + 1][index[0] + 1]
            case _:
                raise IndexError()

    def start_sand(self) -> bool:

        current_coordinates: Coordinate = self._start_sand_coordinate

        while True:
            next_direction: Direction = self._get_next_direction(current_coordinates)
            if next_direction == Direction.NONE:
                self._rounds += 1
                return True

            next_field: Field = self._get_next_field(current_coordinates, next_direction)

            if next_field.get_field_type() == FieldType.FLOOR:
                return False

            assert next_field.get_field_type() == FieldType.NORMAL
            current_index: tuple[int, int] = self._get_index_from_coordinate(current_coordinates)
            current_field: Field = self._fields[current_index[1]][current_index[0]]
            if current_field.get_field_type() != FieldType.START:
                current_field.set_field_type(FieldType.NORMAL)
            next_field.set_field_type(FieldType.SAND)
            current_coordinates = next_field.get_coordinates()

    def get_rounds(self) -> int:
        return self._rounds

    def print(self) -> None:

        for line in self._fields:
            to_print: str = ""

            for field in line:
                to_print += str(field)

            print(to_print)


def get_edge_values(coordinates: tuple[tuple[Coordinate, ...], ...]) -> tuple[Coordinate, ...]:
    minX: int = sys.maxsize
    maxX: int = -sys.maxsize - 1
    minY: int = sys.maxsize
    maxY: int = -sys.maxsize - 1

    for _ in coordinates:
        for coordinate in _:
            minX = min(minX, coordinate.x)
            maxX = max(maxX, coordinate.x)
            minY = min(minY, coordinate.y)
            maxY = max(maxY, coordinate.y)

    return Coordinate(minX, minY), Coordinate(maxX, minY), Coordinate(minX, maxY), Coordinate(maxX, maxY)


def parse(lines: list[str]) -> tuple[tuple[Coordinate, ...], ...]:
    to_return: list[tuple[Coordinate, ...]] = list()

    for line in lines:
        line = line.rstrip()

        coordinates: list[str] = line.split("->")

        line_entries: list[Coordinate] = list()
        for coordinate in coordinates:
            x, y = coordinate.split(',')
            line_entries.append(Coordinate(int(x), int(y)))

        to_return.append(tuple(line_entries))

    return tuple(to_return)


def d_14_main() -> None:
    lines: list[str]
    with open("day_14/raw_input_14.txt", "r") as file:
        lines = file.readlines()

    coordinates: tuple[tuple[Coordinate, ...], ...] = parse(lines)
    edge_values: tuple[Coordinate, ...] = get_edge_values(coordinates)

    cave: Cave = Cave(edge_values, coordinates, Coordinate(500, 0))

    while True:
        print(f"sand: {cave.get_rounds()}")

        if not cave.start_sand():
            break

    cave.print()
    print(f"the cave is full after {cave.get_rounds()} rounds.\n")
