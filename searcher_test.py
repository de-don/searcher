from unittest import TestCase

from click.testing import CliRunner

from searcher import searcher


def split_output(result):
    """ Function to compare result.output and need array """
    return result.output.splitlines()


def to_lines(*args):
    return '\n'.join(args)


class ClickTest(TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def start(self, *args, **kwargs):
        return self.runner.invoke(searcher, *args, **kwargs)

    def test_searcher_input_stdin(self):
        result = self.start(
            ['[\w.\-_]+@[\w.-_]+'],
            input=to_lines('de-don@mail.ru', 'nothing', 'sam@vk.com'),
        )

        self.assertListEqual(
            split_output(result),
            ['de-don@mail.ru', 'sam@vk.com'],
        )
        self.assertEqual(result.exit_code, 0)

    def test_searcher_input_file(self):
        # if file exists
        result = self.start(
            '[\w.\-_]+@[\w.-_]+ emails.txt'.split(),
        )

        self.assertListEqual(
            split_output(result),
            [
                'de-don@mail.ru',
                'de-don2@mail.ru',
                'de-don@inbox.ru',
                'admin_site@google.ru',
            ],
        )
        self.assertEqual(result.exit_code, 0)

        # if file not exists
        result = self.start(
            '\w+ t.txt'.split(),
        )
        self.assertEqual(result.exit_code, 2)

    def test_searcher_flag_u(self):
        result = self.start(
            '\w+ -u'.split(),
            input=to_lines('one', 'two', 'two', 'three', 'one'),
        )
        self.assertListEqual(
            split_output(result),
            ['one', 'two', 'three'],
        )

        result = self.start(
            '\w+ -u'.split(),
            input=to_lines('one', 'two', 'three'),
        )
        self.assertListEqual(
            split_output(result),
            ['one', 'two', 'three'],
        )

    def test_searcher_flag_c(self):
        result = self.start(
            '\w+ -c'.split(),
            input=to_lines('one two', 'three', ''),
        )
        self.assertEqual(result.output, 'Total count of matches: 3\n')

        result = self.start(
            '@\w+ -c'.split(),
            input=to_lines('one two', 'three', ''),
        )
        self.assertEqual(result.output, 'Total count of matches: 0\n')

        result = self.start(
            '\w+ -c -u'.split(),
            input=to_lines('one two', 'three', 'one two', ''),
        )
        self.assertEqual(result.output, 'Total count of matches: 3\n')

    def test_searcher_flag_l(self):
        result = self.start(
            '\w+ -l'.split(),
            input=to_lines('one', 'two', 'three'),
        )
        self.assertEqual(result.output, 'Lines with matches: 3\n')

        result = self.start(
            '\w+ -l'.split(),
            input=to_lines('one', 'two three'),
        )
        self.assertEqual(result.output, 'Lines with matches: 2\n')

    def test_searcher_sort(self):
        # test opt_s == 'abc'
        inp = ['abb', 'bbb', 'aaa', 'ccc']
        out = ['aaa', 'abb', 'bbb', 'ccc']

        result = self.start(
            '\w+ -s abc'.split(),
            input=to_lines(*inp),
        )
        self.assertListEqual(split_output(result), out)

        result = self.start(
            '\w+ -s abc -o asc'.split(),
            input=to_lines(*inp),
        )
        self.assertListEqual(split_output(result), out)

        result = self.start(
            '\w+ -s abc -o desc'.split(),
            input=to_lines(*inp),
        )
        self.assertListEqual(split_output(result), list(reversed(out)))

        # test opt_s == 'freq'
        inp = ['a', 'b', 'b', 'a', 'c', 'b']
        out = ['c', 'a', 'a', 'b', 'b', 'b']

        result = self.start(
            '\w+ -s freq -o asc'.split(),
            input=to_lines(*inp),
        )
        self.assertListEqual(split_output(result), out)

        result = self.start(
            '\w+ -s freq -o desc'.split(),
            input=to_lines(*inp),
        )
        self.assertListEqual(split_output(result), list(reversed(out)))

    def test_searcher_option_n(self):
        inp = ['aa', 'bb', 'cc']

        result = self.start(['-n 2', '\w+'], input=to_lines(*inp))
        self.assertListEqual(split_output(result), ['aa', 'bb'])

        result = self.start(['-n 4', '\w+'], input=to_lines(*inp))
        self.assertListEqual(split_output(result), ['aa', 'bb', 'cc'])

        result = self.start(['-n 1.5', '\w+'], input=to_lines(*inp))
        self.assertEqual(result.exit_code, 2)

    def test_searcher_stat(self):
        inp = ['a', 'b', 'b', 'a', 'c', 'b']

        result = self.start(
            '\w+ --stat freq'.split(),
            input=to_lines(*inp),
        )
        self.assertListEqual(
            split_output(result),
            [
                'Substr | Frequency',
                'a | 0.333',
                'b | 0.500',
                'c | 0.167',
            ],
        )

        result = self.start(
            '\w+ --stat count'.split(),
            input=to_lines(*inp)
        )
        self.assertListEqual(
            split_output(result),
            [
                'Substr | Count',
                'a | 2',
                'b | 3',
                'c | 1',
            ],
        )

        result = self.start(
            '\w+ -s freq --stat count'.split(),
            input=to_lines(*inp),
        )
        self.assertListEqual(
            split_output(result),
            [
                'Substr | Count',
                'c | 1',
                'a | 2',
                'b | 3',
            ],
        )

        result = self.start(
            '\w+ -s freq -o desc --stat count'.split(),
            input=to_lines(*inp),
        )
        self.assertListEqual(
            split_output(result),
            [
                'Substr | Count',
                'b | 3',
                'a | 2',
                'c | 1',
            ],
        )
