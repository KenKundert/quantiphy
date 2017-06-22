.. QuantiPhy

QuantiPhy: Physical Quantities
==============================

| Version: 1.3.5
| Released: 2017-06-22
| Please report all bugs and suggestions to
  `quantiphy@nurdletech.com <mailto://quantiphy@nurdletech.com>`_ or
  `Github <https://github.com/KenKundert/quantiphy>`_.

Synopsis
--------

Quantities are a pairing of a number and units. They are used when specifying 
amounts of some measurable thing.

The *QuantiPhy* package provides the *Quantity* class that extends the *float* 
class that is built into Python. This new *Quantity* class ...

#. Accepts real values with units in a variety of common forms, including those 
   that include SI scale factors.
#. Converts them into an object that is treated as a floating point number in 
   expressions,
#. Generally includes the units when printing or converting to strings and by 
   default employs the SI scale factors.
#. Unit conversion and scaling is supported when converting to or from 
   quantities.
#. Also provides a small but extensible collection of physical constants.


Contents:

* :ref:`overview`

  - :ref:`the alternatives`
  - :ref:`quantities`
  - :ref:`constants`
  - :ref:`preferences`
  - :ref:`ambiguity`
  - :ref:`formatting`
  - :ref:`extract`
  - :ref:`equivalence`
  - :ref:`exceptional values`
  - :ref:`exceptions`

.. toctree::
   :maxdepth: 2

   reference
   examples
   releases

.. _overview:

Overview
--------

*QuantiPhy* adds support for quantities to Python. Quantities are little more 
than a number combined with its units. They are used to represent physical 
quantities. For example, your height and weight are both quantities, having both 
a value and units, and both are important. For example, if I told you that 
Mariam's weight was 8, you might think Mariam was an infant if you lived in the 
US and assume pounds as the unit of measure, or an adult if you lived in the UK 
and assume stones, or a small child almost anywhere else and so assume 
kilograms.  In general it is always best to keep the unit of measure with the 
number and present the complete value when working with quantities. To do 
otherwise invites confusion.  Users often stumble on numbers without units as 
they mentally try to determine the units from context.  Quantity values should 
be treated in a manner similar to money, which is also a quantity. Monetary 
amounts are almost always given with their units (a currency symbol).

Having a single object represent a quantity in a programming language is useful 
because it binds the units to the number making it more likely that the units 
will be presented with the number. In addition, quantities from *QuantiPhy* 
provide another important benefit.  They naturally support the SI scale factors, 
which for those that are familiar with them are much easer to read and write 
than the alternatives. The most common SI scale factors are:

    |   T (10\ :sup:`12`)
    |   G (10\ :sup:`9`)
    |   M (10\ :sup:`6`)
    |   k (10\ :sup:`3`)
    |   m (10\ :sup:`-3`)
    |   μ (10\ :sup:`-6`)
    |   n (10\ :sup:`-9`)
    |   p (10\ :sup:`-12`)
    |   f (10\ :sup:`-15`)
    |   a (10\ :sup:`-18`)

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
in place for over 50 years and is very widely used.

*QuantiPhy* is an attempt to address both of these deficiencies. It allows 
quantities to be represented with a single object that allows the complete 
quantity to be easily read or written as a single unit. It also naturally 
supports SI scale factors.  As such, *QuantiPhy* allows computers to communicate 
more naturally with humans, particularly scientists and engineers.


.. _the alternatives:

Alternatives
''''''''''''

There are a considerable number of Python packages dedicated to units and 
quantities (`Alternatives <https://kdavies4.github.io/natu/seealso.html>`_).  
However, as a rule, they focus on the units rather than the scale factors. In 
particular, they build a system of units that you are expected to use throughout 
your calculations.  These packages demand a high level of commitment from their 
users and in turn provide unit consistency and built-in unit conversions.  In 
contrast, *QuantiPhy* treats units basically as documentation.  They are simply 
strings that are attached to quantities largely so they can be presented to the 
user when the values are printed. As such, *QuantiPhy* is a light-weight package 
that demands little from the user. It is used when inputting and outputting 
values, and then only when it provides value. As a result, it provides 
a simplicity in use that cannot be matched by the other packages.


