# encoding: utf8

from quantiphy import (
    Quantity, add_constant, set_unit_system,
    QuantiPhyError, IncompatibleUnits, UnknownPreference, UnknownConversion,
    UnknownUnitSystem, InvalidRecognizer, UnknownScaleFactor, InvalidNumber,
    ExpectedQuantity, MissingName,
)
import pytest

def test_constants():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None)
    Quantity.set_prefs(show_desc=True)
    assert '{:.12q}'.format(Quantity('h')) == '662.607004e-36 J-s'
    assert '{:.12q}'.format(Quantity('hbar')) == '105.45718e-36 J-s'
    assert '{:.12q}'.format(Quantity('ħ')) == '105.45718e-36 J-s'
    assert '{:.12q}'.format(Quantity('k')) == '13.8064852e-24 J/K'
    assert '{:.12q}'.format(Quantity('q')) == '160.21766208e-21 C'
    assert '{:.12q}'.format(Quantity('c')) == '299.792458 Mm/s'
    assert '{:.12q}'.format(Quantity('0C')) == '273.15 K'
    assert '{:.12q}'.format(Quantity('eps0')) == '8.854187817 pF/m'
    assert '{:.12q}'.format(Quantity('mu0')) == '1.256637061436 uH/m'
    assert '{:.12q}'.format(Quantity('µ₀')) == '1.256637061436 uH/m' # uses micro
    assert '{:.12q}'.format(Quantity('μ₀')) == '1.256637061436 uH/m' # uses mu
    assert '{:.12q}'.format(Quantity('Z0')) == '376.730313461 Ohms'

    assert str(Quantity('h')) == '662.61e-36 J-s'
    assert str(Quantity('hbar')) == '105.46e-36 J-s'
    assert str(Quantity('ħ')) == '105.46e-36 J-s'
    assert str(Quantity('k')) == '13.806e-24 J/K'
    assert str(Quantity('q')) == '160.22e-21 C'
    assert str(Quantity('c')) == '299.79 Mm/s'
    assert str(Quantity('0C')) == '273.15 K'
    assert str(Quantity('eps0')) == '8.8542 pF/m'
    assert str(Quantity('mu0')) == '1.2566 uH/m'
    assert str(Quantity('µ₀')) == '1.2566 uH/m'  # uses micro
    assert str(Quantity('μ₀')) == '1.2566 uH/m'  # uses mu
    assert str(Quantity('Z0')) == '376.73 Ohms'

    assert '{:S}'.format(Quantity('h')) == "h = 662.61e-36 J-s -- Plank's constant"
    assert '{:S}'.format(Quantity('hbar')) == "ħ = 105.46e-36 J-s -- reduced Plank's constant"
    assert '{:S}'.format(Quantity('ħ')) == "ħ = 105.46e-36 J-s -- reduced Plank's constant"
    assert '{:S}'.format(Quantity('k')) == "k = 13.806e-24 J/K -- Boltzmann's constant"
    assert '{:S}'.format(Quantity('q')) == 'q = 160.22e-21 C -- elementary charge'
    assert '{:S}'.format(Quantity('c')) == 'c = 299.79 Mm/s -- speed of light'
    assert '{:S}'.format(Quantity('0C')) == '0°C = 273.15 K -- zero degrees Celsius in Kelvin'
    assert '{:S}'.format(Quantity('eps0')) == 'ε₀ = 8.8542 pF/m -- permittivity of free space'
    assert '{:S}'.format(Quantity('mu0')) == 'µ₀ = 1.2566 uH/m -- permeability of free space'
    assert '{:S}'.format(Quantity('µ₀')) == 'µ₀ = 1.2566 uH/m -- permeability of free space'  # uses micro
    assert '{:S}'.format(Quantity('μ₀')) == 'µ₀ = 1.2566 uH/m -- permeability of free space'  # uses mu
    assert '{:S}'.format(Quantity('Z0')) == 'Z₀ = 376.73 Ohms -- characteristic impedance of free space'

    set_unit_system('cgs')
    assert '{:.12q}'.format(Quantity('h')) == '6.62607004e-27 erg-s'
    assert '{:.12q}'.format(Quantity('hbar')) == '1.0545718e-27 erg-s'
    assert '{:.12q}'.format(Quantity('ħ')) == '1.0545718e-27 erg-s'
    assert '{:.12q}'.format(Quantity('k')) == '138.064852 aerg/K'
    assert '{:.12q}'.format(Quantity('q')) == '480.320425 pFr'
    assert '{:.12q}'.format(Quantity('c')) == '299.792458 Mm/s'
    assert '{:.12q}'.format(Quantity('0C')) == '273.15 K'

    assert str(Quantity('h')) == '6.6261e-27 erg-s'
    assert str(Quantity('hbar')) == '1.0546e-27 erg-s'
    assert str(Quantity('ħ')) == '1.0546e-27 erg-s'
    assert str(Quantity('k')) == '138.06 aerg/K'
    assert str(Quantity('q')) == '480.32 pFr'
    assert str(Quantity('c')) == '299.79 Mm/s'
    assert str(Quantity('0C')) == '273.15 K'

    with pytest.raises(ValueError) as exception:
        str(Quantity('fuzz'))
    assert str(exception.value) == 'fuzz: not a valid number.'
    assert isinstance(exception.value, InvalidNumber)
    assert isinstance(exception.value, QuantiPhyError)
    assert isinstance(exception.value, ValueError)
    assert exception.value.args == ('fuzz',)

    with pytest.raises(ValueError) as exception:
        str(Quantity(None))
    assert str(exception.value) == 'None: not a valid number.'
    assert isinstance(exception.value, InvalidNumber)
    assert isinstance(exception.value, QuantiPhyError)
    assert isinstance(exception.value, TypeError)
    assert exception.value.args == (None,)

    with pytest.raises(ValueError) as exception:
        str(Quantity(None, 'm', scale='in'))
    assert str(exception.value) == 'None: not a valid number.'
    assert isinstance(exception.value, InvalidNumber)
    assert isinstance(exception.value, QuantiPhyError)
    assert isinstance(exception.value, TypeError)
    assert exception.value.args == (None,)

    assert '{:S}'.format(Quantity('h')) == "h = 6.6261e-27 erg-s -- Plank's constant"
    assert '{:S}'.format(Quantity('hbar')) == "ħ = 1.0546e-27 erg-s -- reduced Plank's constant"
    assert '{:S}'.format(Quantity('ħ')) == "ħ = 1.0546e-27 erg-s -- reduced Plank's constant"
    assert '{:S}'.format(Quantity('k')) == "k = 138.06 aerg/K -- Boltzmann's constant"
    assert '{:S}'.format(Quantity('q')) == 'q = 480.32 pFr -- elementary charge'
    assert '{:S}'.format(Quantity('c')) == 'c = 299.79 Mm/s -- speed of light'
    assert '{:S}'.format(Quantity('0C')) == '0°C = 273.15 K -- zero degrees Celsius in Kelvin'

    set_unit_system('mks')
    assert '{:.12q}'.format(Quantity('h')) == '662.607004e-36 J-s'
    assert '{:.12q}'.format(Quantity('hbar')) == '105.45718e-36 J-s'
    assert '{:.12q}'.format(Quantity('ħ')) == '105.45718e-36 J-s'
    assert '{:.12q}'.format(Quantity('k')) == '13.8064852e-24 J/K'
    assert '{:.12q}'.format(Quantity('q')) == '160.21766208e-21 C'
    assert '{:.12q}'.format(Quantity('c')) == '299.792458 Mm/s'
    assert '{:.12q}'.format(Quantity('0C')) == '273.15 K'
    assert '{:.12q}'.format(Quantity('eps0')) == '8.854187817 pF/m'
    assert '{:.12q}'.format(Quantity('mu0')) == '1.256637061436 uH/m'
    assert '{:.12q}'.format(Quantity('µ₀')) == '1.256637061436 uH/m'  # uses micro
    assert '{:.12q}'.format(Quantity('μ₀')) == '1.256637061436 uH/m'  # uses mu
    assert '{:.12q}'.format(Quantity('Z0')) == '376.730313461 Ohms'

    assert str(Quantity('h')) == '662.61e-36 J-s'
    assert str(Quantity('hbar')) == '105.46e-36 J-s'
    assert str(Quantity('ħ')) == '105.46e-36 J-s'
    assert str(Quantity('k')) == '13.806e-24 J/K'
    assert str(Quantity('q')) == '160.22e-21 C'
    assert str(Quantity('c')) == '299.79 Mm/s'
    assert str(Quantity('0C')) == '273.15 K'
    assert str(Quantity('eps0')) == '8.8542 pF/m'
    assert str(Quantity('mu0')) == '1.2566 uH/m'
    assert str(Quantity('µ₀')) == '1.2566 uH/m'  # uses micro
    assert str(Quantity('μ₀')) == '1.2566 uH/m'  # uses mu
    assert str(Quantity('Z0')) == '376.73 Ohms'

    assert '{:S}'.format(Quantity('h')) == "h = 662.61e-36 J-s -- Plank's constant"
    assert '{:S}'.format(Quantity('hbar')) == "ħ = 105.46e-36 J-s -- reduced Plank's constant"
    assert '{:S}'.format(Quantity('ħ')) == "ħ = 105.46e-36 J-s -- reduced Plank's constant"
    assert '{:S}'.format(Quantity('k')) == "k = 13.806e-24 J/K -- Boltzmann's constant"
    assert '{:S}'.format(Quantity('q')) == 'q = 160.22e-21 C -- elementary charge'
    assert '{:S}'.format(Quantity('c')) == 'c = 299.79 Mm/s -- speed of light'
    assert '{:S}'.format(Quantity('0C')) == '0°C = 273.15 K -- zero degrees Celsius in Kelvin'
    assert '{:S}'.format(Quantity('eps0')) == 'ε₀ = 8.8542 pF/m -- permittivity of free space'
    assert '{:S}'.format(Quantity('mu0')) == 'µ₀ = 1.2566 uH/m -- permeability of free space'
    assert '{:S}'.format(Quantity('µ₀')) == 'µ₀ = 1.2566 uH/m -- permeability of free space'  # uses micro
    assert '{:S}'.format(Quantity('μ₀')) == 'µ₀ = 1.2566 uH/m -- permeability of free space'  # uses mu
    assert '{:S}'.format(Quantity('Z0')) == 'Z₀ = 376.73 Ohms -- characteristic impedance of free space'

    add_constant('f_hy = 1420.405751786 MHz -- Frequency of hydrogen line')
    assert str(Quantity('f_hy')) == '1.4204 GHz'

    add_constant(Quantity('1420.405751786 MHz'), 'hline')
    assert str(Quantity('hline')) == '1.4204 GHz'
    add_constant(Quantity(4.80320427e-10, 'Fr'), 'q', 'esu gaussian')
    add_constant(Quantity(1.602176487e-20, 'abC'), alias='q', unit_systems='emu')
    assert str(Quantity('q')) == '160.22e-21 C'
    set_unit_system('cgs')
    assert str(Quantity('q')) == '480.32 pFr'
    set_unit_system('esu')
    assert str(Quantity('q')) == '480.32 pFr'
    set_unit_system('gaussian')
    assert str(Quantity('q')) == '480.32 pFr'
    set_unit_system('emu')
    assert str(Quantity('q')) == '16.022e-21 abC'
    set_unit_system('mks')

    with pytest.raises(NameError) as exception:
        add_constant(Quantity(4.80320427e-10, 'Fr'), unit_systems='esu gaussian')
    assert str(exception.value) == 'no name specified.'
    assert isinstance(exception.value, MissingName)
    assert isinstance(exception.value, QuantiPhyError)
    assert isinstance(exception.value, NameError)
    assert exception.value.args == ()

    with pytest.raises(ValueError) as exception:
        add_constant(1)
    assert str(exception.value) == 'expected a quantity for value.'
    assert isinstance(exception.value, ExpectedQuantity)
    assert isinstance(exception.value, QuantiPhyError)
    assert isinstance(exception.value, ValueError)
    assert exception.value.args == ()

    with pytest.raises(KeyError) as exception:
        set_unit_system('nuts')
    assert str(exception.value) == 'nuts: unknown unit system.'
    assert isinstance(exception.value, UnknownUnitSystem)
    assert isinstance(exception.value, QuantiPhyError)
    assert isinstance(exception.value, KeyError)
    assert exception.value.args == ('nuts',)

    add_constant(
        'f_hy = 1420.405751786 MHz', alias=['hl', 'HL', 'hydrogen line']
    )
    assert str(Quantity('f_hy')) == '1.4204 GHz'
    assert str(Quantity('hl')) == '1.4204 GHz'
    assert str(Quantity('HL')) == '1.4204 GHz'
    assert str(Quantity('hydrogen line')) == '1.4204 GHz'


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
