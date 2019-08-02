import typing
import pandas as pd
from pandas import to_datetime

from strace_parser._parse import Parser


class Analyzer:
    df: pd.DataFrame

    def __init__(self, parsed: typing.List[dict]):
        self.df = pd.DataFrame(parsed)

        self.parse_args()

    def parse_args(self):
        self.df["pid"] = self.df[self.rows_with_pid()].args.str.split(",", expand=True)[0]
        self.df["datetime"] = to_datetime(self.df.datetime)

    @classmethod
    def from_fd(cls, lines):
        parser = Parser(lines)
        return cls(parser.parse())

    def rows_with_pid(self):
        return self.df.method.isin([
            "write",
            "read",
        ])

