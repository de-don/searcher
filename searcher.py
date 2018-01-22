import click

from Matches import Matches


def get_text(filename):
    '''Get text from stdin or file.'''

    # set stdin by default
    stream = click.get_text_stream('stdin')
    if filename:
        # if file is exists, open file
        stream = click.open_file(filename, 'r')

    return stream.read()


def show_stat(matches, stat):
    max_len = len(max(matches.keys, key=len))
    fmt_title = "{:<%d} | {}" % max_len

    # select title column and n (len array for formula Mi/n)
    if stat == "count":
        fmt = "{:<%d} | {}" % max_len
        click.echo(fmt_title.format("Substr", "Count"))
        for k, v in matches:
            click.echo(fmt.format(k, v))
    else:
        fmt = "{:<%d} | {:.3f}" % max_len
        click.echo(fmt_title.format("Substr", "Frequency"))
        n = matches.count_matches
        for k, v in matches:
            click.echo(fmt.format(k, v / n))


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
@click.option('--stat', 'stat', type=click.Choice(['count', 'freq']),
              help="List unique matches with statistic (count or frequency in percents).")
def searcher(pattern, filename, flag_u, flag_c, flag_l, opt_s, opt_o, opt_n, stat):
    text = get_text(filename)

    matches = Matches(pattern, text)

    if flag_l:
        count = matches.count_lines
        click.echo("Lines with matches: %d" % count)
        return

    # sort
    if opt_s:
        matches.sort(opt_s, opt_o)

    if flag_u:
        matches.unique()

    if flag_c:
        count = matches.count_matches
        click.echo("Total count of matches: %d" % count)
        return

    # show statictics
    if stat:
        show_stat(matches, stat)
        return

    # slice of output
    if opt_n:
        matches.slice(opt_n)

    # List results
    for line in matches.print_items():
        click.echo(line)


if __name__ == '__main__':
    searcher()
