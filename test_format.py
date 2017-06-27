# encoding: utf8

from __future__ import unicode_literals
from quantiphy import Quantity
import sys

def test_format():
    Quantity.set_prefs(spacer=' ', label_fmt=None)
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
    assert '{:f}'.format(q) == '1420405751.7860'
    assert '{:F}'.format(q) == 'f = 1420405751.7860'
    assert '{:e}'.format(q) == '1.4204e+09'
    assert '{:E}'.format(q) == 'f = 1.4204e+09'
    assert '{:g}'.format(q) == '1.4204e+09'
    assert '{:G}'.format(q) == 'f = 1.4204e+09'
    assert '{:n}'.format(q) == 'f'
    assert '{:d}'.format(q) == 'frequency of hydrogen line'
    assert '{:X}'.format(q) == '1.4204 GHz'

    q=Quantity('2ns')
    assert float(q) == 2e-9

def test_full_format():
    Quantity.set_prefs(spacer=' ', label_fmt=None, prec='full')
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
    assert '{:.4f}'.format(q) == '1420405751.7860'
    assert '{:.4F}'.format(q) == 'f = 1420405751.7860'
    assert '{:e}'.format(q) == '1.420405751786e+09'
    assert '{:E}'.format(q) == 'f = 1.420405751786e+09'
    assert '{:g}'.format(q) == '1420405751.786'
    assert '{:G}'.format(q) == 'f = 1420405751.786'
    assert '{:n}'.format(q) == 'f'
    assert '{:d}'.format(q) == 'frequency of hydrogen line'
    assert '{:X}'.format(q) == '1.420405751786 GHz'

    q=Quantity('2ns')
    assert float(q) == 2e-9

def test_scaled_format():
    Quantity.set_prefs(spacer=' ', label_fmt=None, prec=None)
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
    assert '{:f°F}'.format(q) == '212.0000'
    assert '{:F°F}'.format(q) == 'Tboil = 212.0000'
    assert '{:e°F}'.format(q) == '2.1200e+02'
    assert '{:E°F}'.format(q) == 'Tboil = 2.1200e+02'
    assert '{:g°F}'.format(q) == '212'
    assert '{:G°F}'.format(q) == 'Tboil = 212'
    assert '{:n°F}'.format(q) == 'Tboil'
    assert '{:d°F}'.format(q) == 'boiling point of water'
    assert '{:X°F}'.format(q) == '100 °C'
