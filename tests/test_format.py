# encoding: utf8

from quantiphy import Quantity, QuantiPhyError, IncompatiblePreferences
import pytest

def test_format():
    Quantity.reset_prefs()
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
    assert '{:pHz}'.format(q) == '1420405751.786 Hz'
    assert '{:pkHz}'.format(q) == '1420405.7518 kHz'
    assert '{:pMHz}'.format(q) == '1420.4058 MHz'
    assert '{:pGHz}'.format(q) == '1.4204 GHz'
    assert '{:pTHz}'.format(q) == '0.0014 THz'
    assert '{:,p}'.format(q) == '1,420,405,751.786 Hz'
    assert '{:P}'.format(q) == 'f = 1420405751.786 Hz'
    assert '{:,P}'.format(q) == 'f = 1,420,405,751.786 Hz'
    assert '{:#.3q}'.format(q) == '1.420 GHz'
    assert '{:#p}'.format(q) == '1420405751.7860 Hz'
    assert '{:.0q}'.format(q) == '1 GHz'
    assert '{:.0p}'.format(q) == '1420405752 Hz'
    assert '{:#.0q}'.format(q) == '1 GHz'
    assert '{:#.0p}'.format(q) == '1420405752. Hz'
    assert '{:#.0f}'.format(q) == '1420405752.'
    assert '{:#.3f}'.format(q) == '1420405751.786'
    assert '{:.0g}'.format(q) == '1e+09'
    assert '{:#.0g}'.format(q) == '1.e+09'
    assert '{:#.3g}'.format(q) == '1.420e+09'

    q = Quantity('2ns')
    assert float(q) == 2e-9

    with pytest.raises(ValueError) as exception:
        q = Quantity('1ns')
        print('{:x}'.format(q))
    assert exception.value.args[0] == "Unknown format code 'x' for object of type 'float'"

