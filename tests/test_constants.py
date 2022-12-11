# encoding: utf8

from quantiphy import (
    Quantity, add_constant, set_unit_system,
    QuantiPhyError, IncompatibleUnits, UnknownPreference, UnknownConversion,
    UnknownUnitSystem, InvalidRecognizer, UnknownScaleFactor, InvalidNumber,
    ExpectedQuantity, MissingName,
)
import pytest

def test_constants():
    Quantity.reset_prefs()
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None)
    Quantity.set_prefs(show_desc=True)
    assert '{:.12q}'.format(Quantity('h')) == '662.607015e-36 J-s'
    assert '{:.12q}'.format(Quantity('hbar')) == '105.4571817e-36 J-s'
    assert '{:.12q}'.format(Quantity('ħ')) == '105.4571817e-36 J-s'
    assert '{:.12q}'.format(Quantity('k')) == '13.80649e-24 J/K'
    assert '{:.12q}'.format(Quantity('q')) == '160.2176634e-21 C'
    assert '{:.12q}'.format(Quantity('c')) == '299.792458 Mm/s'
    assert '{:.12q}'.format(Quantity('0C')) == '273.15 K'
    assert '{:.12q}'.format(Quantity('ε₀')) == '8.8541878128 pF/m'
    assert '{:.12q}'.format(Quantity('eps0')) == '8.8541878128 pF/m'
    assert '{:.12q}'.format(Quantity('mu0')) == '1.25663706212 uH/m'
    assert '{:.12q}'.format(Quantity('µ₀')) == '1.25663706212 uH/m' # uses micro
    assert '{:.12q}'.format(Quantity('μ₀')) == '1.25663706212 uH/m' # uses mu
    assert '{:.12q}'.format(Quantity('Z0')) == '376.730313668 Ohms'

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

    assert '{:S}'.format(Quantity('h')) == "h = 662.61e-36 J-s — Plank's constant"
    assert '{:S}'.format(Quantity('hbar')) == "ħ = 105.46e-36 J-s — reduced Plank's constant"
    assert '{:S}'.format(Quantity('ħ')) == "ħ = 105.46e-36 J-s — reduced Plank's constant"
    assert '{:S}'.format(Quantity('k')) == "k = 13.806e-24 J/K — Boltzmann's constant"
    assert '{:S}'.format(Quantity('q')) == 'q = 160.22e-21 C — elementary charge'
    assert '{:S}'.format(Quantity('c')) == 'c = 299.79 Mm/s — speed of light'
    assert '{:S}'.format(Quantity('0C')) == '0°C = 273.15 K — zero degrees Celsius'
    assert '{:S}'.format(Quantity('eps0')) == 'ε₀ = 8.8542 pF/m — permittivity of free space'
    assert '{:S}'.format(Quantity('mu0')) == 'µ₀ = 1.2566 uH/m — permeability of free space'
    assert '{:S}'.format(Quantity('µ₀')) == 'µ₀ = 1.2566 uH/m — permeability of free space'  # uses micro
    assert '{:S}'.format(Quantity('μ₀')) == 'µ₀ = 1.2566 uH/m — permeability of free space'  # uses mu
    assert '{:S}'.format(Quantity('Z0')) == 'Z₀ = 376.73 Ohms — characteristic impedance of free space'

    assert Quantity('h').render(prec='full') == '662.607015e-36 J-s'
    assert Quantity('hbar').render(prec='full') == '105.4571817e-36 J-s'
    assert Quantity('ħ').render(prec='full') == '105.4571817e-36 J-s'
    assert Quantity('k').render(prec='full') == '13.80649e-24 J/K'
    assert Quantity('q').render(prec='full') == '160.2176634e-21 C'
    assert Quantity('c').render(prec='full') == '299.792458 Mm/s'
    assert Quantity('0C').render(prec='full') == '273.15 K'
    assert Quantity('ε₀').render(prec='full') == '8.8541878128 pF/m'
    assert Quantity('eps0').render(prec='full') == '8.8541878128 pF/m'
    assert Quantity('mu0').render(prec='full') == '1.25663706212 uH/m'
    assert Quantity('µ₀').render(prec='full') == '1.25663706212 uH/m' # uses micro
    assert Quantity('μ₀').render(prec='full') == '1.25663706212 uH/m' # uses mu
    assert Quantity('Z0').render(prec='full') == '376.730313668 Ohms'

    set_unit_system('cgs')
    assert '{:.12q}'.format(Quantity('h')) == '6.62607015e-27 erg-s'
    assert '{:.12q}'.format(Quantity('hbar')) == '1.054571817e-27 erg-s'
    assert '{:.12q}'.format(Quantity('ħ')) == '1.054571817e-27 erg-s'
    assert '{:.12q}'.format(Quantity('k')) == '138.0649 aerg/K'
    assert '{:.12q}'.format(Quantity('q')) == '480.320471257 pFr'
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
    assert str(exception.value) == "'fuzz': not a valid number."
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

    assert '{:S}'.format(Quantity('h')) == "h = 6.6261e-27 erg-s — Plank's constant"
    assert '{:S}'.format(Quantity('hbar')) == "ħ = 1.0546e-27 erg-s — reduced Plank's constant"
    assert '{:S}'.format(Quantity('ħ')) == "ħ = 1.0546e-27 erg-s — reduced Plank's constant"
    assert '{:S}'.format(Quantity('k')) == "k = 138.06 aerg/K — Boltzmann's constant"
    assert '{:S}'.format(Quantity('q')) == 'q = 480.32 pFr — elementary charge'
    assert '{:S}'.format(Quantity('c')) == 'c = 299.79 Mm/s — speed of light'
    assert '{:S}'.format(Quantity('0C')) == '0°C = 273.15 K — zero degrees Celsius'

    set_unit_system('mks')
    assert Quantity('h').render(prec='full') == '662.607015e-36 J-s'
    assert Quantity('hbar').render(prec='full') == '105.4571817e-36 J-s'
    assert Quantity('ħ').render(prec='full') == '105.4571817e-36 J-s'
    assert Quantity('k').render(prec='full') == '13.80649e-24 J/K'
    assert Quantity('q').render(prec='full') == '160.2176634e-21 C'
    assert Quantity('c').render(prec='full') == '299.792458 Mm/s'
    assert Quantity('0C').render(prec='full') == '273.15 K'
    assert Quantity('ε₀').render(prec='full') == '8.8541878128 pF/m'
    assert Quantity('eps0').render(prec='full') == '8.8541878128 pF/m'
    assert Quantity('mu0').render(prec='full') == '1.25663706212 uH/m'
    assert Quantity('µ₀').render(prec='full') == '1.25663706212 uH/m' # uses micro
    assert Quantity('μ₀').render(prec='full') == '1.25663706212 uH/m' # uses mu
    assert Quantity('Z0').render(prec='full') == '376.730313668 Ohms'

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

    assert '{:S}'.format(Quantity('h')) == "h = 662.61e-36 J-s — Plank's constant"
    assert '{:S}'.format(Quantity('hbar')) == "ħ = 105.46e-36 J-s — reduced Plank's constant"
    assert '{:S}'.format(Quantity('ħ')) == "ħ = 105.46e-36 J-s — reduced Plank's constant"
    assert '{:S}'.format(Quantity('k')) == "k = 13.806e-24 J/K — Boltzmann's constant"
    assert '{:S}'.format(Quantity('q')) == 'q = 160.22e-21 C — elementary charge'
    assert '{:S}'.format(Quantity('c')) == 'c = 299.79 Mm/s — speed of light'
    assert '{:S}'.format(Quantity('0C')) == '0°C = 273.15 K — zero degrees Celsius'
    assert '{:S}'.format(Quantity('eps0')) == 'ε₀ = 8.8542 pF/m — permittivity of free space'
    assert '{:S}'.format(Quantity('mu0')) == 'µ₀ = 1.2566 uH/m — permeability of free space'
    assert '{:S}'.format(Quantity('µ₀')) == 'µ₀ = 1.2566 uH/m — permeability of free space'  # uses micro
    assert '{:S}'.format(Quantity('μ₀')) == 'µ₀ = 1.2566 uH/m — permeability of free space'  # uses mu
    assert '{:S}'.format(Quantity('Z0')) == 'Z₀ = 376.73 Ohms — characteristic impedance of free space'

    add_constant('f_hy = 1420.405751786 MHz — Frequency of hydrogen line')
    assert str(Quantity('f_hy')) == '1.4204 GHz'

    add_constant(Quantity('1420.405751786 MHz'), 'hline')
    assert str(Quantity('hline')) == '1.4204 GHz'
    add_constant(Quantity(4.80320471257e-10, 'Fr'), 'q', 'esu gaussian')
    add_constant(Quantity(1.602176634e-20, 'abC'), alias='q', unit_systems='emu')
    assert Quantity('q').render(prec='full') == '160.2176634e-21 C'
    set_unit_system('cgs')
    assert Quantity('q').render(prec='full') == '480.320471257 pFr'
    set_unit_system('esu')
    assert Quantity('q').render(prec='full') == '480.320471257 pFr'
    set_unit_system('gaussian')
    assert Quantity('q').render(prec='full') == '480.320471257 pFr'
    set_unit_system('emu')
    assert Quantity('q').render(prec='full') == '16.02176634e-21 abC'
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
