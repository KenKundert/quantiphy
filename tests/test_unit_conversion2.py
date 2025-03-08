from quantiphy import (
    as_tuple,
    Quantity,
    QuantiPhyError,
    UnitConversion,
    UnknownConversion,
)
import math
from pytest import approx, fixture, raises, mark
parametrize = mark.parametrize


# Utility functions {{{1
@fixture
def initialize_unit_conversions():
    UnitConversion.clear_all()
    Quantity.reset_prefs()

def test_2_lbs(initialize_unit_conversions):
    UnitConversion('g', 'lb lbs', 453.59237)
    assert as_tuple('2 lbs', scale='kg') == approx((0.90718474, 'kg'))
    assert Quantity('2 lbs', scale='kg').as_tuple() == approx((0.90718474, 'kg'))


def test_39_in(initialize_unit_conversions):
    UnitConversion('m', 'in inch inches', 0.0254)
    assert as_tuple('39.37 in', scale='cm') == approx((99.9998, 'cm'))
    assert Quantity('39.37 in', scale='cm').as_tuple() == approx((99.9998, 'cm'))

@UnitConversion.fixture
def from_molarity(M, mw):
    return M * mw

@UnitConversion.fixture
def to_molarity(g_L, mw):
    return g_L / mw

# these are modern scaling functions for Quantiphy.scale()
def from_dB_modern_scale(value):
    return 10**(value/20), value.units[2:]

def to_dB_modern_scale(value):
    return 20*math.log10(value), 'dB'+value.units

# these are modern scaling functions for UnitConversion
def from_dB_modern_uc(value):
    return 10**(value/20)

def to_dB_modern_uc(value):
    return 20*math.log10(value)

# these are deprecated scaling functions for Quantiphy.scale()
def from_dB_deprecated_scale(value, units):
    return 10**(value/20), units[2:]

def to_dB_deprecated_scale(value, units):
    return 20*math.log10(value), 'dB'+units


# test_converter() {{{1
def test_converter(initialize_unit_conversions):
    cc_L = UnitConversion('cc', 'L', 1000)
    assert str(cc_L) == 'cc ← 1000*L'

    volume = cc_L.convert(25, from_units='cc', to_units='uL').as_tuple()
    assert volume == approx((25_000, 'uL'))

    volume = cc_L.convert(25, from_units='mL', to_units='uL').as_tuple()
    assert volume == approx((25_000, 'uL'))

    volume = cc_L.convert(25, from_units='cc', to_units='mcc').as_tuple()
    assert volume == approx((25_000, 'mcc'))

    volume = cc_L.convert(25, from_units='mL', to_units='mcc').as_tuple()
    assert volume == approx((25_000, 'mcc'))

    with raises(UnknownConversion) as exception:
        cc_L.convert(25, from_units='cc', to_units='gallons')
    assert exception.value.args == ()
    assert exception.value.kwargs == dict(from_units='cc', to_units='gallons')
    assert str(exception.value) == 'unable to convert between ‘gallons’ and ‘cc’.'

    with raises(UnknownConversion) as exception:
        cc_L.convert(25, from_units='gallons', to_units='cc')
    assert exception.value.args == ()
    assert exception.value.kwargs == dict(from_units='gallons', to_units='cc')
    assert str(exception.value) == 'unable to convert between ‘cc’ and ‘gallons’.'

    with raises(UnknownConversion) as exception:
        cc_L.convert(25, from_units='L', to_units='gallons')
    assert exception.value.args == ()
    assert exception.value.kwargs == dict(from_units='L', to_units='gallons')
    assert str(exception.value) == 'unable to convert between ‘gallons’ and ‘L’.'

    with raises(UnknownConversion) as exception:
        cc_L.convert(25, from_units='gallons', to_units='L')
    assert exception.value.args == ()
    assert exception.value.kwargs == dict(from_units='gallons', to_units='L')
    assert str(exception.value) == 'unable to convert between ‘L’ and ‘gallons’.'

# test_differing_known_units() {{{1
def test_differing_known_units(initialize_unit_conversions):
    Quantity.set_prefs(known_units='cc')
    UnitConversion('cc', 'L', 1000)

    volume = as_tuple('100 cc', scale='L', ignore_sf=True)
    assert volume == approx((0.1, 'L'))

    volume = as_tuple('100 cc', scale='uL', ignore_sf=True)
    assert volume == approx((100000, 'uL'))

    volume = as_tuple('10 mL', scale='cc', ignore_sf=True)
    assert volume == approx((10, 'cc'))

    volume = as_tuple('100 uL', scale='mcc', ignore_sf=True)
    assert volume == approx((100, 'mcc'))

