from quantiphy import (
    as_tuple,
    Quantity,
    QuantiPhyError,
    UnitConversion,
    UnknownConversion,
)
from pytest import approx, fixture, raises

@fixture
def initialize_preferences():
    Quantity.reset_prefs()

def test_rendering(initialize_preferences):
    preferred_units = {
        "Ω": "Ohm ohm Ohms ohms Ω",  # the capital Omega is preferred over unicode ohm symbol
        "℧": "Mho mho Mhos mhos Ʊ",  # the unicode inverted-omega is preferred over capital upisilon
    }
    with Quantity.prefs(preferred_units=preferred_units, known_units="Mho mho Mhos mhos"):

        assert Quantity.get_pref("preferred_units") == preferred_units

        q = Quantity('50 Ohm')
        assert q.units == 'Ohm'
        assert str(q) == '50 Ω'
        assert q.render() == '50 Ω'
        assert q.fixed() == '50 Ω'
        assert q.binary() == '50 Ω'

        q = Quantity('50 ohm')
        assert q.units == 'ohm'
        assert str(q) == '50 Ω'
        assert q.render() == '50 Ω'
        assert q.fixed() == '50 Ω'
        assert q.binary() == '50 Ω'

        q = Quantity('50 Ohms')
        assert q.units == 'Ohms'
        assert str(q) == '50 Ω'
        assert q.render() == '50 Ω'
        assert q.fixed() == '50 Ω'
        assert q.binary() == '50 Ω'

        q = Quantity('50 ohms')
        assert q.units == 'ohms'
        assert str(q) == '50 Ω'
        assert q.render() == '50 Ω'
        assert q.fixed() == '50 Ω'
        assert q.binary() == '50 Ω'

        q = Quantity('50 Ω')
        assert q.units == 'Ω'
        assert str(q) == '50 Ω'
        assert q.render() == '50 Ω'
        assert q.fixed() == '50 Ω'
        assert q.binary() == '50 Ω'

        q = Quantity('50 Mho')
        assert q.units == 'Mho'
        assert str(q) == '50 ℧'
        assert q.render() == '50 ℧'
        assert q.fixed() == '50 ℧'
        assert q.binary() == '50 ℧'

        q = Quantity('50 mho')
        assert q.units == 'mho'
        assert str(q) == '50 ℧'
        assert q.render() == '50 ℧'
        assert q.fixed() == '50 ℧'
        assert q.binary() == '50 ℧'

        q = Quantity('50 Mhos')
        assert q.units == 'Mhos'
        assert str(q) == '50 ℧'
        assert q.render() == '50 ℧'
        assert q.fixed() == '50 ℧'
        assert q.binary() == '50 ℧'

        q = Quantity('50 mhos')
        assert q.units == 'mhos'
        assert str(q) == '50 ℧'
        assert q.render() == '50 ℧'
        assert q.fixed() == '50 ℧'
        assert q.binary() == '50 ℧'

        q = Quantity('50 Ʊ')
        assert q.units == 'Ʊ'
        assert str(q) == '50 ℧'
        assert q.render() == '50 ℧'
        assert q.fixed() == '50 ℧'
        assert q.binary() == '50 ℧'
