import time
from pathlib import Path
import pandas as pd
from collections import namedtuple, OrderedDict
import copy


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

    def get_data(self) -> None:

        with open(self.filepath, mode="r") as f:
            datalist = f.readlines()
        datalist = [x.strip() for x in datalist]

        return datalist


class Game:
    def __init__(self, filename="example.txt"):
        self.datalist = Reader(filename).data

    def part2(self):
        print(f"\nfinding first marker:\n")
        for data in self.datalist:
            self.find_first_marker(data, unique_chars=14)

    def part1(self):
        print(f"\nfinding first marker:\n")
        for data in self.datalist:
            self.find_first_marker(data)

    @staticmethod
    def find_first_marker(strv, unique_chars=4):
        lib = []

        for i, x in enumerate(strv):
            lib.append(x)
            if len(lib) < unique_chars:
                continue
            else:
                # print(f"{i}: {''.join(lib)} - {len(lib) = }, {len(set(lib)) = }")
                if len(lib) == len(set(lib)):
                    starter = "".join(lib)
                    answer = i + 1
                    print(f"{answer = }, {starter = }\n")
                    break
                else:
                    lib = lib[-(unique_chars-1):]


def main():

    # game = Game("example.txt")
    game = Game("input.txt")
    # game.part1()

    game.part2()
    # game.print_results()


if __name__ == "__main__":
    t0 = time.perf_counter()
    main()
    print(f"*** main executed. time taken = {(time.perf_counter()-t0):.5f}s ***")
