import re
from operator import itemgetter
from collections import Counter

import click


def get_text(filename):
    '''Get text from stdin or file.'''

    # set stdin by default
    stream = click.get_text_stream('stdin')
    if filename:
        # if file is exists, open file
        stream = click.open_file(filename, 'r')

    return stream.read()


def parse(text, pattern):
    result_lines = []

    # Find all matches in each line
    for line in text.splitlines():
        result = re.findall(pattern, line)
        result_lines.append(result)

    return result_lines


def unique(arr):
    ''' Create new array with unique items with save ordering. '''
    s = set()
    add = s.add
    return [x for x in arr if not (x in s or add(x))]


def sort_out(arr, opt_s, opt_o):
    sort_key = itemgetter(int(opt_s == "freq"))
    rev = opt_o == "desc"

    counts = sorted(Counter(arr).items(), key=sort_key, reverse=rev)

    return list(map(itemgetter(0), counts))
    # if need return with repetitions:
    # return sum([[i[0]] * i[1] for i in counts], [])


@click.command()
@click.argument('pattern')
@click.argument('filename', type=click.Path(exists=True), required=False)
@click.option('-u', 'flag_u', is_flag=True, help='List unique matches only.')
@click.option('-c', 'flag_c', is_flag=True, help='Total count of found matches.')
@click.option('-l', 'flag_l', is_flag=True, help='Total count of lines, where at least one match was found.')
@click.option('-s', 'opt_s', type=click.Choice(['freq', 'abc']),
              help='Sorting of found matches by alphabet and frequency (related to all found matches).')
@click.option('-o', 'opt_o', type=click.Choice(['asc', 'desc']), default="asc",
              help="Sorting order can be specified (ascending, descending).")
@click.option('-n', 'opt_n', default=None, help="List first N matches.", type=int)
def searcher(pattern, filename, flag_u, flag_c, flag_l, opt_s, opt_o, opt_n):
    text = get_text(filename)
    find_in_lines = parse(text, pattern)

    if flag_l:
        # calculate count not empty arrays
        count = len(list(filter(None, find_in_lines)))
        click.echo("Lines with matches: %d" % count)
        return

    # convert array with lines to simple array
    out = sum(find_in_lines, [])

    if flag_u:
        out = unique(out)

    if flag_c:
        click.echo("Total count of matches: %d" % len(out))
        return

    # sorting output
    if opt_s:
        out = sort_out(out, opt_s, opt_o)
    
    # slice of output
    if opt_n:
        out = out[:opt_n]

    click.echo("\n".join(out))


if __name__ == '__main__':
    searcher()