def test_full_format():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None, show_desc=False)
    Quantity.set_prefs(prec='full')
    q = Quantity('f = 1420.405751786 MHz — frequency of hydrogen line')
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
    assert '{:p}'.format(q) == '1420405751.786 Hz'
    assert '{:,p}'.format(q) == '1,420,405,751.786 Hz'
    assert '{:,.2pHz}'.format(q) == '1,420,405,751.79 Hz'
    assert '{:,.2pkHz}'.format(q) == '1,420,405.75 kHz'
    assert '{:,.2pMHz}'.format(q) == '1,420.41 MHz'
    assert '{:,.2pGHz}'.format(q) == '1.42 GHz'
    assert '{:,.2pTHz}'.format(q) == '0 THz'
    assert '{:P}'.format(q) == 'f = 1420405751.786 Hz'
    assert '{:,P}'.format(q) == 'f = 1,420,405,751.786 Hz'
    assert '{:#.3q}'.format(q) == '1.420 GHz'
    assert '{:#.6p}'.format(q) == '1420405751.786000 Hz'
    assert '{:.0q}'.format(q) == '1 GHz'
    assert '{:.0p}'.format(q) == '1420405752 Hz'
    assert '{:#.0q}'.format(q) == '1 GHz'
    assert '{:#.0p}'.format(q) == '1420405752. Hz'
    values = '''
        1.000000 +1.000000 -1.000000
        $1.000000 +$1.000000 -$1.000000
        1.000000_V +1.000000_V -1.000000_V
        1.234567 +1.234567 -1.234567
        $1.234567 +$1.234567 -$1.234567
        1.234567_V +1.234567_V -1.234567_V
        -0 -0.0000 -0.0_s -$0.00
    '''
    for given in values.split():
        expected = given.lstrip('+').replace('_', ' ')
        q = Quantity(given)
        if q == 0 and expected[0] == '-':
            expected = expected[1:]
        assert q.render(form='si', strip_zeros=False) == expected, given
        assert q.render(form='si', prec='full', strip_zeros=False) == expected, given

    # check fixed()
    base = '000654321.123456000'
    for d in range(-12, 12):
        num = f"{base}e{d}"
        q = Quantity(num, '$')

        prec = max(6-d, 0)
        fmtd = f"{float(num):25.{prec}f}".strip()
        assert f"${fmtd}" == q.fixed()

    q = Quantity('1234.56 Ω')
    assert q.fixed(scale='MΩ') == "0.00123456 MΩ"


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
        assert '<{:s}>'.format(Quantity('nan Hz')) ==         '<  NaN        Hz    >'
        assert '<{:s}>'.format(Quantity('inf Hz')) ==         '<  inf        Hz    >'

    with Quantity.prefs(number_fmt='{whole:>5s}{frac:<7s} {units:<6s}', minus=Quantity.minus_sign):
        assert '<{:s}>'.format(Quantity('-$1k')) ==           '<  −$1        k     >'
        assert '<{:s}>'.format(Quantity('-$10k')) ==          '< −$10        k     >'
        assert '<{:s}>'.format(Quantity('-$100k')) ==         '<−$100        k     >'
        assert '<{:s}>'.format(Quantity('-$1.234k')) ==       '<  −$1.234    k     >'
        assert '<{:s}>'.format(Quantity('-$12.34k')) ==       '< −$12.34     k     >'
        assert '<{:s}>'.format(Quantity('-$123.4k')) ==       '<−$123.4      k     >'

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

    with Quantity.prefs(number_fmt='{whole:>3s}{frac:<4s} {units:<2s}', radix=',', comma='.'):
        assert '<{:s}>'.format(Quantity('1 mm')) ==     '<  1     mm>'
        assert '<{:s}>'.format(Quantity('10 mm')) ==    '< 10     mm>'
        assert '<{:s}>'.format(Quantity('100 mm')) ==   '<100     mm>'
        assert '<{:s}>'.format(Quantity('1,234 mm')) == '<  1,234 mm>'
        assert '<{:s}>'.format(Quantity('12,34 mm')) == '< 12,34  mm>'
        assert '<{:s}>'.format(Quantity('123,4 mm')) == '<123,4   mm>'

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

    Quantity.set_prefs(
        spacer = None,
        show_label = None,
        label_fmt = None,
        label_fmt_full = None,
        show_desc = False,
        prec = 4,
        strip_zeros = False,
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
    assert q.format('f') == '1420405751.7860'
    assert q.format('F') == 'f = 1420405751.7860'
    assert q.format('e') == '1.4204e+09'
    assert q.format('E') == 'f = 1.4204e+09'
    assert q.format('g') == '1.4204e+09'
    assert q.format('G') == 'f = 1.4204e+09'
    assert q.format('n') == 'f'
    assert q.format('d') == 'frequency of hydrogen line'
    assert q.format('p') == '1420405751.7860 Hz'
    assert q.format(',p') == '1,420,405,751.7860 Hz'
    assert q.format('P') == 'f = 1420405751.7860 Hz'
    assert q.format(',P') == 'f = 1,420,405,751.7860 Hz'
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
    assert q.render(form='eng') == '1.4204e9 Hz'
    assert q.render(form='eng', show_label=True) == 'f = 1.4204e9 Hz'
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
    assert q.render(form='fixed') == '1420405751.786 Hz'

    q=Quantity('$1M')
    assert q.render(strip_zeros=True) == '$1M'
    assert q.render(strip_zeros=False) == '$1.0000M'
    assert q.render(strip_zeros=True, strip_radix=False) == '$1M'
    assert q.render(prec='full') == '$1M'
    assert q.fixed(strip_zeros=True) == '$1000000'
    assert q.fixed(strip_zeros=False) == '$1000000.0000'
    assert q.fixed(strip_zeros=True, strip_radix=False) == '$1000000.'
    assert q.fixed(prec='full') == '$1000000'
    assert q.fixed(prec='full', strip_zeros=False) == '$1000000'
    assert q.render(form='fixed') == '$1000000'

    q=Quantity('$100')
    assert q.fixed(prec=0, strip_zeros=False, strip_radix=False) == '$100.'
    assert q.fixed(prec=0, strip_zeros=True, strip_radix=False) == '$100.'
    assert q.fixed(prec=0, strip_zeros=True, strip_radix='cover') == '$100.0'
    assert q.fixed(prec=0, strip_zeros=False, strip_radix=True) == '$100'
    assert q.fixed(prec=0, strip_zeros=True, strip_radix=True) == '$100'
    assert q.fixed(prec=2, strip_zeros=False, strip_radix=False) == '$100.00'
    assert q.fixed(prec=2, strip_zeros=True, strip_radix=False) == '$100.'
    assert q.fixed(prec=2, strip_zeros=True, strip_radix='cover') == '$100.0'
    assert q.fixed(prec=2, strip_zeros=False, strip_radix=True) == '$100.00'
    assert q.fixed(prec=2, strip_zeros=True, strip_radix=True) == '$100'

    q=Quantity('$123.45')
    assert q.render(prec=0, strip_zeros=False, strip_radix='cover') == '$100.0'
    assert q.render(prec=0, strip_zeros=True, strip_radix=False) == '$100.'
    assert q.render(prec=0, strip_zeros=False, strip_radix=True) == '$100'
    assert q.render(prec=0, strip_zeros=True, strip_radix=True) == '$100'
    assert q.render(prec=2, strip_zeros=False, strip_radix='cover') == '$123.0'
    assert q.render(prec=2, strip_zeros=True, strip_radix=False) == '$123.'
    assert q.render(prec=2, strip_zeros=False, strip_radix=True) == '$123'
    assert q.render(prec=2, strip_zeros=True, strip_radix=True) == '$123'
    assert q.render(prec=4, strip_zeros=False, strip_radix='cover') == '$123.45'
    assert q.render(prec=4, strip_zeros=True, strip_radix=False) == '$123.45'
    assert q.render(prec=4, strip_zeros=False, strip_radix=True) == '$123.45'
    assert q.render(prec=4, strip_zeros=True, strip_radix=True) == '$123.45'

def test_sign():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None, show_desc=False)

    # Positive numbers
    q=Quantity('f = 1420.405751786 MHz -- frequency of hydrogen line')
    assert '{}'.format(q) == '1.4204 GHz'
    assert '{:q}'.format(q) == '1.4204 GHz'
    assert '{:r}'.format(q) == '1.4204G'
    assert '{:f}'.format(q) == '1420405751.786'
    assert '{:e}'.format(q) == '1.4204e+09'
    assert '{:g}'.format(q) == '1.4204e+09'
    assert '{:p}'.format(q) == '1420405751.786 Hz'
    assert '{:,p}'.format(q) == '1,420,405,751.786 Hz'
    assert '{:#.3q}'.format(q) == '1.420 GHz'
    assert '{:#p}'.format(q) == '1420405751.7860 Hz'

    q=Quantity('Total = $1000k -- a large amount of money')
    assert '{}'.format(q) == '$1M'
    assert '{:q}'.format(q) == '$1M'
    assert '{:r}'.format(q) == '1M'
    assert '{:f}'.format(q) == '1000000'
    assert '{:e}'.format(q) == '1e+06'
    assert '{:g}'.format(q) == '1e+06'
    assert '{:p}'.format(q) == '$1000000'
    assert '{:#p}'.format(q) == '$1000000.0000'

    q=Quantity('f = 1e100 atoms')
    assert '{}'.format(q) == '10e99 atoms'
    assert '{:q}'.format(q) == '10e99 atoms'
    assert '{:r}'.format(q) == '10e99'
    assert '{:e}'.format(q) == '1e+100'
    assert '{:g}'.format(q) == '1e+100'

    q=Quantity('light = inf Hz -- a high frequency')
    assert '{}'.format(q) == 'inf Hz'
    assert '{:q}'.format(q) == 'inf Hz'
    assert '{:r}'.format(q) == 'inf'
    assert '{:f}'.format(q) == 'inf'
    assert '{:e}'.format(q) == 'inf'
    assert '{:g}'.format(q) == 'inf'
    assert '{:p}'.format(q) == 'inf Hz'

    q=Quantity('f = -1420.405751786 MHz -- frequency of hydrogen line')
    assert '{}'.format(q) == '-1.4204 GHz'
    assert '{:f}'.format(q) == '-1420405751.786'
    assert '{:e}'.format(q) == '-1.4204e+09'
    assert '{:g}'.format(q) == '-1.4204e+09'
    assert '{:p}'.format(q) == '-1420405751.786 Hz'
    assert '{:,p}'.format(q) == '-1,420,405,751.786 Hz'
    assert '{:#.3q}'.format(q) == '-1.420 GHz'
    assert '{:#p}'.format(q) == '-1420405751.7860 Hz'

    # Negative numbers
    q=Quantity('f = -1420.405751786 MHz -- frequency of hydrogen line')
    assert '{}'.format(q) == '-1.4204 GHz'
    assert '{:q}'.format(q) == '-1.4204 GHz'
    assert '{:r}'.format(q) == '-1.4204G'
    assert '{:f}'.format(q) == '-1420405751.786'
    assert '{:e}'.format(q) == '-1.4204e+09'
    assert '{:g}'.format(q) == '-1.4204e+09'
    assert '{:p}'.format(q) == '-1420405751.786 Hz'
    assert '{:,p}'.format(q) == '-1,420,405,751.786 Hz'
    assert '{:#.3q}'.format(q) == '-1.420 GHz'
    assert '{:#p}'.format(q) == '-1420405751.7860 Hz'

    q=Quantity('Total = -$1000k -- a large amount of money')
    assert '{}'.format(q) == '-$1M'
    assert '{:q}'.format(q) == '-$1M'
    assert '{:r}'.format(q) == '-1M'
    assert '{:f}'.format(q) == '-1000000'
    assert '{:e}'.format(q) == '-1e+06'
    assert '{:g}'.format(q) == '-1e+06'
    assert '{:p}'.format(q) == '-$1000000'
    assert '{:#p}'.format(q) == '-$1000000.0000'

    q=Quantity('f = -1e-100 atoms')
    assert '{}'.format(q) == '-100e-102 atoms'
    assert '{:q}'.format(q) == '-100e-102 atoms'
    assert '{:r}'.format(q) == '-100e-102'
    assert '{:e}'.format(q) == '-1e-100'
    assert '{:g}'.format(q) == '-1e-100'

    q=Quantity('light = -inf Hz -- a high frequency')
    assert '{}'.format(q) == '-inf Hz'
    assert '{:q}'.format(q) == '-inf Hz'
    assert '{:r}'.format(q) == '-inf'
    assert '{:f}'.format(q) == '-inf'
    assert '{:e}'.format(q) == '-inf'
    assert '{:g}'.format(q) == '-inf'
    assert '{:p}'.format(q) == '-inf Hz'

    with Quantity.prefs(plus=Quantity.plus_sign, minus=Quantity.minus_sign):

        # Positive numbers
        q=Quantity('f = 1420.405751786 MHz -- frequency of hydrogen line')
        assert '{}'.format(q) == '1.4204 GHz'
        assert '{:q}'.format(q) == '1.4204 GHz'
        assert '{:r}'.format(q) == '1.4204G'
        assert '{:f}'.format(q) == '1420405751.786'
        assert '{:e}'.format(q) == '1.4204e＋09'
        assert '{:g}'.format(q) == '1.4204e＋09'
        assert '{:p}'.format(q) == '1420405751.786 Hz'
        assert '{:,p}'.format(q) == '1,420,405,751.786 Hz'
        assert '{:#.3q}'.format(q) == '1.420 GHz'
        assert '{:#p}'.format(q) == '1420405751.7860 Hz'

        q=Quantity('Total = $1000k -- a large amount of money')
        assert '{}'.format(q) == '$1M'
        assert '{:q}'.format(q) == '$1M'
        assert '{:r}'.format(q) == '1M'
        assert '{:f}'.format(q) == '1000000'
        assert '{:e}'.format(q) == '1e＋06'
        assert '{:g}'.format(q) == '1e＋06'
        assert '{:p}'.format(q) == '$1000000'
        assert '{:#p}'.format(q) == '$1000000.0000'

        q=Quantity('f = 1e100 atoms')
        assert '{}'.format(q) == '10e99 atoms'
        assert '{:q}'.format(q) == '10e99 atoms'
        assert '{:r}'.format(q) == '10e99'
        assert '{:e}'.format(q) == '1e＋100'
        assert '{:g}'.format(q) == '1e＋100'

        q=Quantity('light = inf Hz -- a high frequency')
        assert '{}'.format(q) == 'inf Hz'
        assert '{:q}'.format(q) == 'inf Hz'
        assert '{:r}'.format(q) == 'inf'
        assert '{:f}'.format(q) == 'inf'
        assert '{:e}'.format(q) == 'inf'
        assert '{:g}'.format(q) == 'inf'
        assert '{:p}'.format(q) == 'inf Hz'

        # Negative numbers
        q=Quantity('f = -1420.405751786 MHz -- frequency of hydrogen line')
        assert '{}'.format(q) == '−1.4204 GHz'
        assert '{:q}'.format(q) == '−1.4204 GHz'
        assert '{:r}'.format(q) == '−1.4204G'
        assert '{:f}'.format(q) == '−1420405751.786'
        assert '{:e}'.format(q) == '−1.4204e＋09'
        assert '{:g}'.format(q) == '−1.4204e＋09'
        assert '{:p}'.format(q) == '−1420405751.786 Hz'
        assert '{:,p}'.format(q) == '−1,420,405,751.786 Hz'
        assert '{:#.3q}'.format(q) == '−1.420 GHz'
        assert '{:#p}'.format(q) == '−1420405751.7860 Hz'

        q=Quantity('Total = -$1000k -- a large amount of money')
        assert '{}'.format(q) == '−$1M'
        assert '{:q}'.format(q) == '−$1M'
        assert '{:r}'.format(q) == '−1M'
        assert '{:f}'.format(q) == '−1000000'
        assert '{:e}'.format(q) == '−1e＋06'
        assert '{:g}'.format(q) == '−1e＋06'
        assert '{:p}'.format(q) == '−$1000000'
        assert '{:#p}'.format(q) == '−$1000000.0000'

        q=Quantity('f = -1e-100 atoms')
        assert '{}'.format(q) == '−100e−102 atoms'
        assert '{:q}'.format(q) == '−100e−102 atoms'
        assert '{:r}'.format(q) == '−100e−102'
        assert '{:e}'.format(q) == '−1e−100'
        assert '{:g}'.format(q) == '−1e−100'

        q=Quantity('light = -inf Hz -- a high frequency')
        assert '{}'.format(q) == '−inf Hz'
        assert '{:q}'.format(q) == '−inf Hz'
        assert '{:r}'.format(q) == '−inf'
        assert '{:f}'.format(q) == '−inf'
        assert '{:e}'.format(q) == '−inf'
        assert '{:g}'.format(q) == '−inf'
        assert '{:p}'.format(q) == '−inf Hz'

    with Quantity.prefs(plus='', minus=Quantity.minus_sign):

        # Positive numbers
        q=Quantity('f = 1420.405751786 MHz -- frequency of hydrogen line')
        assert '{}'.format(q) == '1.4204 GHz'
        assert '{:q}'.format(q) == '1.4204 GHz'
        assert '{:r}'.format(q) == '1.4204G'
        assert '{:f}'.format(q) == '1420405751.786'
        assert '{:e}'.format(q) == '1.4204e09'
        assert '{:g}'.format(q) == '1.4204e09'
        assert '{:p}'.format(q) == '1420405751.786 Hz'
        assert '{:,p}'.format(q) == '1,420,405,751.786 Hz'
        assert '{:#.3q}'.format(q) == '1.420 GHz'
        assert '{:#p}'.format(q) == '1420405751.7860 Hz'

        q=Quantity('Total = $1000k -- a large amount of money')
        assert '{}'.format(q) == '$1M'
        assert '{:q}'.format(q) == '$1M'
        assert '{:r}'.format(q) == '1M'
        assert '{:f}'.format(q) == '1000000'
        assert '{:e}'.format(q) == '1e06'
        assert '{:g}'.format(q) == '1e06'
        assert '{:p}'.format(q) == '$1000000'
        assert '{:#p}'.format(q) == '$1000000.0000'

        q=Quantity('f = 1e100 atoms')
        assert '{}'.format(q) == '10e99 atoms'
        assert '{:q}'.format(q) == '10e99 atoms'
        assert '{:r}'.format(q) == '10e99'
        assert '{:e}'.format(q) == '1e100'
        assert '{:g}'.format(q) == '1e100'

        q=Quantity('light = inf Hz -- a high frequency')
        assert '{}'.format(q) == 'inf Hz'
        assert '{:q}'.format(q) == 'inf Hz'
        assert '{:r}'.format(q) == 'inf'
        assert '{:f}'.format(q) == 'inf'
        assert '{:e}'.format(q) == 'inf'
        assert '{:g}'.format(q) == 'inf'
        assert '{:p}'.format(q) == 'inf Hz'

        # Negative numbers
        q=Quantity('f = -1420.405751786 MHz -- frequency of hydrogen line')
        assert '{}'.format(q) == '−1.4204 GHz'
        assert '{:q}'.format(q) == '−1.4204 GHz'
        assert '{:r}'.format(q) == '−1.4204G'
        assert '{:f}'.format(q) == '−1420405751.786'
        assert '{:e}'.format(q) == '−1.4204e09'
        assert '{:g}'.format(q) == '−1.4204e09'
        assert '{:p}'.format(q) == '−1420405751.786 Hz'
        assert '{:,p}'.format(q) == '−1,420,405,751.786 Hz'
        assert '{:#.3q}'.format(q) == '−1.420 GHz'
        assert '{:#p}'.format(q) == '−1420405751.7860 Hz'

        q=Quantity('Total = -$1000k -- a large amount of money')
        assert '{}'.format(q) == '−$1M'
        assert '{:q}'.format(q) == '−$1M'
        assert '{:r}'.format(q) == '−1M'
        assert '{:f}'.format(q) == '−1000000'
        assert '{:e}'.format(q) == '−1e06'
        assert '{:g}'.format(q) == '−1e06'
        assert '{:p}'.format(q) == '−$1000000'
        assert '{:#p}'.format(q) == '−$1000000.0000'

        q=Quantity('f = -1e-100 atoms')
        assert '{}'.format(q) == '−100e−102 atoms'
        assert '{:q}'.format(q) == '−100e−102 atoms'
        assert '{:r}'.format(q) == '−100e−102'
        assert '{:e}'.format(q) == '−1e−100'
        assert '{:g}'.format(q) == '−1e−100'

        q=Quantity('light = -inf Hz -- a high frequency')
        assert '{}'.format(q) == '−inf Hz'
        assert '{:q}'.format(q) == '−inf Hz'
        assert '{:r}'.format(q) == '−inf'
        assert '{:f}'.format(q) == '−inf'
        assert '{:e}'.format(q) == '−inf'
        assert '{:g}'.format(q) == '−inf'
        assert '{:p}'.format(q) == '−inf Hz'

