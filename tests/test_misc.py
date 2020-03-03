# encoding: utf8

from quantiphy import (
    Quantity, add_constant,
    QuantiPhyError, IncompatibleUnits, UnknownPreference, UnknownConversion,
    UnknownUnitSystem, InvalidRecognizer, UnknownFormatKey, UnknownScaleFactor,
    InvalidNumber, ExpectedQuantity, MissingName,
)
import pytest
import sys
from textwrap import dedent

py3 = int(sys.version[0]) == 3

def test_misc():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None)
    q = Quantity(1420405751.786, 'Hz')
    assert q.render(form='eng', show_units=False) == '1.4204e9'

    t = Quantity('1420405751.786 Hz').as_tuple()
    assert t == (1420405751.786, 'Hz')

    t = Quantity('1420405751.786 Hz').render(form='si', show_units=True, prec='full')
    assert t == '1.420405751786 GHz'

    s = Quantity('1420405751.786 Hz').render(form='eng', show_units=True, prec='full')
    assert s == '1.420405751786e9 Hz'

    f=float(Quantity('1420405751.786 Hz'))
    assert f == 1420405751.786

    t = Quantity('1420405751.786 Hz').render(form='si', show_units=False)
    assert t == '1.4204G'

    s = Quantity('1420405751.786 Hz').render(form='eng', show_units=False)
    assert s == '1.4204e9'

    s = Quantity(1420405751.786, 'Hz').render(form='eng', show_units=False, prec='full')
    assert s == '1.420405751786e9'

    f = Quantity('14204.05751786MHz').render(form='si', show_units=False, prec='full')
    assert f == '14.20405751786G'

    q = Quantity('1420405751.786 Hz', units='HZ').render()
    assert q == '1.4204 GHZ'

    q = Quantity('1420405751.786 Hz')
    assert q.is_nan() is None

    q = Quantity('1420405751.786 Hz')
    assert q.is_infinite() is None

    q = Quantity('NaN Hz')
    assert q.is_nan() == 'NaN'

    q = Quantity('NaN Hz')
    q.nan = 'nan'
    assert q.is_nan() == 'nan'

    q = Quantity('NaN Hz')
    assert q.is_infinite() is None

    q = Quantity('inf Hz')
    assert q.is_nan() is None

    q = Quantity('inf Hz')
    assert q.is_infinite() == 'inf'

    q = Quantity('inf Hz')
    q.inf = '∞'
    assert q.is_infinite() == '∞'

    q = Quantity('∞ Hz')
    assert q.is_infinite() == 'inf'

    q = Quantity('$∞')
    assert q.is_infinite() == 'inf'

    q = Quantity('∞Ω')
    assert q.is_infinite() == 'inf'

    # check the various formats for assignment recognition
    q = Quantity('f_hy = 1420405751.786 Hz -- frequency of hydrogen line')
    assert q.render(show_label='f') == 'f_hy = 1.4204 GHz -- frequency of hydrogen line'
    assert q.name == 'f_hy'
    assert q.desc == 'frequency of hydrogen line'

    q = Quantity('f_hy: 1420405751.786 Hz # frequency of hydrogen line')
    assert q.render(show_label='f') == 'f_hy = 1.4204 GHz -- frequency of hydrogen line'
    assert q.name == 'f_hy'
    assert q.desc == 'frequency of hydrogen line'

    q = Quantity('f_hy = 1420405751.786 Hz // frequency of hydrogen line')
    assert q.render(show_label='f') == 'f_hy = 1.4204 GHz -- frequency of hydrogen line'
    assert q.name == 'f_hy'
    assert q.desc == 'frequency of hydrogen line'

    q = Quantity('f_hy = 1420405751.786 Hz')
    assert q.render(show_label='f') == 'f_hy = 1.4204 GHz'
    assert q.name == 'f_hy'
    assert q.desc == ''

    q = Quantity('1420405751.786 Hz // frequency of hydrogen line')
    assert q.render(show_label='f') == '1.4204 GHz'
    assert q.name == ''
    assert q.desc == 'frequency of hydrogen line'

    q = Quantity('1420405751.786 Hz')
    assert q.render(show_label='f') == '1.4204 GHz'
    assert q.name == ''
    assert q.desc == ''

    if py3:
        # check tight_units
        q = Quantity('90°')
        assert q.render() == '90°'

        q = Quantity('80°F')
        assert q.render() == '80 °F'

        q = Quantity('80°F')
        assert q.render() == '80 °F'
        q.tight_units = '''' % ° ' " ′ ″ °F °C '''.split()
        assert q.render() == '80°F'


