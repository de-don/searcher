import re
from collections import Counter
from itertools import repeat, islice
from operator import itemgetter

import click


def get_file_or_stdin_stream(filename=None):
    """ Function to get file stream, if file exists, else get stdin stream.

    Args:
        filename(str): path to file (relative or absolute)

    Returns:
        _io.TextIOWrapper: file or stdin stream

    """

    if filename:
        # if filename is exists, open file and return stream
        return click.open_file(filename, 'r')
    # else return stdin stream by default
    return click.get_text_stream('stdin')


def show_stat(matches, method):
    """ Function to create stat by input array of pairs (key, count).

    Supported two version representation, Frequency(freq) and Count(count).

    Args:
        matches(List[tuple]): list of pairs (key, count)
        method(str): method to calculate second column "freq" or "count".

    Returns:
        str: multiline string with stat.

    """

    max_len = max(map(len, map(itemgetter(0), matches)))
    fmt_title = '{:<%d} | {}' % max_len
    lines = []
    # select title column and n (len array for formula Mi/n)
    if method == 'count':
        fmt_row = '{:<%d} | {}' % max_len
        lines.append(fmt_title.format('Substr', 'Count'))
        for k, v in matches:
            lines.append(fmt_row.format(k, v))

    elif method == 'freq':
        fmt_row = '{:<%d} | {:.3f}' % max_len
        lines.append(fmt_title.format('Substr', 'Frequency'))
        n = sum(map(itemgetter(1), matches))
        for k, v in matches:
            lines.append(fmt_row.format(k, v / n))

    else:
        lines.append(f'Not supported method to calculate statistic: {method}.')

    return '\n'.join(lines)


HELP_TEXTS = {
    'u': 'List unique matches only.',
    'c': 'Total count of found matches.',
    'l': 'Total count of lines, where at least one match was found.',
    's': 'Sorting of found matches by alphabet and frequency '
         '(related to all found matches).',
    'o': 'Sorting order can be specified (ascending, descending).',
    'n': 'List first N matches.',
    'stat': 'List unique matches with statistic count or frequency '
            'in percents).'
}


@click.command()
@click.argument('pattern')
@click.argument(
    'filename',
    type=click.Path(exists=True),
    required=False,
)
@click.option(
    '-u',
    'flag_u',
    is_flag=True,
    help=HELP_TEXTS['u'],
)
@click.option(
    '-c',
    'flag_c',
    is_flag=True,
    help=HELP_TEXTS['c'],
)
@click.option(
    '-l',
    'flag_l',
    is_flag=True,
    help=HELP_TEXTS['l'],
)
@click.option(
    '-s',
    'opt_s',
    type=click.Choice(['freq', 'abc']),
    help=HELP_TEXTS['s'],
)
@click.option(
    '-o',
    'opt_o',
    type=click.Choice(['asc', 'desc']),
    default='asc',
    help=HELP_TEXTS['o'],
)
@click.option(
    '-n',
    'opt_n',
    type=int,
    default=None,
    help=HELP_TEXTS['n'],
)
@click.option(
    '--stat',
    'stat',
    type=click.Choice(['count', 'freq']),
    help=HELP_TEXTS['stat']
)
def searcher(pattern, filename, flag_u, flag_c, flag_l, opt_s, opt_o, opt_n, stat):

    stream = get_file_or_stdin_stream(filename)

    # getting matches and save it's in counter
    matches_counter = Counter()
    lines_with_matches = 0

    for line in stream:
        result = re.findall(pattern, line)
        if result:
            lines_with_matches += 1
            matches_counter.update(result)

    matches = matches_counter.items()
    del matches_counter

    if flag_l:
        click.echo(f'Lines with matches: {lines_with_matches}')
        return

    # sort
    if opt_s:
        key = itemgetter(opt_s == 'freq')
        matches = sorted(matches, key=key, reverse=(opt_o == 'desc'))

    if flag_u:
        matches = ((k, 1) for k, v in matches)

    if flag_c:
        count = sum(map(itemgetter(1), matches))
        click.echo(f'Total count of matches: {count}')
        return

    if stat:
        click.echo(show_stat(matches, stat))
        return

    # List results
    for k, v in islice(matches, opt_n):
        click.echo('\n'.join(repeat(k, v)))


if __name__ == '__main__':
    searcher()
