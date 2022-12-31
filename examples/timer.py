from timeit import default_timer as timer
from quantiphy import Quantity

class Timer:

    def __init__(self, name='', desc=''):
        self.name = name
        self.desc = desc

    def __enter__(self):
        self.start = timer()
        return self

    def __exit__(self, *args):
        t = timer() - self.start
        self.duration = Quantity(t, units='s', name=self.name, desc=self.desc)

    def __str__(self):
        return str(self.duration)

    def __float__(self):
        return float(self.duration)

s = set('a b c d e f'.split())

with Timer('Tset', 'time required to determine set membership') as t:
    'x' in s
print(str(t))
print(float(t))
print(t.duration.render(show_label='f'))


