from click.testing import CliRunner

from searcher import searcher


def check_output(result, need):
    """ Function to compare result.output and need array """
    out = result.output.splitlines()
    return out == need


def to_lines(*args):
    return "\n".join(args)


# global runner
runner = CliRunner()


def test_searcher_input_stdin():
    result = runner.invoke(searcher, ["[\w.\-_]+@[\w.-_]+"],
                           input="de-don@mail.ru\nnothing\nsam@vk.com")
    assert check_output(result, ["de-don@mail.ru", "sam@vk.com"])
    assert result.exit_code == 0


def test_searcher_input_file():
    # if file exists
    result = runner.invoke(searcher, ["[\w.\-_]+@[\w.-_]+", "emails.txt"])
    assert check_output(result, ["de-don@mail.ru", "de-don2@mail.ru", "de-don@inbox.ru", "admin_site@google.ru"])
    assert result.exit_code == 0

    # if file not exists
    result = runner.invoke(searcher, ["\w+", "t.txt"])
    assert result.exit_code == 2


def test_searcher_flag_u():
    result = runner.invoke(searcher, ['-u', '\w+'], input=to_lines("one", "two", "two", "three", "one"))
    assert check_output(result, ["one", "two", "three"])

    result = runner.invoke(searcher, ['-u', '\w+'], input=to_lines("one", "two", "three"))
    assert check_output(result, ["one", "two", "three"])


def test_searcher_flag_c():
    result = runner.invoke(searcher, ['-c', '\w+'], input=to_lines("one two", "three", ""))
    assert result.output == "Total count of matches: 3\n"

    result = runner.invoke(searcher, ['-c', '@\w+'], input=to_lines("one two", "three", ""))
    assert result.output == "Total count of matches: 0\n"

    result = runner.invoke(searcher, ['-c', '-u', '\w+'], input=to_lines("one two", "three", "one two", ""))
    assert result.output == "Total count of matches: 3\n"


def test_searcher_flag_l():
    result = runner.invoke(searcher, ['-l', '\w+'], input=to_lines("one", "two", "three"))
    assert result.output == "Lines with matches: 3\n"

    result = runner.invoke(searcher, ['-l', '\w+'], input=to_lines("one", "two three"))
    assert result.output == "Lines with matches: 2\n"


def test_searcher_sort():
    # test opt_s == 'abc'
    inp = ["abb", "bbb", "aaa", "ccc"]
    out = ["aaa", "abb", "bbb", "ccc"]

    result = runner.invoke(searcher, ['-s', 'abc', '\w+'], input=to_lines(*inp))
    assert check_output(result, out)

    result = runner.invoke(searcher, ['-s', 'abc', '-o', 'asc', '\w+'], input=to_lines(*inp))
    assert check_output(result, out)

    result = runner.invoke(searcher, ['-s', 'abc', '-o', 'desc', '\w+'], input=to_lines(*inp))
    assert check_output(result, list(reversed(out)))

    # test opt_s == 'freq'
    inp = ["a", "b", "b", "a", "c", "b"]
    out = ["c", "a", "a", "b", "b", "b"]

    result = runner.invoke(searcher, ['-s', 'freq', '-o', 'asc', '\w+'], input=to_lines(*inp))
    assert check_output(result, out)

    result = runner.invoke(searcher, ['-s', 'freq', '-o', 'desc', '\w+'], input=to_lines(*inp))
    assert check_output(result, list(reversed(out)))


def test_searcher_option_n():
    inp = ["aa", "bb", "cc"]

    result = runner.invoke(searcher, ['-n 2', '\w+'], input=to_lines(*inp))
    assert check_output(result, ["aa", "bb"])

    result = runner.invoke(searcher, ['-n 4', '\w+'], input=to_lines(*inp))
    assert check_output(result, ["aa", "bb", "cc"])

    result = runner.invoke(searcher, ['-n 1.5', '\w+'], input=to_lines(*inp))
    assert result.exit_code == 2


def test_searcher_stat():
    inp = ["a", "b", "b", "a", "c", "b"]

    result = runner.invoke(searcher, ['--stat', 'freq', '\w+'], input=to_lines(*inp))
    assert check_output(result, ["Substr | Frequency",
                                 "a | 0.333",
                                 "b | 0.500",
                                 "c | 0.167"])

    result = runner.invoke(searcher, ['--stat', 'count', '\w+'], input=to_lines(*inp))
    assert check_output(result, ["Substr | Count",
                                 "a | 2",
                                 "b | 3",
                                 "c | 1"])

    result = runner.invoke(searcher, ['-s', 'freq', '--stat', 'count', '\w+'], input=to_lines(*inp))
    assert check_output(result, ["Substr | Count",
                                 "c | 1",
                                 "a | 2",
                                 "b | 3"])

    result = runner.invoke(searcher, ['-s', 'freq', '-o', 'desc', '--stat', 'count', '\w+'], input=to_lines(*inp))
    assert check_output(result, ["Substr | Count",
                                 "b | 3",
                                 "a | 2",
                                 "c | 1"])


if __name__ == '__main__':
    test_searcher_input_stdin()
    test_searcher_input_file()
    test_searcher_flag_u()
    test_searcher_flag_c()
    test_searcher_flag_l()

    test_searcher_sort()
    test_searcher_option_n()
    test_searcher_stat()
