# encoding: utf8

from quantiphy import Quantity
import pytest
import sys

def test_format():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None, show_desc=False)
    q=Quantity('f = 1420.405751786 MHz -- frequency of hydrogen line')
    assert '{}'.format(q) == '1.4204 GHz'
    assert '{:.8}'.format(q) == '1.42040575 GHz'
    assert '{:.8s}'.format(q) == '1.42040575 GHz'
    assert '{:.8S}'.format(q) == 'f = 1.42040575 GHz'
    assert '{:.8q}'.format(q) == '1.42040575 GHz'
    assert '{:.8Q}'.format(q) == 'f = 1.42040575 GHz'
    assert '{:r}'.format(q) == '1.4204G'
    assert '{:R}'.format(q) == 'f = 1.4204G'
    assert '{:u}'.format(q) == 'Hz'
    assert '{:f}'.format(q) == '1420405751.786'
    assert '{:F}'.format(q) == 'f = 1420405751.786'
    assert '{:e}'.format(q) == '1.4204e+09'
    assert '{:E}'.format(q) == 'f = 1.4204e+09'
    assert '{:g}'.format(q) == '1.4204e+09'
    assert '{:G}'.format(q) == 'f = 1.4204e+09'
    assert '{:n}'.format(q) == 'f'
    assert '{:d}'.format(q) == 'frequency of hydrogen line'
    assert '{:p}'.format(q) == '1420405751.786 Hz'
    assert '{:,p}'.format(q) == '1,420,405,751.786 Hz'
    assert '{:P}'.format(q) == 'f = 1420405751.786 Hz'
    assert '{:,P}'.format(q) == 'f = 1,420,405,751.786 Hz'
    assert '{:#.3q}'.format(q) == '1.420 GHz'
    assert '{:#p}'.format(q) == '1420405751.7860 Hz'
    assert '{:.0q}'.format(q) == '1 GHz'
    assert '{:.0p}'.format(q) == '1420405752 Hz'
    assert '{:#.0q}'.format(q) == '1 GHz'
    assert '{:#.0p}'.format(q) == '1420405752. Hz'

    q=Quantity('2ns')
    assert float(q) == 2e-9

    with pytest.raises(ValueError) as exception:
        q = Quantity('1ns')
        '{:z}'.format(q)
    assert exception.value.args[0] == "Unknown format code 'z' for object of type 'float'"

def test_full_format():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None, show_desc=False)
    Quantity.set_prefs(prec='full')
    q=Quantity('f = 1420.405751786 MHz -- frequency of hydrogen line')
    assert '{}'.format(q) == '1.420405751786 GHz'
    assert '{:.8}'.format(q) == '1.42040575 GHz'
    assert '{:.8s}'.format(q) == '1.42040575 GHz'
    assert '{:.8S}'.format(q) == 'f = 1.42040575 GHz'
    assert '{:.8q}'.format(q) == '1.42040575 GHz'
    assert '{:.8Q}'.format(q) == 'f = 1.42040575 GHz'
    assert '{:r}'.format(q) == '1.420405751786G'
    assert '{:R}'.format(q) == 'f = 1.420405751786G'
    assert '{:u}'.format(q) == 'Hz'
    assert '{:.4f}'.format(q) == '1420405751.786'
    assert '{:.4F}'.format(q) == 'f = 1420405751.786'
    assert '{:e}'.format(q) == '1.420405751786e+09'
    assert '{:E}'.format(q) == 'f = 1.420405751786e+09'
    assert '{:g}'.format(q) == '1420405751.786'
    assert '{:G}'.format(q) == 'f = 1420405751.786'
    assert '{:n}'.format(q) == 'f'
    assert '{:d}'.format(q) == 'frequency of hydrogen line'
    assert '{:.2p}'.format(q) == '1420405751.79 Hz'
    assert '{:,.2p}'.format(q) == '1,420,405,751.79 Hz'
    assert '{:.2P}'.format(q) == 'f = 1420405751.79 Hz'
    assert '{:,.2P}'.format(q) == 'f = 1,420,405,751.79 Hz'
    assert '{:#.3q}'.format(q) == '1.420 GHz'
    assert '{:#.6p}'.format(q) == '1420405751.786000 Hz'
    assert '{:.0q}'.format(q) == '1 GHz'
    assert '{:.0p}'.format(q) == '1420405752 Hz'
    assert '{:#.0q}'.format(q) == '1 GHz'
    assert '{:#.0p}'.format(q) == '1420405752. Hz'

    q=Quantity('2ns')
    assert float(q) == 2e-9

