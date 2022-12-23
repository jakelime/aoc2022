import time
from pathlib import Path
import pandas as pd
from collections import namedtuple, OrderedDict
import copy


class Move:
    @staticmethod
    def read_command(command: str):
        try:
            commands = command.split(" ")
            for keyword in ["move", "from", "to"]:
                if keyword not in commands:
                    raise Exception(f"{keyword=} not found in command")
            Command = namedtuple("Command", "n i_from i_to")
            command = Command(
                n=int(commands[1]), i_from=int(commands[3]), i_to=int(commands[5])
            )
            return command
        except Exception as e:
            raise Exception(f"Could not parse command; {e}")

    @staticmethod
    def move9000(board: dict, command: str):
        new_board = OrderedDict()
        command = Move.read_command(command)
        for _ in range(command.n):
            crate = board[command.i_from].pop()
            board[command.i_to].append(crate)
        print(
            f" >>moved {command.n} crates from index{command.i_from} to index{command.i_to}"
        )
        return new_board

    @staticmethod
    def move9001(board: dict, command: str):
        new_board = OrderedDict()
        command = Move.read_command(command)

        if command.n == 1:
            crate = board[command.i_from].pop()
            board[command.i_to].append(crate)
        else:
            column = copy.deepcopy(
                board[command.i_from]
            )  # the column of crates to be moved from

            crates = copy.deepcopy(
                column[-command.n :]
            )  # the number of crates to be moved
            remaining = column[:(len(column) - command.n)]

            # print(f"crates = \n{crates}")
            # print(f"board[command.i_from] = \n{board[command.i_from]}")
            # print(f"column = \n{column}")
            # print(f"remaining = \n{remaining}")

            board[command.i_from] = remaining  # after removing the number of crates
            board[command.i_to] = board[command.i_to] + crates

        print(
            f" >>moved {command.n} crates from index{command.i_from} to index{command.i_to}"
        )
        return new_board


class LayoutReader:
    def __init__(self, filepath=None):
        self.axis_mapping = {}
        self.layout = OrderedDict()
        self.axis_mapping, self.layout, self.instructions = self.get_data(filepath)

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
    def get_columns(board_data: list[list], axis_to_index_map: dict) -> OrderedDict:
        data = OrderedDict()
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

    def get_data(self, fpath: Path) -> tuple:

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
                            axis_mapping = self.get_axis_mapping_dict(axis_datalist)
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
        layout = self.get_columns(board_datalist, axis_mapping)

        return axis_mapping, layout, instructions_datalist


class Game:
    def __init__(self, filename: str = "example.txt"):
        self.filepath = self.get_filepath(filename)
        self.layout = LayoutReader(self.filepath)

    def part1(self):
        m = Move()
        layout = self.layout
        for _, instr in enumerate(layout.instructions):
            m.move9000(board=layout.layout, command=instr)
        self.print_results()

    def part2(self, print_results=False):
        m = Move()
        layout = self.layout

        if print_results:
            self.print_board()
        for i, instr in enumerate(layout.instructions):
            # if i > 0:
            #     break
            m.move9001(board=layout.layout, command=instr)
            if print_results:
                self.print_board()
                self.print_results()
        if not print_results:
            self.print_results()

    def get_filepath(self, filename: str = "example.txt") -> Path:
        cwd_ = Path(__file__)
        cwd = cwd_.parent
        fileinput = cwd / filename
        if not fileinput.exists():
            raise Exception(f"invalid filepath, {fileinput=}")
        return fileinput

    def print_results(self):
        result_list = [v[-1] if v else " " for _, v in self.layout.layout.items()]
        result = "".join(result_list)
        print(f"{result = }")

    def print_board(self):
        pl = OrderedDict()
        max_length = 0
        for v in self.layout.layout.values():
            if len(v) > max_length:
                max_length = len(v)

        for k, v in self.layout.layout.items():
            if len(v) != max_length:
                nv = v + ((max_length - len(v)) * [""])
                pl[k] = nv[::-1]
            else:
                pl[k] = v[::-1]

        df = pd.DataFrame(pl)
        print(df)


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
