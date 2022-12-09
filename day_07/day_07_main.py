#
# Purpur Tentakel
# 05.12.2022
#

class File:
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size


class Directory:
    def __init__(self, name):
        self.name: str = name
        self._directories: list["Directory", ...] = list()
        self._files: list[File, ...] = list()

    def get_directories(self) -> list["Directory"]:
        return self._directories

    def add_directory(self, to_add: "Directory") -> None:
        for dir in self._directories:
            if dir == to_add:
                return
        self._directories.append(to_add)

    def add_file(self, to_add: File):
        for file in self._files:
            if file == to_add:
                return
        self._files.append(to_add)

    def count_size(self) -> int:
        count: int = 0

        for file in self._files:
            count += file.size

        for dir in self._directories:
            count += dir.count_size()

        return count

    def get_directory_by_name(self, name: str) -> "Directory":
        for dir in self._directories:
            if name == dir.name:
                return dir


def parse_entries(lines: list[str, ...]) -> Directory:
    dirs: Directory = Directory("/")
    current_directory: list[Directory, ...] = [dirs]

    for line in lines:

        if line[-1] == "\n":
            line = line[:-1]

        arguments: list[str, ...] = line.split(" ")

        if arguments[0] == "$":
            if arguments[1] == "cd":

                match arguments[2]:
                    case "/":
                        current_directory = [dirs]
                    case "..":
                        current_directory.pop()
                        if len(current_directory) == 0:
                            current_directory = [dirs]
                    case _:
                        current_directory.append(current_directory[-1].get_directory_by_name(arguments[2]))

            elif arguments[1] == "ls":
                pass

        else:
            if arguments[0] == "dir":
                current_directory[-1].add_directory(Directory(arguments[1]))

            else:
                current_directory[-1].add_file(File(arguments[1], int(arguments[0])))

    return dirs


def get_directories_smaller_than(directory: Directory, upper_border: int, lower_border) -> list[
    list[Directory, ...], list[Directory, ...]]:
    upper_dirs: list[Directory, ...] = list()
    lower_dirs: list[Directory, ...] = list()

    size: int = directory.count_size()
    if size <= upper_border:
        upper_dirs.append(directory)

    if size >= lower_border:
        lower_dirs.append(directory)

    for dir in directory.get_directories():
        low, up = get_directories_smaller_than(dir, upper_border, lower_border)
        lower_dirs.extend(low)
        upper_dirs.extend(up)

    return [lower_dirs, upper_dirs]


def get_dir_count(dirs: list[Directory, ...]) -> int:
    count: int = 0

    for dir in dirs:
        count += dir.count_size()

    return count


def get_lowest_dir(dirs: list[Directory, ...]) -> Directory:
    current_directory: Directory | None = None

    for dir in dirs:
        if not current_directory:
            current_directory = dir
            continue

        if current_directory.count_size() > dir.count_size():
            current_directory = dir

    return current_directory


def d_07_main() -> None:
    size_filesystem: int = 70000000
    size_update: int = 30000000

    with open("day_07/input_07_2.txt", "r") as f:
        lines = f.readlines()

        dirs: Directory = parse_entries(lines)

        # 1
        total_used_size: int = dirs.count_size()
        needed_size: int = size_update - (size_filesystem - total_used_size)

        large_dirs, small_dirs = get_directories_smaller_than(dirs, 100000, needed_size)
        print("small directory count: " + str(get_dir_count(small_dirs)))
        directory_to_delete: Directory = get_lowest_dir(large_dirs)
        print("smallest directory to delete: " + str(directory_to_delete.count_size()))
