from quantiphy import Quantity

def test_format():
    Quantity.set_preferences(spacer=' ', assign_fmt=None)
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