def test_width():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None, show_desc=False)
    Quantity.set_prefs(prec='full')
    q=Quantity('f = 1420.405751786 MHz -- frequency of hydrogen line')
    assert '{:25}'.format(q) == '       1.420405751786 GHz'
    assert '{:>25.8}'.format(q) == '           1.42040575 GHz'
    assert '{:25.8s}'.format(q) == '           1.42040575 GHz'
    assert '{:<25.8s}'.format(q) == '1.42040575 GHz           '
    assert '{:^25.8S}'.format(q) == '   f = 1.42040575 GHz    '
    assert '{:25.8q}'.format(q) == '           1.42040575 GHz'
    assert '{:>25.8Q}'.format(q) == '       f = 1.42040575 GHz'
    assert '{:<25r}'.format(q) == '1.420405751786G          '
    assert '{:^25R}'.format(q) == '   f = 1.420405751786G   '
    assert '{:25u}'.format(q) == 'Hz                       '
    assert '{:>25.4f}'.format(q) == '           1420405751.786'
    assert '{:<25.4F}'.format(q) == 'f = 1420405751.786       '
    assert '{:^25e}'.format(q) == '   1.420405751786e+09    '
    assert '{:25E}'.format(q) == '   f = 1.420405751786e+09'
    assert '{:>25g}'.format(q) == '           1420405751.786'
    assert '{:<25G}'.format(q) == 'f = 1420405751.786       '
    assert '{:^25n}'.format(q) == '            f            '
    assert '{:30d}'.format(q) == 'frequency of hydrogen line    '
    assert '{:>25.2p}'.format(q) == '         1420405751.79 Hz'
    assert '{:<25,.2p}'.format(q) == '1,420,405,751.79 Hz      '
    assert '{:^25.2P}'.format(q) == '  f = 1420405751.79 Hz   '
    assert '{:25,.2P}'.format(q) == '  f = 1,420,405,751.79 Hz'
    assert '{:#25.3q}'.format(q) == '                1.420 GHz'
    assert '{:#25.6p}'.format(q) == '     1420405751.786000 Hz'
    assert '{:25.0q}'.format(q) == '                    1 GHz'
    assert '{:25.0p}'.format(q) == '            1420405752 Hz'
    assert '{:#25.0q}'.format(q) == '                    1 GHz'
    assert '{:#25.0p}'.format(q) == '           1420405752. Hz'

def test_currency():
    Quantity.set_prefs(
        spacer = None,
        show_label = None,
        label_fmt = None,
        label_fmt_full = None,
        show_desc = False,
        prec = 4,
    )
    q=Quantity('Total = $1000k -- a large amount of money')
    assert '{}'.format(q) == '$1M'
    assert '{:.8}'.format(q) == '$1M'
    assert '{:.8s}'.format(q) == '$1M'
    assert '{:.8S}'.format(q) == 'Total = $1M'
    assert '{:.8q}'.format(q) == '$1M'
    assert '{:.8Q}'.format(q) == 'Total = $1M'
    assert '{:r}'.format(q) == '1M'
    assert '{:R}'.format(q) == 'Total = 1M'
    assert '{:u}'.format(q) == '$'
    assert '{:.4f}'.format(q) == '1000000'
    assert '{:.4F}'.format(q) == 'Total = 1000000'
    assert '{:e}'.format(q) == '1e+06'
    assert '{:E}'.format(q) == 'Total = 1e+06'
    assert '{:g}'.format(q) == '1e+06'
    assert '{:G}'.format(q) == 'Total = 1e+06'
    assert '{:n}'.format(q) == 'Total'
    assert '{:d}'.format(q) == 'a large amount of money'
    assert '{:#p}'.format(q) == '$1000000.0000'
    assert '{:#.2p}'.format(q) == '$1000000.00'
    assert '{:#,.2p}'.format(q) == '$1,000,000.00'
    assert '{:#,P}'.format(q) == 'Total = $1,000,000.0000'
    assert '{:#.2P}'.format(q) == 'Total = $1000000.00'
    assert '{:#,.2P}'.format(q) == 'Total = $1,000,000.00'
    assert '{:p}'.format(q) == '$1000000'
    assert '{:.2p}'.format(q) == '$1000000'
    assert '{:,.2p}'.format(q) == '$1,000,000'
    assert '{:,P}'.format(q) == 'Total = $1,000,000'
    assert '{:.2P}'.format(q) == 'Total = $1000000'
    assert '{:,.2P}'.format(q) == 'Total = $1,000,000'

    q=Quantity('2ns')
    assert float(q) == 2e-9