# test_same_unknown_units() {{{1
def test_same_unknown_units(initialize_unit_conversions):
    freq = as_tuple('100 Hz', scale='Hz', ignore_sf=True)
    assert freq == approx((100, 'Hz'))

    freq = as_tuple('100 Hz', scale='kHz', ignore_sf=True)
    assert freq == approx((0.1, 'kHz'))

    freq = as_tuple('10 kHz', scale='Hz', ignore_sf=True)
    assert freq == approx((10000, 'Hz'))

    freq = as_tuple('100 kHz', scale='MHz', ignore_sf=True)
    assert freq == approx((0.1, 'MHz'))

# test_exceptions() {{{1
def test_exceptions(initialize_unit_conversions):
    # unknown units case
    with raises(UnknownConversion) as exception:
        Quantity('100 Hz', scale='V')
    assert exception.value.args == ()
    assert exception.value.kwargs == dict(from_units='Hz', to_units='V')
    assert str(exception.value) == 'unable to convert between ‘V’ and ‘Hz’.'

    # known units case
    UnitConversion('m', 'in inch inches', 0.0254)
    UnitConversion('g', 'lb lbs', 453.59237)
    with raises(UnknownConversion) as exception:
        Quantity('1 kg', scale='m')
    assert exception.value.args == ()
    assert exception.value.kwargs == dict(from_units='g', to_units='m')
    assert str(exception.value) == 'unable to convert between ‘m’ and ‘g’.'


# test_molarity() {{{1
def test_molarity(initialize_unit_conversions):
    mol_conv = UnitConversion('g/L', 'M', from_molarity, to_molarity)

    assert as_tuple('1.2 mg/L', scale='uM', params=74.55) == approx((16.096579477, 'uM'))
    assert as_tuple('1.2 mg/L', scale='µM', params=74.55) == approx((16.096579477, 'µM'))

# test_cc() {{{1
def test_cc(initialize_unit_conversions):
    cc_L = UnitConversion('cc', 'L', 1000)
    assert str(cc_L) == 'cc ← 1000*L'
    assert cc_L.convert(25, from_units='cc', to_units='uL').as_tuple() == approx((25_000, 'uL'))
    assert cc_L.convert(25, from_units='mL', to_units='uL').as_tuple() == approx((25_000, 'uL'))
    assert cc_L.convert(25, from_units='cc', to_units='mcc').as_tuple() == approx((25_000, 'mcc'))
    assert cc_L.convert(25, from_units='mL', to_units='mcc').as_tuple() == approx((25_000, 'mcc'))

    Quantity.set_prefs(known_units='cc')
    assert as_tuple('0.25 L', scale='cc') == approx((250, 'cc'))
    assert as_tuple('25 mL', scale='cc') == approx((25, 'cc'))
    assert as_tuple('25 mcc', scale='uL', ignore_sf=True) == approx((25, 'uL'))
    assert as_tuple('25 cc', scale='mL') == approx((25, 'mL'))
    assert as_tuple('25 mcc', scale='L', ignore_sf=True) == approx((25e-6, 'L'))
    assert as_tuple('25 cc', scale='L') == approx((0.025, 'L'))

# test_scaling() {{{1
@parametrize(
    "value, to_units, expected", [
        ('10e6 s',   's',   '10,000,000 s'),   # same units no scale factor
        ('10e6 s',   'ks',  '10,000 ks'),      # same units with to scale factor
        ('10e3 ks',  's',   '10,000,000 s'),   # same units with from scale factor
        ('10e3 ks',  'Ms',  '10 Ms'),          # same units with to and from scale factor
        ('10e6 s',   'sec', '10,000,000 sec'), # equiv units no scale factor
        ('10e6 s',   'ksec','10,000 ksec'),    # equiv units with to scale factor
        ('10e3 ksec','s',   '10,000,000 s'),   # equiv units with from scale factor
        ('10e3 ksec','Ms',  '10 Ms'),          # equiv units with to and from scale factor
        ('10e6 sec', 's',   '10,000,000 s'),   # equiv units no scale factor
        ('10e6 sec', 'ks',  '10,000 ks'),      # equiv units with to scale factor
        ('10e3 ks',  'sec', '10,000,000 sec'), # equiv units with from scale factor
        ('10e3 ks',  'Msec','10 Msec'),        # equiv units with to and from scale factor
        ('10e6 x',   'x',   '10,000,000 x'),   # unknown units no scale factor
        ('10e6 x',   'kx',  '10,000 kx'),      # unknown units with to scale factor
        ('10e3 kx',  'x',   '10,000,000 x'),   # unknown units with from scale factor
        ('10e3 kx',  'Mx',  '10 Mx'),          # unknown units with to and from scale factor
        ('10e3 kx',  'My',  'ERR My✗kx'),      # incompatible units
        ('10e3 fuzz','buzz','10,000 buzz'),    # known units that start with a sf
        ('10e3 buzz','fuzz','10,000 fuzz'),    # known units that start with a sf
        ('10e3 fuzz','g',   'ERR g✗fuzz'),     # incompatible units, one starts with sf
        ('10e3 g',   'fuzz','ERR fuzz✗g'),     # incompatible units, other starts with sf
        ('10e6',     '',    '10,000,000'),       # no units no scale factor
        ('10e6',     'k',   '10,000 k'),         # no units with to scale factor
        ('10e3k',    '',    '10,000,000'),       # no units with from scale factor
        ('10e3k',    'M',   '10 M'),             # no units with to and from scale factor
    ]
)
def test_scaling(initialize_unit_conversions, value, to_units, expected):
    UnitConversion('s', 'sec second seconds')
    UnitConversion('g', 'lb lbs', 453.59237)
    UnitConversion("fuzz", "buzz")

    q = Quantity(value)
    try:
        scaled = q.scale(to_units)
        rendered = scaled.fixed(show_commas=True)
    except UnknownConversion as e:
        rendered = f"ERR {e.kwargs['to_units']}✗{e.kwargs['from_units']}"
    assert rendered == expected, q

