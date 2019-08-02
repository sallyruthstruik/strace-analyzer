import io
import re
import typing

from attr import dataclass

LINE_REGEXP = re.compile(
    "^(?P<datetime>[^ ]*) "
    "(?P<method>\w+)"
    "\((?P<args>.*?)\)"
)


def join_array(data, sep=", "):
    return sep.join(map(str, data))


@dataclass(slots=True)
class ParsedLine:
    line_index: int
    datetime: str
    method: str
    args: str
    raw_line: str

    def check_keys(self, k):
        diff = set(k.keys()).difference(self.__slots__)
        if diff:
            raise ValueError(f"Bad keys passed: {join_array(diff)}")


class Parser:

    def __init__(self, lines):
        self.lines = lines
        self.current_line = None
        self.current_line_index = None

    def parse(self):
        for i, line in enumerate(self.lines):
            self.set_current_line(line, i)
            if self.ignore_line():
                continue
            yield self.parse_line()

    def ignore_line(self):
        if "futex(" in self.current_line:
            return True
        if self.current_line.startswith("strace:"):
            return True
        return False

    def parse_line(self) -> dict:
        m = LINE_REGEXP.match(self.current_line)

        if not m:
            raise ValueError(f"Bad line [{self.current_line_index}] {self.current_line}")

        return dict(
            datetime=self.get_value(m, "datetime"),
            method=self.get_value(m, "method"),
            args=self.get_value(m, "args"),
            raw_line=self.current_line,
            line_index=self.current_line_index,
        )

    def set_current_line(self, line, line_index):
        self.current_line = line
        self.current_line_index = line_index

    def get_value(self, match: typing.Match[str], name):
        return match.group(name)


def parse(fd) -> typing.List[dict]:
    p = Parser(fd)
    return p.parse()





