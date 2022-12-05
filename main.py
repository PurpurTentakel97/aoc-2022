#
# Purpur Tentakel
# 05.12.2022
#

import day_imports as d

if __name__ == "__main__":
    while True:
        raw_input: str = input("enter the day\ntype \"q\" for closing\n")

        if raw_input == "q":
            break

        day: int
        try:
            day = int(raw_input)
        except ValueError:
            print("no number entered\n\n")
            continue

        match day:
            case 1:
                print("\nday:" + str(day) + "\n")
                d.d_01.d_01_main()
            case 2:
                print("\nday:" + str(day) + "\n")
                d.d_02.d_02_main()
            case 3:
                print("\nday:" + str(day) + "\n")
                d.d_03.d_03_main()
            case 4:
                print("\nday:" + str(day) + "\n")
                d.d_04.d_04_main()
            case 5:
                print("\nday:" + str(day) + "\n")
                d.d_05.d_05_main()
            case 6:
                print("\nday:" + str(day) + "\n")
            case 7:
                print("\nday:" + str(day) + "\n")
            case 8:
                print("\nday:" + str(day) + "\n")
            case 9:
                print("\nday:" + str(day) + "\n")
            case 10:
                print("\nday:" + str(day) + "\n")
            case 11:
                print("\nday:" + str(day) + "\n")
            case 12:
                print("\nday:" + str(day) + "\n")
            case 13:
                print("\nday:" + str(day) + "\n")
            case 14:
                print("\nday:" + str(day) + "\n")
            case 15:
                print("\nday:" + str(day) + "\n")
            case 16:
                print("\nday:" + str(day) + "\n")
            case 17:
                print("\nday:" + str(day) + "\n")
            case 18:
                print("\nday:" + str(day) + "\n")
            case 19:
                print("\nday:" + str(day) + "\n")
            case 20:
                print("\nday:" + str(day) + "\n")
            case 21:
                print("\nday:" + str(day) + "\n")
            case 22:
                print("\nday:" + str(day) + "\n")
            case 23:
                print("\nday:" + str(day) + "\n")
            case 24:
                print("\nday:" + str(day) + "\n")
            case _:
                print("day not existing\n\n")
                continue