def test_radix_comma_output():
    with Quantity.prefs(
        spacer = None,
        show_label = None,
        label_fmt = None,
        label_fmt_full = None,
        show_desc = False,
        prec = 4,
        radix = ',',
        comma = '.',
    ):
        q=Quantity('c')
        assert '{}'.format(q) == '299,79 Mm/s'
        assert '{:.8}'.format(q) == '299,792458 Mm/s'
        assert '{:.8s}'.format(q) == '299,792458 Mm/s'
        assert '{:.8S}'.format(q) == 'c = 299,792458 Mm/s'
        assert '{:.8q}'.format(q) == '299,792458 Mm/s'
        assert '{:.8Q}'.format(q) == 'c = 299,792458 Mm/s'
        assert '{:r}'.format(q) == '299,79M'
        assert '{:R}'.format(q) == 'c = 299,79M'
        assert '{:u}'.format(q) == 'm/s'
        assert '{:.4f}'.format(q) == '299792458'
        assert '{:.4F}'.format(q) == 'c = 299792458'
        assert '{:e}'.format(q) == '2.9979e+08'
        assert '{:E}'.format(q) == 'c = 2.9979e+08'
        assert '{:g}'.format(q) == '2.9979e+08'
        assert '{:G}'.format(q) == 'c = 2.9979e+08'
        assert '{:n}'.format(q) == 'c'
        assert '{:d}'.format(q) == 'speed of light'
        assert '{:#p}'.format(q) == '299792458,0000 m/s'
        assert '{:#.2p}'.format(q) == '299792458,00 m/s'
        assert '{:#,.2p}'.format(q) == '299.792.458,00 m/s'
        assert '{:#,P}'.format(q) == 'c = 299.792.458,0000 m/s'
        assert '{:#.2P}'.format(q) == 'c = 299792458,00 m/s'
        assert '{:#,.2P}'.format(q) == 'c = 299.792.458,00 m/s'
        assert '{:p}'.format(q) == '299792458 m/s'
        assert '{:.2p}'.format(q) == '299792458 m/s'
        assert '{:,.2p}'.format(q) == '299.792.458 m/s'
        assert '{:,P}'.format(q) == 'c = 299.792.458 m/s'
        assert '{:.2P}'.format(q) == 'c = 299792458 m/s'
        assert '{:,.2P}'.format(q) == 'c = 299.792.458 m/s'

