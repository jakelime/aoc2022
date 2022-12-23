import time
from pathlib import Path
import pandas as pd
import csv

# pd.options.mode.chained_assignment = None
# import numpy as np


class Game:
    def __init__(self, filename: str = "example.txt"):
        self.filepath = self.get_filepath(filename)
        self.df = self.get_data(self.filepath)

    def part1(self):
        self.score_map = {
            "A": 1,  # rock
            "B": 2,  # paper
            "C": 3,  # scissors
            "X": 1,  # rock
            "Y": 2,  # paper
            "Z": 3,  # scissors
            "win": 6,
            "draw": 3,
            "loss": 0,
        }
        self.score = self.count_score(self.df)
        pass

    def get_results(self, elf, human):
        if (
            (elf == "A" and human == "X")
            or (elf == "B" and human == "Y")
            or (elf == "C" and human == "Z")
        ):
            results = "draw"
        elif (
            (elf == "A" and human == "Y")
            or (elf == "B" and human == "Z")
            or (elf == "C" and human == "X")
        ):
            results = "win"
        elif (
            (elf == "A" and human == "Z")
            or (elf == "B" and human == "X")
            or (elf == "C" and human == "Y")
        ):
            results = "loss"
        else:
            results = "error"
        return results

    def get_filepath(self, filename: str = "example.txt") -> Path:
        cwd = Path(__file__).parent
        fileinput = cwd / filename
        if not fileinput.exists():
            raise Exception(f"invalid filepath, {fileinput=}")
        return fileinput

    def get_data(self, fpath):
        df = pd.read_csv(fpath, header=None, sep=" ")
        df.columns = ["elf", "human"]
        return df

    def count_score(self, df):
        df["score"] = 0
        df["results"] = ""
        for i, row in enumerate(df.itertuples()):
            results = self.get_results(row.elf, row.human)
            df.loc[df.index[i], "results"] = results
            df.loc[df.index[i], "score"] = (
                self.score_map[row.human] + self.score_map[results]
            )
        total_score = df["score"].sum()
        print(df)
        print(f"{total_score = }")
        return

    def part2(self):
        self.score_map = {
            "A": 1,  # rock
            "B": 2,  # paper
            "C": 3,  # scissors
            "X": "loss",  # rock
            "Y": "draw",  # paper
            "Z": "win",  # scissors
            "rock": 1,  # rock
            "paper": 2,  # paper
            "scissors": 3,  # scissors
            "win": 6,
            "draw": 3,
            "loss": 0,
        }
        df = self.df
        df["results"] = df["human"].map(self.score_map)
        df["human"] = df.apply(lambda x: self.get_human_input(x.elf, x.results), axis=1)
        df["score"] = df.apply(
            lambda x: self.score_map[x.human] + self.score_map[x.results], axis=1
        )
        total_score = df["score"].sum()
        print(f"{total_score = }")

    def get_human_input(self, elf, results):
        if elf == "A":  # rock
            if results == "win":
                return "paper"
            elif results == "loss":
                return "scissors"
            elif results == "draw":
                return "rock"
            else:
                return "error"
        elif elf == "B":  # paper
            if results == "win":
                return "scissors"
            elif results == "loss":
                return "rock"
            elif results == "draw":
                return "paper"
            else:
                return "error"
        elif elf == "C":  # scissors
            if results == "win":
                return "rock"
            elif results == "loss":
                return "paper"
            elif results == "draw":
                return "scissors"
            else:
                return "error"
        else:
            return "error"


def main():

    # game = Game("example.txt")
    game = Game("input.txt")

    # game.part1()
    game.part2()

    pass


if __name__ == "__main__":
    t0 = time.perf_counter()
    main()
    print(f"*** main executed. time taken = {(time.perf_counter()-t0):.5f}s ***")