.. _quantities:

Quantities
''''''''''

*QuantiPhy* is a library that adds support to Python for both reading and 
writing numbers with SI scale factors and units. The primary working construct 
for *QuantiPhy* is Quantity, which is a class whose objects hold the number and 
units that are used to represent a physical quantity. For example, to create 
a quantity from a string you can use:

.. code-block:: python

    >>> from quantiphy import Quantity

    >>> distance_to_sun = Quantity('150 Gm')
    >>> distance_to_sun.real
    150000000000.0

    >>> distance_to_sun.units
    'm'

    >>> print(distance_to_sun)
    150 Gm

Now ``distance_to_sun`` contains two items, the number 150000000000.0 and the 
units 'm'.  The 'G' was interpreted as the *giga* scale factor, which scales by 
10\ :sup:`9`.

Quantity is a subclass of float, and so ``distance_to_sun`` can be used just 
like any real number. For example, you can convert the distance to miles using:

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

Quantities naturally work with all the normal ways that Python provides for 
printing values or converting them to strings:

.. code-block:: python

    >>> print(distance_to_sun)
    150 Gm

    >>> str(distance_to_sun)
    '150 Gm'

    >>> 'Distance to sun = {}.'.format(distance_to_sun)
    'Distance to sun = 150 Gm.'

    >>> 'Distance to sun = %s.' % distance_to_sun
    'Distance to sun = 150 Gm.'

    >>> f'Distance to sun = {distance_to_sun}.'
    'Distance to sun = 150 Gm.'

And finally, Quantity provides a method that allows you to control the manner in 
which the conversion to a string is performed:

.. code-block:: python

    >>> distance_to_sun.render(show_units=False, show_si=False)
    '150e9'

Besides converting to a string, there are a variety of ways of accessing the 
information in the quantity.

.. code-block:: python

    >>> float(distance_to_sun)
    150000000000.0

    >>> distance_to_sun.real
    150000000000.0

    >>> distance_to_sun.units
    'm'

    >>> distance_to_sun.as_tuple()
    (150000000000.0, 'm')

Of course you can also use a quantity in an expression, in which case it acts 
like a float.

When creating a quantity, you can also give it a name and description. For 
example:

.. code-block:: python

    >>> period = Quantity('Tclk = 10ns -- clock period')
    >>> print(f'{period.name} = {period} -- {period.desc}')
    Tclk = 10 ns -- clock period

If you only specify a real number for the value of a Quantity, then the units, 
name, and description do not get values. This is where the second argument, 
*model*, helps. It may be another quantity or it may be a string.  Any 
attributes that are not provided by the first argument are taken from the second 
if available.  If *model* is a quantity, only its units are taken. If *model* is 
a string, it is split.  If it contains one value, that value is taken to be the 
units, if it contains two, those values are taken to be the name and units, and 
it it contains more than two, the remaining values are taken to be the 
description.  For example:

.. code-block:: python

    >>> out_period = Quantity(10*period, period)
    >>> print(out_period.render(show_label=True))
    100 ns

    >>> freq = Quantity(1/period, 'Hz')
    >>> print(freq.render(show_label=True))
    100 MHz

    >>> freq = Quantity(1/period, 'Fclk Hz')
    >>> print(freq.render(show_label=True))
    Fclk = 100 MHz

    >>> freq = Quantity(1/period, 'Fclk Hz input frequency')
    >>> print(freq.render(show_label=True))
    Fclk = 100 MHz

Notice in the last example a description was given when creating the quantity, 
but it was not displayed. That is because by default the descriptions are not 
shown. This is under control of the :meth:`label_fmt <Quantity.set_preferences>` 
preference. That will be adjusted and the quantity reprinted:

.. code-block:: python

    >>> Quantity.set_preferences(label_fmt=('{n} = {v} -- {d}', '{n} = {v}'))
    >>> print(freq.render(show_label=True))
    Fclk = 100 MHz -- input frequency

Alternatively, you can explicitly specify the units, the name, and the 
description using named arguments. These values override anything specified in 
the value or *model*.

.. code-block:: python

    >>> out_period = Quantity(
    ...     10*period, period, name='Tout',
    ...     desc='period at output of frequency divider'
    ... )
    >>> print(out_period.render(show_label=True))
    Tout = 100 ns -- period at output of frequency divider

Finally, you can overwrite the quantities attributes to override the units, 
name, or description.

.. code-block:: python

    >>> out_period = Quantity(10*period)
    >>> out_period.units = 's'
    >>> out_period.name = 'Tout'
    >>> out_period.desc = 'period at output of frequency divider'
    >>> print(out_period.render(show_label=True))
    Tout = 100 ns -- period at output of frequency divider


Scaling When Creating a Quantity
................................

Quantities tend to be used primarily when reading and writing numbers, and less 
often when processing numbers. Often data comes in an undesirable form. For 
example, imagine data that has been normalized to kilograms but the numbers 
themselves have neither units or scale factors.  *QuantiPhy* allows you to scale 
tne number and assign the units when creating the quantity:

.. code-block:: python

    >>> mass = Quantity('2.529', scale=1000, units='g')
    >>> print(mass)
    2.529 kg

In this case the value is given in kilograms, and is converted to the base units 
of grams by multiplying the given value by 1000.

*QuantiPhy* provides other mechanisms for scaling numbers as they are converted 
to quantities.  You can also specify a function to do the conversion, which is 
helpful when the conversion is not linear:

.. code-block:: python

    >>> def from_dB(value, units=''):
    ...     return 10**(value/20), units[2:]

    >>> Quantity('-100 dBV', scale=from_dB)
    Quantity('10 uV')

The conversion can also often occur if you simply state the units you wish the 
quantity to have:

.. code-block:: python

    >>> T_boil = Quantity('212 °F', scale='K')
    >>> print(T_boil)
    373.15 K

To do the conversion, *QuantiPhy* examines the given units (°F) and the desired 
units (K) and choses the appropriate converter.  *QuantiPhy* provides 
:class:`predefined converters <UnitConversion>` for common units and you are 
free to add your own.  To create your own scale converters, you would use 
:class:`UnitConversion`:

.. code-block:: python

    >>> from quantiphy import UnitConversion

    >>> UnitConversion('m', 'pc parsec', 3.0857e16)
    <...>

    >>> d = Quantity('5 μpc', scale='m')
    >>> print(d)
    154.28 Gm

This unit conversion says, when converting units of 'm' to either 'pc' or 
'parsec' multiply by 3.0857e16, when going the other way, divide by 3.0857e16.

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
where that comes in handy: a logarithmic conversion to dBV is performed.

.. code-block:: python

    >>> import math
    >>> def to_dB(value, units):
    ...     return 20*math.log10(value), 'dB'+units

    >>> T = Quantity('100mV')
    >>> print(T.render(scale=to_dB))
    -20 dBV

Finally, :class:`you can also use <UnitConversion>` either the built in 
conversion or the converters your added to do the conversion simply based on the 
units:

.. code-block:: python

    >>> print(m.render(scale='lb'))
    5.5755 lb

In an earlier example the units of time and temperature data were converted to 
normal SI units. Presumably this make processing easier. Now, when producing 
output, the units can be converted back to the original units if desired:

.. code-block:: python

    >>> for time, temp in data:
    ...     print('%-7s %s' % (time.render(scale='min'), temp.render(scale='°F')))
    0 min   450 °F
    10 min  400 °F
    20 min  360 °F


.. _constants:

Physical Constants
''''''''''''''''''

The Quantity class also supports a small number of predefined physical 
constants, partitioned into two different unit systems. By default the MKS unit 
system is used, but CGS units are also available. You can also create your own 
:class:`constants and unit systems <Constant>`.

You access a constant by specifying its name when creating a quantity.  For 
example:

.. code-block:: python

    >>> h = Quantity('h')
    >>> print(h)
    662.61e-36 J-s

The following quantities are built in:

========  =====================  ===================== ==========================
name      mks value              cgs value             description
========  =====================  ===================== ==========================
h         6.626070040e-34 J-s    6.626070040e-27 erg-s Plank's constant
hbar, ħ   1.054571800e-34 J-s    1.054571800e-27 erg-s Reduces Plank's constant
k         1.38064852e-23 J/K     1.38064852e-16 erg/K  Boltzmann's constant
q         1.6021766208e-19 C     4.80320425e-10 Fr     elementary charge
c         2.99792458e8 m/s       2.99792458e8 m/s      speed of light
0C, 0°C   273.15 K               273.15 K              O Celsius
eps0, ε₀  8.854187817e-12 F/m    ---                   permittivity of free space
mu0, μ₀   4e-7π H/m              ---                   permeability of free space
Z0, Z₀    376.730313461 Ohms     ---                   characteristic impedance
                                                       of free space
========  =====================  ===================== ==========================

Constants are given in base units rather than the natural units for the unit 
system. For example, when using the CGS unit system, the speed of light is given 
as 300Mm/s (rather than 30Gcm/s).

You can create your own constants by instantiating the :class:`Constant` class:

.. code-block:: python

    >>> from quantiphy import Constant

    >>> h_line = Quantity('f_hy = 1420.405751786 MHz -- frequency of the hydrogen line')
    >>> Constant(h_line, name='h line frequency')
    <...>

Now it is available by name:

.. code-block:: python

    >>> fh = Quantity('h line frequency')
    >>> print(fh)
    1.4204 GHz


.. _preferences:

Preferences
'''''''''''