def test_misc2():
    class Foo(Quantity):
        pass
    Foo.set_prefs(assign_rec=r'(?P<name>\w+)\s*=\s*(?P<val>.*)')
    q = Foo('seven = 7')
    assert q.name == 'seven'
    assert str(q) == '7'
    with pytest.raises(ValueError) as exception:
        q = Foo('%')
    assert str(exception.value) == '%: not a valid number.'
    assert isinstance(exception.value, InvalidNumber)
    assert isinstance(exception.value, QuantiPhyError)
    assert isinstance(exception.value, ValueError)
    assert exception.value.args == ('%',)
    assert exception.value.render(template='bad number given ({!r})') == "bad number given ('%')"
    assert exception.value.render(template='bad number given') == "%: bad number given"
    # the following is not kosher, but it should work
    exception.value._template = 'bad number ({!r})'
    assert str(exception.value) == "bad number ('%')"
    assert repr(exception.value) == "InvalidNumber('%')"
    with pytest.raises(ValueError):
        exception.value.render(template=['{} {}', '{} {} {}'])
    with pytest.raises(ValueError):
        exception.value.render(template=['{a} {b}', '{a} {b} {c}'])

    with pytest.raises(KeyError) as exception:
        Foo.set_prefs(assign_rec=r'(\w+)\s*=\s*(.*)') # no named groups
        Foo('seven = 7')
    assert str(exception.value) == "recognizer does not contain 'val' key."
    assert isinstance(exception.value, InvalidRecognizer)
    assert isinstance(exception.value, QuantiPhyError)
    assert isinstance(exception.value, KeyError)
    assert exception.value.args == ()

    assert Foo.get_pref('prec') == 4
    assert Foo.get_pref('full_prec') == 12
    with Foo.prefs(prec=5, full_prec=13):
        assert Foo.get_pref('prec') == 5
        assert Foo.get_pref('full_prec') == 13
        with Foo.prefs(prec=6, full_prec=14):
            assert Foo.get_pref('prec') == 6
            assert Foo.get_pref('full_prec') == 14
        assert Foo.get_pref('prec') == 5
        assert Foo.get_pref('full_prec') == 13
    assert Foo.get_pref('prec') == 4
    assert Foo.get_pref('full_prec') == 12

    q = Quantity('1.8_V')
    assert q.render(prec='full') == '1.8 V'

    with pytest.raises(ValueError) as exception:
        q = Quantity('x*y = z')
    assert str(exception.value) == 'z: not a valid number.'
    assert isinstance(exception.value, InvalidNumber)
    assert isinstance(exception.value, QuantiPhyError)
    assert isinstance(exception.value, ValueError)
    assert exception.value.args == ('z',)

    # this used to be an ValueError because 'x*y' is not an identifier
    vals = Quantity.extract('x*y = 1 m/s')
    assert str(vals['x*y']) == '1 m/s'

    # this used to be an ValueError because 'in' is a python keyword
    vals = Quantity.extract('in = 1mA')
    assert str(vals['in']) == '1 mA'

    with pytest.raises(ValueError) as exception:
        Quantity('x\ny = z')
    assert str(exception.value) == 'z: not a valid number.'
    assert isinstance(exception.value, InvalidNumber)
    assert isinstance(exception.value, QuantiPhyError)
    assert isinstance(exception.value, ValueError)
    assert exception.value.args == ('z',)

    Quantity.set_prefs(label_fmt='{x}')
    with pytest.raises(KeyError) as exception:
        '{:S}'.format(Quantity('f = 1kHz'))
    assert str(exception.value) == 'x: unknown format key.'
    assert isinstance(exception.value, UnknownFormatKey)
    assert isinstance(exception.value, QuantiPhyError)
    assert isinstance(exception.value, KeyError)
    assert exception.value.args == ('x',)

    Quantity.set_prefs(label_fmt_full='{n} = {v}  # {d}', label_fmt='{n} = {v}', show_desc=True)
    q1 = Quantity('10ns', name='trise')
    q2 = Quantity('10ns', name='trise', desc='rise time')
    assert '{:G}'.format(q1) == 'trise = 1e-08'
    assert '{:G}'.format(q2) == 'trise = 1e-08  # rise time'

    q3 = Quantity('10cm', name='foo')
    q4 = Quantity('10%', name='bar', desc='buzz')
    assert '{:G}'.format(q3) == 'foo = 0.1'
    assert '{:G}'.format(q4) == 'bar = 10  # buzz'
    assert '{:S}'.format(q4) == 'bar = 10%  # buzz'

    class Derived(Quantity):
        pass
    Derived.set_prefs(prec=8)
    mu = Derived('mu0')
    assert mu.render() == '1.25663706 uH/m'
    Derived.set_prefs(prec=None)
    assert mu.render() == '1.2566 uH/m'

    q = Quantity('Tclk = 10ns -- clock period')
    assert q.render(show_label=True) == 'Tclk = 10 ns  # clock period'

    q = Quantity('Tclk = 10ns')
    assert q.render(show_label=True) == 'Tclk = 10 ns'
    assert q.is_close(1e-8) is True
    assert q.is_close(1.001e-8) is False

    add_constant(Quantity('F_hy = 1420405751.786 Hz -- frequency of hydrogen line'))
    h_line = Quantity('F_hy')
    assert h_line.render(show_label=True) == 'F_hy = 1.4204 GHz  # frequency of hydrogen line'

    h_line2 = Quantity(h_line, h_line)
    assert h_line2.render(show_label=True) == 'F_hy = 1.4204 GHz  # frequency of hydrogen line'

    h_line3 = Quantity(1*h_line, h_line)
    assert h_line3.render(show_label=True) == '1.4204 GHz'

    h_line4 = Quantity(1420405751.786, 'F_hy Hz frequency of hydrogen line')
    assert h_line4.render(show_label=True) == 'F_hy = 1.4204 GHz  # frequency of hydrogen line'

    size = Quantity('100k', 'B')
    assert size.render() == '100 kB'

    f1 = Quantity('1GHz')
    f2 = Quantity('1GOhms')
    assert f1.is_close(f1) is True
    assert f1.is_close(f2) is False
    assert f1.is_close(f1+1) is True
    assert f1.is_close(f1+1e6) is False

    p = Quantity('3_1_4_1.592_65_36mRads')
    assert p.render() == '3.1416 Rads'

    Quantity.set_prefs(known_units='au pc')
    d1 = Quantity('1 au')
    d2 = Quantity('1000 pc')
    assert d1.render(form='eng') == '1 au'
    assert d2.render() == '1 kpc'

    p = Quantity.get_pref(name='known_units')
    assert ' '.join(p) == 'au pc'

    if sys.version_info.major == 3:
        class Foo(Quantity):
            pass
        t = Foo('1us')

        assert Foo.get_pref('map_sf') == {}
        assert Quantity.get_pref('map_sf') == {}

        Foo.set_prefs(map_sf=Foo.map_sf_to_greek)
        assert t.render() == '1 µs'
        assert Foo.get_pref('map_sf') == Foo.map_sf_to_greek
        assert Quantity.get_pref('map_sf') == {}

        Foo.set_prefs(map_sf=Quantity.map_sf_to_sci_notation)
        assert t.render(form='eng') == '1×10⁻⁶ s'
        assert t.render(form='si') == '1 µs'
        assert Foo.get_pref('map_sf') == Foo.map_sf_to_sci_notation
        assert Quantity.get_pref('map_sf') == {}

    Quantity.set_prefs(label_fmt_full='{V:<18}  # {d}', label_fmt='{n} = {v}', show_desc=True)
    T = Quantity('T = 300K -- ambient temperature', ignore_sf=True)
    k = Quantity('k')
    q = Quantity('q')
    Vt = Quantity(k*T/q, 'Vt V thermal voltage')
    result = '{:S}\n{:S}\n{:S}\n{:S}'.format(T, k, q, Vt)
    expected = dedent("""
        T = 300 K           # ambient temperature
        k = 13.806e-24 J/K  # Boltzmann's constant
        q = 160.22e-21 C    # elementary charge
        Vt = 25.852 mV      # thermal voltage
    """).strip()
    assert result == expected

    result = '{:Q}\n{:R}\n{:E}\n{:G}'.format(T, k, q, Vt)
    expected = dedent("""
        T = 300 K           # ambient temperature
        k = 13.806e-24      # Boltzmann's constant
        q = 1.6022e-19      # elementary charge
        Vt = 0.025852       # thermal voltage
    """).strip()
    assert result == expected

    Quantity.set_prefs(label_fmt_full='{V:<18}  # {d}', label_fmt='{n}: {v}', show_desc=True)
    result = '{:S}\n{:S}\n{:S}\n{:S}'.format(T, k, q, Vt)
    expected = dedent("""
        T: 300 K            # ambient temperature
        k: 13.806e-24 J/K   # Boltzmann's constant
        q: 160.22e-21 C     # elementary charge
        Vt: 25.852 mV       # thermal voltage
    """).strip()
    assert result == expected

    processed = Quantity.all_from_conv_fmt('1420405751.786Hz', form='si')
    assert processed == '1.4204 GHz'
    processed = Quantity.all_from_conv_fmt('1.420405751786e9Hz', form='si')
    assert processed == '1.4204 GHz'
    processed = Quantity.all_from_si_fmt('1420.405751786MHz', form='eng')
    assert processed == '1.4204e9 Hz'
    processed = Quantity.all_from_si_fmt('1420405751.786_Hz', form='eng')
    assert processed == '1.4204e9 Hz'

    if sys.version_info.major == 3:
        # spacer is non-breaking space
        processed = Quantity.all_from_conv_fmt('1420405751.786 Hz', form='si')
        assert processed == '1.4204 GHz'

        q = Quantity('3.45e6 m·s⁻²')
        assert q.render() == '3.45 Mm·s⁻²'
        q = Quantity('accel = 3.45e6 m·s⁻² -- acceleration')
        assert q.render() == '3.45 Mm·s⁻²'

    processed = Quantity.all_from_si_fmt('0s', form='si')
    assert processed == '0 s'

    # test input_sf
    Quantity.set_prefs(input_sf='GMk', unity_sf='_', spacer='')
    assert Quantity('10m').render(form='eng') == '10_m'
    Quantity.set_prefs(input_sf=None, unity_sf='_')
    assert Quantity('10m').render(form='eng') == '10e-3'
    with pytest.raises(ValueError) as exception:
        Quantity.set_prefs(input_sf='GMkwq', unity_sf='_', spacer='')
    assert str(exception.value) == 'q, w: unknown scale factors.'
    assert isinstance(exception.value, UnknownScaleFactor)
    assert isinstance(exception.value, QuantiPhyError)
    assert isinstance(exception.value, ValueError)
    assert exception.value.args == ('q', 'w')
    assert repr(exception.value) == "UnknownScaleFactor('q', 'w')"
    exception.value.render('{}, {}: unknown') == 'q, w: unknown'

    Quantity.set_prefs(input_sf=None, unity_sf=None, spacer=None)
    assert Quantity('10m').render(form='eng') == '10e-3'

    Quantity.input_sf = 'GMkwq'
    with pytest.raises(ValueError) as exception:
        Quantity('10m')
    assert str(exception.value) == 'q, w: unknown scale factors.'
    assert isinstance(exception.value, UnknownScaleFactor)
    assert isinstance(exception.value, QuantiPhyError)
    assert isinstance(exception.value, ValueError)
    assert exception.value.args == ('q', 'w')
    assert repr(exception.value) == "UnknownScaleFactor('q', 'w')"
    exception.value.render('{}, {}: unknown') == 'q, w: unknown'

    del Quantity.input_sf

    # test map_sf
    if sys.version_info.major == 3:
        Quantity.set_prefs(map_sf=Quantity.map_sf_to_greek)
        assert Quantity('10e-6 m').render() == '10 µm'
        Quantity.set_prefs(map_sf=Quantity.map_sf_to_sci_notation)
        assert Quantity('10e-6 m').render() == '10 µm'
        assert Quantity('10e-6 m').render(form='eng') == '10×10⁻⁶ m'
        Quantity.set_prefs(map_sf=None)
    sf_map = {
        'u': ' PPM',
        'n': ' PPB',
        'p': ' PPT',
        'f': ' PPQ',
    }
    with Quantity.prefs(map_sf=sf_map):
        assert Quantity('10e-6').render() == '10 PPM'
        assert Quantity('1e-7').render() == '100 PPB'
        assert Quantity('1e-12').render() == '1 PPT'
        assert Quantity('1e-13').render() == '100 PPQ'

    # test set_prefs error handling
    with pytest.raises(KeyError) as exception:
        Quantity.set_prefs(fuzz=True)
    assert exception.value.args[0] == 'fuzz'
    with pytest.raises(KeyError) as exception:
        fuzz = Quantity.get_pref('fuzz')
    assert str(exception.value) == 'fuzz: unknown preference.'
    assert isinstance(exception.value, UnknownPreference)
    assert isinstance(exception.value, QuantiPhyError)
    assert isinstance(exception.value, KeyError)
    assert exception.value.args == ('fuzz',)

    c = Quantity('c')
    Quantity.set_prefs(label_fmt=None, label_fmt_full=None)
    Quantity.set_prefs(show_label=False, show_desc=False)
    assert str(c) == '299.79 Mm/s'
    assert '{:s}'.format(c) == '299.79 Mm/s'
    assert '{:S}'.format(c) == 'c = 299.79 Mm/s'
    assert c.render() == '299.79 Mm/s'
    assert c.render(show_label=False) == '299.79 Mm/s'
    assert c.render(show_label=True) == 'c = 299.79 Mm/s'
    assert c.render(show_label='f') == 'c = 299.79 Mm/s -- speed of light'
    assert c.render(show_label='a') == 'c = 299.79 Mm/s'
    Quantity.set_prefs(show_label=True)
    assert str(c) == 'c = 299.79 Mm/s'
    assert '{:s}'.format(c) == '299.79 Mm/s'
    assert '{:S}'.format(c) == 'c = 299.79 Mm/s'
    assert c.render() == 'c = 299.79 Mm/s'
    assert c.render(show_label=False) == '299.79 Mm/s'
    assert c.render(show_label=True) == 'c = 299.79 Mm/s'
    assert c.render(show_label='f') == 'c = 299.79 Mm/s -- speed of light'
    assert c.render(show_label='a') == 'c = 299.79 Mm/s'
    Quantity.set_prefs(show_label='f')
    assert str(c) == 'c = 299.79 Mm/s -- speed of light'
    assert '{:s}'.format(c) == '299.79 Mm/s'
    assert '{:S}'.format(c) == 'c = 299.79 Mm/s -- speed of light'
    assert c.render() == 'c = 299.79 Mm/s -- speed of light'
    assert c.render(show_label=False) == '299.79 Mm/s'
    assert c.render(show_label=True) == 'c = 299.79 Mm/s -- speed of light'
    assert c.render(show_label='f') == 'c = 299.79 Mm/s -- speed of light'
    assert c.render(show_label='a') == 'c = 299.79 Mm/s'

    Quantity.set_prefs(label_fmt='{n}: {v}', label_fmt_full='{n}: {v} -- {d}')
    Quantity.set_prefs(show_label=False, show_desc=False)
    assert str(c) == '299.79 Mm/s'
    assert '{:s}'.format(c) == '299.79 Mm/s'
    assert '{:S}'.format(c) == 'c: 299.79 Mm/s'
    assert c.render() == '299.79 Mm/s'
    assert c.render(show_label=False) == '299.79 Mm/s'
    assert c.render(show_label=True) == 'c: 299.79 Mm/s'
    assert c.render(show_label='f') == 'c: 299.79 Mm/s -- speed of light'
    assert c.render(show_label='a') == 'c: 299.79 Mm/s'
    Quantity.set_prefs(show_label=True)
    assert str(c) == 'c: 299.79 Mm/s'
    assert '{:s}'.format(c) == '299.79 Mm/s'
    assert '{:S}'.format(c) == 'c: 299.79 Mm/s'
    assert c.render() == 'c: 299.79 Mm/s'
    assert c.render(show_label=False) == '299.79 Mm/s'
    assert c.render(show_label=True) == 'c: 299.79 Mm/s'
    assert c.render(show_label='f') == 'c: 299.79 Mm/s -- speed of light'
    assert c.render(show_label='a') == 'c: 299.79 Mm/s'
    Quantity.set_prefs(show_label='f')
    assert str(c) == 'c: 299.79 Mm/s -- speed of light'
    assert '{:s}'.format(c) == '299.79 Mm/s'
    assert '{:S}'.format(c) == 'c: 299.79 Mm/s -- speed of light'
    assert c.render() == 'c: 299.79 Mm/s -- speed of light'
    assert c.render(show_label=False) == '299.79 Mm/s'
    assert c.render(show_label=True) == 'c: 299.79 Mm/s -- speed of light'
    assert c.render(show_label='f') == 'c: 299.79 Mm/s -- speed of light'
    assert c.render(show_label='a') == 'c: 299.79 Mm/s'

    Quantity.set_prefs(label_fmt='{n}: {v}', label_fmt_full='{V} // {d}')
    Quantity.set_prefs(show_label=False, show_desc=True)
    assert str(c) == '299.79 Mm/s'
    assert '{:s}'.format(c) == '299.79 Mm/s'
    assert '{:S}'.format(c) == 'c: 299.79 Mm/s // speed of light'
    assert c.render() == '299.79 Mm/s'
    assert c.render(show_label=False) == '299.79 Mm/s'
    assert c.render(show_label=True) == 'c: 299.79 Mm/s // speed of light'
    assert c.render(show_label='f') == 'c: 299.79 Mm/s // speed of light'
    assert c.render(show_label='a') == 'c: 299.79 Mm/s'
    Quantity.set_prefs(show_label=True)
    assert str(c) == 'c: 299.79 Mm/s // speed of light'
    assert '{:s}'.format(c) == '299.79 Mm/s'
    assert '{:S}'.format(c) == 'c: 299.79 Mm/s // speed of light'
    assert c.render() == 'c: 299.79 Mm/s // speed of light'
    assert c.render(show_label=False) == '299.79 Mm/s'
    assert c.render(show_label=True) == 'c: 299.79 Mm/s // speed of light'
    assert c.render(show_label='f') == 'c: 299.79 Mm/s // speed of light'
    assert c.render(show_label='a') == 'c: 299.79 Mm/s'
    Quantity.set_prefs(show_label='f')
    assert str(c) == 'c: 299.79 Mm/s // speed of light'
    assert '{:s}'.format(c) == '299.79 Mm/s'
    assert '{:S}'.format(c) == 'c: 299.79 Mm/s // speed of light'
    assert c.render() == 'c: 299.79 Mm/s // speed of light'
    assert c.render(show_label=False) == '299.79 Mm/s'
    assert c.render(show_label=True) == 'c: 299.79 Mm/s // speed of light'
    assert c.render(show_label='f') == 'c: 299.79 Mm/s // speed of light'
    assert c.render(show_label='a') == 'c: 299.79 Mm/s'


