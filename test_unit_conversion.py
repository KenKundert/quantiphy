# encoding: utf8

from quantiphy import Quantity
import math
import sys
import pytest

def test_simple_scaling():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None)
    q=Quantity('1kg')
    assert q.render() == '1 kg'
    assert q.render(scale=0.001, show_units=False) == '1'
    with pytest.raises(KeyError, message="Unable to convert between 'fuzz' and 'g'."):
        q.render(scale='fuzz')

    q=Quantity('1', units='g', scale=1000)
    assert q.render() == '1 kg'
    assert q.render(scale=(0.0022046, 'lbs')) == '2.2046 lbs'

    q=Quantity('1', scale=(1000, 'g'))
    assert q.render() == '1 kg'
    assert q.render(scale=lambda v, u: (0.0022046*v, 'lbs')) == '2.2046 lbs'

    def dB(v, u):
        return 20*math.log(v, 10), 'dB'+u

    def adB(v, u):
        return pow(10, v/20), u[2:] if u.startswith('dB') else u

    q=Quantity('-40 dBV', scale=adB)
    assert q.render() == '10 mV'
    assert q.render(scale=dB) == '-40 dBV'

def test_temperature():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None)
    Quantity.set_prefs(ignore_sf=True)
    if sys.version_info.major == 3:
        q=Quantity('100 °C')
        assert q.render() == '100 °C'
        assert q.render(scale='C') == '100 C'
        assert q.render(scale='°C') == '100 °C'
        assert q.render(scale='K') == '373.15 K'
        assert q.render(scale='°F') == '212 °F'
        assert q.render(scale='F') == '212 F'
        assert q.render(scale='°R') == '671.67 °R'
        assert q.render(scale='R') == '671.67 R'

    q=Quantity('100 C')
    assert q.render() == '100 C'
    assert q.render(scale='C') == '100 C'
    assert q.render(scale='K') == '373.15 K'
    assert q.render(scale='F') == '212 F'
    assert q.render(scale='R') == '671.67 R'
    if sys.version_info.major == 3:
        assert q.render(scale='°C') == '100 °C'
        assert q.render(scale='°F') == '212 °F'
        assert q.render(scale='°R') == '671.67 °R'

    q=Quantity('373.15 K')
    assert q.render() == '373.15 K'
    assert q.render(scale='C') == '100 C'
    assert q.render(scale='K') == '373.15 K'
    assert q.render(scale='F') == '212 F'
    assert q.render(scale='R') == '671.67 R'
    if sys.version_info.major == 3:
        assert q.render(scale='°C') == '100 °C'
        assert q.render(scale='°F') == '212 °F'
        assert q.render(scale='°R') == '671.67 °R'

    if sys.version_info.major == 3:
        q=Quantity('212 °F')
        assert q.render() == '212 °F'
        assert q.render(scale='°C') == '100 °C'
        assert q.render(scale='C') == '100 C'
        assert q.render(scale='K') == '373.15 K'
        #assert q.render(scale='°F') == '212 °F'
        #assert q.render(scale='F') == '212 F'
        #assert q.render(scale='°R') == '671.67 °R'
        #assert q.render(scale='R') == '671.67 R'

    q=Quantity('212 F')
    assert q.render() == '212 F'
    assert q.render(scale='C') == '100 C'
    assert q.render(scale='K') == '373.15 K'
    if sys.version_info.major == 3:
        assert q.render(scale='°C') == '100 °C'
        #assert q.render(scale='°F') == '212 °F'
        #assert q.render(scale='F') == '212 F'
        #assert q.render(scale='°R') == '671.67 °R'
        #assert q.render(scale='R') == '671.67 R'

    if sys.version_info.major == 3:
        q=Quantity('100 °C', scale='K')
        assert q.render() == '373.15 K'

        q=Quantity('212 °F', scale='K')
        assert q.render() == '373.15 K'

        q=Quantity('212 °F', scale='C')
        assert q.render() == '100 C'

        q=Quantity('212 F', scale='°C')
        assert q.render() == '100 °C'

        q=Quantity('491.67 R', scale='°C')
        assert q.is_close(Quantity('0 °C'))

    q=Quantity('491.67 R', scale='K')
    assert q.render() == '273.15 K'

