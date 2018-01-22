import re
from operator import itemgetter

from OrderedCounter import OrderedCounter


class Matches:
    _l = None  # for -l parameter
    _items = None  # list of pairs (match, count)
    _count = None  # count of all matches

    def __init__(self, pattern, text):
        counter = OrderedCounter()
        self._l = 0

        for line in text.splitlines():
            result = re.findall(pattern, line)

            if result:
                self._l += 1
                counter.update(result)

        self._items = list(counter.items())

    def unique(self):
        self._items = [(k, 1) for k, v in self._items]
        self._count = len(self._items)

    def __iter__(self):
        return iter(self._items)

    def sort(self, s, o):
        ''' Sort by frequency or alphabet. Order can be specified (ascending, descending)

        param s: "freq" or "abc"
        param o: "asc" or "desc"
        '''
        key = itemgetter(int(s == "freq"))
        rev = (o == "desc")

        self._items.sort(key=key, reverse=rev)

    @property
    def count_matches(self):
        if self._count is None:
            self._count = sum(map(itemgetter(1), self._items))
        return self._count

    @property
    def keys(self):
        ''' List of unique matches '''
        return list(map(itemgetter(0), self._items))

    @property
    def count_lines(self):
        return self._l

    def slice(self, n):
        self._items = self._items[:n]

    def print_items(self):
        ''' Generator which returned matches with repetitions '''
        for match, count in self._items:
            for _ in range(count):
                yield match