*QuantiPhy* supports a wide variety of :meth:`preferences 
<Quantity.set_preferences>` that control its behavior.  For example, when 
rendering quantities you can control the number of digits used (*prec*), whether 
SI scale factors are used (*show_si*), whether the units are included 
(*show_units*), etc.  Similar preferences also control the conversion of strings 
into quantities, which can help disambiguate whether a suffix represents a scale 
factor or a unit.

To set a preference, use the :meth:`Quantity.set_preferences` class method. You 
can set more than one preference at once:

.. code-block:: python

    >>> Quantity.set_preferences(prec=6, map_sf={'u': 'μ'})

This statements tells *QuantiPhy* to use 7 digits (the *prec* plus 1) and to 
output μ rather u for the 10\ :sup:`-6` scale factor.

Setting preferences to *None* return them to their default values:

.. code-block:: python

    >>> Quantity.set_preferences(prec=None, map_sf=None)

The preferences are changed on the class itself, meaning that they affect any 
instance of that class regardless of whether they were instantiated before or 
after the preferences were set. If you would like to have more than one set of 
preferences, then you should subclass Quantity. For example:

.. code-block:: python

    >>> class ConventionalQuantity(Quantity):
    ...     pass

    >>> ConventionalQuantity.set_preferences(show_si=False, show_units=False)

    >>> period1 = Quantity(1e-9, 's')
    >>> period2 = ConventionalQuantity(1e-9, 's')
    >>> print(period1, period2, sep='\n')
    1 ns
    1e-9

