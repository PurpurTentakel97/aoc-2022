#
# Purpur Tentakel
# 05.12.2022
#
from enum import Enum


class InstructionType(Enum):
    NOOP = "noop"
    ADDX = "addx"


class Instruction:
    def __init__(self, instruction_type: InstructionType, count: int):
        self._instruction_type = instruction_type
        self._count = count

    def get_instruction(self) -> InstructionType:
        return self._instruction_type

    def get_count(self) -> int:
        return self._count

    def __str__(self) -> str:
        return f"{self._instruction_type}, {self._count}"

    def __repr__(self) -> str:
        return self.__str__()


def is_reasonable_cycle(cycle: int) -> bool:
    return ((cycle - 20) % 40) == 0


def calculate_single_signal_strength(cycle: int, value: int) -> int:
    return cycle * value


def parse_instructions(lines: list[str, ...]) -> list[Instruction, ...]:
    instructions: list[Instruction, ...] = list()

    for line in lines:
        parts = line.split(" ")

        type_: InstructionType = InstructionType(parts[0].rstrip("\n"))

        match type_:
            case InstructionType.NOOP:
                instructions.append(Instruction(type_, 0))
            case InstructionType.ADDX:
                instructions.append(Instruction(InstructionType.NOOP, 0))
                instructions.append(Instruction(type_, int(parts[1])))

    return instructions


def get_char_to_draw(cycle: int, value: int) -> str:
    if (cycle - 1) % 40 in list(range(value - 1, value + 2)):
        return "#"
    else:
        return "."


def run_cycle(instructions: list[Instruction, ...]) -> list[int, ...]:
    cycle: int = 0
    value: int = 1
    signal_strength: list[int, ...] = list()
    to_print = str()
    line = str()

    for instruction in instructions:
        cycle += 1

        if is_reasonable_cycle(cycle):
            signal_strength.append(calculate_single_signal_strength(cycle, value))

        line += get_char_to_draw(cycle, value)
        if len(line) % 40 == 0:
            line += "\n"
            to_print += line
            line = ""

        match instruction.get_instruction():
            case InstructionType.NOOP:
                continue
            case InstructionType.ADDX:
                value += instruction.get_count()

    print(to_print)
    return signal_strength


def d_10_main() -> None:
    lines: list = list()
    with open("day_10/input_10_2.txt", "r") as file:
        lines = file.readlines()

    instructions = parse_instructions(lines)

    signal_strength = run_cycle(instructions)
    print(f"sum of the signal strength: {sum(signal_strength)}")
