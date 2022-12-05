#
# Purpur Tentakel
# 05.12.2022
#

def d_04_main() -> None:
    with open("day_04/input_04_1.txt") as file:
        counter: int = 0
        for line in file:

            lhs, rhs = line.split(",")

            lhs = [int(x) for x in lhs.split("-")]
            rhs = [int(x) for x in rhs.split("-")]

            lhs = set(range(lhs[0], lhs[1] + 1))
            rhs = set(range(rhs[0], rhs[1] + 1))

            if lhs.issubset(rhs) or rhs.issubset(lhs):
                counter += 1

        print("counter is: " + str(counter))
