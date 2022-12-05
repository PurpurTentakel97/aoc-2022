#
# Purpur Tentakel
# 05.12.2022
#

def d_03_main() -> None:
    with open("day_03/input_03_1.txt", "r") as file:
        score: int = 0
        for line in file:
            first_part, second_part = line[:len(line) // 2], line[len(line) // 2:]

            for char in first_part:
                if char in second_part:
                    character: str = char
                    character_int: int = ord(character)
                    if character.islower():
                        character_int -= 96
                    else:
                        character_int -= 38
                    score += character_int
                    break

        print("the score is: " + str(score))
