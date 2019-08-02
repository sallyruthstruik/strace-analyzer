from strace_parser import parse


def test_parse(trace_example):
    parsed = list(parse(trace_example))

    for line in parsed[:10]:
        print(line)

    assert len(parsed) == 3041
