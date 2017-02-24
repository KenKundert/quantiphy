# encoding: utf8

from quantiphy import Quantity

def test_constants():
    Quantity.set_preferences(spacer=' ', label_fmt='{n} = {v} -- {d}')
    assert '{:.12q}'.format(Quantity('h')) == '662.606957e-36 J-s'
    assert '{:.12q}'.format(Quantity('hbar')) == '105.4571725336e-36 J-s'
    assert '{:.12q}'.format(Quantity('k')) == '13.806488e-24 J/K'
    assert '{:.12q}'.format(Quantity('q')) == '160.2176565e-21 C'
    assert '{:.12q}'.format(Quantity('c')) == '299.792458 Mm/s'
    assert '{:.12q}'.format(Quantity('0C')) == '273.15 K'
    assert '{:.12q}'.format(Quantity('eps0')) == '8.854187817 pF/m'
    assert '{:.12q}'.format(Quantity('mu0')) == '1.256637061436 uH/m'
    assert '{:.12q}'.format(Quantity('Z0')) == '376.730313461 Ohms'

    assert str(Quantity('h')) == '662.61e-36 J-s'
    assert str(Quantity('hbar')) == '105.46e-36 J-s'
    assert str(Quantity('k')) == '13.806e-24 J/K'
    assert str(Quantity('q')) == '160.22e-21 C'
    assert str(Quantity('c')) == '299.79 Mm/s'
    assert str(Quantity('0C')) == '273.15 K'
    assert str(Quantity('eps0')) == '8.8542 pF/m'
    assert str(Quantity('mu0')) == '1.2566 uH/m'
    assert str(Quantity('Z0')) == '376.73 Ohms'

    assert '{:S}'.format(Quantity('h')) == "h = 662.61e-36 J-s -- Plank's constant"
    assert '{:S}'.format(Quantity('hbar')) == "ħ = 105.46e-36 J-s -- reduced Plank's constant"
    assert '{:S}'.format(Quantity('k')) == "k = 13.806e-24 J/K -- Boltzmann's constant"
    assert '{:S}'.format(Quantity('q')) == 'q = 160.22e-21 C -- elementary charge'
    assert '{:S}'.format(Quantity('c')) == 'c = 299.79 Mm/s -- speed of light'
    assert '{:S}'.format(Quantity('0C')) == '0°C = 273.15 K -- zero degrees Celsius in Kelvin'
    assert '{:S}'.format(Quantity('eps0')) == 'ε₀ = 8.8542 pF/m -- permittivity of free space'
    assert '{:S}'.format(Quantity('mu0')) == 'μ₀ = 1.2566 uH/m -- permeability of free space'
    assert '{:S}'.format(Quantity('Z0')) == 'Z₀ = 376.73 Ohms -- characteristic impedance of free space'
