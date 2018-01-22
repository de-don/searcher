from collections import Counter, OrderedDict


class OrderedCounter(Counter, OrderedDict):
    def __repr__(self):
        return '%r(%s)' % (self.__class__.__name__, OrderedDict(self))

    def __reduce__(self):
        return self.__class__, (OrderedDict(self),)