def test_plus_minus():
    with Quantity.prefs(
        spacer = None,
        show_label = None,
        label_fmt = None,
        label_fmt_full = None,
        show_desc = False,
        prec = 4,
        plus = Quantity.plus_sign,
        minus = Quantity.minus_sign,
        map_sf = Quantity.map_sf_to_sci_notation,
    ):
        qpp=Quantity('+1Ms')
        qpm=Quantity('+1us')
        qmp=Quantity('-1Ms')
        qmm=Quantity('-1us')

        assert '{}'.format(qpp) == '1 Ms'
        assert '{}'.format(qpm) == '1 µs'
        assert '{}'.format(qmp) == '−1 Ms'
        assert '{}'.format(qmm) == '−1 µs'

        assert '{0:e} {0:u}'.format(qpp) == '1e＋06 s'
        assert '{0:e} {0:u}'.format(qpm) == '1e−06 s'
        assert '{0:e} {0:u}'.format(qmp) == '−1e＋06 s'
        assert '{0:e} {0:u}'.format(qmm) == '−1e−06 s'

        assert '{:.8p}'.format(qpp) == '1000000 s'
        assert '{:.8p}'.format(qpm) == '0.000001 s'
        assert '{:.8p}'.format(qmp) == '−1000000 s'
        assert '{:.8p}'.format(qmm) == '−0.000001 s'

        assert qpp.render(form='sia') == '1 Ms'
        assert qpm.render(form='sia') == '1 us'
        assert qmp.render(form='sia') == '−1 Ms'
        assert qmm.render(form='sia') == '−1 us'

