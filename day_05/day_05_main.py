#
# Purpur Tentakel
# 05.12.2022
#

def get_split_index(lines: list[str, ...]) -> int:
    for i, line in enumerate(lines):
        if len(line) <= 1:
            return i


def get_crates(split_index: int, lines: list[str, ...]) -> list[list[str]]:
    crates: list[list[str, ...]] = list()
    no_char: list[str, ...] = [" ", "[", "]", "\n"]

    for char in lines[split_index - 1]:
        if char == " " or char == "\n":
            continue
        crates.append(list())

    for i in range(split_index - 2, -1, -1):

        for j, char in enumerate(lines[i]):

            if char in no_char:
                continue

            ind: int = j // 4
            crates[ind].append(char)

    return crates


def parse_moves(introduction: str) -> list[int, int, int]:
    _, count, _, from_, _, to_ = introduction.split(" ")
    return [int(count), int(from_) - 1, int(to_) - 1]


def move_crates1(crate_list: list[list[str]], introduction: str) -> list[list[str]]:
    introduction: list[int, int, int] = parse_moves(introduction)

    for i in range(introduction[0]):
        temporary = crate_list[introduction[1]].pop()
        crate_list[introduction[2]].append(temporary)

    return crate_list


def move_crates2(crate_list: list[list[str]], introduction: str) -> list[list[str]]:
    introduction: list[int, int, int] = parse_moves(introduction)

    temporary = crate_list[introduction[1]][-introduction[0]:]
    del crate_list[introduction[1]][-introduction[0]:]
    crate_list[introduction[2]] += temporary

    return crate_list


def get_result(crate_list: list[list[str]]) -> str:
    result: str = ""
    for entry in crate_list:
        result += entry.pop()

    return result


def d_05_main() -> None:
    crate_list1: list[list[str]]
    crate_list2: list[list[str]]
    with open("day_05/input_05_2.txt", "r") as file:
        lines: list[str, ...] = file.readlines()
        split_index: int = get_split_index(lines)

        crate_list1 = get_crates(split_index, lines)
        crate_list2 = get_crates(split_index, lines)

        for i, line in enumerate(lines):
            if i <= split_index:
                continue
            crate_list1 = move_crates1(crate_list1, line)
            crate_list2 = move_crates2(crate_list2, line)

        result1: str = get_result(crate_list1)
        print("the result1 is: " + result1)

        result2: str = get_result(crate_list2)
        print("the result2 is: " + result2)
