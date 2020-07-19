# encoding: utf8

import math
from math import pi
from textwrap import dedent
import pytest
from quantiphy import Quantity, add_constant

def test_workout():
    Quantity.reset_prefs()
    qs = Quantity.extract(
        r"""
            Fclk = 50MHz        -- clock frequency

            This is an arbitrary line of text.
            This is an line of text that: triggers the line processing but still should be ignored..
        """
    )
    f_clk = qs.pop('Fclk')
    assert f_clk.is_close(Quantity(5e7, 'Hz'), check_units=True)
    assert f_clk.is_close(5e7)
    assert f_clk.units == 'Hz'
    assert f_clk.name == 'Fclk'
    assert f_clk.desc == 'clock frequency'
    assert not qs

def test_roomful():
    Quantity.reset_prefs()
    qs = Quantity.extract(
        r"""
            Fclk: 50MHz        // clock frequency
        """
    )
    f_clk = qs.pop('Fclk')
    assert f_clk.is_close(Quantity(5e7, 'Hz'), check_units=True)
    assert f_clk.is_close(5e7)
    assert f_clk.units == 'Hz'
    assert f_clk.name == 'Fclk'
    assert f_clk.desc == 'clock frequency'
    assert not qs

def test_bulletin():
    Quantity.reset_prefs()
    qs = Quantity.extract(
        r"""
            Fclk = 50MHz        # clock frequency
        """
    )
    f_clk = qs.pop('Fclk')
    assert f_clk.is_close(Quantity(5e7, 'Hz'), check_units=True)
    assert f_clk.is_close(5e7)
    assert f_clk.units == 'Hz'
    assert f_clk.name == 'Fclk'
    assert f_clk.desc == 'clock frequency'
    assert not qs

def test_deduce():
    Quantity.reset_prefs()
    qs = Quantity.extract(
        r"""
            Fclk = 50MHz
        """
    )
    f_clk = qs.pop('Fclk')
    assert f_clk.is_close(Quantity(5e7, 'Hz'), check_units=True)
    assert f_clk.is_close(5e7)
    assert f_clk.units == 'Hz'
    assert f_clk.name == 'Fclk'
    assert f_clk.desc == ''
    assert not qs

def test_proof():
    Quantity.reset_prefs()
    qs = Quantity.extract(
        r"""
            $F_{\rm clk}$ = 50MHz        -- clock frequency
        """
    )
    f_clk = qs.pop(r'$F_{\rm clk}$')
    assert f_clk.is_close(Quantity(5e7, 'Hz'), check_units=True)
    assert f_clk.is_close(5e7)
    assert f_clk.units == 'Hz'
    assert f_clk.name == r'$F_{\rm clk}$'
    assert f_clk.desc == 'clock frequency'
    assert not qs

def test_wager():
    Quantity.reset_prefs()
    qs = Quantity.extract(
        r"""
            Fclk ($F_{\rm clk}$) = 50MHz -- clock frequency
        """
    )
    f_clk = qs.pop('Fclk')
    assert f_clk.is_close(Quantity(5e7, 'Hz'), check_units=True)
    assert f_clk.is_close(5e7)
    assert f_clk.units == 'Hz'
    assert f_clk.name == r'$F_{\rm clk}$'
    assert f_clk.desc == 'clock frequency'
    assert not qs

def test_disallow():
    Quantity.reset_prefs()
    qs = Quantity.extract(
        r"""
            rate = 64GiB/s -- bit rate
        """,
        binary = True,
    )
    rate = qs.pop('rate')
    assert float(rate) == 68719476736
    assert rate.units == 'B/s'
    assert not qs

def test_anatomy():
    Quantity.reset_prefs()
    qs = Quantity.extract(
        r"""
            Rin = ∞Ω -- input resistance
        """,
    )
    Rin = qs.pop('Rin')
    assert float(Rin) == float('inf')
    assert Rin.units == 'Ω'
    assert Rin.is_infinite() == 'inf'
    assert not qs

