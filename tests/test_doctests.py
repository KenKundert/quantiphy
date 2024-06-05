# encoding: utf8

from quantiphy import Quantity
import pytest
import doctest
import glob
import sys


def test_README():
    if sys.version_info < (3, 6):
        # code used in doctests assumes python3.6
        return
    Quantity.reset_prefs()
    rv = doctest.testfile('../README.rst', optionflags=doctest.ELLIPSIS)
    assert rv.failed == 0
    assert rv.attempted == 29

def test_quantiphy():
    if sys.version_info < (3, 6):
        # code used in doctests assumes python3.6
        return
    Quantity.reset_prefs()
    rv = doctest.testfile('../quantiphy/quantiphy.py', optionflags=doctest.ELLIPSIS)
    assert rv.failed == 0
    assert rv.attempted == 132
        # this target should be updated when the number of doctests change

def test_manual():
    if sys.version_info < (3, 6):
        # code used in doctests assumes python3.6
        return
    Quantity.reset_prefs()
    expected_test_count = {
        '../doc/index.rst': 31,
        '../doc/user.rst': 450,
        '../doc/api.rst': 0,
        '../doc/examples.rst': 42,
        '../doc/accessories.rst': 12,
        '../doc/releases.rst': 0,
    }
    found = glob.glob('../doc/*.rst')
    for f in found:
        assert f in expected_test_count, f
    for path, tests in expected_test_count.items():
        rv = doctest.testfile(path, optionflags=doctest.ELLIPSIS)
        assert rv.failed == 0, path
        assert rv.attempted == tests, path

if __name__ == '__main__':
    # As a debugging aid allow the tests to be run on their own, outside pytest.
    # This makes it easier to see and interpret and textual output.

    defined = dict(globals())
    for k, v in defined.items():
        if callable(v) and k.startswith('test_'):
            print()
            print('Calling:', k)
            print((len(k)+9)*'=')
            v()