def test_exceptional():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None, show_desc=False)
    Quantity.set_prefs(prec='full')
    q=Quantity('light = inf Hz -- a high frequency')
    assert '{}'.format(q) == 'inf Hz'
    assert '{:.8}'.format(q) == 'inf Hz'
    assert '{:.8s}'.format(q) == 'inf Hz'
    assert '{:.8S}'.format(q) == 'light = inf Hz'
    assert '{:.8q}'.format(q) == 'inf Hz'
    assert '{:.8Q}'.format(q) == 'light = inf Hz'
    assert '{:r}'.format(q) == 'inf'
    assert '{:R}'.format(q) == 'light = inf'
    assert '{:u}'.format(q) == 'Hz'
    assert '{:.4f}'.format(q) == 'inf'
    assert '{:.4F}'.format(q) == 'light = inf'
    assert '{:e}'.format(q) == 'inf'
    assert '{:E}'.format(q) == 'light = inf'
    assert '{:g}'.format(q) == 'inf'
    assert '{:G}'.format(q) == 'light = inf'
    assert '{:n}'.format(q) == 'light'
    assert '{:d}'.format(q) == 'a high frequency'
    assert '{:.2p}'.format(q) == 'inf Hz'
    assert '{:,.2p}'.format(q) == 'inf Hz'
    assert '{:.2P}'.format(q) == 'light = inf Hz'
    assert '{:,.2P}'.format(q) == 'light = inf Hz'

def test_scaled_format():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None, show_desc=False)
    Quantity.set_prefs(prec=None)
    if sys.version_info.major == 3:
        q=Quantity('Tboil = 100 °C -- boiling point of water')
        assert '{}'.format(q) == '100 °C'
        assert '{:.8}'.format(q) == '100 °C'
        assert '{:.8s°F}'.format(q) == '212 °F'
        assert '{:.8S°F}'.format(q) == 'Tboil = 212 °F'
        assert '{:.8q°F}'.format(q) == '212 °F'
        assert '{:.8Q°F}'.format(q) == 'Tboil = 212 °F'
        assert '{:r°F}'.format(q) == '212'
        assert '{:R°F}'.format(q) == 'Tboil = 212'
        assert '{:u°F}'.format(q) == '°F'
        assert '{:f°F}'.format(q) == '212'
        assert '{:F°F}'.format(q) == 'Tboil = 212'
        assert '{:e°F}'.format(q) == '2.12e+02'
        assert '{:E°F}'.format(q) == 'Tboil = 2.12e+02'
        assert '{:g°F}'.format(q) == '212'
        assert '{:G°F}'.format(q) == 'Tboil = 212'
        assert '{:n°F}'.format(q) == 'Tboil'
        assert '{:d°F}'.format(q) == 'boiling point of water'
        assert '{!r}'.format(q) == "Quantity('100 °C')"
        assert '{:.8s°C}'.format(q) == '100 °C'
        assert '{:p°F}'.format(q) == '212 °F'
        assert '{:,.2p°F}'.format(q) == '212 °F'
        assert '{:P°F}'.format(q) == 'Tboil = 212 °F'
        assert '{:,.2P°F}'.format(q) == 'Tboil = 212 °F'
        assert '{:#p°F}'.format(q) == '212.0000 °F'
        assert '{:#,.2p°F}'.format(q) == '212.00 °F'
        assert '{:#P°F}'.format(q) == 'Tboil = 212.0000 °F'
        assert '{:#,.2P°F}'.format(q) == 'Tboil = 212.00 °F'

