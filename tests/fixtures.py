import io
import pathlib

import pytest

fixtures = pathlib.Path(__file__).parent / "fixtures"

trace_path = fixtures / "trace_example"


@pytest.fixture(scope="session")
def trace_example():
    with open(trace_path, "r") as fd:
        return [
            line
            for line in fd
        ]
