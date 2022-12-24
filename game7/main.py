import time
from pathlib import Path
import pandas as pd
from collections import defaultdict, namedtuple, OrderedDict
import copy
from functools import lru_cache


class Reader:
    def __init__(self, filename: str = "example.txt"):
        self.filepath = self.get_filepath(filename)
        self.data = self.get_data()

    def get_filepath(self, filename: str) -> Path:
        cwd_ = Path(__file__)
        cwd = cwd_.parent
        fileinput = cwd / filename
        if not fileinput.exists():
            raise Exception(f"invalid filepath, {fileinput=}")
        return fileinput

    def get_data(self) -> list[str]:
        with open(self.filepath, mode="r") as f:
            blocks = ("\n" + f.read().strip()).split("\n$ ")[1:]

        # [print(f"[{b}]\n") for b in blocks]
        return blocks


class Game:
    def __init__(self, filename="example.txt"):
        self.total_filesystem_size = 70000000
        self.required_size = 30000000
        self.dir_sizes = defaultdict(int)
        self.children = defaultdict(list)
        self.blocks = Reader(filename).data
        self.cw_path = []
        # [print(x) for x in self.datalist]

    def part1(self):

        for block in self.blocks:
            self.parse(block)

        print(f"self.dir_sizes:")
        for k, v in self.dir_sizes.items():
            print(f"{k}: {v}")
            # print(f"{k}: {v} = {self.`dfs(v)}")
        print("")

        print(f"self.children:")
        for k, _ in self.children.items():
            print(f"{k}: .. ")
        print("")

        answer = 0
        for abspath in self.dir_sizes:
            if self.get_dir_filesize(abspath) <= 100000:
                answer += self.get_dir_filesize(abspath)
        print(f"{answer = }")

    def part2(self):

        self.dir_total_sizes = defaultdict(int)

        for block in self.blocks:
            self.parse(block)

        print(f"total_recursive_sizes:")
        for k, v in self.dir_sizes.items():
            total_recursive_size = self.get_dir_filesize(k)
            self.dir_total_sizes[k] = total_recursive_size
            print(f"{k}: {total_recursive_size}")
        print("")

        available_size = self.total_filesystem_size - self.get_dir_filesize("/")
        print(f"{available_size = }")
        required_size_ =  self.required_size - available_size
        print(f"{required_size_ = }")
        available_dirs = []
        for k, v in self.dir_total_sizes.items():
            if "//" in k:
                if v > required_size_:
                    available_dirs.append((k, v))
        if available_dirs:
            available_dirs = sorted(available_dirs, key=lambda x: x[-1])
            print(f"list of available directories:")
            for i, x in enumerate(available_dirs):
                if i>=5:
                    print("...")
                    break
                print(x)
            print("")
            print(f"dir to deleted with least size = {available_dirs[0]}")


    def parse(self, block: str):
        lines = block.split("\n")
        command = lines[0]
        outputs = lines[1:]

        command_parts = command.split(" ")
        op = command_parts[0]
        if op == "cd":
            if command_parts[1] == "..":
                self.cw_path.pop()
            else:
                self.cw_path.append(command_parts[1])
            # print(self.cw_path)
            return

        elif op == "ls":
            abspath = "/".join(self.cw_path)
            # print(f"{abspath = }")
            filesizes = []
            for line in outputs:
                if not line.startswith("dir"):
                    filesizes.append(int(line.split(" ")[0]))
                else:
                    dir_name = line.split(" ")[1]
                    self.children[abspath].append(f"{abspath}/{dir_name}")

            self.dir_sizes[abspath] = sum(filesizes)
            # print(f"{self.dir_sizes[abspath] = }\n")

        else:
            raise Exception(f"unknown command {command}")

    @lru_cache
    def get_dir_filesize(self, abspath: str):
        size = self.dir_sizes[abspath]
        for child in self.children[abspath]:
            size += self.get_dir_filesize(child)
        return size

    def get_summary(self):
        for block in self.blocks:
            self.parse(block)

        print(f"self.dir_sizes:")
        for k, v in self.dir_sizes.items():
            print(f"{k}: {v}; total ==> {self.get_dir_filesize(k)}")
            # print(f"{k}: {v} = {self.`dfs(v)}")
        print("")

        print(f"self.children:")
        for k, v in self.children.items():
            print(f"{k}: {v}")
        print("")


def main():

    # game = Game("example.txt")
    game = Game("input.txt")
    # game.get_summary()
    # game.part1()
    game.part2()
    # game.print_results()


if __name__ == "__main__":
    t0 = time.perf_counter()
    main()
    print(f"*** main executed. time taken = {(time.perf_counter()-t0):.5f}s ***")