def test_number_fmt():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None, show_desc=False)
    Quantity.set_prefs(prec=None)
    with Quantity.prefs(number_fmt='{whole:>3s}{frac:<4s} {units:<2s}'):
        assert '<{:s}>'.format(Quantity('1 mm')) ==     '<  1     mm>'
        assert '<{:s}>'.format(Quantity('10 mm')) ==    '< 10     mm>'
        assert '<{:s}>'.format(Quantity('100 mm')) ==   '<100     mm>'
        assert '<{:s}>'.format(Quantity('1.234 mm')) == '<  1.234 mm>'
        assert '<{:s}>'.format(Quantity('12.34 mm')) == '< 12.34  mm>'
        assert '<{:s}>'.format(Quantity('123.4 mm')) == '<123.4   mm>'

    with Quantity.prefs(number_fmt='{whole:>5s}{frac:<7s} {units:<6s}'):
        assert '<{:s}>'.format(Quantity('1 mm')) ==           '<    1        mm    >'
        assert '<{:s}>'.format(Quantity('10 mm')) ==          '<   10        mm    >'
        assert '<{:s}>'.format(Quantity('100 mm')) ==         '<  100        mm    >'
        assert '<{:s}>'.format(Quantity('1.234 mm')) ==       '<    1.234    mm    >'
        assert '<{:s}>'.format(Quantity('12.34 mm')) ==       '<   12.34     mm    >'
        assert '<{:s}>'.format(Quantity('123.4 mm')) ==       '<  123.4      mm    >'
        assert '<{:s}>'.format(Quantity('123.4 mmeter')) ==   '<  123.4      mmeter>'
        assert '<{:s}>'.format(Quantity('1e36 m')) ==         '<    1e36     m     >'
        assert '<{:s}>'.format(Quantity('10e36 m')) ==        '<   10e36     m     >'
        assert '<{:s}>'.format(Quantity('100e36 m')) ==       '<  100e36     m     >'
        assert '<{:s}>'.format(Quantity('1.234e36 m')) ==     '<    1.234e36 m     >'
        assert '<{:s}>'.format(Quantity('12.34e36 m')) ==     '<   12.34e36  m     >'
        assert '<{:s}>'.format(Quantity('123.4e36 m')) ==     '<  123.4e36   m     >'
        assert '<{:s}>'.format(Quantity('123.4e36 meter')) == '<  123.4e36   meter >'
        assert '<{:s}>'.format(Quantity('$1k')) ==            '<   $1        k     >'
        assert '<{:s}>'.format(Quantity('$10k')) ==           '<  $10        k     >'
        assert '<{:s}>'.format(Quantity('$100k')) ==          '< $100        k     >'
        assert '<{:s}>'.format(Quantity('$1.234k')) ==        '<   $1.234    k     >'
        assert '<{:s}>'.format(Quantity('$12.34k')) ==        '<  $12.34     k     >'
        assert '<{:s}>'.format(Quantity('$123.4k')) ==        '< $123.4      k     >'
        assert '<{:s}>'.format(Quantity('-$1k')) ==           '<  -$1        k     >'
        assert '<{:s}>'.format(Quantity('-$10k')) ==          '< -$10        k     >'
        assert '<{:s}>'.format(Quantity('-$100k')) ==         '<-$100        k     >'
        assert '<{:s}>'.format(Quantity('-$1.234k')) ==       '<  -$1.234    k     >'
        assert '<{:s}>'.format(Quantity('-$12.34k')) ==       '< -$12.34     k     >'
        assert '<{:s}>'.format(Quantity('-$123.4k')) ==       '<-$123.4      k     >'
        assert '<{:s}>'.format(Quantity('NaN Hz')) ==         '<  nan        Hz    >'
        assert '<{:s}>'.format(Quantity('inf Hz')) ==         '<  inf        Hz    >'

    with Quantity.prefs(number_fmt='{whole:>3s}{frac} {units}'):
        assert '<{:s}>'.format(Quantity('1 mm')) ==     '<  1 mm>'
        assert '<{:s}>'.format(Quantity('10 mm')) ==    '< 10 mm>'
        assert '<{:s}>'.format(Quantity('100 mm')) ==   '<100 mm>'
        assert '<{:s}>'.format(Quantity('1.234 mm')) == '<  1.234 mm>'
        assert '<{:s}>'.format(Quantity('12.34 mm')) == '< 12.34 mm>'
        assert '<{:s}>'.format(Quantity('123.4 mm')) == '<123.4 mm>'

    def fmt_num(whole, frac, units):
        return '{mantissa:>5s} {units}'.format(mantissa=whole+frac, units=units)

    with Quantity.prefs(number_fmt=fmt_num):
        assert '<{:s}>'.format(Quantity('1 mm')) ==     '<    1 mm>'
        assert '<{:s}>'.format(Quantity('10 mm')) ==    '<   10 mm>'
        assert '<{:s}>'.format(Quantity('100 mm')) ==   '<  100 mm>'
        assert '<{:s}>'.format(Quantity('1.234 mm')) == '<1.234 mm>'
        assert '<{:s}>'.format(Quantity('12.34 mm')) == '<12.34 mm>'
        assert '<{:s}>'.format(Quantity('123.4 mm')) == '<123.4 mm>'