You can also go the other way and override the preferences on a specific 
quantity.

    >>> period1.show_si = False
    >>> period1.show_units = False
    >>> print(period1)
    1e-9


.. _ambiguity:

Ambiguity of Scale Factors and Units
''''''''''''''''''''''''''''''''''''

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
scale factor by specifying the *unity_sf* argument to *set_preferences*:

.. code-block:: python

    >>> Quantity.set_preferences(unity_sf='_', spacer='')
    >>> l = Quantity(1, 'm')
    >>> print(l)
    1_m

If you need to interpret numbers that have units and are known not to have scale 
factors, you can specify the *ignore_sf* preference:

.. code-block:: python

    >>> Quantity.set_preferences(ignore_sf=True, unity_sf='', spacer=' ')
    >>> l = Quantity('1000m')
    >>> l.as_tuple()
    (1000.0, 'm')

    >>> print(l)
    1 km

    >>> Quantity.set_preferences(ignore_sf=False)
    >>> l = Quantity('1000m')
    >>> l.as_tuple()
    (1.0, '')

If there are scale factors that you know you will never use, you can instruct 
*QuantiPhy* to interpret a specific set and ignore the rest using the *input_sf* 
preference.

.. code-block:: python

    >>> Quantity.set_preferences(input_sf='GMk')
    >>> l = Quantity('1000m')
    >>> l.as_tuple()
    (1000.0, 'm')

    >>> print(l)
    1 km

