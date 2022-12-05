#
# Purpur Tentakel
# 05.12.2022
#

def get_number_from_char(char: str) -> int:
    character_int: int = ord(char)
    if char.islower():
        character_int -= 96
    else:
        character_int -= 38

    return character_int


def d_03_main() -> None:
    with open("day_03/input_03_2.txt", "r") as file:
        score1: int = 0
        score2: int = 0

        lines: list[str] = file.readlines()
        for i, line in enumerate(lines):
            first_part, second_part = line[:len(line) // 2], line[len(line) // 2:]

            for char in first_part:
                if char in second_part:
                    score1 += get_number_from_char(char)
                    break

            if i % 3 == 0:
                for char in lines[i]:
                    if char in lines[i+1] and char in lines[i+2]:
                        score2 += get_number_from_char(char)
                        break

        print("the score1 is: " + str(score1))
        print("the score2 is: " + str(score2))
