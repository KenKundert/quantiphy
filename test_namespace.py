# encoding: utf8

from quantiphy import Quantity

def test_namespace():
    Quantity.set_prefs(spacer=None, show_label=None, label_fmt=None, label_fmt_full=None)
    globals().update(Quantity.extract('''
        h_line = 1420.405751786 MHz -- Frequency of the hydrogen line
        k = 13.806488e-24 J/K -- Boltzmann's constant
        Temp = 300_K -- Temperature
        M = 2  -- Divide ratio of HF divider
        N = 8  -- Divide ratio of MF divider
        F = 2  -- Divide ratio of LF divider
        Fref = 156MHz  -- Reference frequency
        Kdet = 88.3uA  -- Gain of phase detector (Imax)
        Kvco = 9.07GHz/V  -- Gain of VCO
        Cs = 1.41pF  -- Shunt capacitance
        Cp = 59.7pF  -- Pole capacitance
        Rz = 2.24KOhms  -- Zero resistance
        Fstart = 1KHz  -- Lower frequency bound
        Fstop = 1GHz  -- Upper frequency bound
        Spd = 1.47E-24 A^2/Hz  -- Spectral density of the output noise of the PFD/CP
        FcorPD = 1.5MHz  -- PFD/CP flicker noise corner frequency
        JdivM = 2.43E-18 s/rt(Hz)  -- Spectral density of the output jitter of divM
        FcorDivM = 7MHz  -- divM flicker noise corner frequency
        JdivN = 4.47E-18 s/rt(Hz)  -- Spectral density of the output jitter of divN
        FcorDivN = 1.5MHz  -- divN flicker noise corner frequency
        JdivF = 1.82E-17 s/rt(Hz)  -- Spectral density of the output jitter of divF
        FcorDivF = 2MHz  -- divF flicker noise corner frequency
        Jbuf = 3.70E-18 s/rt(Hz)  -- Spectral density of the output jitter of output buffer
        FcorBuf = 2.5MHz  -- buf flicker noise corner frequency
        Lvco = -125.00 dBc/Hz -- Oscillator phase noise injected after VCO
        FcorVCO = 3MHz  -- VCO flicker noise corner frequency
        Lref = -110.00 dbc/Hz -- Oscillator phase noise injected at reference input
        FcorRef = 0_Hz  -- Freq. reference flicker noise corner frequency
        FmaskLFcor = 12kHz  -- Jitter generation mask low frequency corner
        FmaskHFbound = 5MHz  -- Jitter generation mask high frequency bound

        -- The remainder are built in constants
        plank = h  -- Plank's constant
        boltz = k  -- Boltzmann's constant
        ec = q  -- Elementary charge
        speed_of_light = c -- Speed of light
        zero_celsius = 0C -- Zero degree Celsius in Kelvin
        epsilon0 = eps0 -- Permittivity of free space
        mu0 = mu0 -- Permeability of free space
        Z0 = Z0 -- Characteristic impedance of free space
        c = c  -- speed of light
    '''))

    assert str(h_line) == '1.4204 GHz'
    assert str(k) == '13.806e-24 J/K'
    assert str(Temp) == '300 K'
    assert str(M) == '2'
    assert str(N) == '8'
    assert str(F) == '2'
    assert str(Fref) == '156 MHz'
    assert str(Kdet) == '88.3 uA'
    assert str(Kvco) == '9.07 GHz/V'
    assert str(Cs) == '1.41 pF'
    assert str(Cp) == '59.7 pF'
    assert str(Rz) == '2.24 kOhms'
    assert str(Fstart) == '1 kHz'
    assert str(Fstop) == '1 GHz'
    assert str(Spd) == '1.47e-24 A^2/Hz'
    assert str(FcorPD) == '1.5 MHz'
    assert str(JdivM) == '2.43 as/rt(Hz)'
    assert str(FcorDivM) == '7 MHz'
    assert str(JdivN) == '4.47 as/rt(Hz)'
    assert str(FcorDivN) == '1.5 MHz'
    assert str(JdivF) == '18.2 as/rt(Hz)'
    assert str(FcorDivF) == '2 MHz'
    assert str(Jbuf) == '3.7 as/rt(Hz)'
    assert str(FcorBuf) == '2.5 MHz'
    assert str(Lvco) == '-125 dBc/Hz'
    assert str(FcorVCO) == '3 MHz'
    assert str(Lref) == '-110 dbc/Hz'
    assert str(FcorRef) == '0 Hz'
    assert str(FmaskLFcor) == '12 kHz'
    assert str(FmaskHFbound) == '5 MHz'
    assert str(plank) == '662.61e-36 J-s'
    assert str(boltz) == '13.806e-24 J/K'
    assert str(ec) == '160.22e-21 C'
    assert str(speed_of_light) == '299.79 Mm/s'
    assert str(zero_celsius) == '273.15 K'
    assert str(epsilon0) == '8.8542 pF/m'
    assert str(mu0) == '1.2566 uH/m'
    assert str(Z0) == '376.73 Ohms'
