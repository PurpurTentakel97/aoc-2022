#
# Purpur Tentakel
# 05.12.2022
#
import math
import sys
from enum import Enum
import copy


class FieldType(Enum):
    START = "start"
    FINISH = "finish"
    NORMAL = "normal"


class Field:
    def __init__(self, field_type: FieldType, height: int):
        self._field_type: FieldType = field_type
        self._height: int = height
        self._costs: int | None = None
        self._calculated_costs: int | None = None

    def get_field_type(self) -> FieldType:
        return self._field_type

    def get_height(self) -> int:
        return self._height

    def get_calculated_costs(self) -> int:
        return self._calculated_costs

    def set_calculated_costs(self, calculates_costs: int) -> None:
        self._calculated_costs = calculates_costs

    def get_costs(self) -> int:
        return self._costs

    def set_costs(self, costs: int) -> None:
        self._costs = costs

    def __str__(self) -> str:
        return f"/{self._field_type}, {self._height}\\"

    def __repr__(self) -> str:
        return self.__str__()


class Map:
    def __init__(self, fields: list[list[Field, ...], ...]):
        self._fields: list[list[Field, ...], ...] = fields
        self._start_coordinates: tuple[int, int] = self._get_start_coordinates()
        self._finish_coordinates: tuple[int, int] = self._get_finish_coordinates()

        self._to_visit: list[tuple[int, int], ...] = list()
        self._predecessors: dict[tuple[int, int], tuple[int, int]] = dict()

    def _get_start_coordinates(self) -> tuple[int, int]:
        for line, _ in enumerate(self._fields):
            for row, field in enumerate(_):
                if field.get_field_type() == FieldType.START:
                    return line, row

        raise ValueError("no starting field in map")

    def _get_finish_coordinates(self) -> tuple[int, int]:
        for line, _ in enumerate(self._fields):
            for row, field in enumerate(_):
                if field.get_field_type() == FieldType.FINISH:
                    return line, row

        raise ValueError("no finish field in map")

    def _get_next_to_coordinates(self, coordinates: tuple[int, int]) -> list[tuple[int, int], ...]:
        to_return = list()

        assert (0 <= coordinates[0] <= self.get_height() - 1)
        assert (0 <= coordinates[1] <= self.get_length() - 1)

        if coordinates[0] > 0:
            to_return.append((coordinates[0] - 1, coordinates[1]))

        if coordinates[1] > 0:
            to_return.append((coordinates[0], coordinates[1] - 1))

        if coordinates[0] < self.get_height() - 1:
            to_return.append((coordinates[0] + 1, coordinates[1]))

        if coordinates[1] < self.get_length() - 1:
            to_return.append((coordinates[0], coordinates[1] + 1))

        return to_return

    def _get_costs_from_field_to_finish(self, parent: Field, current: tuple[int, int]) -> int:

        distance_line: int = self._finish_coordinates[0] - current[0]
        distance_row: int = self._finish_coordinates[1] - current[1]
        distance_to_finish: int = int(math.sqrt((distance_line * distance_line) + (distance_row * distance_row)))

        return parent.get_costs() + distance_to_finish

    def _get_calculated_costs_from_coordinates(self, coordinates: tuple[int, int]) -> int:
        return self._fields[coordinates[0]][coordinates[1]].get_calculated_costs()

    def _get_index_with_lowest_costs(self, visit: list[[int, int], ...]) -> tuple[int, int]:

        assert (len(visit) > 0)

        if len(visit) == 1:
            value = visit[0]
            visit.clear()
            return value

        lowest_value: int = sys.maxsize
        current_coordinates: tuple[int, int] = (0, 0)
        current_index: int = 0
        for index, coordinates in enumerate(visit):
            value = self._get_calculated_costs_from_coordinates(coordinates)
            if value < lowest_value:
                lowest_value = value
                current_coordinates = coordinates
                current_index = index

        del self._to_visit[current_index]
        return current_coordinates

    @staticmethod
    def _is_valid_way(parent: Field, child: Field) -> bool:
        return parent.get_height() >= child.get_height() - 1

    def get_height(self) -> int:
        return len(self._fields)

    def get_length(self) -> int:
        return len(self._fields[0])

    def get_fields_copy(self) -> list:
        return copy.deepcopy(self._fields)

    def get_start_coordinates(self) -> tuple[int, int]:
        return self._start_coordinates

    def get_finish_coordinates(self) -> tuple[int, int]:
        return self._finish_coordinates

    def get_finish_field(self) -> Field:
        return self._fields[self._finish_coordinates[0]][self._finish_coordinates[1]]

    def calculate_shortest_way(self) -> bool:
        self._to_visit.append(self._start_coordinates)
        self._fields[self._start_coordinates[0]][self._start_coordinates[1]].set_costs(0)

        finish: bool = False
        success: bool = True

        while not finish:

            if len(self._to_visit) == 0:
                finish = True
                success = False
                continue

            current_field_coordinates = self._get_index_with_lowest_costs(self._to_visit)
            current_field = self._fields[current_field_coordinates[0]][current_field_coordinates[1]]
            nearby_coordinates: list = self._get_next_to_coordinates(current_field_coordinates)

            for coordinates in nearby_coordinates:
                next_field = self._fields[coordinates[0]][coordinates[1]]

                if not self._is_valid_way(current_field, next_field):
                    continue

                next_costs: int = current_field.get_costs() + 1
                next_calculated_costs: int = self._get_costs_from_field_to_finish(current_field, coordinates)

                if next_field.get_field_type() == FieldType.FINISH:
                    next_field.set_costs(next_costs)
                    next_field.set_calculated_costs(next_calculated_costs)
                    self._predecessors[coordinates] = current_field_coordinates
                    finish = True
                    break

                if next_field.get_costs() is None:
                    self._to_visit.append(coordinates)
                    next_field.set_costs(next_costs)
                    next_field.set_calculated_costs(next_calculated_costs)
                    self._predecessors[coordinates] = current_field_coordinates
                    continue

                if next_field.get_costs() > next_costs:
                    next_field.set_costs(next_costs)
                    next_field.set_calculated_costs(next_calculated_costs)
                    self._predecessors[coordinates] = current_field_coordinates
                    continue

        return success


def parse(lines: list[str, ...]) -> list[list[Field, ...], ...]:
    to_return: list[list[Field, ...], ...] = list()

    for line in lines:
        line = line.rstrip()
        single_line: list[Field, ...] = list()

        for char in line:
            if char.isupper():
                match char:
                    case "S":
                        single_line.append(Field(FieldType.START, 1))
                    case "E":
                        single_line.append((Field(FieldType.FINISH, 26)))
                continue

            single_line.append(Field(FieldType.NORMAL, ord(char) - 96))

        to_return.append(single_line)

    return to_return


def print_fields(fields) -> None:
    for line in fields:
        print(line)


def d_12_main() -> None:
    lines: list[str, ...] = list()
    with open("day_12/input_12_1.txt", "r") as file:
        lines = file.readlines()

    map_ = Map(parse(lines))
    success: bool = map_.calculate_shortest_way()

    print(f"The war is valid: {success}")
    print(f"the shortest way is: {map_.get_finish_field().get_costs()}")