def test_converters():
    mvi_raw_conv = '''
Status @ 0.00000000e+00s: Tests started for mylib.sh:MiM.
    Assertion successfully detects expected fault @ 1.00013334e-04s in sh_tb.REF (sh): 'V(cm)' out of range.
    Assertion successfully detects expected fault @ 1.00123334e-04s in sh_tb.REF (sh): 'V(cm)' out of range.
Status @ 2.00500000e-04s: in_val = 5.000000e-01.
    Pass @ 3.00500000e-04s: V(out) voltage: expected=2.00000000e+00V, measured=1.99999965e+00V, diff=3.46117130e-07V.
Status @ 3.00500000e-04s: in_val = 7.500000e-01.
    Pass @ 4.00500000e-04s: V(out) voltage: expected=1.75000000e+00V, measured=1.74999966e+00V, diff=3.41027651e-07V.
Status @ 4.00500000e-04s: in_val = 1.000000e+00.
    Pass @ 5.00500000e-04s: V(out) voltage: expected=1.50000000e+00V, measured=1.49999944e+00V, diff=5.55270307e-07V.
Status @ 5.00500000e-04s: in_val = 1.250000e+00.
    Pass @ 6.00500000e-04s: V(out) voltage: expected=1.25000000e+00V, measured=1.25000000e+00V, diff=1.26565425e-14V.
Status @ 6.00500000e-04s: in_val = 1.500000e+00.
    Pass @ 7.00500000e-04s: V(out) voltage: expected=1.00000000e+00V, measured=9.99999924e-01V, diff=7.59200380e-08V.
Status @ 7.00500000e-04s: in_val = 1.750000e+00.
    Pass @ 8.00500000e-04s: V(out) voltage: expected=7.50000000e-01V, measured=7.50017054e-01V, diff=1.70539238e-05V.
Status @ 8.00500000e-04s: in_val = 2.000000e+00.
    FAIL @ 9.00500000e-04s: V(out) voltage: expected=5.00000000e-01V, measured=5.48562457e-01V, diff=4.85624570e-02V.
Summary @ 9.00510000e-04s: 7 tests run, 1 failures detected, 0 faults detected, 0 test sequences skipped.
    '''

    mvi_raw_si = '''
Status @ 0s: Tests started for mylib.sh:MiM.
    Assertion successfully detects expected fault @ 100.013334us in sh_tb.REF (sh): 'V(cm)' out of range.
    Assertion successfully detects expected fault @ 100.123334us in sh_tb.REF (sh): 'V(cm)' out of range.
Status @ 200.5us: in_val = 500m.
    Pass @ 300.5us: V(out) voltage: expected=2V, measured=1.99999965V, diff=346.11713nV.
Status @ 300.5us: in_val = 750m.
    Pass @ 400.5us: V(out) voltage: expected=1.75V, measured=1.74999966V, diff=341.027651nV.
Status @ 400.5us: in_val = 1.
    Pass @ 500.5us: V(out) voltage: expected=1.5V, measured=1.49999944V, diff=555.270307nV.
Status @ 500.5us: in_val = 1.25.
    Pass @ 600.5us: V(out) voltage: expected=1.25V, measured=1.25V, diff=12.6565425fV.
Status @ 600.5us: in_val = 1.5.
    Pass @ 700.5us: V(out) voltage: expected=1V, measured=999.999924mV, diff=75.920038nV.
Status @ 700.5us: in_val = 1.75.
    Pass @ 800.5us: V(out) voltage: expected=750mV, measured=750.017054mV, diff=17.0539238uV.
Status @ 800.5us: in_val = 2.
    FAIL @ 900.5us: V(out) voltage: expected=500mV, measured=548.562457mV, diff=48.562457mV.
Summary @ 900.51us: 7 tests run, 1 failures detected, 0 faults detected, 0 test sequences skipped.
    '''

    mvi_conv = '''
Status @ 0 s: Tests started for mylib.sh:MiM.
    Assertion successfully detects expected fault @ 100.01e-6 s in sh_tb.REF (sh): 'V(cm)' out of range.
    Assertion successfully detects expected fault @ 100.12e-6 s in sh_tb.REF (sh): 'V(cm)' out of range.
Status @ 200.5e-6 s: in_val = 500e-3.
    Pass @ 300.5e-6 s: V(out) voltage: expected=2 V, measured=2 V, diff=346.12e-9 V.
Status @ 300.5e-6 s: in_val = 750e-3.
    Pass @ 400.5e-6 s: V(out) voltage: expected=1.75 V, measured=1.75 V, diff=341.03e-9 V.
Status @ 400.5e-6 s: in_val = 1.
    Pass @ 500.5e-6 s: V(out) voltage: expected=1.5 V, measured=1.5 V, diff=555.27e-9 V.
Status @ 500.5e-6 s: in_val = 1.25.
    Pass @ 600.5e-6 s: V(out) voltage: expected=1.25 V, measured=1.25 V, diff=12.657e-15 V.
Status @ 600.5e-6 s: in_val = 1.5.
    Pass @ 700.5e-6 s: V(out) voltage: expected=1 V, measured=1 V, diff=75.92e-9 V.
Status @ 700.5e-6 s: in_val = 1.75.
    Pass @ 800.5e-6 s: V(out) voltage: expected=750e-3 V, measured=750.02e-3 V, diff=17.054e-6 V.
Status @ 800.5e-6 s: in_val = 2.
    FAIL @ 900.5e-6 s: V(out) voltage: expected=500e-3 V, measured=548.56e-3 V, diff=48.562e-3 V.
Summary @ 900.51e-6 s: 7 tests run, 1 failures detected, 0 faults detected, 0 test sequences skipped.
    '''

    mvi_conv_full = '''
Status @ 0 s: Tests started for mylib.sh:MiM.
    Assertion successfully detects expected fault @ 100.013334e-6 s in sh_tb.REF (sh): 'V(cm)' out of range.
    Assertion successfully detects expected fault @ 100.123334e-6 s in sh_tb.REF (sh): 'V(cm)' out of range.
Status @ 200.5e-6 s: in_val = 500e-3.
    Pass @ 300.5e-6 s: V(out) voltage: expected=2 V, measured=1.99999965 V, diff=346.11713e-9 V.
Status @ 300.5e-6 s: in_val = 750e-3.
    Pass @ 400.5e-6 s: V(out) voltage: expected=1.75 V, measured=1.74999966 V, diff=341.027651e-9 V.
Status @ 400.5e-6 s: in_val = 1.
    Pass @ 500.5e-6 s: V(out) voltage: expected=1.5 V, measured=1.49999944 V, diff=555.270307e-9 V.
Status @ 500.5e-6 s: in_val = 1.25.
    Pass @ 600.5e-6 s: V(out) voltage: expected=1.25 V, measured=1.25 V, diff=12.6565425e-15 V.
Status @ 600.5e-6 s: in_val = 1.5.
    Pass @ 700.5e-6 s: V(out) voltage: expected=1 V, measured=999.999924e-3 V, diff=75.920038e-9 V.
Status @ 700.5e-6 s: in_val = 1.75.
    Pass @ 800.5e-6 s: V(out) voltage: expected=750e-3 V, measured=750.017054e-3 V, diff=17.0539238e-6 V.
Status @ 800.5e-6 s: in_val = 2.
    FAIL @ 900.5e-6 s: V(out) voltage: expected=500e-3 V, measured=548.562457e-3 V, diff=48.562457e-3 V.
Summary @ 900.51e-6 s: 7 tests run, 1 failures detected, 0 faults detected, 0 test sequences skipped.
    '''

    mvi_si = '''
Status @ 0 s: Tests started for mylib.sh:MiM.
    Assertion successfully detects expected fault @ 100.01 us in sh_tb.REF (sh): 'V(cm)' out of range.
    Assertion successfully detects expected fault @ 100.12 us in sh_tb.REF (sh): 'V(cm)' out of range.
Status @ 200.5 us: in_val = 500m.
    Pass @ 300.5 us: V(out) voltage: expected=2 V, measured=2 V, diff=346.12 nV.
Status @ 300.5 us: in_val = 750m.
    Pass @ 400.5 us: V(out) voltage: expected=1.75 V, measured=1.75 V, diff=341.03 nV.
Status @ 400.5 us: in_val = 1.
    Pass @ 500.5 us: V(out) voltage: expected=1.5 V, measured=1.5 V, diff=555.27 nV.
Status @ 500.5 us: in_val = 1.25.
    Pass @ 600.5 us: V(out) voltage: expected=1.25 V, measured=1.25 V, diff=12.657 fV.
Status @ 600.5 us: in_val = 1.5.
    Pass @ 700.5 us: V(out) voltage: expected=1 V, measured=1 V, diff=75.92 nV.
Status @ 700.5 us: in_val = 1.75.
    Pass @ 800.5 us: V(out) voltage: expected=750 mV, measured=750.02 mV, diff=17.054 uV.
Status @ 800.5 us: in_val = 2.
    FAIL @ 900.5 us: V(out) voltage: expected=500 mV, measured=548.56 mV, diff=48.562 mV.
Summary @ 900.51 us: 7 tests run, 1 failures detected, 0 faults detected, 0 test sequences skipped.
    '''

    mvi_si_full = '''
Status @ 0 s: Tests started for mylib.sh:MiM.
    Assertion successfully detects expected fault @ 100.013334 us in sh_tb.REF (sh): 'V(cm)' out of range.
    Assertion successfully detects expected fault @ 100.123334 us in sh_tb.REF (sh): 'V(cm)' out of range.
Status @ 200.5 us: in_val = 500m.
    Pass @ 300.5 us: V(out) voltage: expected=2 V, measured=1.99999965 V, diff=346.11713 nV.
Status @ 300.5 us: in_val = 750m.
    Pass @ 400.5 us: V(out) voltage: expected=1.75 V, measured=1.74999966 V, diff=341.027651 nV.
Status @ 400.5 us: in_val = 1.
    Pass @ 500.5 us: V(out) voltage: expected=1.5 V, measured=1.49999944 V, diff=555.270307 nV.
Status @ 500.5 us: in_val = 1.25.
    Pass @ 600.5 us: V(out) voltage: expected=1.25 V, measured=1.25 V, diff=12.6565425 fV.
Status @ 600.5 us: in_val = 1.5.
    Pass @ 700.5 us: V(out) voltage: expected=1 V, measured=999.999924 mV, diff=75.920038 nV.
Status @ 700.5 us: in_val = 1.75.
    Pass @ 800.5 us: V(out) voltage: expected=750 mV, measured=750.017054 mV, diff=17.0539238 uV.
Status @ 800.5 us: in_val = 2.
    FAIL @ 900.5 us: V(out) voltage: expected=500 mV, measured=548.562457 mV, diff=48.562457 mV.
Summary @ 900.51 us: 7 tests run, 1 failures detected, 0 faults detected, 0 test sequences skipped.
    '''

    processed = Quantity.all_from_conv_fmt(mvi_raw_conv, form='si')
    assert processed == mvi_si
    processed = Quantity.all_from_conv_fmt(mvi_raw_conv, form='eng')
    assert processed == mvi_conv
    processed = Quantity.all_from_conv_fmt(mvi_raw_conv, form='si', prec='full')
    assert processed == mvi_si_full
    processed = Quantity.all_from_conv_fmt(mvi_raw_conv, form='eng', prec='full')
    assert processed == mvi_conv_full

    processed = Quantity.all_from_si_fmt(mvi_raw_si, form='si')
    assert processed == mvi_si
    processed = Quantity.all_from_si_fmt(mvi_raw_si, form='eng')
    assert processed == mvi_conv
    processed = Quantity.all_from_si_fmt(mvi_raw_si, form='si', prec='full')
    assert processed == mvi_si_full
    processed = Quantity.all_from_si_fmt(mvi_raw_si, form='eng', prec='full')
    assert processed == mvi_conv_full

    processed = Quantity.all_from_si_fmt('1420.40575MHz+1420.40575MHz+1420.40575MHz', form='si')
    assert processed == '1.4204 GHz+1.4204 GHz+1.4204 GHz'

    processed = Quantity.all_from_si_fmt('1420.40575MHz+abc+1420.40575MHz+abc+1420.40575MHz', form='si')
    assert processed == '1.4204 GHz+abc+1.4204 GHz+abc+1.4204 GHz'

    processed = Quantity.all_from_si_fmt('1420.40575e+6+1420.40575e+6', form='si')
    assert processed == '1420.40575e+6+1420.40575e+6'


