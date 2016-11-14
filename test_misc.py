# encoding: utf8

from quantiphy import Quantity, CONSTANTS
import pytest

def test_misc():
    Quantity.set_preferences(spacer=' ')
    q = Quantity(1420405751.786, 'Hz')
    assert q.render(si=False, units=False) == '1.4204e9'

    t = Quantity('1420405751.786 Hz').as_tuple()
    assert t == (1420405751.786, 'Hz')

    t = Quantity('1420405751.786 Hz').render(si=True, units=True, prec='full')
    assert t == '1.420405751786 GHz'

    s = Quantity('1420405751.786 Hz').render(si=False, units=True, prec='full')
    assert s == '1.420405751786e9 Hz'

    f=float(Quantity('1420405751.786 Hz'))
    assert f == 1420405751.786

    t = Quantity('1420405751.786 Hz').render(si=True, units=False)
    assert t == '1.4204G'

    s = Quantity('1420405751.786 Hz').render(si=False, units=False)
    assert s == '1.4204e9'

    s = Quantity(1420405751.786, 'Hz').render(si=False, units=False, prec='full')
    assert s == '1.420405751786e9'

    f = Quantity('14204.05751786MHz').render(si=True, units=False, prec='full')
    assert f == '14.20405751786G'

    q = Quantity('1420405751.786 Hz', units='HZ').render()
    assert q == '1.4204 GHZ'

    q = Quantity('1420405751.786 Hz')
    assert q.is_nan() == False

    q = Quantity('1420405751.786 Hz')
    assert q.is_infinite() == False

    q = Quantity('NaN Hz')
    assert q.is_nan() == True

    q = Quantity('NaN Hz')
    assert q.is_infinite() == False

    q = Quantity('inf Hz')
    assert q.is_nan() == False

    q = Quantity('inf Hz')
    assert q.is_infinite() == True

    assert repr(q) == "Quantity('inf Hz')"

    with pytest.raises(ValueError):
        class Foo(Quantity):
            pass
        Foo.set_preferences(assign_rec=r'(\w+)\s*=\s*(.*)')
        q = Foo('%')

    with pytest.raises(ValueError):
        q = Quantity('x*y = z')

    with pytest.raises(ValueError):
        Quantity.add_to_namespace('1ns')

    with pytest.raises(ValueError):
        Quantity.add_to_namespace('x*y = z')

    with pytest.raises(ValueError):
        Quantity.add_to_namespace('in = 1mA')

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

    q = Quantity('Tclk = 10ns -- clock period')
    assert q.render(fmt=True) == 'Tclk = 10 ns  # clock period'

    q = Quantity('Tclk = 10ns')
    assert q.render(fmt=True) == 'Tclk = 10 ns'
    assert q.is_close(1e-8) is True
    assert q.is_close(1.001e-8) is False

    CONSTANTS['h_line'] = 'F_hy = 1420405751.786 Hz -- frequency of hydrogen line'
    h_line = Quantity('h_line')
    assert h_line.render(fmt=True) == 'F_hy = 1.4204 GHz  # frequency of hydrogen line'

    h_line2 = Quantity(h_line, h_line)
    assert h_line2.render(fmt=True) == 'F_hy = 1.4204 GHz  # frequency of hydrogen line'

    h_line3 = Quantity(1420405751.786, 'F_hy Hz frequency of hydrogen line')
    assert h_line3.render(fmt=True) == 'F_hy = 1.4204 GHz  # frequency of hydrogen line'

    size = Quantity('100k', 'B')
    assert size.render() == '100 kB'

    f1 = Quantity('1GHz')
    f2 = Quantity('1GOhms')
    assert f1.is_close(f1) == True
    assert f1.is_close(f2) == False
    assert f1.is_close(f1+1) == True
    assert f1.is_close(f1+1e6) == False

    class Foo(Quantity):
        pass
    Foo.set_preferences(render_sf=Foo.render_sf_in_greek)
    t = Foo('1us')
    assert t.render() == '1 μs'

    Foo.set_preferences(render_sf=Quantity.render_sf_in_sci_notation)
    assert t.render(si=False) == '1×10⁻⁶ s'
