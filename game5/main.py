import time
from pathlib import Path
import pandas as pd
import csv


class Mover:
    def __init__(self):
        pass


class CreateLayout:
    def __init__(self, filepath=None):
        self.axis_mapping = {}
        self.layout = self.get_data(filepath)

    @staticmethod
    def check_axis_in_sequence(given_sequence: list[int]):
        previous = 0
        for x in given_sequence:
            if x == previous + 1:
                previous = x
                continue
            else:
                raise Exception(f"given_sequence is not a sequence\n{given_sequence=}")

    @staticmethod
    def get_axis_mapping_dict(axis_data: list[int]) -> dict:
        axis_mapping = {}
        current_value = 1
        if axis_data[0] != 1:
            raise Exception(f"axis_data[0] is not 1")
        else:
            axis_mapping[axis_data[0]] = current_value

        if len(axis_data) > 1:
            for x in axis_data[1:]:
                current_value += 4
                axis_mapping[x] = current_value
        return axis_mapping

    @staticmethod
    def get_columns(board_data: list[list], axis_to_index_map: dict) -> dict:
        data = {}
        for k in axis_to_index_map.keys():
            data[k] = []
        for row in board_data:
            for k, v in axis_to_index_map.items():
                try:
                    obj = row[v].strip()
                    if obj:
                        data[k].insert(0, obj)
                except IndexError as e:
                    continue
                except Exception as e:
                    raise e
        return data

    def get_data(self, fpath):

        board_datalist, axis_datalist, instructions_datalist = [], [], []
        step1_findaxis = False

        with open(fpath, mode="r") as f:
            line = f.readline()
            while line:
                temp = line.strip()

                if not step1_findaxis:
                    if "1 " in temp:
                        try:
                            # This is to identify axis in the board drawing
                            # Example: axis_datalist = [1, 2, 3]
                            axis_datalist = [int(x) for x in temp.split(" ") if x]
                            self.check_axis_in_sequence(axis_datalist)
                            self.axis_mapping = self.get_axis_mapping_dict(
                                axis_datalist
                            )
                            step1_findaxis = True
                        except Exception as e:
                            raise Exception(
                                f"failed to find axis. thought that line {line} was axis; {e}"
                            )
                    else:
                        # temp is the result of list[  '[Z] [M] [P]', ..  ]
                        temp = line.split("\n")[:-1][0]
                        board_datalist.append(temp)

                else:
                    instructions_datalist.append(temp)
                    instructions_datalist = [x for x in instructions_datalist if x]

                line = f.readline()
        data = self.get_columns(board_datalist, self.axis_mapping)
        return data


class Game:
    def __init__(self, filename: str = "example.txt"):
        self.filepath = self.get_filepath(filename)
        self.layout = CreateLayout(self.filepath).layout

        print(self.layout)

    def part1(self):
        pass
        # print(f"{self.df=}")

    def get_filepath(self, filename: str = "example.txt") -> Path:
        cwd_ = Path(__file__)
        cwd = cwd_.parent
        fileinput = cwd / filename
        if not fileinput.exists():
            raise Exception(f"invalid filepath, {fileinput=}")
        return fileinput


def main():

    game = Game("example.txt")
    # game = Game("input.txt")
    # game.part1()
    # game.part2()
    pass


if __name__ == "__main__":
    t0 = time.perf_counter()
    main()
    print(f"*** main executed. time taken = {(time.perf_counter()-t0):.5f}s ***")
