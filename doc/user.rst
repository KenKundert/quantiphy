.. _users guide:

Users' Guide
============

.. _overview:

Overview
--------

*QuantiPhy* adds support for quantities to Python. Quantities are little more 
than a number combined with its units. They are used to represent physical 
quantities. For example, your height and weight are both quantities, having both 
a value and units, and both are important. For example, if I told you that 
Mariam's weight was 8, you might assume pounds as the unit of measure if you 
lived in the US and think Mariam was an infant, or you might assume stones as 
the units if you live in the UK and assume that she was an adult, or you might 
assume kilograms if you lived anywhere else and assume she was a small child.
The units are very important, and in general it is always best to keep the unit 
of measure with the number and present the complete value when working with 
quantities. To do otherwise invites confusion.  Just ask `NASA 
<http://www.cnn.com/TECH/space/9909/30/mars.metric.02/>`_.  Readers often 
stumble on numbers without units as they mentally try to determine the units 
from context.  Quantity values should be treated in a manner similar to money, 
which is also a quantity. Monetary amounts are almost always given with their 
units (a currency symbol).

Having a single object represent a quantity in a programming language is useful 
because it binds the units to the number making it more likely that the units 
will be presented with the number. In addition, quantities from *QuantiPhy* 
provide another important benefit.  They naturally support the SI scale factors, 
which for those that are familiar with them are much easer to read and write 
than the alternatives. The most common SI scale factors are:

    |   T (10\ :sup:`12`) tera
    |   G (10\ :sup:`9`) giga
    |   M (10\ :sup:`6`) mega
    |   k (10\ :sup:`3`) kilo
    |   m (10\ :sup:`-3`) milli
    |   μ (10\ :sup:`-6`) micro
    |   n (10\ :sup:`-9`) nano
    |   p (10\ :sup:`-12`) pico
    |   f (10\ :sup:`-15`) fempto
    |   a (10\ :sup:`-18`) atto

Numbers with SI scale factors are commonly used in science and engineering
to represent physical quantities because it is easy to read and write numbers
both large and small. For example, the distance between the atoms in a silicon
lattice is roughly 230 pm whereas the distance to the sun is about 150 Gm.
Unfortunately, computers do not normally use SI scale factors. Instead, they
use E-notation. The two distances would be written as 2.3e-10 m and 1.5e+11 m.
Virtually all computer languages such as Python both read and write numbers in
E-notation, but none naturally read or write numbers that use SI scale factors,
even though SI is an `international standard
<https://en.wikipedia.org/wiki/International_System_of_Units>`_ that has been
in place for over 50 years and is widely used.

*QuantiPhy* is an attempt to address both of these deficiencies. It allows 
quantities to be represented with a single object that allows the complete 
quantity to be easily read or written as a single unit. It also naturally 
supports SI scale factors.  As such, *QuantiPhy* allows computers to communicate 
more naturally with humans, particularly scientists and engineers.


.. _quantities:

Quantities
----------

*QuantiPhy* is a library that adds support to Python for both reading and 
writing numbers with SI scale factors and units. The primary working construct 
for *QuantiPhy* is :class:`quantiphy.Quantity`, which is a class whose objects 
hold the number and units that are used to represent a physical quantity. For 
example, to create a quantity from a string you can use:

.. code-block:: python

    >>> from quantiphy import Quantity

    >>> distance_to_sun = Quantity('150 Gm')
    >>> distance_to_sun.real
    150000000000.0

    >>> distance_to_sun.units
    'm'

    >>> print(distance_to_sun)
    150 Gm

Now *distance_to_sun* contains two items, the number 150000000000.0 and the 
units 'm'.  The 'G' was interpreted as the *giga* scale factor, which scales by 
10\ :sup:`9`.

It is worth considering the alternative for a moment:

.. code-block:: python

    >>> d_sol = float('150000000000.0')
    >>> print(f'{d_sol} m')
    150000000000.0 m

Ignoring the difficulty in writing and reading the number, there is another 
important difference. The units are placed in the print statement and not kept 
with the number. This makes the value ambiguous, it clutters the print 
statement, and it introduces a vulnerability. When coming back and refactoring 
your code after some time has passed, you might change the units of the number 
and forget to change the units in the print statement. This is particularly 
likely if the number is defined far from where it is printed. The result is that 
erroneous results are printed and is always a risk when two related pieces of 
information are specified far from one another. *QuantiPhy* addresses this issue 
by binding the value and the units into one object.

:class:`quantiphy.Quantity` is a subclass of float, and so *distance_to_sun* can 
be used just like any real number. For example, you can convert the distance to 
miles using:

.. code-block:: python

    >>> distance_in_miles = distance_to_sun / 1609.34
    >>> print(distance_in_miles)
    93205910.49747102

When printed or converted to strings quantities naturally use SI scale factors.  
For example, you can clean up that distance in miles using:

.. code-block:: python

    >>> distance_in_miles = Quantity(distance_to_sun / 1609.34, 'miles')
    >>> print(distance_in_miles)
    93.206 Mmiles

However, you need not explicitly do the conversion yourself. *QuantiPhy* 
provides many of the most common conversions for you:

.. code-block:: python

    >>> distance_in_miles = Quantity(distance_to_sun, scale='miles')
    >>> print(distance_in_miles)
    93.206 Mmiles


Specifying a Quantity Value
...........................

Normally, creating a quantity takes one or two arguments.  The first is taken to 
be the value, and the second, if given, is taken to be the model, which is 
a source of default values.  The value may be given as a float, as a string, or 
as a quantity.  The string may be the name of a known constant or it may 
represent a number. If the string represents a number, it may be in floating 
point notation, in E-notation (ex: 1.2e+3), or use SI scale factors. It may also 
include the units.  And like Python in general, the numbers may include 
underscores to make them easier to read (they are ignored).  For example, any of 
the following ways can be used to specify 1ns:

.. code-block:: python

    >>> period = Quantity(1e-9, 's')
    >>> print(period)
    1 ns

    >>> period = Quantity('0.000_000_001 s')
    >>> print(period)
    1 ns

    >>> period = Quantity('1e-9s')
    >>> print(period)
    1 ns

    >>> period = Quantity('1ns')
    >>> print(period)
    1 ns

    >>> period2 = Quantity(period)
    >>> print(period2)
    1 ns