def test_radix_comma_input():
    with Quantity.prefs(
        spacer = None,
        show_label = None,
        label_fmt = None,
        label_fmt_full = None,
        show_desc = False,
        prec = 4,
        radix = ',',
        comma = '.',
    ):
        assert Quantity('299,79 Mm/s').render() == '299,79 Mm/s'
        assert Quantity('299,792458e6 m/s').render() == '299,79 Mm/s'
        assert Quantity('299,792458 Mm/s').render() == '299,79 Mm/s'
        assert Quantity('299.792.458,0000 m/s').render() == '299,79 Mm/s'
        assert Quantity('299792458,0000 m/s').render() == '299,79 Mm/s'
        assert Quantity('1.000.000,00 KiB', binary=True).render() == '1,024 GB'
        assert Quantity('$1.000.000,00').render() == '$1M'
        assert Quantity('$1.000.000,00e3').render() == '$1G'

    with Quantity.prefs(
        spacer = None,
        show_label = None,
        label_fmt = None,
        label_fmt_full = None,
        show_desc = False,
        prec = 4,
        radix = ',',
        comma = '',
    ):
        assert Quantity('299,79 Mm/s').render() == '299,79 Mm/s'
        assert Quantity('299.79 Mm/s').render() == '299,79 Mm/s'
        assert Quantity('$1000000,00').render() == '$1M'
        assert Quantity('$1000000.00').render() == '$1M'
        assert Quantity('$1,00e8').render() == '$100M'
        assert Quantity('$1.00e8').render() == '$100M'

def test_radix_comma_exception():
    with pytest.raises(ValueError) as exception:
        with Quantity.prefs(
            radix = ',',
        ):
            Quantity('$1M')
    assert exception.value.args[0] == "comma and radix must differ."

    with pytest.raises(QuantiPhyError) as exception:
        with Quantity.prefs(
            comma = '.',
        ):
            Quantity('$1M')
    assert exception.value.args[0] == "comma and radix must differ."

    with pytest.raises(IncompatiblePreferences) as exception:
        with Quantity.prefs(
            comma = '^',
            radix = '^',
        ):
            Quantity('$1M')
    assert exception.value.args[0] == "comma and radix must differ."