def test_distance():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None)
    Quantity.set_prefs(ignore_sf=False)
    q=Quantity('1_m')
    assert q.render() == '1 m'
    assert q.render(scale='cm', show_si=False) == '100 cm'
    assert q.render(scale='mm', show_si=False) == '1e3 mm'
    assert q.render(scale='um', show_si=False) == '1e6 um'
    assert q.render(scale='μm', show_si=False) == '1e6 μm'
    assert q.render(scale='nm', show_si=False) == '1e9 nm'
    if sys.version_info.major == 3:
        assert q.render(scale='Å', show_si=False) == '10e9 Å'
    assert q.render(scale='angstrom', show_si=False) == '10e9 angstrom'
    assert q.render(scale='mi') == '621.37 umi'
    assert q.render(scale='mile') == '621.37 umile'
    assert q.render(scale='miles') == '621.37 umiles'

    q=Quantity('1_m')
    assert q.render() == '1 m'

    q=Quantity('100cm', scale='m')
    assert q.render() == '1 m'

    q=Quantity('1cm', scale='m')
    assert q.render() == '10 mm'

    q=Quantity('1000mm', scale='m')
    assert q.render() == '1 m'

    q=Quantity('1mm', scale='m')
    assert q.render() == '1 mm'

    q=Quantity('1000000um', scale='m')
    assert q.render() == '1 m'

    q=Quantity('1um', scale='m')
    assert q.render() == '1 um'

    if sys.version_info.major == 3:
        q=Quantity('1000000μm', scale='m')
        assert q.render() == '1 m'

        q=Quantity('1μm', scale='m')
        assert q.render() == '1 um'

    q=Quantity('1000000000nm', scale='m')
    assert q.render() == '1 m'

    q=Quantity('1nm', scale='m')
    assert q.render() == '1 nm'

    if sys.version_info.major == 3:
        q=Quantity('10000000000Å', scale='m')
        assert q.render() == '1 m'

        q=Quantity('1Å', scale='m')
        assert q.render() == '100 pm'

    q=Quantity('1_mi', scale='m')
    assert q.render() == '1.6093 km'

    q=Quantity('1_mile', scale='m')
    assert q.render() == '1.6093 km'

    q=Quantity('1_miles', scale='m')
    assert q.render() == '1.6093 km'

    q=Quantity('d = 93 Mmiles  -- average distance from Sun to Earth', scale='m')
    assert q.render() == '149.67 Gm'

def test_mass():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None)
    Quantity.set_prefs(ignore_sf=False)
    q=Quantity('1 g')
    assert q.render() == '1 g'
    assert q.render(scale='oz') == '35.274 moz'
    assert q.render(scale='lb') == '2.2046 mlb'
    assert q.render(scale='lbs') == '2.2046 mlbs'

    q=Quantity('1 oz', scale='g')
    assert q.render() == '28.35 g'

    q=Quantity('1 lb', scale='g')
    assert q.render() == '453.59 g'

    q=Quantity('1 lbs', scale='g')
    assert q.render() == '453.59 g'

def test_time():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None)
    Quantity.set_prefs(ignore_sf=True)
    q=Quantity('86400 s')
    assert q.render() == '86.4 ks'
    assert q.render(scale='sec') == '86.4 ksec'
    assert q.render(scale='min') == '1.44 kmin'
    assert q.render(scale='hr') == '24 hr'
    assert q.render(scale='hour') == '24 hour'
    assert q.render(scale='day') == '1 day'

    q=Quantity('1 day', scale='s')
    assert q.render() == '86.4 ks'

    q=Quantity('24 hour', scale='s')
    assert q.render() == '86.4 ks'

    q=Quantity('24 hr', scale='s')
    assert q.render() == '86.4 ks'

    q=Quantity('60 min', scale='s')
    assert q.render() == '3.6 ks'

    q=Quantity('60 sec', scale='s')
    assert q.render() == '60 s'
