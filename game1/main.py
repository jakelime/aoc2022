import time
from pathlib import Path
import pandas as pd
import csv

# pd.options.mode.chained_assignment = None
# import numpy as np


def isLast(itr):
    old = next(itr)
    for new in itr:
        yield False, old
        old = new
    yield True, old


class Game1:
    def __init__(self, filename: str = "example.txt"):
        self.filepath = self.get_filepath(filename)
        self.elves = self.get_data()
        self.df = self.get_elf_calories_df(self.elves)
        self.top3 = self.get_top3()

    def get_filepath(self, filename: str = "example.txt") -> Path:
        cwd = Path(__file__).parent
        fileinput = cwd / filename
        if not fileinput.exists():
            raise Exception(f"invalid filepath, {fileinput=}")
        return fileinput

    def get_data(self):

        with open(self.filepath) as csv_file:
            reader = csv.reader(csv_file)
            elves, food_bag = [], []

            for _, (is_last, food) in enumerate(isLast(reader)):
                if food:
                    food_bag.append(food[0])
                    if is_last:
                        elves.append(food_bag)
                else:
                    elves.append(food_bag)
                    food_bag = []

            return elves

    def get_elf_calories_df(self, elves: list[list]) -> pd.DataFrame:
        elf_calories = []
        for i, elf in enumerate(elves):
            if elf:
                total_calories = sum([int(x) for x in elf])
                elf_calories.append((i + 1, total_calories))
        df = pd.DataFrame(elf_calories, columns=["elf_index", "calories"])
        df = df.set_index("elf_index")
        # elf_max = df[df["calories"] == df["calories"].max()]
        # print(f"{elf_max=}")
        return df

    def get_top3(self):
        df = self.df.sort_values(by="calories", ascending=False).reset_index()
        df = df.loc[df.index[:3], :].set_index("elf_index")
        print(f"top3:\n{df}")
        print(f"Total calories: {df['calories'].sum()}")
        return df


def main():

    # g = Game1()
    g = Game1("input.txt")

    pass


if __name__ == "__main__":
    t0 = time.perf_counter()
    main()
    print(f"*** main executed. time taken = {(time.perf_counter()-t0):.5f}s ***")