If given as a string, the value may also be the name of a known :ref:`constant 
<constants>`:

.. code-block:: python

    >>> k = Quantity('k')
    >>> q = Quantity('q')
    >>> print(k, q, sep='\n')
    13.806e-24 J/K
    160.22e-21 C

The following constants are pre-defined: *h*, *ħ*, *k*, *q*, *c*, *0°C'*, *ε₀*, 
*μ₀*, and *Z₀*. You may add your own constants.

Currency units ($£€ɃΞ) are a bit different than other units, they are placed 
at the front of the quantity.

.. code-block:: python

    >>> print(Quantity('$11_200_000'))
    $11.2M

    >>> print(Quantity(11.2e6, '$'))
    $11.2M

When using currency units, if the number has a sign, it should precede the 
units:

.. code-block:: python

    >>> print(Quantity('-$11_200_000'))
    -$11.2M

    >>> print(Quantity(-11.2e6, '$'))
    -$11.2M

When given as a string, the number may use any of the following scale factors 
(though you can use the *input_sf* preference to prune this list if desired):

    |   Y (10\ :sup:`24`) yotta
    |   Z (10\ :sup:`21`) zetta
    |   E (10\ :sup:`18`) exa
    |   P (10\ :sup:`15`) peta
    |   T (10\ :sup:`12`) tera
    |   G (10\ :sup:`9`) giga
    |   M (10\ :sup:`6`) mega
    |   k (10\ :sup:`3`) kilo
    |   _ (1)
    |   c (10\ :sup:`-2`) centi
    |   m (10\ :sup:`-3`) milli
    |   u (10\ :sup:`-6`) micro
    |   μ (10\ :sup:`-6`) micro
    |   n (10\ :sup:`-9`) nano
    |   p (10\ :sup:`-12`) pico
    |   f (10\ :sup:`-15`) fempto
    |   a (10\ :sup:`-18`) atto
    |   z (10\ :sup:`-21`) zepto
    |   y (10\ :sup:`-24`) yocto

When specifying the value as a string you may also give a name and description, 
and if you do they become available as the attributes *name* and *desc*.  This 
conversion is under the control of the *assign_rec* preference.  The default 
version of *assign_rec* accepts either '=' or ':' to separate the name from the 
value, and either '--', '#', or '//' to separate the value from the description 
if a description is given. Thus, by default *QuantiPhy* recognizes 
specifications of the following forms::

    <name> = <value>
    <name> = <value> -- <description>
    <name> = <value> # <description>
    <name> = <value> // <description>
    <name>: <value>
    <name>: <value> -- <description>
    <name>: <value> # <description>
    <name>: <value> // <description>

For example:

.. code-block:: python

    >>> period = Quantity('Tclk = 10ns -- clock period')
    >>> print(f'{period.name} = {period}  # {period.desc}')
    Tclk = 10 ns  # clock period

If you only specify a real number for the value, then the units, name, and 
description do not get values. Even if given as a string or quantity the value 
may not contain these extra attributes. This is where the second argument, the 
model, helps.  It may be another quantity or it may be a string.  Any attributes 
that are not provided by the first argument are taken from the second if 
available.  If the second argument is a string, it is split.  If it contains one 
value, that value is taken to be the units, if it contains two, those values are 
taken to be the name and units, and it it contains more than two, the remaining 
values are taken to be the description.  If the model is a quantity, only the 
units are inherited. For example:

.. code-block:: python

    >>> out_period = Quantity(10*period, period)
    >>> print(out_period)
    100 ns

    >>> freq = Quantity(100e6, 'Hz')
    >>> print(freq)
    100 MHz

    >>> freq = Quantity(100e6, 'Fin Hz')
    >>> print(f'{freq.name} = {freq}')
    Fin = 100 MHz

    >>> freq = Quantity(100e6, 'Fin Hz input frequency')
    >>> print(f'{freq.name} = {freq} -- {freq.desc}')
    Fin = 100 MHz -- input frequency

In addition, you can explicitly specify the units, the name, and the description 
using named arguments. These values override anything specified in the value or 
the model.

.. code-block:: python

    >>> out_period = Quantity(
    ...     10*period, period, name='output period',
    ...     desc='period at output of frequency divider'
    ... )
    >>> print(f'{out_period.name} = {out_period} -- {out_period.desc}')
    output period = 100 ns -- period at output of frequency divider

Finally, you can overwrite the quantity's attributes to override the units, 
name, or description.

.. code-block:: python

    >>> out_period = Quantity(10*period)
    >>> out_period.units = 's'
    >>> out_period.name = 'output period'
    >>> out_period.desc = 'period at output of frequency divider'
    >>> print(f'{out_period.name} = {out_period} -- {out_period.desc}')
    output period = 100 ns -- period at output of frequency divider


Scaling When Creating a Quantity
................................

Quantities tend to be used primarily when reading and writing numbers, and less 
often when processing numbers.  Often data comes in an undesirable form. For 
example, imagine data that has been normalized to kilograms but the numbers 
themselves have neither units or scale factors.  *QuantiPhy* allows you to scale 
the number and assign the units when creating the quantity:

.. code-block:: python

    >>> mass = Quantity('2.529', scale=1000, units='g')
    >>> print(mass)
    2.529 kg

In this case the value is given in kilograms, and is converted to the base units 
of grams by multiplying the given value by 1000. This can also be expressed as 
follows:

.. code-block:: python

    >>> mass = Quantity('2.529', scale=(1000, 'g'))
    >>> print(mass)
    2.529 kg

You can also specify a function to do the conversion, which is helpful when the 
conversion is :index:`not linear <dB>`:

.. code-block:: python

    >>> def from_dB(value, units=''):
    ...     return 10**(value/20), units[2:]

    >>> Quantity('-100 dBV', scale=from_dB)
    Quantity('10 uV')

The conversion can also often occur if you simply state the units you wish the 
quantity to have:

.. code-block:: python

    >>> Tboil = Quantity('212 °F', scale='K')
    >>> print(Tboil)
    373.15 K

This assumes that the initial value is specified with units. If not, you need to 
provide them for this mechanism to work.

.. code-block:: python

    >>> Tboil = Quantity('212', '°F', scale='K')
    >>> print(Tboil)
    373.15 K

