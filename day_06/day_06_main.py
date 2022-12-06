#
# Purpur Tentakel
# 05.12.2022
#

def get_count_for_chars_repeating(line: str, value: int) -> int:
    chars: list[str, ...] = list()
    counter = 0
    for char in line:
        counter += 1
        if len(chars) == len(set(chars)):
            if char not in chars and len(chars) == value - 1:
                return counter

        chars.append(char)
        if len(chars) >= value:
            del chars[0]

    return 0


def d_06_main() -> None:
    with open("day_06/input_06_2.txt", "r") as file:
        lines: list[str, ...] = file.readlines()

        for line in lines:
            result1: int = get_count_for_chars_repeating(line, 4)
            print("result: " + str(result1))

            result2: int = get_count_for_chars_repeating(line, 14)
            print("result: " + str(result2))

            print("---")
