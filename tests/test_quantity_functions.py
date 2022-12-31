from quantiphy import (
    as_real, as_tuple, render, fixed, binary,
    UnitConversion, QuantiPhyError,
)
from pytest import approx, fixture, raises

def test_as_real():
    UnitConversion('g', 'lb lbs', 453.59237)
    assert as_real('2 lbs') == approx(2)
    assert as_real('2 lbs', scale='lb') == approx(2)
    assert as_real('2 lbs', scale='g') == approx(907.18474)
    assert as_real('2 lbs', scale='kg') == approx(0.90718474)
    assert as_real('1000 g', scale='kg') == approx(1)
    assert as_real('1 Mg', scale='g') == approx(1_000_000)
    assert as_real('1 Mg', scale='kg') == approx(1_000)

def test_as_tuple():
    UnitConversion('g', 'lb lbs', 453.59237)
    assert as_tuple('2 lbs') == approx((2, 'lbs'))
    assert as_tuple('2 lbs', scale='lb') == approx((2, 'lb'))
    assert as_tuple('2 lbs', scale='g') == approx((907.18474, 'g'))
    assert as_tuple('2 lbs', scale='kg') == approx((0.90718474, 'kg'))
    assert as_tuple('1000 g', scale='kg') == approx((1, 'kg'))
    assert as_tuple('1 Mg', scale='g') == approx((1_000_000, 'g'))
    assert as_tuple('1 Mg', scale='kg') == approx((1_000, 'kg'))

def test_render():
    UnitConversion('g', 'lb lbs', 453.59237)
    assert render(2, 'lbs') == '2 lbs'
    assert render(2, 'lbs', scale='lb') == '2 lb'
    assert render(2, 'lbs', scale='g') == '907.18 g'
    assert render(2, 'lbs', scale='kg') == '907.18 mkg'
    assert render(1000, 'g', scale='kg') == '1 kg'
    assert render(1e6, 'g') == '1 Mg'
    assert render(1e6, 'g', scale='g') == '1 Mg'
    assert render(1e6, 'g', scale='kg') == '1 kkg'
    assert render(1, 'Mg', scale='g') == '1 Mg'
    assert render(1, 'Mg', scale='kg') == '1 kkg'

def test_fixed():
    UnitConversion('g', 'lb lbs', 453.59237)
    assert fixed(2, 'lbs') == '2 lbs'
    assert fixed(2, 'lbs', scale='lb') == '2 lb'
    assert fixed(2, 'lbs', scale='g') == '907.1847 g'
    assert fixed(2, 'lbs', scale='kg') == '0.9072 kg'
    assert fixed(1000, 'g', scale='kg') == '1 kg'
    assert fixed(1, 'Mg', scale='g', show_commas=True) == '1,000,000 g'
    assert fixed(1, 'Mg', scale='kg', show_commas=True) == '1,000 kg'
    assert fixed(1e6, 'g', scale='g', show_commas=True) == '1,000,000 g'
    assert fixed(1e6, 'g', scale='kg', show_commas=True) == '1,000 kg'

def test_binary():
    UnitConversion('b', 'B', 8)
    assert binary(2, 'B') == '2 B'
    assert binary(2, 'B', scale='b') == '16 b'
    assert binary(2, 'b', scale='B') == '0.25 B'
    assert binary(2048, 'B') == '2 KiB'
    assert binary(2048, 'B', scale='b') == '16 Kib'