To do this conversion, *QuantiPhy* examines the given units (°F) and the desired 
units (K) and choses the appropriate converter.  *QuantiPhy* provides 
a collection of pre-defined converters for common units:

====== ===============================================================
K:     K, F, °F, R, °R
C, °C: K, C, °C, F, °F, R, °R
m:     km, m, cm, mm, um, μm, micron, nm, Å, angstrom, mi, mile, miles
g:     oz, lb, lbs
s:     s, sec, min, hour, hr , day
b:     B
====== ===============================================================

You can also create your own converters using :class:`quantiphy.UnitConversion`:

.. code-block:: python

    >>> from quantiphy import UnitConversion

    >>> m2pc = UnitConversion('m', 'pc parsec', 3.0857e16)

    >>> d_sol = Quantity('5 μpc', scale='m')
    >>> print(d_sol)
    154.28 Gm

This unit conversion says, when converting units of 'm' to either 'pc' or 
'parsec' multiply by 3.0857e16, when going the other way, divide by 3.0857e16.

    >>> d_sol = Quantity('154.285 Gm', scale='pc')
    >>> print(d_sol)
    5 upc

Notice that the return value of *UnitConversion* was not used. It is enough to 
simply create the *UnitConversion* for it to be available to *Quantity*. So, it 
is normal to not capture the return value. However, there are two things you can 
do with the return value. First you can convert it to a string to get 
a description of the relationship. This is largely used as a sanity check:

.. code-block:: python

    >>> print(str(m2pc))
    m = 3.0857e+16*pc

In addition, you can use it to directly perform conversions:

.. code-block:: python

    >>> m = m2pc.convert(1, 'pc')
    >>> print(str(m))
    30.857e15 m

    >>> kpc = m2pc.convert(30.857e+18, 'm')
    >>> print(str(kpc))
    1 kpc

You can find an example of this usage in :ref:`cryptocurrency example`.

When using unit conversions it is important to only convert to units without 
scale factors (such as those in the first column above) when creating 
a quantity.  For example, it is better to convert to 'm' rather than 'cm'.  If 
the desired units used when creating a quantity includes a scale factor, then it 
is easy to end up with two scale factors when converting the number to a string 
(ex: 1 mkm or one milli-kilo-meter).

Here is an example that uses quantity rescaling. Imagine that a table is being 
read that gives temperature versus time, but the temperature is given in °F and 
the time is given in minutes, but for the purpose of later analysis it is 
desired that the values be converted to the more natural units of Kelvin and 
seconds:

.. code-block:: python

    >>> rawdata = '0 450, 10 400, 20 360'
    >>> data = []
    >>> for pair in rawdata.split(','):
    ...     time, temp = pair.split()
    ...     time = Quantity(time, 'min', scale='s')
    ...     temp = Quantity(temp, '°F', scale='K')
    ...     data += [(time, temp)]

    >>> for time, temp in data:
    ...     print(f'{time:7s} {temp}')
    0 s     505.37 K
    600 s   477.59 K
    1.2 ks  455.37 K


Accessing Quantity Values
.........................

There are a variety of ways of accessing the value of a quantity. If you are 
just interested in its numeric value, you access it with:

.. code-block:: python

    >>> h_line = Quantity('1420.405751786 MHz')

    >>> h_line.real
    1420405751.786

    >>> float(h_line)
    1420405751.786

Or you can use a quantity in the same way that you would use any real number, 
meaning that you can use it in expressions and it will evaluate to its numeric 
value:

.. code-block:: python

    >>> import math
    >>> sagan_freq = math.pi * h_line
    >>> print(sagan_freq)
    4462336274.927585

    >>> sagan = Quantity(sagan_freq, h_line)
    >>> print(sagan)
    4.4623 GHz

    >>> type(h_line)
    <class 'quantiphy.Quantity'>

    >>> type(sagan_freq)
    <class 'float'>

    >>> type(sagan)
    <class 'quantiphy.Quantity'>

Notice that when performing arithmetic operations on quantities the units 
are completely ignored and do not propagate in any way to the newly computed 
result.

If you are interested in the units of a quantity, you can use:

.. code-block:: python

    >>> h_line.units
    'Hz'

Or you can access both the value and the units, either as a tuple or in 
a string:

.. code-block:: python

    >>> h_line.as_tuple()
    (1420405751.786, 'Hz')

    >>> str(h_line)
    '1.4204 GHz'

SI scale factors are used by default when converting numbers to strings. The 
following scale factors could be used:

    |   Y (10\ :sup:`24`) yotta
    |   Z (10\ :sup:`21`) zetta
    |   E (10\ :sup:`18`) exa
    |   P (10\ :sup:`15`) peta
    |   T (10\ :sup:`12`) tera
    |   G (10\ :sup:`9`) giga
    |   M (10\ :sup:`6`) mega
    |   k (10\ :sup:`3`) kilo
    |   m (10\ :sup:`-3`) milli
    |   u (10\ :sup:`-6`) micro
    |   n (10\ :sup:`-9`) nano
    |   p (10\ :sup:`-12`) pico
    |   f (10\ :sup:`-15`) fempto
    |   a (10\ :sup:`-18`) atto
    |   z (10\ :sup:`-21`) zepto
    |   y (10\ :sup:`-24`) yocto

However, only the scale factors listed in the *output_sf* preference are 
actually used, and by default that is set to 'TGMkmunpfa', which avoids the more
uncommon scale factors.

The render() method allows you to control the process of converting a quantity 
to a string. For example:

.. code-block:: python

    >>> h_line.render()
    '1.4204 GHz'

    >>> h_line.render(show_si=False)
    '1.4204e9 Hz'

    >>> h_line.render(show_units=False)
    '1.4204G'

    >>> h_line.render(show_si=False, show_units=False)
    '1.4204e9'

    >>> h_line.render(prec=6)
    '1.420406 GHz'

