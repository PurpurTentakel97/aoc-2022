#
# Purpur Tentakel
# 05.12.2022
#

def d_01_main() -> None:
    with open("day_01/real_input_01.txt", "r") as file:

        max_entry: int = 0
        current_entry = 0

        for line in file:

            if len(line) <= 1:
                if max_entry < current_entry:
                    max_entry = current_entry
                current_entry = 0
                continue

            current_entry += int(line[:-1])

        print("the elf with the most calories carries: " + str(max_entry))
