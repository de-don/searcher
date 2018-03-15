from click.testing import CliRunner
from memory_profiler import profile
from time import perf_counter

from searcher import searcher


# global runner
runner = CliRunner()

#@profile
def war_and_peace_all():
    result = runner.invoke(
        searcher,
        [
            "[a-zA-Zа-яА-Я0-9-_]+",
            "war_and_peace.fb2",
        ]
    )

#@profile
def war_and_peace_stat():
    result = runner.invoke(
        cli=searcher,
        args=[
            '[a-zA-Zа-яА-Я0-9-_]+',
            'war_and_peace.fb2',
            '-s', 'freq',
            '-o', 'asc',
            '--stat', 'count',
        ]
    )


if __name__ == '__main__':
    t = perf_counter()
    war_and_peace_all()
    war_and_peace_stat()
    print("time:", perf_counter() - t)