def test_output_sf():
    with Quantity.prefs(output_sf = Quantity.all_sf):
        q=Quantity('c')
        assert f"{Quantity(1e35, 'Hz')}" == '100e33 Hz'
        assert f"{Quantity(1e34, 'Hz')}" == '10e33 Hz'
        assert f"{Quantity(1e33, 'Hz')}" == '1e33 Hz'
        assert f"{Quantity(1e32, 'Hz')}" == '100 QHz'
        assert f"{Quantity(1e31, 'Hz')}" == '10 QHz'
        assert f"{Quantity(1e30, 'Hz')}" == '1 QHz'
        assert f"{Quantity(1e29, 'Hz')}" == '100 RHz'
        assert f"{Quantity(1e28, 'Hz')}" == '10 RHz'
        assert f"{Quantity(1e27, 'Hz')}" == '1 RHz'
        assert f"{Quantity(1e26, 'Hz')}" == '100 YHz'
        assert f"{Quantity(1e25, 'Hz')}" == '10 YHz'
        assert f"{Quantity(1e24, 'Hz')}" == '1 YHz'
        assert f"{Quantity(1e23, 'Hz')}" == '100 ZHz'
        assert f"{Quantity(1e22, 'Hz')}" == '10 ZHz'
        assert f"{Quantity(1e21, 'Hz')}" == '1 ZHz'
        assert f"{Quantity(1e20, 'Hz')}" == '100 EHz'
        assert f"{Quantity(1e19, 'Hz')}" == '10 EHz'
        assert f"{Quantity(1e18, 'Hz')}" == '1 EHz'
        assert f"{Quantity(1e17, 'Hz')}" == '100 PHz'
        assert f"{Quantity(1e16, 'Hz')}" == '10 PHz'
        assert f"{Quantity(1e15, 'Hz')}" == '1 PHz'
        assert f"{Quantity(1e14, 'Hz')}" == '100 THz'
        assert f"{Quantity(1e13, 'Hz')}" == '10 THz'
        assert f"{Quantity(1e12, 'Hz')}" == '1 THz'
        assert f"{Quantity(1e11, 'Hz')}" == '100 GHz'
        assert f"{Quantity(1e10, 'Hz')}" == '10 GHz'
        assert f"{Quantity(1e9, 'Hz')}" == '1 GHz'
        assert f"{Quantity(1e8, 'Hz')}" == '100 MHz'
        assert f"{Quantity(1e7, 'Hz')}" == '10 MHz'
        assert f"{Quantity(1e6, 'Hz')}" == '1 MHz'
        assert f"{Quantity(1e5, 'Hz')}" == '100 kHz'
        assert f"{Quantity(1e4, 'Hz')}" == '10 kHz'
        assert f"{Quantity(1e3, 'Hz')}" == '1 kHz'
        assert f"{Quantity(1e2, 'Hz')}" == '100 Hz'
        assert f"{Quantity(1e1, 'Hz')}" == '10 Hz'
        assert f"{Quantity(1e0, 'Hz')}" == '1 Hz'
        assert f"{Quantity(1e-1, 'Hz')}" == '100 mHz'
        assert f"{Quantity(1e-2, 'Hz')}" == '10 mHz'
        assert f"{Quantity(1e-3, 'Hz')}" == '1 mHz'
        assert f"{Quantity(1e-4, 'Hz')}" == '100 uHz'
        assert f"{Quantity(1e-5, 'Hz')}" == '10 uHz'
        assert f"{Quantity(1e-6, 'Hz')}" == '1 uHz'
        assert f"{Quantity(1e-7, 'Hz')}" == '100 nHz'
        assert f"{Quantity(1e-8, 'Hz')}" == '10 nHz'
        assert f"{Quantity(1e-9, 'Hz')}" == '1 nHz'
        assert f"{Quantity(1e-10, 'Hz')}" == '100 pHz'
        assert f"{Quantity(1e-11, 'Hz')}" == '10 pHz'
        assert f"{Quantity(1e-12, 'Hz')}" == '1 pHz'
        assert f"{Quantity(1e-13, 'Hz')}" == '100 fHz'
        assert f"{Quantity(1e-14, 'Hz')}" == '10 fHz'
        assert f"{Quantity(1e-15, 'Hz')}" == '1 fHz'
        assert f"{Quantity(1e-16, 'Hz')}" == '100 aHz'
        assert f"{Quantity(1e-17, 'Hz')}" == '10 aHz'
        assert f"{Quantity(1e-18, 'Hz')}" == '1 aHz'
        assert f"{Quantity(1e-19, 'Hz')}" == '100 zHz'
        assert f"{Quantity(1e-20, 'Hz')}" == '10 zHz'
        assert f"{Quantity(1e-21, 'Hz')}" == '1 zHz'
        assert f"{Quantity(1e-22, 'Hz')}" == '100 yHz'
        assert f"{Quantity(1e-23, 'Hz')}" == '10 yHz'
        assert f"{Quantity(1e-24, 'Hz')}" == '1 yHz'
        assert f"{Quantity(1e-25, 'Hz')}" == '100 rHz'
        assert f"{Quantity(1e-26, 'Hz')}" == '10 rHz'
        assert f"{Quantity(1e-27, 'Hz')}" == '1 rHz'
        assert f"{Quantity(1e-28, 'Hz')}" == '100 qHz'
        assert f"{Quantity(1e-29, 'Hz')}" == '10 qHz'
        assert f"{Quantity(1e-30, 'Hz')}" == '1 qHz'
        assert f"{Quantity(1e-31, 'Hz')}" == '100e-33 Hz'
        assert f"{Quantity(1e-32, 'Hz')}" == '10e-33 Hz'
        assert f"{Quantity(1e-33, 'Hz')}" == '1e-33 Hz'

    with Quantity.prefs(output_sf = 'YZEPTGMkmunpfazy'):
        q=Quantity('c')
        assert f"{Quantity(1e35, 'Hz')}" == '100e33 Hz'
        assert f"{Quantity(1e34, 'Hz')}" == '10e33 Hz'
        assert f"{Quantity(1e33, 'Hz')}" == '1e33 Hz'
        assert f"{Quantity(1e32, 'Hz')}" == '100e30 Hz'
        assert f"{Quantity(1e31, 'Hz')}" == '10e30 Hz'
        assert f"{Quantity(1e30, 'Hz')}" == '1e30 Hz'
        assert f"{Quantity(1e29, 'Hz')}" == '100e27 Hz'
        assert f"{Quantity(1e28, 'Hz')}" == '10e27 Hz'
        assert f"{Quantity(1e27, 'Hz')}" == '1e27 Hz'
        assert f"{Quantity(1e26, 'Hz')}" == '100 YHz'
        assert f"{Quantity(1e25, 'Hz')}" == '10 YHz'
        assert f"{Quantity(1e24, 'Hz')}" == '1 YHz'
        assert f"{Quantity(1e23, 'Hz')}" == '100 ZHz'
        assert f"{Quantity(1e22, 'Hz')}" == '10 ZHz'
        assert f"{Quantity(1e21, 'Hz')}" == '1 ZHz'
        assert f"{Quantity(1e20, 'Hz')}" == '100 EHz'
        assert f"{Quantity(1e19, 'Hz')}" == '10 EHz'
        assert f"{Quantity(1e18, 'Hz')}" == '1 EHz'
        assert f"{Quantity(1e17, 'Hz')}" == '100 PHz'
        assert f"{Quantity(1e16, 'Hz')}" == '10 PHz'
        assert f"{Quantity(1e15, 'Hz')}" == '1 PHz'
        assert f"{Quantity(1e14, 'Hz')}" == '100 THz'
        assert f"{Quantity(1e13, 'Hz')}" == '10 THz'
        assert f"{Quantity(1e12, 'Hz')}" == '1 THz'
        assert f"{Quantity(1e11, 'Hz')}" == '100 GHz'
        assert f"{Quantity(1e10, 'Hz')}" == '10 GHz'
        assert f"{Quantity(1e9, 'Hz')}" == '1 GHz'
        assert f"{Quantity(1e8, 'Hz')}" == '100 MHz'
        assert f"{Quantity(1e7, 'Hz')}" == '10 MHz'
        assert f"{Quantity(1e6, 'Hz')}" == '1 MHz'
        assert f"{Quantity(1e5, 'Hz')}" == '100 kHz'
        assert f"{Quantity(1e4, 'Hz')}" == '10 kHz'
        assert f"{Quantity(1e3, 'Hz')}" == '1 kHz'
        assert f"{Quantity(1e2, 'Hz')}" == '100 Hz'
        assert f"{Quantity(1e1, 'Hz')}" == '10 Hz'
        assert f"{Quantity(1e0, 'Hz')}" == '1 Hz'
        assert f"{Quantity(1e-1, 'Hz')}" == '100 mHz'
        assert f"{Quantity(1e-2, 'Hz')}" == '10 mHz'
        assert f"{Quantity(1e-3, 'Hz')}" == '1 mHz'
        assert f"{Quantity(1e-4, 'Hz')}" == '100 uHz'
        assert f"{Quantity(1e-5, 'Hz')}" == '10 uHz'
        assert f"{Quantity(1e-6, 'Hz')}" == '1 uHz'
        assert f"{Quantity(1e-7, 'Hz')}" == '100 nHz'
        assert f"{Quantity(1e-8, 'Hz')}" == '10 nHz'
        assert f"{Quantity(1e-9, 'Hz')}" == '1 nHz'
        assert f"{Quantity(1e-10, 'Hz')}" == '100 pHz'
        assert f"{Quantity(1e-11, 'Hz')}" == '10 pHz'
        assert f"{Quantity(1e-12, 'Hz')}" == '1 pHz'
        assert f"{Quantity(1e-13, 'Hz')}" == '100 fHz'
        assert f"{Quantity(1e-14, 'Hz')}" == '10 fHz'
        assert f"{Quantity(1e-15, 'Hz')}" == '1 fHz'
        assert f"{Quantity(1e-16, 'Hz')}" == '100 aHz'
        assert f"{Quantity(1e-17, 'Hz')}" == '10 aHz'
        assert f"{Quantity(1e-18, 'Hz')}" == '1 aHz'
        assert f"{Quantity(1e-19, 'Hz')}" == '100 zHz'
        assert f"{Quantity(1e-20, 'Hz')}" == '10 zHz'
        assert f"{Quantity(1e-21, 'Hz')}" == '1 zHz'
        assert f"{Quantity(1e-22, 'Hz')}" == '100 yHz'
        assert f"{Quantity(1e-23, 'Hz')}" == '10 yHz'
        assert f"{Quantity(1e-24, 'Hz')}" == '1 yHz'
        assert f"{Quantity(1e-25, 'Hz')}" == '100e-27 Hz'
        assert f"{Quantity(1e-26, 'Hz')}" == '10e-27 Hz'
        assert f"{Quantity(1e-27, 'Hz')}" == '1e-27 Hz'
        assert f"{Quantity(1e-28, 'Hz')}" == '100e-30 Hz'
        assert f"{Quantity(1e-29, 'Hz')}" == '10e-30 Hz'
        assert f"{Quantity(1e-30, 'Hz')}" == '1e-30 Hz'
        assert f"{Quantity(1e-31, 'Hz')}" == '100e-33 Hz'
        assert f"{Quantity(1e-32, 'Hz')}" == '10e-33 Hz'
        assert f"{Quantity(1e-33, 'Hz')}" == '1e-33 Hz'

    with Quantity.prefs(output_sf = None):
        q=Quantity('c')
        assert f"{Quantity(1e35, 'Hz')}" == '100e33 Hz'
        assert f"{Quantity(1e34, 'Hz')}" == '10e33 Hz'
        assert f"{Quantity(1e33, 'Hz')}" == '1e33 Hz'
        assert f"{Quantity(1e32, 'Hz')}" == '100e30 Hz'
        assert f"{Quantity(1e31, 'Hz')}" == '10e30 Hz'
        assert f"{Quantity(1e30, 'Hz')}" == '1e30 Hz'
        assert f"{Quantity(1e29, 'Hz')}" == '100e27 Hz'
        assert f"{Quantity(1e28, 'Hz')}" == '10e27 Hz'
        assert f"{Quantity(1e27, 'Hz')}" == '1e27 Hz'
        assert f"{Quantity(1e26, 'Hz')}" == '100e24 Hz'
        assert f"{Quantity(1e25, 'Hz')}" == '10e24 Hz'
        assert f"{Quantity(1e24, 'Hz')}" == '1e24 Hz'
        assert f"{Quantity(1e23, 'Hz')}" == '100e21 Hz'
        assert f"{Quantity(1e22, 'Hz')}" == '10e21 Hz'
        assert f"{Quantity(1e21, 'Hz')}" == '1e21 Hz'
        assert f"{Quantity(1e20, 'Hz')}" == '100e18 Hz'
        assert f"{Quantity(1e19, 'Hz')}" == '10e18 Hz'
        assert f"{Quantity(1e18, 'Hz')}" == '1e18 Hz'
        assert f"{Quantity(1e17, 'Hz')}" == '100e15 Hz'
        assert f"{Quantity(1e16, 'Hz')}" == '10e15 Hz'
        assert f"{Quantity(1e15, 'Hz')}" == '1e15 Hz'
        assert f"{Quantity(1e14, 'Hz')}" == '100 THz'
        assert f"{Quantity(1e13, 'Hz')}" == '10 THz'
        assert f"{Quantity(1e12, 'Hz')}" == '1 THz'
        assert f"{Quantity(1e11, 'Hz')}" == '100 GHz'
        assert f"{Quantity(1e10, 'Hz')}" == '10 GHz'
        assert f"{Quantity(1e9, 'Hz')}" == '1 GHz'
        assert f"{Quantity(1e8, 'Hz')}" == '100 MHz'
        assert f"{Quantity(1e7, 'Hz')}" == '10 MHz'
        assert f"{Quantity(1e6, 'Hz')}" == '1 MHz'
        assert f"{Quantity(1e5, 'Hz')}" == '100 kHz'
        assert f"{Quantity(1e4, 'Hz')}" == '10 kHz'
        assert f"{Quantity(1e3, 'Hz')}" == '1 kHz'
        assert f"{Quantity(1e2, 'Hz')}" == '100 Hz'
        assert f"{Quantity(1e1, 'Hz')}" == '10 Hz'
        assert f"{Quantity(1e0, 'Hz')}" == '1 Hz'
        assert f"{Quantity(1e-1, 'Hz')}" == '100 mHz'
        assert f"{Quantity(1e-2, 'Hz')}" == '10 mHz'
        assert f"{Quantity(1e-3, 'Hz')}" == '1 mHz'
        assert f"{Quantity(1e-4, 'Hz')}" == '100 uHz'
        assert f"{Quantity(1e-5, 'Hz')}" == '10 uHz'
        assert f"{Quantity(1e-6, 'Hz')}" == '1 uHz'
        assert f"{Quantity(1e-7, 'Hz')}" == '100 nHz'
        assert f"{Quantity(1e-8, 'Hz')}" == '10 nHz'
        assert f"{Quantity(1e-9, 'Hz')}" == '1 nHz'
        assert f"{Quantity(1e-10, 'Hz')}" == '100 pHz'
        assert f"{Quantity(1e-11, 'Hz')}" == '10 pHz'
        assert f"{Quantity(1e-12, 'Hz')}" == '1 pHz'
        assert f"{Quantity(1e-13, 'Hz')}" == '100 fHz'
        assert f"{Quantity(1e-14, 'Hz')}" == '10 fHz'
        assert f"{Quantity(1e-15, 'Hz')}" == '1 fHz'
        assert f"{Quantity(1e-16, 'Hz')}" == '100 aHz'
        assert f"{Quantity(1e-17, 'Hz')}" == '10 aHz'
        assert f"{Quantity(1e-18, 'Hz')}" == '1 aHz'
        assert f"{Quantity(1e-19, 'Hz')}" == '100e-21 Hz'
        assert f"{Quantity(1e-20, 'Hz')}" == '10e-21 Hz'
        assert f"{Quantity(1e-21, 'Hz')}" == '1e-21 Hz'
        assert f"{Quantity(1e-22, 'Hz')}" == '100e-24 Hz'
        assert f"{Quantity(1e-23, 'Hz')}" == '10e-24 Hz'
        assert f"{Quantity(1e-24, 'Hz')}" == '1e-24 Hz'
        assert f"{Quantity(1e-25, 'Hz')}" == '100e-27 Hz'
        assert f"{Quantity(1e-26, 'Hz')}" == '10e-27 Hz'
        assert f"{Quantity(1e-27, 'Hz')}" == '1e-27 Hz'
        assert f"{Quantity(1e-28, 'Hz')}" == '100e-30 Hz'
        assert f"{Quantity(1e-29, 'Hz')}" == '10e-30 Hz'
        assert f"{Quantity(1e-30, 'Hz')}" == '1e-30 Hz'
        assert f"{Quantity(1e-31, 'Hz')}" == '100e-33 Hz'
        assert f"{Quantity(1e-32, 'Hz')}" == '10e-33 Hz'
        assert f"{Quantity(1e-33, 'Hz')}" == '1e-33 Hz'

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