def test_billow():
    Quantity.reset_prefs()
    qs = Quantity.extract(
        r"""
            C3 = 250.7nF
            f_corner (f₀) = 500mHz
            w_corner (ω₀) = 2*pi*f_corner 'rads/s'
            Aw = C3*sqrt(w_corner) '√Ω'
        """,
        predefined = dict(sqrt=math.sqrt)
    )
    C3 = qs.pop('C3')
    assert str(C3) == '250.7 nF'
    assert C3.units == 'F'
    assert C3.name == 'C3'
    f_corner = qs.pop('f_corner')
    assert str(f_corner) == '500 mHz'
    assert f_corner.units == 'Hz'
    assert f_corner.name == 'f₀'
    w_corner = qs.pop('w_corner')
    assert str(w_corner) == '3.1416 rads/s'
    assert w_corner.units == 'rads/s'
    assert w_corner.name == 'ω₀'
    Aw = qs.pop('Aw')
    assert str(Aw) == '444.35 n√Ω'
    assert Aw.units == '√Ω'
    assert Aw.name == 'Aw'
    assert not qs

def test_invention():
    Quantity.reset_prefs()
    qs = Quantity.extract(
        r"""
            Fin = 10MHz        -- input frequency
            Tstop = 5/Fin      -- stop time
        """
    )
    f_in = qs.pop('Fin')
    assert f_in.is_close(Quantity(1e7, 'Hz'), check_units=True)
    assert f_in.is_close(1e7)
    assert f_in.units == 'Hz'
    assert f_in.name == 'Fin'
    assert f_in.desc == 'input frequency'
    t_stop = qs.pop('Tstop')
    assert t_stop.is_close(Quantity(5/f_in, ''), check_units=True)
    assert t_stop.is_close(5/f_in)
    assert t_stop.units == ''
    assert t_stop.name == 'Tstop'
    assert t_stop.desc == 'stop time'
    assert not qs

def test_route():
    Quantity.reset_prefs()
    qs = Quantity.extract(
        r"""
            Fin = 10MHz        -- input frequency
            Tstop = 5/Fin "s"  -- stop time
        """
    )
    f_in = qs.pop('Fin')
    assert f_in.is_close(Quantity(1e7, 'Hz'), check_units=True)
    assert f_in.is_close(1e7)
    assert f_in.units == 'Hz'
    assert f_in.name == 'Fin'
    assert f_in.desc == 'input frequency'
    t_stop = qs.pop('Tstop')
    assert t_stop.is_close(Quantity(5/f_in, 's'), check_units=True)
    assert t_stop.is_close(5/f_in)
    assert t_stop.units == 's'
    assert t_stop.name == 'Tstop'
    assert t_stop.desc == 'stop time'
    assert not qs

def test_critique():
    Quantity.reset_prefs()
    qs = Quantity.extract(
        r"""
            -- Fclk = 50MHz        -- clock frequency
        """
    )
    assert not qs

def test_socialist():
    Quantity.reset_prefs()
    qs = Quantity.extract(
        r"""
            # Fclk = 50MHz        -- clock frequency
        """
    )
    assert not qs

def test_stumble():
    Quantity.reset_prefs()
    qs = Quantity.extract(
        r"""
            // Fclk = 50MHz        -- clock frequency
        """
    )
    assert not qs

def test_guardian():
    Quantity.reset_prefs()
    qs = Quantity.extract(
        r"""
            This is a non conforming line.
        """
    )
    assert not qs

def test_hussy():
    Quantity.reset_prefs()
    qs = Quantity.extract(
        r"""
            This is a non conforming line.
        """
    )
    assert not qs

def test_affiliate():
    Quantity.reset_prefs()
    qs = Quantity.extract(
        r"""
            This is a non conforming line.

            Fin = 10MHz        -- input frequency
            -- Fin = 10MHz        -- input frequency

            Tstop = 5/Fin "s"  -- stop time

            This is a non conforming line.
        """
    )
    f_in = qs.pop('Fin')
    assert f_in.is_close(Quantity(1e7, 'Hz'), check_units=True)
    assert f_in.is_close(1e7)
    assert f_in.units == 'Hz'
    assert f_in.name == 'Fin'
    assert f_in.desc == 'input frequency'
    t_stop = qs.pop('Tstop')
    assert t_stop.is_close(Quantity(5/f_in, 's'), check_units=True)
    assert t_stop.is_close(5/f_in)
    assert t_stop.units == 's'
    assert t_stop.name == 'Tstop'
    assert t_stop.desc == 'stop time'
    assert not qs