*show_label* allows you to display the name and description of the quantity when 
rendering. If *show_label* is *False*, the quantity is not labeled with the name 
or description. Otherwise the quantity is labeled under the control of the 
*show_label* value and the *show_desc*, *label_fmt* and *label_fmt_full*  
preferences (described further in :ref:`preferences` and 
:meth:`quantiphy.Quantity.set_prefs()`).  If *show_label* is 'a' (for 
abbreviated) or if the quantity has no description, *label_fmt* is used to label 
the quantity with its name.  If *show_label* is 'f' (for full), *label_fmt_full* 
is used to label the quantity with its name and description.  Otherwise 
*label_fmt_full* is used if *show_desc* is True and *label_fmt* otherwise.

.. code-block:: python

    >>> freq.render(show_label=True)
    'Fin = 100 MHz'

    >>> freq.render(show_label='f')
    'Fin = 100 MHz -- input frequency'

    >>> Quantity.set_prefs(show_desc=True)
    >>> freq.render(show_label=True)
    'Fin = 100 MHz -- input frequency'

    >>> freq.render(show_label='a')
    'Fin = 100 MHz'


You can also access the full precision of the quantity:

.. code-block:: python

    >>> h_line.render(prec='full')
    '1.420405751786 GHz'

    >>> h_line.render(show_si=False, prec='full')
    '1.420405751786e9 Hz'

Full precision implies whatever precision was used when specifying the quantity 
if it was specified as a string and if the *keep_components* preference is True.  
Otherwise a fixed number of digits, specified in the *full_prec* preference, is 
used (default=12).  Generally one uses 'full' when generating output that is 
intended to be read by a machine.


Scaling When Rendering a Quantity
.................................

Once it comes time to output quantities from your program, you may again may be 
constrained in the way the numbers must be presented. *QuantiPhy* also allows 
you to rescale the values as you render them to strings. In this case, the value 
of the quantity itself remains unchanged. For example, imagine having a quantity 
in grams and wanting to present it in either kilograms or in pounds:

.. code-block:: python

    >>> m = Quantity('2529 g')
    >>> print('mass (kg): %s' % m.render(show_units=False, scale=0.001))
    mass (kg): 2.529

    >>> print(m.render(scale=(0.0022046, 'lb'), show_si=False))
    5.5754 lb

As before, functions can also be used to do the conversion. Here is an example 
where that comes in handy: a logarithmic conversion to :index:`dBV <dB>` is 
performed.

.. code-block:: python

    >>> import math
    >>> def to_dB(value, units):
    ...     return 20*math.log10(value), 'dB'+units

    >>> T = Quantity('100mV')
    >>> print(T.render(scale=to_dB))
    -20 dBV

Finally, you can also use either the built-in converters or the converters you 
created to do the conversion simply based on the units:

.. code-block:: python

    >>> print(m.render(scale='lb'))
    5.5755 lb

In an earlier example the units of time and temperature data were converted to 
normal SI units. Presumably this makes processing easier. Now, when producing 
the output, the units can be converted back to the original units if desired:

.. code-block:: python

    >>> for time, temp in data:
    ...     print('%-7s %s' % (time.render(scale='min'), temp.render(scale='°F')))
    0 min   450 °F
    10 min  400 °F
    20 min  360 °F


.. _formatting:

String Formatting
.................

Quantities can be passed into the string *format* method:

.. code-block:: python

    >>> print('{}'.format(h_line))
    1.4204 GHz

    >>> print('{:s}'.format(h_line))
    1.4204 GHz

In these cases the preferences for SI scale factors, units, and precision are 
honored.

You can override the precision as part of the format specification

.. code-block:: python

    >>> print('{:.6}'.format(h_line))
    1.420406 GHz

You can also specify the width and alignment.

.. code-block:: python

    >>> print('|{:15.6}|'.format(h_line))
    |1.420406 GHz   |

    >>> print('|{:<15.6}|'.format(h_line))
    |1.420406 GHz   |

    >>> print('|{:>15.6}|'.format(h_line))
    |   1.420406 GHz|

The 'q' type specifier can be used to explicitly indicate that both the number 
and the units are desired and that SI scale factors should be used, regardless 
of the current preferences.

.. code-block:: python

    >>> print('{:.6q}'.format(h_line))
    1.420406 GHz

Alternately, 'r' can be used to indicate just the number represented using SI 
scale factors is desired, and the units should not be included.

.. code-block:: python

    >>> print('{:r}'.format(h_line))
    1.4204G

You can also use the floating point format type specifiers:

.. code-block:: python

    >>> print('{:f}'.format(h_line))
    1420405751.7860

    >>> print('{:e}'.format(h_line))
    1.4204e+09

    >>> print('{:g}'.format(h_line))
    1.4204e+09

Use 'u' to indicate that only the units are desired:

.. code-block:: python

    >>> print('{:u}'.format(h_line))
    Hz

Access the name or description of the quantity using 'n' and 'd'.

.. code-block:: python

    >>> print('{:n}'.format(freq))
    Fin

    >>> print('{:d}'.format(freq))
    input frequency

Using the upper case versions of the format codes that print the numerical value 
of the quantity (SQRFEG) indicates that the quantity should be labeled with its 
name and perhaps its description (as if the *show_label* preference were set). 
They are under the control of the *show_desc*, *label_fmt* and *label_fmt_full*  
preferences (described further in :ref:`preferences` and 
:meth:`quantiphy.Quantity.set_prefs()`).

If *show_desc* is False or the quantity does not have a description, then 
*label_fmtl* use used to add the labeling.

.. code-block:: python

    >>> Quantity.set_prefs(show_desc=False)
    >>> trise = Quantity('10ns', name='trise')

    >>> print('{:S}'.format(trise))
    trise = 10 ns

    >>> print('{:Q}'.format(trise))
    trise = 10 ns

    >>> print('{:R}'.format(trise))
    trise = 10n

    >>> print('{:F}'.format(trise))
    trise = 0.0000

    >>> print('{:E}'.format(trise))
    trise = 1.0000e-08

    >>> print('{:G}'.format(trise))
    trise = 1e-08

    >>> print('{0:n} = {0:q} ({0:d})'.format(freq))
    Fin = 100 MHz (input frequency)

    >>> print('{:S}'.format(freq))
    Fin = 100 MHz

If *show_desc* is True and the quantity has a description, then *label_fmt_full* 
is used if the quantity has a description.

.. code-block:: python

    >>> Quantity.set_prefs(show_desc=True)

    >>> print('{:S}'.format(trise))
    trise = 10 ns

    >>> print('{:S}'.format(freq))
    Fin = 100 MHz -- input frequency