Specifying *input_sf=None* causes *QuantiPhy* to again accept all known scale 
factors.

.. code-block:: python

    >>> Quantity.set_preferences(input_sf=None)
    >>> l = Quantity('1000m')
    >>> l.as_tuple()
    (1.0, '')

Alternatively, you can specify the units you wish to use whose leading character 
is a scale factor.  Once known, these units will no longer confuse *QuantiPhy*.  
These units can be specified as a list or as a string. If specified as a string 
the string is split to form the list. Specifying the known units replaces any 
existing known units.

.. code-block:: python

    >>> d1 = Quantity('1 au')
    >>> d2 = Quantity('1000 pc')
    >>> print(d1.render(show_si=False), d2, sep='\n')
    1e-18 u
    1 nc

    >>> Quantity.set_preferences(known_units='au pc')
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


.. _formatting:

String Formatting
'''''''''''''''''

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

    >>> vacuum_permittivity = Quantity('eps0')
    >>> print('{:n}'.format(vacuum_permittivity))
    ε₀

    >>> print('{:d}'.format(vacuum_permittivity))
    permittivity of free space

Using the upper case versions of the format codes that print the numerical value 
of the quantity (SQRFEG) to indicate that the name and perhaps description 
should be included as well. They are under the control of the *label_fmt* 
preference.

.. code-block:: python

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

    >>> print('{0:n} = {0:q} ({0:d})'.format(vacuum_permittivity))
    ε₀ = 8.8542 pF/m (permittivity of free space)

    >>> print('{:S}'.format(vacuum_permittivity))
    ε₀ = 8.8542 pF/m -- permittivity of free space

You can also specify two values as a tuple to *label_fmt*, in which case the 
first is used if there is a description and the second used otherwise.

.. code-block:: python

    >>> Quantity.set_preferences(label_fmt=('{n} = {v} -- {d}', '{n} = {v}'))

    >>> print('{:S}'.format(trise))
    trise = 10 ns

    >>> print('{:S}'.format(vacuum_permittivity))
    ε₀ = 8.8542 pF/m -- permittivity of free space

Finally, you can add units after the format code, which causes the number to be 
scaled to those units if the transformation represents a known unit conversion.

.. code-block:: python

    >>> Tboil = Quantity('Boiling point = 100 °C')
    >>> print('{:S°F}'.format(Tboil))
    Boiling point = 212 °F

    >>> eff_channel_length = Quantity('leff = 14nm')
    >>> print('{:SÅ}'.format(eff_channel_length))
    leff = 140 Å

This feature can be used to simplify the conversion of the time and temperature 
information back into the original units:

.. code-block:: python

    >>> for time, temp in data:
    ...     print('{:<7smin} {:s°F}'.format(time, temp))
    0 min   450 °F
    10 min  400 °F
    20 min  360 °F

All of these features can be used with formatted strings, which are new to 
Python in version 3.6:

.. code-block:: python

    >>> for time, temp in data:
    ...     print(f'{time:<7smin} {temp:s°F}')
    0 min   450 °F
    10 min  400 °F
    20 min  360 °F


.. _extract:

Extract Quantities
''''''''''''''''''

It is possible to put a collection of quantities in a text string and then use 
the *extract* function to parse the quantities and return them in a dictionary.  
For example:

.. code-block:: python

    >>> design_parameters = '''
    ...     Fref = 156 MHz     -- Reference frequency
    ...     Kdet = 88.3 uA     -- Gain of phase detector (Imax)
    ...     Kvco = 9.07 GHz/V  -- Gain of VCO
    ... '''
    >>> globals().update(Quantity.extract(design_parameters))
    >>> Quantity.set_preferences(
    ...     label_fmt=('{V:<18}  # {d}', '{n} = {v}'),
    ...     show_label=True
    ... )

    >>> print(Fref, Kdet, Kvco, sep='\n')
    Fref = 156 MHz      # Reference frequency
    Kdet = 88.3 uA      # Gain of phase detector (Imax)
    Kvco = 9.07 GHz/V   # Gain of VCO

Any number of quantities may be given, with each quantity given on its own line.  
The identifier given to the left '=' is the name of the variable in the local 
namespace that is used to hold the quantity. The text after the '--' is used as 
a description of the quantity.

In this example the output of *extract()* is added into the local names space.  
This is an example of how simulation scripts could be written. The system and 
simulation parameters would be gathered together at the top into a multiline 
string, which would then be read and loaded into the local name space. It allows 
you to quickly give a complete description to a collection of parameters when 
the goal is to put something together quickly in an expressive manner.

Here is an example that uses this feature to read parameters from a file. This 
is basically the same idea as above, except the design parameters are kept in 
a separate file.  It also subclasses Quantity to create a version that displays 
the name and description by default.

.. code-block:: python

    >>> from quantiphy import Quantity
    >>> from inform import os_error, fatal, display

    >>> class VerboseQuantity(Quantity):
    ...    show_label = True
    ...    label_fmt = ('{V:<18} -- {d}', '{n} = {v}')

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


.. _equivalence:

Equivalence
'''''''''''

