#
# Purpur Tentakel
# 05.12.2022
#

class Tree:
    def __init__(self, height):
        self._height = height
        self._visible = False

    def get_height(self) -> int:
        return self._height

    def set_visible(self) -> None:
        self._visible = True

    def is_visible(self) -> bool:
        return self._visible

    def __str__(self) -> str:
        return f"{self._height} ,{self._visible}"

    def __repr__(self) -> str:
        return self.__str__()


def parse_input(lines) -> list[list[Tree, ...], ...]:
    to_return = list()

    for line in lines:
        entry = list()
        for char in line:
            if char == "\n":
                continue

            entry.append(Tree(int(char)))

        to_return.append(entry)

    return to_return


def check_trees_seen(trees) -> list:
    trees = check_outer_trees_seen(trees)
    trees = check_trees_from_left_seen(trees)
    trees = check_trees_from_top_seen(trees)
    trees = check_trees_from_right_seen(trees)
    trees = check_trees_from_bottom_seen(trees)

    return trees


def check_outer_trees_seen(trees) -> list:
    for ind_l, line in enumerate(trees):
        for ind_r, tree in enumerate(line):
            if ind_l == 0:
                tree.set_visible()
                continue
            if ind_l == len(trees) - 1:
                tree.set_visible()
                continue
            if ind_r == 0:
                tree.set_visible()
                continue
            if ind_r == len(line) - 1:
                tree.set_visible()
                continue

    return trees


def check_trees_from_left_seen(trees) -> list:
    for i_l, line in enumerate(trees):
        current_value = 0
        for i_r, tree in enumerate(line):
            if i_l == 0 or i_l == len(trees) - 1:
                continue

            if current_value < tree.get_height():
                tree.set_visible()
                current_value = tree.get_height()

    return trees


def check_trees_from_top_seen(trees) -> list:
    to_check = [0 for x in trees]

    for l_i, line in enumerate(trees):
        for r_i, tree in enumerate(line):
            if r_i == 0 or r_i == len(line) -1:
                continue
            if to_check[r_i] < tree.get_height():
                tree.set_visible()
                to_check[r_i] = tree.get_height()

    return trees


    return trees


def check_trees_from_right_seen(trees) -> list:
    for line in trees:
        line.reverse()

    trees = check_trees_from_left_seen(trees)

    for line in trees:
        line.reverse()

    return trees


def check_trees_from_bottom_seen(trees) -> list:
    trees.reverse()

    trees = check_trees_from_top_seen(trees)

    trees.reverse()

    return trees


def count_seen_trees(trees) -> int:
    count = 0

    for row in trees:
        for tree in row:
            if tree.is_visible():
                count += 1

    return count


def get_seen_trees_count(trees) -> int:
    trees = check_trees_seen(trees)
    count = count_seen_trees(trees)
    return count


def d_08_main() -> None:
    with open("day_08/input_08_1.txt", "r") as file:
        lines = file.readlines()

        trees = parse_input(lines)

        #1
        count = get_seen_trees_count(trees)
        print(f"trees that are be seen are: {count}")

        #2