def test_alignment():
    assert '<{:<16s}>'.format(Quantity('h')) == '<662.61e-36 J-s  >'
    assert '<{:^16s}>'.format(Quantity('h')) == '< 662.61e-36 J-s >'
    assert '<{:>16s}>'.format(Quantity('h')) == '<  662.61e-36 J-s>'
    assert '<{:<17s}>'.format(Quantity('h')) == '<662.61e-36 J-s   >'
    assert '<{:^17s}>'.format(Quantity('h')) == '< 662.61e-36 J-s  >'
    assert '<{:>17s}>'.format(Quantity('h')) == '<   662.61e-36 J-s>'

def test_format_method():
    Quantity.set_prefs(
        spacer = None,
        show_label = None,
        label_fmt = None,
        label_fmt_full = None,
        show_desc = False,
        prec = 4,
        strip_zeros = True,
    )
    q=Quantity('f = 1420.405751786 MHz -- frequency of hydrogen line')
    assert q.format() == '1.4204 GHz'
    assert q.format('') == '1.4204 GHz'
    assert q.format('.8') == '1.42040575 GHz'
    assert q.format('.8s') == '1.42040575 GHz'
    assert q.format('.8S') == 'f = 1.42040575 GHz'
    assert q.format('.8q') == '1.42040575 GHz'
    assert q.format('.8Q') == 'f = 1.42040575 GHz'
    assert q.format('r') == '1.4204G'
    assert q.format('R') == 'f = 1.4204G'
    assert q.format('u') == 'Hz'
    assert q.format('f') == '1420405751.786'
    assert q.format('F') == 'f = 1420405751.786'
    assert q.format('e') == '1.4204e+09'
    assert q.format('E') == 'f = 1.4204e+09'
    assert q.format('g') == '1.4204e+09'
    assert q.format('G') == 'f = 1.4204e+09'
    assert q.format('n') == 'f'
    assert q.format('d') == 'frequency of hydrogen line'
    assert q.format('p') == '1420405751.786 Hz'
    assert q.format(',p') == '1,420,405,751.786 Hz'
    assert q.format('P') == 'f = 1420405751.786 Hz'
    assert q.format(',P') == 'f = 1,420,405,751.786 Hz'
    assert q.format('#p') == '1420405751.7860 Hz'
    assert q.format('#,p') == '1,420,405,751.7860 Hz'
    assert q.format('#P') == 'f = 1420405751.7860 Hz'
    assert q.format('#,P') == 'f = 1,420,405,751.7860 Hz'

def test_render():
    Quantity.set_prefs(
        spacer = None,
        show_label = None,
        label_fmt = None,
        label_fmt_full = None,
        show_desc = False,
        prec = 4,
        strip_zeros = True,
    )
    q=Quantity('f = 1420.405751786 MHz -- frequency of hydrogen line')
    assert q.render() == '1.4204 GHz'
    assert q.render(prec=8) == '1.42040575 GHz'
    assert q.render(prec=8, show_label=True) == 'f = 1.42040575 GHz'
    assert q.render(show_units=False) == '1.4204G'
    assert q.render(show_units=False, show_label=True) == 'f = 1.4204G'
    assert q.render(show_si=False) == '1.4204e9 Hz'
    assert q.render(show_si=False, show_label=True) == 'f = 1.4204e9 Hz'
    assert q.render(prec=15, strip_zeros=False) == '1.420405751786000 GHz'
    assert q.render(prec=15, strip_zeros=True) == '1.420405751786 GHz'
    assert q.units == 'Hz'
    assert q.name == 'f'
    assert q.desc == 'frequency of hydrogen line'
    assert q.fixed() == '1420405751.786 Hz'
    assert q.fixed(show_commas=True) == '1,420,405,751.786 Hz'
    assert q.fixed(show_units=False) == '1420405751.786'
    assert q.fixed(strip_zeros=True) == '1420405751.786 Hz'
    assert q.fixed(strip_zeros=False) == '1420405751.7860 Hz'
    assert q.fixed(show_label=True) == 'f = 1420405751.786 Hz'
    assert q.fixed(show_label=True, show_commas=True) == 'f = 1,420,405,751.786 Hz'

    q=Quantity('$1M')
    assert q.render(strip_zeros=True) == '$1M'
    assert q.render(strip_zeros=False) == '$1.0000M'
    assert q.render(strip_zeros=True, strip_radix=False) == '$1M'
    assert q.render(prec='full') == '$1M'
    assert q.fixed(strip_zeros=True) == '$1000000'
    assert q.fixed(strip_zeros=False) == '$1000000.0000'
    assert q.fixed(strip_zeros=True, strip_radix=False) == '$1000000.'
    assert q.fixed(prec='full') == '$1000000'
    assert q.fixed(prec='full', strip_zeros=False) == '$1000000.000000000000'
