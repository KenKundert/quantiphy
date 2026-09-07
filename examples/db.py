#!/usr/bin/env python3
"""
Implement and test various dB conversions.
"""

from quantiphy import Quantity, UnitConversion
from inform import InformantFactory, display
fails = InformantFactory(clone=display, message_color='red')
succeeds = InformantFactory(clone=display, message_color='green')
import numpy as np

# Unit conversions {{{1
# dB, dBV, and dBA {{{2
def from_dB(dB):
    return 10**(dB/20), dB.units[2:]

def to_dB(value):
    return 20*np.log10(value), 'dB'+value.units

UnitConversion('V', 'dBV', from_dB, to_dB)
UnitConversion('A', 'dBA', from_dB, to_dB)
UnitConversion('', 'dB', from_dB, to_dB)

# dBm {{{2
@UnitConversion.fixture
def from_dBm_to_Vp(dBm, R):
    return np.sqrt(2*R*(10**((dBm - 30)/10)))

@UnitConversion.fixture
def to_dBm_from_Vp(Vp, R):
    return 10*np.log10(Vp*Vp/(2*R)) + 30

UnitConversion('V', 'dBm', from_dBm_to_Vp, to_dBm_from_Vp)

@UnitConversion.fixture
def from_dBm_to_Ip(dBm, R):
    return np.sqrt(2*10**((dBm - 30)/10)/R)

@UnitConversion.fixture
def to_dBm_from_Ip(Ip, R):
    return 10*np.log10(R*Ip*Ip/2) + 30

UnitConversion('A', 'dBm', from_dBm_to_Ip, to_dBm_from_Ip)

# Tests {{{1
tests = """
    1V  0dBV
    10V  20dBV
    1uV  -120dBV
    1A  0dBA
    10A  20dBA
    1uA  -120dBA
    1  0dB
    10  20dB
    1u  -120dB
    1V  10dBm
    100mV  -10dBm
    1A  43.9794dBm
    100mA  23.9794dBm
    10mA  3.9794dBm
    1mA  -16.0206dBm
"""

def report(given, expected, achieved):
    if expected == achieved:
        succeeds(f"pass: {given} → {achieved}")
    else:
        diff = Quantity(achieved) - Quantity(expected)
        err = Quantity(100*diff/Quantity(expected), '%')
        fails(f"FAIL: {given} → {achieved}, expected {expected}, Δ={err:.1}")

Quantity.set_prefs(spacer='', prec=6)

for line in tests.splitlines():
    if line:
        sig, dB = line.split()
        q_sig = Quantity(sig, params=50)
        q_dB = Quantity(dB, params=50)
        converted_to_dB = f"{q_sig.scale(q_dB.units)}"
        converted_to_sig = f"{q_dB.scale(q_sig.units)}"
        report(sig, dB, converted_to_dB)
        report(dB, sig, converted_to_sig)
