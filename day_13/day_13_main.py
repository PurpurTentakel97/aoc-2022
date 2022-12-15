#
# Purpur Tentakel
# 05.12.2022
#
import copy
from enum import Enum
from typing import Union, List

MyList = List[Union["MyList", int]]


class Result(Enum):
    RIGHT = 1
    WRONG = 2
    NONE = 3


def evaluate_single_signal(lhs: MyList, rhs: MyList) -> Result:
    for entry_lhs, entry_rhs in zip(lhs, rhs):

        if isinstance(entry_lhs, list) and isinstance(entry_rhs, list):
            valid = evaluate_single_signal(entry_lhs, entry_rhs)

        elif isinstance(entry_lhs, list) and isinstance(entry_rhs, int):
            valid = evaluate_single_signal(entry_lhs, [copy.copy(entry_rhs)])

        elif isinstance(entry_lhs, int) and isinstance(entry_rhs, list):
            valid = evaluate_single_signal([copy.copy(entry_lhs)], entry_rhs)

        else:
            assert (isinstance(entry_lhs, int))
            assert (isinstance(entry_rhs, int))
            if entry_lhs < entry_rhs:
                valid = Result.RIGHT
            elif entry_lhs > entry_rhs:
                valid = Result.WRONG
            else:
                valid = Result.NONE

        if valid != Result.NONE:
            return valid

    assert (isinstance(lhs, list))
    assert (isinstance(rhs, list))
    if len(lhs) < len(rhs):
        return Result.RIGHT
    elif len(lhs) > len(rhs):
        return Result.WRONG
    else:
        return Result.NONE


def evaluate_signal(signals: MyList) -> list[int]:
    to_return = list()
    i: int = 1

    while True:
        if len(signals) <= i:
            break

        lhs = signals[i - 1]
        rhs = signals[i]
        assert isinstance(lhs, list)
        assert isinstance(rhs, list)

        if evaluate_single_signal(lhs, rhs) == Result.RIGHT:
            to_return.append(int((i - 1) / 2 + 1))

        i += 2

    return to_return


def sort_signals(signals: MyList) -> MyList:
    n = len(signals)
    swapped = False

    for i in range(n - 1):
        for j in range(0, n - i - 1):

            if evaluate_single_signal(signals[j], signals[j + 1]) == Result.WRONG:  # type: ignore
                swapped = True
                signals[j], signals[j + 1] = signals[j + 1], signals[j]

        if not swapped:
            return signals

    return signals


def is_divider(signal: MyList, to_search: list[int]) -> bool:
    if isinstance(signal, list) and len(signal) == 1:
        if isinstance(signal[0], list) and len(signal[0]) == 1:
            if isinstance(signal[0][0], int):
                if signal[0][0] in to_search:
                    print(signal)
                    return True
    return False


def get_divider_IDs(signals: MyList, to_search: list[int]) -> list[int]:
    IDs: list[int] = list()

    for i, signal in enumerate(signals):
        if is_divider(signal, to_search):  # type: ignore
            IDs.append(i + 1)

    return IDs


def multiply(IDs: list[int]) -> int:
    if len(IDs) == 0:
        return 0

    value = IDs[0]

    for i in range(1, len(IDs)):
        value *= IDs[i]

    return value


def parse_line(line: str) -> tuple[int, MyList]:
    to_return: MyList = list()
    i = 1

    current_string = ""
    while True:

        char: str = line[i]

        if not char.isdigit() and len(current_string) > 0:
            to_return.append(int(current_string))
            current_string = ""

        if char == '[':
            min_index, entries = parse_line(line[i:])
            i += min_index
            to_return.append(entries)
            continue

        if char == ']':
            i += 1
            break

        if char.isdigit():
            current_string += char

        i += 1

    return i, to_return


def parse(lines: list[str]) -> MyList:
    to_return: MyList = list()

    for line in lines:
        line = line.rstrip()

        if len(line) == 0:
            continue

        _, input_ = parse_line(line)
        to_return.append(input_)

    assert (len(to_return) % 2 == 0)
    return to_return


def d_13_main() -> None:
    lines: list[str]
    with open("day_13/input_13_2.txt", "r") as file:
        lines = file.readlines()

    input_ = parse(lines)

    # 1
    result: list[int] = evaluate_signal(input_)
    print(f"the result #1 is: {sum(result)}")

    # 2
    input_ = parse(lines)
    sort: MyList = sort_signals(input_)
    for _ in sort:
        print(_)
    IDs: list[int] = get_divider_IDs(sort, [2,6])
    print(IDs)
    result: int = multiply(IDs)  # type: ignore
    print(f"the result #2 is: {result}")
