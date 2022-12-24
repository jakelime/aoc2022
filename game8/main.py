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

    def get_data(self) -> pd.DataFrame:
        with open(self.filepath, mode="r") as fin:
            lines = fin.readlines()
            # lines = fin.read().strip().split("\n")
            lines = [list(x.strip()) for x in lines]
        df = pd.DataFrame(lines)
        return df


class Game:
    edge_visible_trees = 0

    def __init__(self, filename="example.txt"):
        self.data = Reader(filename).get_data()
        self.count_trees()

    def part1(self):
        return self

    def part2(self):
        return self

    def count_trees(self):
        df = self.data.astype(int)
        # print(df.reset_index(drop=True).to_string(index=False))
        self.edge_visible_trees = (2 * df.shape[0]) + (2 * (df.shape[1] - 2))
        print(f"{self.edge_visible_trees = }")

        corr_map = namedtuple("CoordinateMap", "coorx coory value visible vfrom")
        datalist = []
        for i, row in enumerate(df.itertuples()):
            if i == 0 or i == df.shape[0] - 1:  # skip top and bottom edges
                continue
            # if i != 3: continue
            # print(row)
            for j, x in enumerate(row):
                if j <= 1 or j == df.shape[1]:  # skip index, left and right edges
                    continue
                # if j != 3: continue
                coory = i
                coorx = j - 1
                v = df.iloc[coory, coorx]
                # print(f"{x} ({v=}), [{coory=},{coorx=}]")

                visible = False
                vfrom = ""

                ## TOP ##
                top_trees = df.iloc[:coory, coorx]
                # print(f"top_trees: \n{top_trees}")
                if v > top_trees.max():
                    visible = True
                    vfrom = 'top'

                ## BTM ##
                if not visible:
                    btm_trees = df.iloc[coory+1:, coorx]
                    # print(f"btm_trees: \n{btm_trees}")
                    if v > btm_trees.max():
                        visible = True
                        vfrom = 'btm'

                ## LEFT ##
                if not visible:
                    left_trees = df.iloc[coory, :coorx]
                    # print(f"left_trees: \n{left_trees}")
                    if v > left_trees.max():
                        visible = True
                        vfrom = 'left'

                ## RIGHT ##
                if not visible:
                    right_trees = df.iloc[coory, coorx+1:]
                    # print(f"right_trees: \n{right_trees}")
                    if v > right_trees.max():
                        visible = True
                        vfrom = 'right'

                datalist.append(
                    corr_map(
                        coorx=coorx, coory=coory, value=v, visible=visible, vfrom=vfrom
                    )
                )

        datalist = sorted(datalist, key=lambda x: x.coory)
        visible_trees = [x for x in datalist if x.visible]
        print(f"{len(visible_trees) = }")
        total_visible_trees = len(visible_trees) + self.edge_visible_trees
        print(f"{total_visible_trees = }")



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
