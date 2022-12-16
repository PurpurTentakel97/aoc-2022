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
                print("\nday:" + str(day) + " \"Calorie Counting\"\n")
                d.d_01.d_01_main()
            case 2:
                print("\nday:" + str(day) + " \"Rock Paper Scissors\"\n")
                d.d_02.d_02_main()
            case 3:
                print("\nday:" + str(day) + " \"Rucksack Reorganization\"\n")
                d.d_03.d_03_main()
            case 4:
                print("\nday:" + str(day) + " \"Camp Cleanup\"\n")
                d.d_04.d_04_main()
            case 5:
                print("\nday:" + str(day) + " \"Supply Stacks\"\n")
                d.d_05.d_05_main()
            case 6:
                print("\nday:" + str(day) + " \"Tuning Trouble\"\n")
                d.d_06.d_06_main()
            case 7:
                print("\nday:" + str(day) + " \"No Space Left On Device\"\n")
                d.d_07.d_07_main()
            case 8:
                print("\nday:" + str(day) + " \"Treetop Tree House\"\n")
                d.d_08.d_08_main()
            case 9:
                print("\nday:" + str(day) + " \"Rope Bridge\"\n")
                d.d_09.d_09_main()
            case 10:
                print("\nday:" + str(day) + " \"Cathode-Ray Tube\"\n")
                d.d_10.d_10_main()
            case 11:
                print("\nday:" + str(day) + " \"Monkey in the Middle\"\n")
                d.d_11.d_11_main()
            case 12:
                print("\nday:" + str(day) + " \"Hill Climbing Algorithm\"\n")
                d.d_12.d_12_main()
            case 13:
                print("\nday:" + str(day) + " \"Distress Signal\"\n")
                d.d_13.d_13_main()
            case 14:
                print("\nday:" + str(day) + " \"Regolith Reservoir\"\n")
                d.d_14.d_14_main()
            case 15:
                print("\nday:" + str(day) + "\n")
                d.d_15.d_15_main()
            case 16:
                print("\nday:" + str(day) + "\n")
                d.d_16.d_16_main()
            case 17:
                print("\nday:" + str(day) + "\n")
                d.d_17.d_17_main()
            case 18:
                print("\nday:" + str(day) + "\n")
                d.d_18.d_18_main()
            case 19:
                print("\nday:" + str(day) + "\n")
                d.d_19.d_19_main()
            case 20:
                print("\nday:" + str(day) + "\n")
                d.d_20.d_20_main()
            case 21:
                print("\nday:" + str(day) + "\n")
                d.d_21.d_21_main()
            case 22:
                print("\nday:" + str(day) + "\n")
                d.d_22.d_22_main()
            case 23:
                print("\nday:" + str(day) + "\n")
                d.d_23.d_23_main()
            case 24:
                print("\nday:" + str(day) + "\n")
                d.d_24.d_24_main()
            case _:
                print("day not existing\n\n")
                continue