def test_sagan():
    Quantity.reset_prefs()
    qs = Quantity.extract(
        r"""
            Carl Sagan's frequencies
            -- These are the frequencies that Carl Sagan asserted were of
            -- high interest to SETI.

            f_hy ($f_{\rm hy}$) = 1420.405751786 MHz -- Hydrogen line frequency
            f_sagan1 ($f_{\rm sagan1}$) = pi*f_hy "Hz" -- Sagan's first frequency
            f_sagan2 ($f_{\rm sagan2}$) = 2*pi*f_hy "Hz" -- Sagan's second frequency
            f_sagan2x ($f_{\rm sagan2}$) = tau*f_hy "Hz" -- Sagan's second frequency
            half_c ($\frac{c}{2}$) = c/2 "m/s" -- Half the speed of light
            a_string (a string) = 'a string' -- yep, its a string
            a_dict (a dict) = {0:0, 1:1} -- yep, its a dict
        """
    )
    f_hy = qs.pop('f_hy')
    assert f_hy.is_close(Quantity(1.420405751786e9, 'Hz'), check_units=True)
    assert f_hy.is_close(1.420405751786e9)
    assert f_hy.units == 'Hz'
    assert f_hy.name == r'$f_{\rm hy}$'
    assert f_hy.desc == 'Hydrogen line frequency'
    f_sagan1 = qs.pop('f_sagan1')
    assert f_sagan1.is_close(Quantity(pi*1.420405751786e9, 'Hz'), check_units=True)
    assert f_sagan1.is_close(pi*1.420405751786e9)
    assert f_sagan1.units == 'Hz'
    assert f_sagan1.name == r'$f_{\rm sagan1}$'
    assert f_sagan1.desc == "Sagan's first frequency"
    f_sagan2 = qs.pop('f_sagan2')
    assert f_sagan2.is_close(Quantity(2*pi*1.420405751786e9, 'Hz'), check_units=True)
    assert f_sagan2.is_close(2*pi*1.420405751786e9)
    assert f_sagan2.units == 'Hz'
    assert f_sagan2.name == r'$f_{\rm sagan2}$'
    assert f_sagan2.desc == "Sagan's second frequency"
    f_sagan2x = qs.pop('f_sagan2x')
    assert f_sagan2x.is_close(Quantity(2*pi*1.420405751786e9, 'Hz'), check_units=True)
    assert f_sagan2x.is_close(2*pi*1.420405751786e9)
    assert f_sagan2x.units == 'Hz'
    assert f_sagan2x.name == r'$f_{\rm sagan2}$'
    assert f_sagan2x.desc == "Sagan's second frequency"
    half_c = qs.pop('half_c')
    assert half_c.is_close(Quantity('c')/2, check_units=True)
    assert half_c.is_close(Quantity('c')/2)
    assert half_c.units == 'm/s'
    assert half_c.name == r'$\frac{c}{2}$'
    assert half_c.desc == "Half the speed of light"
    a_string = qs.pop('a_string')
    assert a_string == 'a string'
    a_dict = qs.pop('a_dict')
    assert a_dict == {0:0, 1:1}
    assert not qs

def test_assign_rec():
    Quantity.reset_prefs()
    with Quantity.prefs(
        assign_rec=r'(?P<name>\w+?)\s*=\s*(?P<val>\w*)(\s+(--)\s*(?P<desc>.*?))?\Z'
    ):
        qs = Quantity.extract(
            r"""
                -- The Hydrogen Line
                bad = --    Also known as the 21 cm line
                = bad --    The spectral line associated with a spin flip.

                f_hy = 1420MHz -- Hydrogen line frequency
            """
        )
        f_hy = qs.pop('f_hy')
        assert f_hy.is_close(Quantity(1.42e9, 'Hz'), check_units=True)
        assert f_hy.is_close(1.42e9)
        assert f_hy.units == 'Hz'
        assert f_hy.name == 'f_hy'
        assert f_hy.desc == 'Hydrogen line frequency'
        assert not qs


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
