#!/usr/bin/env python3

from timeit import timeit
from random import random, randint
from quantiphy import Quantity

# preferences
trials = 1_000_000
trials = 100_000
Quantity.set_prefs(
    prec = 2,
    show_label = True,
    label_fmt = '{n:>40}: {v}',
    map_sf = Quantity.map_sf_to_greek
)

# build the raw data, arrays of random numbers
s_numbers = []
s_quantities = []
numbers = []
quantities = []
for i in range(trials):
    mantissa = 20*random()-10
    exponent = randint(-35, 35)
    number = '%0.25fe%s' % (mantissa, exponent)
    quantity = number + ' Hz'
    s_numbers.append(number)
    s_quantities.append(quantity)
    numbers.append(float(number))
    quantities.append(Quantity(number, 'Hz'))

# define testcases
testcases = [
    '[float(v) for v in s_numbers]',
    '[Quantity(v) for v in s_quantities]',
    '[str(v) for v in numbers]',
    '[str(v) for v in quantities]',
]

# run testcases and print results
print('For {} iterations ...'.format(Quantity(trials)))
for case in testcases:
    elapsed = timeit(case, number=1, globals=globals())
    result = Quantity(elapsed/trials, units='s/op', name=case)
    print(result)
