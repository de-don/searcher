from click.testing import CliRunner

from searcher import searcher


def check_output(result, need):
    ''' Function to compare result.output and need array '''
    out = result.output.splitlines()
    return out == need


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


if __name__ == '__main__':
    test_searcher_input_stdin()
    test_searcher_input_file()
