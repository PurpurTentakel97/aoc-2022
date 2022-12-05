#
# Purpur Tentakel
# 05.12.2022
#

from enum import IntEnum


class TicTacToeType(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


def get_enum_from_string(value: str) -> TicTacToeType:
    match value:
        case "A":
            return TicTacToeType.ROCK
        case "B":
            return TicTacToeType.PAPER
        case "C":
            return TicTacToeType.SCISSORS

        case "X":
            return TicTacToeType.ROCK
        case "Y":
            return TicTacToeType.PAPER
        case "Z":
            return TicTacToeType.SCISSORS


def d_02_main() -> None:
    with open("day_02/input_02_1.txt", "r") as file:
        score: int = 0
        for line in file:
            if len(line) == 0:
                continue

            enemy, me = line.strip().split(" ")
            enemy = get_enum_from_string(enemy)
            me = get_enum_from_string(me)

            score += me

            if enemy == me:
                score += 3
                continue

            match enemy:
                case TicTacToeType.ROCK:
                    if me == TicTacToeType.PAPER:
                        score += 6
                case TicTacToeType.PAPER:
                    if me == TicTacToeType.SCISSORS:
                        score += 6
                case TicTacToeType.SCISSORS:
                    if me == TicTacToeType.ROCK:
                        score += 6

        print("the total score is: " + str(score))