Finally, you can add units after the format code, which causes the number to be 
scaled to those units if the transformation represents a known unit conversion.

.. code-block:: python

    >>> Tboil = Quantity('Boiling point = 100 °C')
    >>> print('{:S°F}'.format(Tboil))
    Boiling point = 212 °F

    >>> eff_channel_length = Quantity('leff = 14nm')
    >>> print(f'{eff_channel_length:SÅ}')
    leff = 140 Å

This feature can be used to simplify the conversion of the time and temperature 
information back into the original units:

.. code-block:: python

    >>> for time, temp in data:
    ...     print(f'{time:<7smin} {temp:s°F}')
    0 min   450 °F
    10 min  400 °F
    20 min  360 °F


.. _constants:

Physical Constants
------------------

*QuantiPhy* has several built-in constants that are available by specifying 
their name to the :class:`quantiphy.Quantity` class.  The following quantities 
are built in:

========  =====================  ===================== ==========================
Name      MKS value              CGS value             Description
========  =====================  ===================== ==========================
h         6.626070040e-34 J-s    6.626070040e-27 erg-s Plank's constant
hbar, ħ   1.054571800e-34 J-s    1.054571800e-27 erg-s Reduced Plank's constant
k         1.38064852e-23 J/K     1.38064852e-16 erg/K  Boltzmann's constant
q         1.6021766208e-19 C     4.80320425e-10 Fr     Elementary charge
c         2.99792458e8 m/s       2.99792458e8 m/s      Speed of light
0C, 0°C   273.15 K               273.15 K              0 Celsius
eps0, ε₀  8.854187817e-12 F/m    ---                   Permittivity of free space
mu0, μ₀   4e-7π H/m              ---                   Permeability of free space
Z0, Z₀    376.730313461 Ohms     ---                   Characteristic impedance
                                                       of free space
========  =====================  ===================== ==========================

Constants are given in base units (*g*, *m*, etc.) rather than the natural units 
for the unit system (*kg*, *cm*, etc.). For example, when using the CGS unit 
system, the speed of light is given as 300Mm/s (rather than 30Gcm/s).

As shown, these constants are partitioned into two *unit systems*: *mks* and 
*cgs*.  Only those constants that are associated with the active unit system and 
those that are not associated with any unit system are available when creating 
a new quantity. You can activate a unit system using 
:func:`quantiphy.set_unit_system`.  Doing so deactivates the previous system. By 
default, the *mks* system is active.

You can create your own constants and unit systems using
:func:`quantiphy.add_constant`:

.. code-block:: python

    >>> from quantiphy import Quantity, add_constant
    >>> add_constant(Quantity("λh: 211.061140539mm // wavelength of hydrogen line"))

    >>> hy_wavelength = Quantity('λh')
    >>> print(hy_wavelength.render(show_label=True))
    λh = 211.06 mm -- wavelength of hydrogen line

In this case is the name given in the quantity is used when creating the 
constant.  You can also specify an alias as an argument to *add_constant*.

.. code-block:: python

    >>> add_constant(
    ...     Quantity("λh = 211.061140539mm # wavelength of hydrogen line"),
    ...     alias='lambda h'
    ... )

    >>> hy_wavelength = Quantity('lambda h')
    >>> print(hy_wavelength.render(show_label=True))
    λh = 211.06 mm -- wavelength of hydrogen line

It is not necessary to specify both the name and the alias, one is sufficient, 
but the constant is accessible using either.  Notice that the alias does not 
actually become part of the constant, it is only used for looking up the 
constant.

By default, user defined constants are not associated with a unit system, 
meaning that they are always available regardless of which unit system is 
being used.  However, when creating a constant you can specify one or more 
unit systems for the constant. You need not limit yourself to the predefined 
*mks* and *cgs* unit systems. You can specify multiple unit systems either by 
specifying a list of strings for the unit systems, or by specifying one string 
that would contain more than one name once split.

.. code-block:: python

    >>> from quantiphy import Quantity, add_constant, set_unit_system

    >>> add_constant(Quantity(4.80320427e-10, 'Fr'), 'q', 'esu gaussian')
    >>> add_constant(Quantity(1.602176487e-20, 'abC'), alias='q', unit_systems='emu')
    >>> q_mks = Quantity('q')
    >>> set_unit_system('cgs')
    >>> q_cgs = Quantity('q')
    >>> set_unit_system('esu')
    >>> q_esu = Quantity('q')
    >>> set_unit_system('gaussian')
    >>> q_gaussian = Quantity('q')
    >>> set_unit_system('emu')
    >>> q_emu = Quantity('q')
    >>> set_unit_system('mks')
    >>> print(q_mks, q_cgs, q_esu, q_gaussian, q_emu, sep='\n')
    160.22e-21 C
    480.32 pFr
    480.32 pFr
    480.32 pFr
    16.022e-21 abC


.. _preferences:

Preferences
-----------

*QuantiPhy* supports a wide variety of preferences that control its behavior.  
For example, when rendering quantities you can control the number of digits used 
(*prec*), whether SI scale factors are used (*show_si*), whether the units are 
included (*show_units*), etc.  Similar preferences also control the conversion 
of strings into quantities, which can help disambiguate whether a suffix 
represents a scale factor or a unit. The list of available preferences and their 
descriptions are given in the description of the 
:meth:`quantiphy.Quantity.set_prefs` method.

To set a preference, use the :meth:`quantiphy.Quantity.set_prefs` class method.  
You can set more than one preference at once:

.. code-block:: python

    >>> Quantity.set_prefs(prec=6, map_sf={'u': 'μ'})

This statements tells *QuantiPhy* to use 7 digits (the *prec* plus 1) and to 
output μ rather u for the 10\ :sup:`-6` scale factor.

Setting preferences to *None* returns them to their default values:

.. code-block:: python

    >>> Quantity.set_prefs(prec=None, map_sf=None)

The preferences are changed on the class itself, meaning that they affect any 
instance of that class regardless of whether they were instantiated before or 
after the preferences were set. If you would like to have more than one set of 
preferences, then you should subclass :class:`quantiphy.Quantity`. For example, 
imagine a situation where you have different types of quantities that would 
naturally want different precisions:

