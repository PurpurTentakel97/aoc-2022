#
# Purpur Tentakel
# 05.12.2022
#

class Item:
    def __init__(self, worry_level: int):
        self.worry_level = worry_level

    def __str__(self) -> str:
        return f"{self.worry_level}"

    def __repr__(self) -> str:
        return self.__str__()


class Monkey:
    def __init__(self, ID: int, items: list, worry_operation, division_test, to_monkey_valid, to_monkey_invalid):
        self._ID = ID
        self._items: list[Item, ...] = items
        self._worry_operation = worry_operation
        self._division_test = division_test
        self._to_monkey_valid: int = to_monkey_valid
        self._to_monkey_invalid: int = to_monkey_invalid
        self._visited_items = 0

    def __str__(self) -> str:
        return f"({self._ID}, {self._items}, {self._worry_operation}, {self._division_test}, {self._to_monkey_valid}, {self._to_monkey_invalid}, {self._visited_items})"

    def __repr__(self) -> str:
        return self.__str__()

    def get_visited_count(self) -> int:
        return self._visited_items

    def visit_item(self) -> list[bool, int, Item]:
        if not bool(self._items):
            return [False, -1, Item(0)]

        self._visited_items += 1

        item = self._items.pop(0)
        old = item.worry_level
        item.worry_level = eval(self._worry_operation)
        item.worry_level = int(item.worry_level / 3)

        old = item.worry_level
        valid = eval(self._division_test)

        if valid:
            return [True, self._to_monkey_valid, item]
        else:
            return [True, self._to_monkey_invalid, item]

    def add_item(self, item: Item) -> None:
        self._items.append(item)


def single_round(monkeys: list[Monkey, ...]) -> list[Monkey, ...]:
    for monkey in monkeys:
        valid_visit = True

        while valid_visit:
            valid, index, item = monkey.visit_item()

            valid_visit = valid
            if valid:
                monkeys[index].add_item(item)

    return monkeys


def all_rounds(monkeys: list[Monkey, ...], rounds: int) -> list[Monkey, ...]:
    for round_ in range(rounds):
        print(f"start {round_ + 1}")
        monkeys = single_round(monkeys)
        print(f"end {round_ + 1}")

    return monkeys


def get_scores_from_monkeys(monkeys: list[Monkey, ...]) -> list[int, ...]:
    to_return = list()

    for monkey in monkeys:
        to_return.append(monkey.get_visited_count())

    return to_return


def get_top_highest_entries_from_list(numbers: list[int, ...], count: int) -> list[int, int]:
    if count <= 0:
        return []

    sorted_numbers = sorted(numbers)
    if len(sorted_numbers) < count:
        return sorted_numbers
    return sorted_numbers[-count:]


def get_multiplied_values_from_list(numbers: list[int, ...]) -> int:
    if not bool(numbers):
        return 0

    value = numbers[0]
    for i in range(1, len(numbers)):
        value *= numbers[i]
    return value


def parse_input(lines: list[str, ...]) -> list[Monkey, ...]:
    to_parse: list = [list()]

    for line in lines:
        if len(line.rstrip()) == 0:
            to_parse.append(list())
        else:
            to_parse[len(to_parse) - 1].append(line.rstrip())

    to_return: list[Monkey, ...] = list()
    for parse in to_parse:
        input_parts: list = list()

        line_0 = int(parse[0].split(" ")[1].split(":")[0])
        input_parts.append(line_0)

        line_1 = parse[1].split(":")[1].split(",")
        for i, entry in enumerate(line_1):
            line_1[i] = Item(int(entry))
        input_parts.append(line_1)

        line_2 = parse[2].split("=")[1].strip()
        input_parts.append(line_2)

        line_3 = parse[3].split("y")[1].strip()
        input_parts.append(f"old % {line_3} == 0")

        line_4 = int(parse[4].split("y")[1])
        input_parts.append(line_4)

        line_5 = int(parse[5].split("y")[1])
        input_parts.append(line_5)

        to_return.append(Monkey(
            input_parts[0],
            input_parts[1],
            input_parts[2],
            input_parts[3],
            input_parts[4],
            input_parts[5]
        ))

    return to_return


def d_11_main() -> None:
    lines = list()
    with open("day_11/input_11_1.txt", "r") as file:
        lines = file.readlines()

    monkeys: list[Monkey, ...] = parse_input(lines)

    monkeys = all_rounds(monkeys, 20)
    scores = get_scores_from_monkeys(monkeys)
    two_top_scores = get_top_highest_entries_from_list(scores, 2)
    result = get_multiplied_values_from_list(two_top_scores)
    print(f"the result is: {result}")