def test_add():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None)
    q1 = Quantity('1ns')
    q2 = Quantity('2ns')
    assert str(q1.add(q2)) == '3 ns'
    assert repr(q1.add(q2)) == "Quantity('3 ns')"
    assert str(q2.add(q1)) == '3 ns'
    assert repr(q2.add(q1)) == "Quantity('3 ns')"
    assert str(q1.add(q2, check_units=False)) == '3 ns'
    assert str(q1.add(q2, check_units=True)) == '3 ns'
    assert str(q1.add(q2, check_units='strict')) == '3 ns'
    assert str(q1.add(2e-9, check_units=False)) == '3 ns'
    assert str(q1.add(2e-9, check_units=True)) == '3 ns'
    with pytest.raises(TypeError) as exception:
        q1.add(2e-9, check_units='strict')
    q3 = Quantity('2nm')
    assert str(q1.add(q3, check_units=False)) == '3 ns'
    with pytest.raises(TypeError) as exception:
        q1.add(q3, check_units=True)
    with pytest.raises(TypeError) as exception:
        q1.add(q3, check_units='strict')

    q1.name = 'period'
    assert q1.add(q2).name == 'period'
    q1.desc = 'duration of one cycle'
    assert q1.add(q2).name == 'period'
    assert q1.add(q2).desc == 'duration of one cycle'

    class Dollars(Quantity):
        units = '$'
        prec = 2
        form = 'fixed'
        show_commas = True
        if sys.version_info.major == 3:
            minus = Quantity.minus_sign
        strip_zeros = False

    total = Dollars(0)
    assert str(total) == '$0.00'
    total = total.add(1000000)
    assert str(total) == '$1,000,000.00'
    total = total.add(Quantity('-2MHz'), check_units=False)
    if sys.version_info.major == 3:
        assert str(total) == '−$1,000,000.00'
    else:
        assert str(total) == '-$1,000,000.00'
    with pytest.raises(IncompatibleUnits) as exception:
        total.add(Quantity('-2MHz'), check_units=True)
    total = total.add(Quantity('$6M'), check_units=True)
    assert str(total) == '$5,000,000.00'

    class WholeDollars(Dollars):
        prec = 0

    total = WholeDollars(0)
    total.name = 'total'
    assert str(total) == '$0'
    total = total.add(1000000)
    assert str(total) == '$1,000,000'
    assert total.name == 'total'
    total = total.add(Quantity('-2MHz'), check_units=False)
    if sys.version_info.major == 3:
        assert str(total) == '−$1,000,000'
    else:
        assert str(total) == '-$1,000,000'
    assert total.name == 'total'
    with pytest.raises(IncompatibleUnits) as exception:
        total.add(Quantity('-2MHz'), check_units=True)
    total = total.add(Quantity('$6M'), check_units=True)
    assert str(total) == '$5,000,000'
    assert total.name == 'total'