.. code-block:: python

    >>> class Temperature(Quantity):
    ...     pass
    >>> Temperature.set_prefs(prec=1, known_units='K', spacer='')

    >>> class Frequency(Quantity):
    ...     pass
    >>> Frequency.set_prefs(prec=5, spacer='')

    >>> frequencies = []
    >>> for each in '-25.3 999987.7, 25.1  1000207.1, 74.9  1001782.3'.split(','):
    ...     temp, freq = each.split()
    ...     frequencies.append((Temperature(temp, 'C'),  Frequency(freq, 'Hz')))

    >>> for temp, freq in frequencies:
    ...     print(f'{temp:>4s}  {freq}')
    -25C  999.988kHz
     25C  1.00021MHz
     75C  1.00178MHz

In this example, a subclass is created that is intended to report in 
concentrations.

.. code-block:: python

    >>> class Concentration(Quantity):
    ...     pass
    >>> Concentration.set_prefs(
    ...     map_sf = dict(u=' PPM', n= ' PPB', p=' PPT'),
    ...     show_label = True,
    ... )

    >>> pollutants = dict(CO=5, SO2=20, NO2=0.10)
    >>> concentrations = [Concentration(v, scale=1e-6, name=k) for k, v in pollutants.items()]
    >>> for each in concentrations:
    ...     print(each)
    CO = 5 PPM
    SO2 = 20 PPM
    NO2 = 100 PPB

When a subclass is created, the preferences active in the main class are copied 
into the subclass. Subsequent changes to the preferences in the main class do 
not affect the subclass.

You can also go the other way and override the preferences on a specific 
quantity.

.. code-block:: python

    >>> print(hy_wavelength)
    211.06 mm

    >>> hy_wavelength.show_label = True
    >>> print(hy_wavelength)
    λh = 211.06 mm -- wavelength of hydrogen line

This is often the way to go with quantities that have :index:`logarithmic units`
such as decibels (:index:`dB`) or shannons (Sh) (or the related bit, digits, 
nats, hartleys, etc.). In these cases use of SI scale factors is often 
undesired.

.. code-block:: python

    >>> gain = Quantity(0.25, 'dB')
    >>> print(gain)
    250 mdB

    >>> gain.show_si = False
    >>> print(gain)
    250e-3 dB

To retrieve a preference, use the :meth:`quantiphy.Quantity.get_pref` class 
method. This is useful with *known_units*. Normally setting *known_units* 
overrides the existing units. You can simply add more with:

.. code-block:: python

    >>> Quantity.set_prefs(known_units=Quantity.get_pref('known_units') + ['K'])

A variation on :meth:`quantiphy.Quantity.set_prefs` is 
:meth:`quantiphy.Quantity.prefs`. It is basically the same, except that it is 
meant to work with Python's *with* statement to temporarily override 
preferences:

.. code-block:: python

    >>> with Quantity.prefs(show_si=False, show_units=False):
    ...     for time, temp in data:
    ...         print('%-7s %s' % (time, temp))
    0       505.37
    600     477.59
    1.2e3   455.37

    >>> print('Final temperature = %s @ %s.' % data[-1][::-1])
    Final temperature = 455.37 K @ 1.2 ks.

Notice that the specified preferences only affected the table, not the final 
printed values, which were rendered outside the *with* statement.


.. _ambiguity:

Ambiguity of Scale Factors and Units
------------------------------------

.. index::
   single: meter/milli ambiguity

By default, *QuantiPhy* treats both the scale factor and the units as being 
optional.  With the scale factor being optional, the meaning of some 
specifications can be ambiguous. For example, '1m' may represent 1 milli or it 
may represent 1 meter.  Similarly, '1meter' my represent 1 meter or 
1 milli-eter.  In this case *QuantiPhy* gives preference to the scale factor, so 
'1m' normally converts to 1e-3. To allow you to avoid this ambiguity, 
*QuantiPhy* accepts '_' as the unity scale factor.  In this way '1_m' is 
unambiguously 1 meter. You can instruct *QuantiPhy* to output '_' as the unity 
scale factor by specifying the *unity_sf* argument to 
:meth:`quantiphy.Quantity.set_prefs()`:

.. code-block:: python

    >>> Quantity.set_prefs(unity_sf='_', spacer='')
    >>> l = Quantity(1, 'm')
    >>> print(l)
    1_m

This is often a good way to go if you are outputting numbers intended to be read 
by people and machines.

If you need to interpret numbers that have units and are known not to have scale 
factors, you can specify the *ignore_sf* preference:

.. code-block:: python

    >>> Quantity.set_prefs(ignore_sf=True, unity_sf='', spacer=' ')
    >>> l = Quantity('1000m')
    >>> l.as_tuple()
    (1000.0, 'm')

    >>> print(l)
    1 km

    >>> Quantity.set_prefs(ignore_sf=False)
    >>> l = Quantity('1000m')
    >>> l.as_tuple()
    (1.0, '')

If there are scale factors that you know you will never use, you can instruct 
*QuantiPhy* to interpret a specific set and ignore the rest using the *input_sf* 
preference.

.. code-block:: python

    >>> Quantity.set_prefs(input_sf='GMk')
    >>> l = Quantity('1000m')
    >>> l.as_tuple()
    (1000.0, 'm')

    >>> print(l)
    1 km

Specifying *input_sf=None* causes *QuantiPhy* to again accept all known scale 
factors again.

.. code-block:: python

    >>> Quantity.set_prefs(input_sf=None)
    >>> l = Quantity('1000m')
    >>> l.as_tuple()
    (1.0, '')

Alternatively, you can specify the units you wish to use whose leading character 
is a scale factor.  Once known, these units no longer confuse *QuantiPhy*.  
These units can be specified as a list or as a string. If specified as a string 
the string is split to form the list. Specifying the known units replaces any 
existing known units.

.. code-block:: python

    >>> d1 = Quantity('1 au')
    >>> d2 = Quantity('1000 pc')
    >>> print(d1.render(show_si=False), d2, sep='\n')
    1e-18 u
    1 nc

    >>> Quantity.set_prefs(known_units='au pc')
    >>> d1 = Quantity('1 au')
    >>> d2 = Quantity('1000 pc')
    >>> print(d1.render(show_si=False), d2, sep='\n')
    1 au
    1 kpc

