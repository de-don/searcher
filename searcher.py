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


@click.command()
@click.argument('pattern')
@click.argument('filename', type=click.Path(exists=True), required=False)
def searcher(pattern, filename):
    text = get_text(filename)
    find_in_lines = parse(text, pattern)

    click.echo("\n".join(find_in_lines))


if __name__ == '__main__':
    searcher()
