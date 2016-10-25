# encoding: utf8

from quantiphy import Quantity
import pytest

def test_misc():
    Quantity.set_preferences(spacer=' ')
    q=Quantity(1420405751.786, 'Hz')
    assert q.render(si=False, units=False) == '1.4204e9'

    t=Quantity('1420405751.786 Hz').as_tuple()
    assert t == (1420405751.786, 'Hz')

    t=Quantity('1420405751.786 Hz').render(si=True, units=True, prec='full')
    assert t == '1.420405751786 GHz'

    s=Quantity('1420405751.786 Hz').render(si=False, units=True, prec='full')
    assert s == '1.420405751786e9 Hz'

    f=float(Quantity('1420405751.786 Hz'))
    assert f == 1420405751.786

    t=Quantity('1420405751.786 Hz').render(si=True, units=False)
    assert t == '1.4204G'

    s=Quantity('1420405751.786 Hz').render(si=False, units=False)
    assert s == '1.4204e9'

    s=Quantity(1420405751.786, 'Hz').render(si=False, units=False, prec='full')
    assert s == '1.420405751786e9'

    f=Quantity('14204.05751786MHz').render(si=True, units=False, prec='full')
    assert f == '14.20405751786G'

    q=Quantity('1420405751.786 Hz', units='HZ').render()
    assert q == '1.4204 GHZ'

    q=Quantity('1420405751.786 Hz')
    assert q.is_nan() == False

    q=Quantity('1420405751.786 Hz')
    assert q.is_infinite() == False

    q=Quantity('NaN Hz')
    assert q.is_nan() == True

    q=Quantity('NaN Hz')
    assert q.is_infinite() == False

    q=Quantity('inf Hz')
    assert q.is_nan() == False

    q=Quantity('inf Hz')
    assert q.is_infinite() == True

    assert repr(q) == "Quantity('inf Hz')"

    with pytest.raises(ValueError):
        q=Quantity('x*y = z')

    with pytest.raises(ValueError):
        Quantity.add_to_namespace('1ns')

    with pytest.raises(ValueError):
        Quantity.add_to_namespace('x*y = z')

    with pytest.raises(ValueError):
        Quantity('x\ny = z')

    Quantity.set_preferences(assign_fmt='{x}')
    with pytest.raises(KeyError):
        '{:S}'.format(Quantity('f = 1kHz'))

    Quantity.set_preferences(assign_fmt=('{n} = {v}  # {d}', '{n} = {v}'))
    q1 = Quantity('10ns', name='trise')
    q2 = Quantity('10ns', name='trise', desc='rise time')
    assert '{:G}'.format(q1) == 'trise = 1e-08'
    assert '{:G}'.format(q2) == 'trise = 1e-08  # rise time'

    q3 = Quantity('10cm', name='foo')
    q4 = Quantity('10%', name='bar', desc='buzz')
    assert '{:G}'.format(q3) == 'foo = 0.1'
    assert '{:G}'.format(q4) == 'bar = 0.1  # buzz'

    class Derived(Quantity):
        pass
    Derived.set_preferences(prec=8)
    mu = Derived('mu0')
    assert mu.render() == '1.25663706 uH/m'
    Derived.set_preferences(prec=None)
    assert mu.render() == '1.2566 uH/m'