.. index::
   single: Kelvin/kilo ambiguity

This same issue comes up for temperature quantities when given in Kelvin. There 
are again several ways to handle this. First you can specify the acceptable 
input scale factors leaving out 'K', ex. *input_sf* = 'TGMkmunpfa'.  
Alternatively, you can specify 'K' as one of the known units. Finally, if you 
know exactly when you will be converting a temperature to a quantity, you can 
specify *ignore_sf* for that specific conversion. The effect is the same either 
way, 'K' is interpreted as a unit rather than a scale factor.


.. _tabular data:

Formatting Tabular Data
-----------------------

When creating tables it is often desirable to align the decimal points of the 
numbers, and perhaps align the units. You can use the *number_fmt* to arrange 
this. *number_fmt* is a format string that if specified is used to convert the 
components of a number into the final number. You can control the widths and 
alignments of the components to implement specific arrangements.  *number_fmt* 
is passed to the string *format* function with named arguments: *whole*, *frac* 
and *units*, which contains the integer part of the number, the fractional part 
including the decimal point, and the units including the scale factor.  More 
information about the content of the components can be found in 
:meth:`quantiphy.Quantity.set_prefs()`.

For example, you can align the decimal point and units of a column of numbers 
like this:

.. code-block:: python

    >>> lengths = [
    ...     Quantity(l)
    ...     for l in '1mm, 10mm, 100mm, 1.234mm, 12.34mm, 123.4mm'.split(',')
    ... ]

    >>> with Quantity.prefs(number_fmt='{whole:>3s}{frac:<4s} {units}'):
    ...     for l in lengths:
    ...         print(l)
      1     mm
     10     mm
    100     mm
      1.234 mm
     12.34  mm
    123.4   mm

You can also give a function as the value for *number_fmt* rather than a string.  
It would be called with *whole*, *frac* and *units* as arguments given in that 
order.  The function is expected to return the assembled number as a string. For 
example:

.. code-block:: python

    >>> def fmt_num(whole, frac, units):
    ...     return '{mantissa:<5s} {units}'.format(mantissa=whole+frac, units=units)

    >>> with Quantity.prefs(number_fmt=fmt_num):
    ...     for l in lengths:
    ...         print(l)
    1     mm
    10    mm
    100   mm
    1.234 mm
    12.34 mm
    123.4 mm

If there are multiple columns it might be necessary to apply a different format 
to each column. In this case, it often makes sense to create a subclass of 
Quantity for each column that requires distinct formatting:

.. code-block:: python

    >>> def format_temperature(whole, frac, units):
    ...     return '{:>5s} {:<5s}'.format(whole+frac, units)

    >>> class Temperature(Quantity):
    ...     pass
    >>> Temperature.set_prefs(
    ...     prec = 1, known_units = 'K', number_fmt = format_temperature
    ... )

    >>> class Frequency(Quantity):
    ...     pass
    >>> Frequency.set_prefs(prec=5, number_fmt = '{whole:>3s}{frac:<6s} {units}')

    >>> frequencies = []
    >>> for each in '-25.3 999987.7, 25.1 1000207.1, 74.9 1001782.3'.split(','):
    ...     temp, freq = each.split()
    ...     frequencies.append((Temperature(temp, 'C'),  Frequency(freq, 'Hz')))

    >>> for temp, freq in frequencies:
    ...     print(temp, freq)
      -25 C     999.988   kHz
       25 C       1.00021 MHz
       75 C       1.00178 MHz


.. _extract:

Extract Quantities
------------------

It is possible to put a collection of quantities in a text string and then use 
the :meth:`quantiphy.Quantity.extract()` method to parse the quantities and 
return them in a dictionary.  For example:

.. code-block:: python

    >>> design_parameters = '''
    ...     Fref = 156 MHz     -- Reference frequency
    ...     Kdet = 88.3 uA     -- Gain of phase detector
    ...     Kvco = 9.07 GHz/V  -- Gain of VCO
    ... '''
    >>> quantities = Quantity.extract(design_parameters)

    >>> Quantity.set_prefs(
    ...     label_fmt='{n} = {v}',
    ...     label_fmt_full='{V:<18}  # {d}',
    ...     show_label='f',
    ... )
    >>> for q in quantities.values():
    ...     print(q)
    Fref = 156 MHz      # Reference frequency
    Kdet = 88.3 uA      # Gain of phase detector
    Kvco = 9.07 GHz/V   # Gain of VCO

:meth:`quantiphy.Quantity.extract()` ignores blank lines and any line that does 
not have a value, so you can insert comments into the string by giving 
a description without a name or value:

.. code-block:: python

    >>> design_parameters = '''
    ...     -- PLL Design Parameters
    ...
    ...     Fref = 156 MHz  -- Reference frequency
    ...     Kdet = 88.3 uA  -- Gain of phase detector
    ...     Kvco = 9.07 GHz/V  -- Gain of VCO
    ... '''
    >>> globals().update(Quantity.extract(design_parameters))

    >>> print(f'{Fref:S}\n{Kdet:S}\n{Kvco:S}', sep='\n')
    Fref = 156 MHz      # Reference frequency
    Kdet = 88.3 uA      # Gain of phase detector
    Kvco = 9.07 GHz/V   # Gain of VCO

In this case the output of the :meth:`quantiphy.Quantity.extract()` call is fed 
into globals().update() so as to add the quantities into the module namespace, 
making the quantities accessible as local variables.

Any number of quantities may be given, with each quantity given on its own line.  
The identifier given to the left '=' is the name of the variable in the local 
namespace that is used to hold the quantity. The text after the '--' is used as 
a description of the quantity.

In this example the output of :meth:`quantiphy.Quantity.extract()` is added into 
the local names space.  This is an example of how simulation scripts could be 
written. The system and simulation parameters would be gathered together at the 
top into a multiline string, which would then be read and loaded into the local 
name space. It allows you to quickly give a complete description of a collection 
of parameters when the goal is to put something together quickly in an 
expressive manner.

Here is an example that uses this feature to read parameters from a file. This 
is basically the same idea as above, except the design parameters are kept in 
a separate file.  It also subclasses :class:`quantiphy.Quantity` to create 
a version that displays the name and description by default.

