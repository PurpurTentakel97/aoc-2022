#
# Purpur Tentakel
# 05.12.2022
#

from enum import Enum


class Result(Enum):
    RIGHT = 1
    WRONG = 2
    NONE = 3


def evaluate_single_signal(lhs: list, rhs: list) -> Result:
    for entry_lhs, entry_rhs in zip(lhs, rhs):

        if isinstance(entry_lhs, list) and isinstance(entry_rhs, list):
            valid = evaluate_single_signal(entry_lhs, entry_rhs)

        elif isinstance(entry_lhs, list) and isinstance(entry_rhs, int):
            valid = evaluate_single_signal(entry_lhs, [entry_rhs])

        elif isinstance(entry_lhs, int) and isinstance(entry_rhs, list):
            valid = evaluate_single_signal([entry_lhs], entry_rhs)

        else:
            if lhs > rhs:
                valid = Result.WRONG
            elif lhs < rhs:
                valid = Result.RIGHT
            else:
                valid = Result.NONE

        if valid != Result.NONE:
            return valid

    if len(lhs) > len(rhs):
        return Result.WRONG
    elif len(lhs) < len(rhs):
        return Result.RIGHT
    else:
        return Result.NONE


def evaluate_signal(signals: list) -> list[int, ...]:
    to_return = list()
    i: int = 1

    while True:
        if len(signals) <= i:
            break

        lhs = signals[i - 1]
        rhs = signals[i]

        if evaluate_single_signal(lhs, rhs) == Result.RIGHT:
            to_return.append(int((i - 1) / 2 + 1))

        i += 2

    return to_return


def parse_line(line: str) -> tuple[int, list]:
    # [1,[2,[3,[4,[5,6,7]]]],8,9]

    to_return = list()
    i = 1

    char: str = str()
    while True:

        char = line[i]

        if char == '[':
            min_index, entries = parse_line(line[i:])
            i += min_index
            to_return.append(entries)
            continue

        if char == ']':
            i += 1
            break

        if char.isdigit():
            to_return.append(int(char))

        i += 1

    return i, to_return


def parse(lines: list[str, ...]) -> list:
    to_return = list()

    for line in lines:
        line = line.rstrip()

        if len(line) == 0:
            continue

        _, input_ = parse_line(line)
        to_return.append(input_)

    assert (len(to_return) % 2 == 0)
    return to_return


def d_13_main() -> None:
    lines = list
    with open("day_13/input_13_1.txt", "r") as file:
        lines = file.readlines()

    input_ = parse(lines)

    # 1
    result = evaluate_signal(input_)
    print(result)
    print(f"the result is: {sum(result)}")
