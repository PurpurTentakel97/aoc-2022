#
# Purpur Tentakel
# 05.12.2022
#

from enum import IntEnum


class TicTacToeType(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Result(IntEnum):
    LOOSE = 0
    DRAW = 3
    WIN = 6


def get_tic_tac_toe_from_string(value: str) -> TicTacToeType:
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


def get_result_from_string(value: str) -> Result:
    match value:
        case "X":
            return Result.LOOSE
        case "Y":
            return Result.DRAW
        case "Z":
            return Result.WIN


def get_score1(enemy, me) -> int:
    score: int = 0

    score += me

    if enemy == me:
        score += Result.DRAW
    else:
        match enemy:
            case TicTacToeType.ROCK:
                if me == TicTacToeType.PAPER:
                    score += Result.WIN
            case TicTacToeType.PAPER:
                if me == TicTacToeType.SCISSORS:
                    score += Result.WIN
            case TicTacToeType.SCISSORS:
                if me == TicTacToeType.ROCK:
                    score += Result.WIN

    return score


def get_score2(enemy, result) -> int:
    score: int = 0

    score += result

    match result:
        case Result.WIN:
            match enemy:
                case TicTacToeType.ROCK:
                    score += TicTacToeType.PAPER
                case TicTacToeType.PAPER:
                    score += TicTacToeType.SCISSORS
                case TicTacToeType.SCISSORS:
                    score += TicTacToeType.ROCK
        case Result.DRAW:
            score += enemy
        case Result.LOOSE:
            match enemy:
                case TicTacToeType.ROCK:
                    score += TicTacToeType.SCISSORS
                case TicTacToeType.PAPER:
                    score += TicTacToeType.ROCK
                case TicTacToeType.SCISSORS:
                    score += TicTacToeType.PAPER

    return score


def d_02_main() -> None:
    with open("day_02/input_02_2.txt", "r") as file:
        score1: int = 0
        score2: int = 0

        for line in file:
            if len(line) == 0:
                continue

            enemy, second = line.strip().split(" ")
            enemy = get_tic_tac_toe_from_string(enemy)
            predicted_me = get_tic_tac_toe_from_string(second)
            predicted_result = get_result_from_string(second)

            score1 += get_score1(enemy, predicted_me)
            score2 += get_score2(enemy, predicted_result)

        print("the total score1 is: " + str(score1))
        print("the total score2 is: " + str(score2))
