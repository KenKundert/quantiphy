from quantiphy import (
    as_tuple,
    Quantity,
    QuantiPhyError,
    UnitConversion,
    UnknownConversion,
)
from pytest import approx, fixture, raises, mark
parametrize = mark.parametrize


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

def test_same_unknown_units(initialize_unit_conversions):
    freq = as_tuple('100 Hz', scale='Hz', ignore_sf=True)
    assert freq == approx((100, 'Hz'))

    freq = as_tuple('100 Hz', scale='kHz', ignore_sf=True)
    assert freq == approx((0.1, 'kHz'))

    freq = as_tuple('10 kHz', scale='Hz', ignore_sf=True)
    assert freq == approx((10000, 'Hz'))

    freq = as_tuple('100 kHz', scale='MHz', ignore_sf=True)
    assert freq == approx((0.1, 'MHz'))

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


def test_molarity(initialize_unit_conversions):
    mol_conv = UnitConversion('g/L', 'M', from_molarity, to_molarity)

    assert as_tuple('1.2 mg/L', scale='uM', params=74.55) == approx((16.096579477, 'uM'))
    assert as_tuple('1.2 mg/L', scale='µM', params=74.55) == approx((16.096579477, 'µM'))

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
    ]
)
def test_scaling( initialize_unit_conversions, value, to_units, expected):
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
