import re
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


@click.command()
@click.argument('pattern')
@click.argument('filename', type=click.Path(exists=True), required=False)
@click.option('-u', 'flag_u', is_flag=True, help='List unique matches only.')
@click.option('-c', 'flag_c', is_flag=True, help='Total count of found matches.')
def searcher(pattern, filename, flag_u, flag_c):
    text = get_text(filename)
    find_in_lines = parse(text, pattern)

    # convert array with lines to simple array
    out = sum(find_in_lines, [])

    if flag_u:
        out = unique(out)

    if flag_c:
        click.echo("Total count of matches: %d" % len(out))
        return

    click.echo("\n".join(out))


if __name__ == '__main__':
    searcher()
