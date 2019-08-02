from strace_parser._analyzer import Analyzer


def test_analyze(trace_example):
    a = Analyzer.from_fd(trace_example)



    print(a.df)