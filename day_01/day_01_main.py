#
# Purpur Tentakel
# 05.12.2022
#

def get_top_x_sum(max_entries: list[int], sum_up: int) -> int:
    max_entries.sort(reverse=True)

    sum_: int = 0
    for i in range(sum_up):
        sum_ += max_entries[i]

    return sum_


def d_01_main() -> None:
    with open("day_01/input_01_2.txt", "r") as file:

        max_entry: list[int] = list()
        current_entry = 0

        for line in file:

            if len(line) <= 1:
                max_entry.append(current_entry)
                current_entry = 0
                continue

            current_entry += int(line)
        max_entry.append(current_entry)

        sum_: int = get_top_x_sum(max_entry, 3)
        print("the elf with the most calories carries: " + str(sum_))
