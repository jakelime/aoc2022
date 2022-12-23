import time
from pathlib import Path
import pandas as pd
import string


class Game:
    def __init__(self, filename: str = "example.txt"):
        self.filepath = self.get_filepath(filename)
        self.df = self.get_data(self.filepath)
        self.generate_priorities()

    def get_filepath(self, filename: str = "example.txt") -> Path:
        cwd = Path(__file__).parent
        fileinput = cwd / filename
        if not fileinput.exists():
            raise Exception(f"invalid filepath, {fileinput=}")
        return fileinput

    def get_data(self, fpath):
        df = pd.read_csv(fpath, header=None, sep=" ")
        df.columns = ["cipher"]
        return df

    def get_intersection(self, *args):
        setlist = [set(x) for x in args]
        results = [x for x in set.intersection(*setlist)]
        if len(results) > 0:
            if len(results) != 1:
                print(f"len(results) != 1, {results=}")
            return results[0]
        else:
            return ""

    def generate_priorities(self):
        self.priority_score = {}
        score = 0
        for i in string.ascii_letters:
            score += 1
            self.priority_score[i] = score
        print("priority_score generated.")

    def part1(self):
        df = self.df
        df["first_compartment"] = df.cipher.apply(lambda x: x[: int(len(x) / 2)])
        df["second_compartment"] = df.cipher.apply(lambda x: x[int(len(x) / 2) :])
        df["common_char"] = df.apply(
            lambda x: self.get_intersection(x.first_compartment, x.second_compartment),
            axis=1,
        )
        df["score"] = df["common_char"].map(self.priority_score)
        total_score = df.score.sum()
        print(f"{total_score = }")

    def part2(self):
        df = self.df
        df["common_char"] = ""
        df["score"] = 0
        for i, row in enumerate(df.itertuples()):
            if (i + 1) % 3 == 0:
                group_rucksack = []
                for x in [i, i - 1, i - 2]:
                    group_rucksack.append(df.loc[df.index[x], "cipher"])
                df.loc[df.index[i], "common_char"] = self.get_intersection(
                    *group_rucksack
                )

        df = df[df["common_char"] != ""].copy()
        df["score"] = df["common_char"].map(self.priority_score)
        total_score = df.score.sum()
        print(f"{total_score = }")


def main():

    game = Game("input.txt")
    # game = Game("example.txt")
    # game.part1()
    game.part2()

    pass


if __name__ == "__main__":
    t0 = time.perf_counter()
    main()
    print(f"*** main executed. time taken = {(time.perf_counter()-t0):.5f}s ***")