# test_bin_unit_scaling() {{{1
def test_bin_unit_scaling(initialize_unit_conversions):
    q = Quantity('1 MiB', binary=True)
    assert q.render() == '1.0486 MB'
    assert q.scale('MiB').render() == '1 MiB'
    assert q.render(scale='MiB') == '1 MiB'
    assert q.binary() == '1 MiB'
    assert q.fixed(scale='MiB') == '1 MiB'
    assert q.fixed(scale='KiB') == '1024 KiB'

# test_enable_sf_scaling() {{{1
def test_enable_sf_scaling(initialize_unit_conversions):
    q = Quantity('1 MiB', binary=True)
    assert q.as_tuple() == (1048576.0, 'B')
    scaled = q.scale('KiB')
    assert scaled.as_tuple() == (1024, 'KiB')
    scaled = q.scale('MB')
    assert scaled.as_tuple() == (1.048576, 'MB')

    UnitConversion.enable_sf_scaling(bin_scaling=False)
    with raises(UnknownConversion) as exception:
        scaled = q.scale('KiB')

    UnitConversion.enable_sf_scaling(si_scaling=False)
    with raises(UnknownConversion) as exception:
        scaled = q.scale('MB')

    UnitConversion.enable_sf_scaling(bin_scaling=True)
    scaled = q.scale('KiB')
    assert scaled.as_tuple() == (1024, 'KiB')

    UnitConversion.enable_sf_scaling(si_scaling=True)
    scaled = q.scale('MB')
    assert scaled.as_tuple() == (1.048576, 'MB')

# test_deprecated_scaling_functions() {{{1
def test_deprecated_scaling_functions(initialize_unit_conversions):
    # first test modern functions for Quantity.scale()
    dBV = Quantity('-40 dBV')
    assert dBV.scale(from_dB_modern_scale).render() == '10 mV'
    V = Quantity('10 mV')
    assert V.scale(to_dB_modern_scale).render() == '-40 dBV'

    # assure these functions can also be passed to UnitConversion
    converter = UnitConversion('V', 'dBV', from_dB_modern_scale, to_dB_modern_scale)
    assert converter.convert(dBV).render() == '10 mV'
    assert converter.convert(V).render() == '-40 dBV'

    # second test modern functions for UnitConversion
    dBV = Quantity('-40 dBV')
    V = Quantity('10 mV')

    # assure these functions can also be passed to UnitConversion
    converter = UnitConversion('V', 'dBV', from_dB_modern_uc, to_dB_modern_uc)
    assert converter.convert(dBV).render() == '10 mV'
    assert converter.convert(V).render() == '-40 dBV'

    # third test deprecated functions for Quantity.scale()
    dBV = Quantity('-40 dBV')
    assert dBV.scale(from_dB_deprecated_scale).render() == '10 mV'
    V = Quantity('10 mV')
    assert V.scale(to_dB_deprecated_scale).render() == '-40 dBV'

    # assure these functions can also be passed to UnitConversion
    converter = UnitConversion('V', 'dBV', from_dB_deprecated_scale, to_dB_deprecated_scale)
    assert converter.convert(dBV).render() == '10 mV'
    assert converter.convert(V).render() == '-40 dBV'