You can determine whether the value of a quantity or real number is equivalent 
to that of a quantity. The two values need not be identical, they just need to 
be close to be deemed equivalent. The *reltol* and *abstol* preferences are used 
to determine if they are close.

.. code-block:: python

   >>> h_line.is_close(h_line)
   True

   >>> h_line.is_close(h_line + 1)
   True

   >>> h_line.is_close(h_line + 1e4)
   False

By default, *is_close()* looks at the both the value and the units if the 
argument has units. In this way if you compare two quantities with different 
units, the *is_close* test will always fail if their units differ.

.. code-block:: python

   >>> Quantity('10ns').is_close(Quantity('10nm'))
   False


.. _exceptional values:

Exceptional Values
''''''''''''''''''

You can test whether the value of the quantity is infinite or is not-a-number.

.. code-block:: python

   >>> h_line.is_infinite()
   False

   >>> h_line.is_nan()
   False


.. _exceptions:

Exceptions
''''''''''

A *ValueError* is raised if *Quantity* is passed a string it cannot convert into 
a number:

.. code-block:: python

   >>> try:
   ...     q = Quantity('g')
   ... except ValueError as err:
   ...     print(err)
   g: not a valid number.

A KeyError is raised if a unit conversion is requested but no suitable unit
converter is available.

.. code-block:: python

   >>> q = Quantity('93 Mmi', scale='pc')
   Traceback (most recent call last):
   ...
   KeyError: ('pc', 'mi')

A NameError is raised if a constant is created without a name or if you try to 
set or get a preference that is not supported.

.. code-block:: python

   >>> q = Constant(Quantity('1ns'))
   Traceback (most recent call last):
   ...
   NameError: no name specified.


**Navigation**:

    * :ref:`Back to start of Overview <overview>`
    * :ref:`Reference Manual <reference manual>`
    * :ref:`Examples <examples>`
