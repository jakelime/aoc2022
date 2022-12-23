import time
from pathlib import Path
import pandas as pd


class Game:
    def __init__(self, filename: str = "example.txt"):
        self.filepath = self.get_filepath(filename)
        self.df = self.get_data(self.filepath)

    def part1(self):
        df = self.df.copy()
        df['elf1_sections'] = df['elf1'].apply(lambda x: self.generate_range_sectionids(x))
        df['elf2_sections'] = df['elf2'].apply(lambda x: self.generate_range_sectionids(x))
        df['compare'] = df[['elf1_sections','elf2_sections']].apply(lambda x: self.compare_2lists(*x), axis=1)
        print(df.head(5))
        print(f"Pairs with range fully contained in each other is {df['compare'].sum()}")
        return df

    def part2(self):
        df = self.df.copy()
        df['elf1_sections'] = df['elf1'].apply(lambda x: self.generate_range_sectionids(x))
        df['elf2_sections'] = df['elf2'].apply(lambda x: self.generate_range_sectionids(x))
        df['compare'] = df[['elf1_sections','elf2_sections']].apply(lambda x: self.compare_2lists_part2(*x), axis=1)
        print(df.head(5))
        print(f"Pairs intersected somehow {df['compare'].sum()}")
        return df


    def get_filepath(self, filename: str = "example.txt") -> Path:
        cwd = Path(__file__).parent
        fileinput = cwd / filename
        if not fileinput.exists():
            raise Exception(f"invalid filepath, {fileinput=}")
        return fileinput

    def get_data(self, fpath):
        df = pd.read_csv(fpath, header=None, sep=",")
        df.columns = ['elf1', 'elf2']
        return df

    @staticmethod
    def generate_range_sectionids(strvalue):
        start, end = strvalue.split('-')
        start = int(start)
        end = int(end)
        generated_range = [str(x) for x in range(start, end+1)]
        # generated_range = "".join(generated_range)
        return generated_range

    @staticmethod
    def compare_2lists_part1(list1: str, list2: str):
        result = list(set(list1).intersection(set(list2)))
        if len(result) == len(list1) or len(result) == len(list2):
            return True
        else:
            return False

    @staticmethod
    def compare_2lists_part2(list1: str, list2: str):
        result = list(set(list1).intersection(set(list2)))
        if result:
            return True
        else:
            return False




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