.. code-block:: python

    >>> from quantiphy import Quantity
    >>> from inform import os_error, fatal, display

    >>> class VerboseQuantity(Quantity):
    ...    show_label = 'f'
    ...    label_fmt = '{n} = {v}'
    ...    label_fmt_full = '{V:<18} -- {d}'

    >>> filename = 'parameters'
    >>> try:
    ...     with open(filename) as f:
    ...         globals().update(VerboseQuantity.extract(f.read()))
    ... except OSError as err:
    ...     fatal(os_error(err))
    ... except ValueError as err:
    ...     fatal(err, culprit=filename)

    >>> display(Fref, Kdet, Kvco, sep='\n')
    Fref = 156 MHz     -- Reference frequency
    Kdet = 88.3 uA     -- Gain of phase detector (Imax)
    Kvco = 9.07 GHz/V  -- Gain of VCO


.. _translate:

Translating Quantities
----------------------

:meth:`quantiphy.Quantity.all_from_conv_fmt()` recognizes conventionally 
formatted numbers and quantities embedded in text and reformats them using 
:meth:`quantiphy.Quantity.render()`. This is an difficult task in general, and 
so some constraints are placed on the values to make them easier to distinguish.  
Specifically, the units, if given, must be simple and immediately adjacent to 
the number. Units are simple if they only consist of letters and underscores.  
The characters °, Å, Ω and ℧ are also allowed.  So '47e3Ohms', '50_Ohms' and 
'1.0e+12Ω' are recognized as quantities, but '50 Ohms' and '12m/s' are not.

Besides the text to be translated, :meth:`all_from_conv_fmt` takes the same 
arguments as :meth:`render`, though they must be given as named arguments.

.. code-block:: python

    >>> test_results = '''
    ... Applying stimulus @ 2.00500000e-04s: V(in) = 5.000000e-01V.
    ... Pass @ 3.00500000e-04s: V(out): expected=2.00000000e+00V, measured=1.99999965e+00V, diff=3.46117130e-07V.
    ... '''.strip()

    >>> Quantity.set_prefs(spacer='')
    >>> translated = Quantity.all_from_conv_fmt(test_results)
    >>> print(translated)
    Applying stimulus @ 200.5us: V(in) = 500mV.
    Pass @ 300.5us: V(out): expected=2V, measured=2V, diff=346.12nV.

:meth:`quantiphy.Quantity.all_from_si_fmt()` is similar, except that it 
recognizes quantities formatted with either a scale factor or units and ignores 
plain numbers. Again, units are expected to be simple and adjacent to their 
number.

.. code-block:: python

    >>> Quantity.set_prefs(spacer='')
    >>> translated_back = Quantity.all_from_si_fmt(translated, show_si=False)
    >>> print(translated_back)
    Applying stimulus @ 200.5e-6s: V(in) = 500e-3V.
    Pass @ 300.5e-6s: V(out): expected=2V, measured=2V, diff=346.12e-9V.

Notice in the translations the quantities lost resolution. This is avoided if 
you use 'full' precision:

.. code-block:: python

    >>> translated = Quantity.all_from_conv_fmt(test_results, prec='full')
    >>> print(translated)
    Applying stimulus @ 200.5us: V(in) = 500mV.
    Pass @ 300.5us: V(out): expected=2V, measured=1.99999965V, diff=346.11713nV.


.. _equivalence:

Equivalence
-----------

You can determine whether the value of a quantity or real number is equivalent 
to that of a quantity using :meth:`quantiphy.Quantity.is_close()`.  The two 
values need not be identical, they just need to be close to be deemed 
equivalent. The *reltol* and *abstol* preferences are used to determine if they 
are close.

.. code-block:: python

   >>> h_line.is_close(h_line)
   True

   >>> h_line.is_close(h_line + 1)
   True

   >>> h_line.is_close(h_line + 1e4)
   False

:meth:`quantiphy.Quantity.is_close()` returns true if the units match and if:

   | abs(*a* - *b*) <= max(reltol * max(abs(*a*), abs(*b*)), abstol)

where *a* and *b* represent *other* and the numeric value of the underlying 
quantity.

By default, *is_close()* looks at the both the value and the units if the 
argument has units. In this way if you compare two quantities with different 
units, the *is_close()* test will always fail if their units differ.  This 
behavior can be overridden by specifying *check_units*.

.. code-block:: python

   >>> Quantity('10ns').is_close(Quantity('10nm'))
   False

   >>> Quantity('10ns').is_close(Quantity('10nm'), check_units=False)
   True


.. _exceptional values:

Exceptional Values
------------------

*QuantiPhy* supports NaN (not a number) and infinite values:

   >>> inf = Quantity('inf Hz')
   >>> print(inf)
   inf Hz

   >>> nan = Quantity('NaN Hz')
   >>> print(nan)
   nan Hz

You can test whether the value of the quantity is infinite or is not-a-number
using :meth:`quantiphy.Quantity.is_infinite()` or 
:meth:`quantiphy.Quantity.is_nan()`:

.. code-block:: python

   >>> h_line.is_infinite()
   False

   >>> inf.is_infinite()
   True

   >>> h_line.is_nan()
   False

   >>> nan.is_nan()
   True


.. _exceptions:

Exceptions
----------

A *ValueError* is raised if :class:`quantiphy.Quantity` is passed a string it 
cannot convert into a number:

.. code-block:: python

   >>> try:
   ...     q = Quantity('g')
   ... except ValueError as err:
   ...     print(err)
   g: not a valid number.

A *KeyError* is raised if a unit conversion is requested but no suitable unit
converter is available.

.. code-block:: python

   >>> q = Quantity('93 Mmi', scale='pc')
   Traceback (most recent call last):
   ...
   KeyError: "Unable to convert between 'pc' and 'mi'."

A *KeyError* is also raised if you specify an unknown preference.

.. code-block:: python

   >>> Quantity.set_prefs(precision=6)
   Traceback (most recent call last):
   ...
   KeyError: 'precision'


A *NameError* is raised if a constant is created without a name or if you try to 
set or get a preference that is not supported.

.. code-block:: python

   >>> q = add_constant(Quantity('1ns'))
   Traceback (most recent call last):
   ...
   NameError: No name specified.
