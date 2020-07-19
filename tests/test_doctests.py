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
    assert rv.attempted == 27

def test_quantiphy():
    if sys.version_info < (3, 6):
        # code used in doctests assumes python3.6
        return
    Quantity.reset_prefs()
    rv = doctest.testfile('../quantiphy.py', optionflags=doctest.ELLIPSIS)
    assert rv.failed == 0
    assert rv.attempted == 97

def test_manual():
    if sys.version_info < (3, 6):
        # code used in doctests assumes python3.6
        return
    Quantity.reset_prefs()
    files = {
        '../doc/index.rst': 29,
        '../doc/user.rst': 361,
        '../doc/api.rst': 0,
        '../doc/examples.rst': 50,
        '../doc/releases.rst': 0,
    }
    found = glob.glob('../doc/*.rst')
    for f in found:
        assert f in files, f
    for path, tests in files.items():
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