def test_scale():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None)
    q1 = Quantity('3ns')
    q2 = Quantity('2')
    v2 = 2
    assert str(q1.scale(q2)) == '6 ns'
    assert repr(q1.scale(q2)) == "Quantity('6 ns')"
    assert str(q1.scale(v2)) == '6 ns'
    assert repr(q1.scale(v2)) == "Quantity('6 ns')"

    q1.name = 'period'
    q3 = q1.scale(q2).name == 'period'
    q1.desc = 'duration of one cycle'
    assert q1.scale(q2).name == 'period'
    assert q1.scale(q2).desc == 'duration of one cycle'

    class Dollars(Quantity):
        units = '$'
        prec = 2
        form = 'fixed'
        show_commas = True
        minus = Quantity.minus_sign
        strip_zeros = False

    total = Dollars(1)
    assert str(total) == '$1.00'
    total = total.scale(1000000)
    assert str(total) == '$1,000,000.00'

    class WholeDollars(Dollars):
        prec = 0

    total = WholeDollars(1)
    assert str(total) == '$1'
    total = total.scale(1000000)
    assert str(total) == '$1,000,000'
    total = total.scale(5, Dollars)
    assert str(total) == '$5,000,000.00'

def test_negligible():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None)
    pn=Quantity('1nV')
    nn=Quantity('-1nV')
    pf=Quantity('1fV')
    nf=Quantity('-1fV')
    assert pn.render() == '1 nV'
    assert nn.render() == '-1 nV'
    assert pf.render() == '1 fV'
    assert nf.render() == '-1 fV'
    assert pn.render(negligible=1e-12) == '1 nV'
    assert nn.render(negligible=1e-12) == '-1 nV'
    assert pf.render(negligible=1e-12) == '0 V'
    assert nf.render(negligible=1e-12) == '0 V'
    with Quantity.prefs(negligible=1e-12):
        assert pn.render() == '1 nV'
        assert nn.render() == '-1 nV'
        assert pf.render() == '0 V'
        assert nf.render() == '0 V'
        assert repr(pn) == "Quantity('1 nV')"
        assert repr(nn) == "Quantity('-1 nV')"
        assert repr(pf) == "Quantity('1 fV')"
        assert repr(nf) == "Quantity('-1 fV')"
        assert pn.render(negligible=1e-6) == '0 V'
        assert nn.render(negligible=1e-6) == '0 V'
        assert pf.render(negligible=1e-6) == '0 V'
        assert nf.render(negligible=1e-6) == '0 V'

    q=Quantity('-0')
    assert q.render() == '-0'
    assert q.render(negligible=0) == '0'

    v=Quantity('1nV')
    c=Quantity('1fA')
    f=Quantity('1mHz')
    k=Quantity('k')
    u=Quantity(1e-9)
    with Quantity.prefs():
        assert v.render() == '1 nV'
        assert c.render() == '1 fA'
        assert f.render() == '1 mHz'
        assert u.render() == '1n'
        assert k.render() == '13.806e-24 J/K'
    with Quantity.prefs(negligible = 1e-6):
        assert v.render() == '0 V'
        assert c.render() == '0 A'
        assert f.render() == '1 mHz'
        assert u.render() == '0'
        assert k.render() == '0 J/K'
    with Quantity.prefs(negligible = dict(V=1e-6, A=1e-12, Hz=1)):
        assert v.render() == '0 V'
        assert c.render() == '0 A'
        assert f.render() == '0 Hz'
        assert u.render() == '1n'
        assert k.render() == '13.806e-24 J/K'
    with Quantity.prefs(negligible = {'V':1e-6, 'A':1e-12, 'Hz':1, None:1e-12}):
        assert v.render() == '0 V'
        assert c.render() == '0 A'
        assert f.render() == '0 Hz'
        assert u.render() == '1n'
        assert k.render() == '0 J/K'
    with Quantity.prefs(negligible = {'V':1e-6, 'A':1e-12, 'Hz':1, None:1e-6}):
        assert v.render() == '0 V'
        assert c.render() == '0 A'
        assert f.render() == '0 Hz'
        assert u.render() == '0'
        assert k.render() == '0 J/K'
    with Quantity.prefs(negligible = {'V':1e-6, 'A':1e-12, 'Hz':1, '':1e-10, None:1e-12}):
        assert v.render() == '0 V'
        assert c.render() == '0 A'
        assert f.render() == '0 Hz'
        assert u.render() == '1n'
        assert k.render() == '0 J/K'
    with Quantity.prefs(negligible = {'V':1e-6, 'A':1e-12, 'Hz':1, '':1e-6, None:1e-12}):
        assert v.render() == '0 V'
        assert c.render() == '0 A'
        assert f.render() == '0 Hz'
        assert u.render() == '0'
        assert k.render() == '0 J/K'

    given = 'Pass @ 3.40000006e-03s: V(atb) voltage: expected=0.00000000e+00V, measured=-8.60793065e-76V, diff=8.60793065e-76V.'
    expected = 'Pass @ 3.4 ms: V(atb) voltage: expected=0 V, measured=-860.79e-78 V, diff=860.79e-78 V.'
    got = Quantity.all_from_conv_fmt(given)
    assert got == expected

    expected = 'Pass @ 3.4 ms: V(atb) voltage: expected=0 V, measured=0 V, diff=0 V.'
    got = Quantity.all_from_conv_fmt(given, negligible=1e-12)
    assert got == expected


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
