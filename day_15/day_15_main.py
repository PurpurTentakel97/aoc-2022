#
# Purpur Tentakel
# 05.12.2022
#
import copy
import sys
from enum import Enum


class Coordinates:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def subtract(self, other: "Coordinates") -> "Coordinates":
        diffX = self.x - other.x
        diffY = self.y - other.y

        return Coordinates(diffX, diffY)

    def distance(self, other: "Coordinates") -> int:
        dis = self.subtract(other)

        dis.x = max(dis.x, -dis.x)
        dis.y = max(dis.y, -dis.y)

        return dis.x + dis.y

    def __str__(self) -> str:
        return f"/ {self.x} | {self.y} \\"

    def __repr__(self) -> str:
        return self.__str__()


class PointType(Enum):
    EMPTY = 1
    SENDER = 2
    BEACON = 3
    COVERED = 4


class Point:
    def __init__(self, coordinates: Coordinates, point_type: PointType = PointType.EMPTY):
        self._point_type: PointType = point_type
        self._coordinates: Coordinates = coordinates
        self._nearest_beacon: Coordinates | None = None

    def __str__(self) -> str:
        match self._point_type:
            case PointType.EMPTY:
                return '.'
            case PointType.SENDER:
                return 'S'
            case PointType.BEACON:
                return 'B'
            case PointType.COVERED:
                return '#'
            case _:
                return 'X'

    def set_nearest_beacon(self, beacon: Coordinates) -> None:

        assert self._point_type == PointType.SENDER

        self._nearest_beacon = beacon

    def get_nearst_beacon(self) -> Coordinates:
        return self._coordinates

    def set_point_type(self, point_type: PointType) -> None:
        self._point_type = point_type

    def get_point_type(self) -> PointType:
        return self._point_type

    def get_distance_to_beacon(self) -> int:

        assert self._point_type == PointType.SENDER
        assert self._nearest_beacon

        return self._coordinates.distance(self._nearest_beacon)


class World:
    def __init__(self, dimensions: Coordinates, coordinates: list[tuple[Coordinates, Coordinates]],
                 to_left_coordinate: Coordinates) -> None:
        self._dimensions: Coordinates = dimensions
        self._raw_coordinates: list[tuple[Coordinates, Coordinates]] = coordinates
        self._top_left_coordinate: Coordinates = to_left_coordinate
        self._points: list[list[Point]] = list()

        self._initialize()

    def _initialize(self) -> None:
        self._points.clear()
        self._initialize_points()
        self._initialize_senders_and_beacons()

    def _initialize_points(self) -> None:

        for i in range(self._dimensions.y + 1):
            line: list[Point] = list()
            for j in range(self._dimensions.x + 1):
                print(f"point: {i}/{j}")
                point: Point = Point(Coordinates(self._top_left_coordinate.x + j, self._top_left_coordinate.y + i))
                line.append(point)

            self._points.append(line)

    def _initialize_senders_and_beacons(self) -> None:

        for sender, beacon in self._raw_coordinates:
            sender_index: Coordinates = self._get_index_from_coordinates(sender)
            beacon_index: Coordinates = self._get_index_from_coordinates(beacon)

            self._points[sender_index.y][sender_index.x].set_point_type(PointType.SENDER)
            self._points[sender_index.y][sender_index.x].set_nearest_beacon(beacon)

            self._points[beacon_index.y][beacon_index.x].set_point_type(PointType.BEACON)

    def _get_index_from_coordinates(self, coordinates: Coordinates) -> Coordinates:
        i_x: int = coordinates.x - self._top_left_coordinate.x
        i_y: int = coordinates.y - self._top_left_coordinate.y
        return Coordinates(i_x, i_y)

    def _get_index_from_int(self, line: int, is_line: bool = True) -> int:
        if is_line:
            return line - self._top_left_coordinate.y
        else:
            return line - self._top_left_coordinate.x

    def _set_coverage(self, index: Coordinates, range_: int) -> None:

        min_row: int = index.y - range_
        max_row: int = index.y + range_

        for i in range(min_row, max_row + 1):

            if i < 0 or i > len(self._points) - 1:
                continue

            min_column: int
            max_column: int

            if i <= index.y:
                min_column = index.x - (range_ - (index.y - i))
                max_column = index.x + (range_ - (index.y - i))
            else:
                min_column = index.x - (range_ + (index.y - i))
                max_column = index.x + (range_ + (index.y - i))

            for j in range(min_column, max_column + 1):
                if j < 0 or j > len(self._points[0]) - 1:
                    continue

                point: Point = self._points[i][j]

                if point.get_point_type() != PointType.EMPTY:
                    continue

                point.set_point_type(PointType.COVERED)

    def calculate_sensor_ranges(self) -> None:

        for index, [sender, beacon] in enumerate(self._raw_coordinates):
            print(f"round: {index + 1}")
            sender_index = self._get_index_from_coordinates(sender)

            self._set_coverage(sender_index, self._points[sender_index.y][sender_index.x].get_distance_to_beacon())

    def get_non_beacon_count(self, line: int) -> int:
        index = self._get_index_from_int(line)

        count: int = 0
        for point in self._points[index]:
            if point.get_point_type() in [PointType.COVERED, PointType.SENDER]:
                count += 1

        return count

    def print(self) -> None:

        print("World 1:")

        for _ in self._points:

            toPrint: str = ""
            for point in _:
                toPrint += str(point)

            print(toPrint)

        print()


def get_dimensions(coordinates: list[tuple[Coordinates, Coordinates]]) -> tuple[Coordinates, Coordinates]:
    x_min: int = sys.maxsize
    x_max: int = -sys.maxsize - 1

    y_min: int = sys.maxsize
    y_max: int = -sys.maxsize - 1

    for _ in coordinates:
        for coordinate in _:
            x_min = min(x_min, coordinate.x)
            x_max = max(x_max, coordinate.x)

            y_min = min(y_min, coordinate.y)
            y_max = max(y_max, coordinate.y)

    return Coordinates(x_min, y_min), Coordinates(x_max - x_min, y_max - y_min)


def parse(lines: list[str]) -> list[tuple[Coordinates, Coordinates]]:
    to_return: list[tuple[Coordinates, Coordinates]] = list()

    for line in lines:

        line = line.rstrip()
        if len(line) == 0:
            continue

        tiles: list[str] = line.split('=')
        sx = int(tiles[1].split(',')[0])
        sy = int(tiles[2].split(':')[0])
        s = Coordinates(sx, sy)

        bx = int(tiles[3].split(',')[0])
        by = int(tiles[4])
        b = Coordinates(bx, by)

        to_return.append((s, b))

    return to_return


def d_15_main() -> None:
    lines: list[str]
    with open("day_15/input_15_1.txt", "r") as file:
        lines = file.readlines()

    coordinates: list[tuple[Coordinates, Coordinates]] = parse(lines)
    top_left_coordinate, dimensions = get_dimensions(coordinates)
    # 1
    world_1: World = World(copy.deepcopy(dimensions), copy.deepcopy(coordinates), top_left_coordinate)
    world_1.print()
    world_1.calculate_sensor_ranges()
    world_1.print()
    print(f"the covered space in line{10} is: {world_1.get_non_beacon_count(10)}")
