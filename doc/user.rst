.. _users guide:

Users' Guide
============

.. _quantiphy overview:

Overview
--------

*QuantiPhy* adds support for quantities to Python. Quantities are little more 
than a number combined with its units. They are used to represent physical 
quantities. Your height and weight are both quantities, having both a value and 
units, and both are important. For example, if I told you that Mariam's weight 
was 8, you might assume pounds as the unit of measure if you lived in the US and 
think Mariam was an infant, or you might assume stones as the units if you live 
in the UK and assume that she was an adult, or you might assume kilograms if you 
lived anywhere else and assume she was a small child.
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
which for those that are familiar with them are much easier to read and write 
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

Now *distance_to_sun* contains an object with two values, the number 
150000000000.0 and the units 'm'.  The 'G' was interpreted as the *giga* scale 
factor, which scales 150 by 10\ :sup:`9`.

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


Specifying Quantities
.....................

Normally, creating a :class:`quantiphy.Quantity` takes one or two arguments.  
The first is taken to be the value, and the second, if given, is taken to be the 
model, which is a source of default values.


The First Argument: The Value
"""""""""""""""""""""""""""""

The value may be given as a float, as a string, or as a quantity.  The string 
may be the name of a known constant or it may represent a number. If the string 
represents a number, it may be in floating point notation (1200.0), in 
E-notation (ex: 1.2e+3), or use SI scale factors (1.2k). It may also include the 
units.  And like Python in general, the numbers may include underscores to make 
them easier to read (they are ignored).  For example, any of the following ways 
can be used to specify 1ns:

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

The following constants are pre-defined: *h*, *ħ*, *k*, *q*, *c*, *0°C*, *ε₀*, 
*μ₀*, and *Z₀*. You may add your own :ref:`constants <constants>`.

Currency units ($€¥£₩₺₽₹ɃΞ) are a bit different than other units in that they 
are placed at the front of the quantity.

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

In addition, the units must start with a letter or any of these characters: 
``%√°ÅΩƱ``, and may be followed by those characters or digits or any of these 
characters: ``-^/()·⁻⁰¹²³⁴⁵⁶⁷⁸⁹``.  Thus, any of the following would be accepted 
as units: ``Ohms``, ``V/A``, ``J-s``, ``m/s^2``, ``H/(m-s)``, ``Ω``, ``%``, 
``m·s⁻²``, ``V/√Hz``.

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


The Second Argument: The Model
""""""""""""""""""""""""""""""

If you only specify a real number for the value, then the units, name, and 
description do not get values. Even if given as a string or quantity, the value 
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

If the model contains units, those units are only used if the value does not 
have units. The same is true for the description. For example:

    >>> h = Quantity('18in', 'm')
    >>> print(h)
    18 in


The Remaining Arguments
"""""""""""""""""""""""

Any arguments beyond the first two should be given as named arguments (though 
not a requirement at the moment, it eventually will be).

If you need to override the name, units or the description given in either the 
value or the model, you can do so by specifying them with corresponding named 
arguments.  For example:

.. code-block:: python

    >>> out_period = Quantity(
    ...     10*period, period, name='output period',
    ...     desc='period at output of frequency divider'
    ... )
    >>> print(f'{out_period.name} = {out_period} -- {out_period.desc}')
    output period = 100 ns -- period at output of frequency divider

In this the value is ``10*period``, which is a float and so has no name, units, 
or description attributes, but the model is ``period`` that has all three 
attributes, but the name name and description, coming from a quantity, are 
ignored. As such, they specified explicitly using the *name* and *desc* named 
arguments.

Specifying *binary* as *True* allows you to use the binary scale factors. The 
binary scale factors are *Ki*, *Mi*, *Gi*, *Ti*, *Pi*, *Ei*, *Zi*, and *Yi*.  
Unlike the normal scale factors, you cannot use a lower case *k* in *Ki*. Also, 
*input_sf* is ignored. The normal recognizers are used if none of the binary 
scale factors are found.

    >>> bytes = Quantity('1 KiB', binary=True)
    >>> print(bytes)
    1.024 kB

Finally, you can also specify *scale* and *ignore_sf* as named arguments.  
*scale* allows you to scale the value or convert it to different units. It is 
described :ref:`in a bit <scaling upon creation>`. *ignore_sf* indicates that 
any scale factors should be ignored. This is one way of handling units whose 
name starts with a scale factor character. For example:

    >>> x = Quantity('1m')                                  # unitless value
    >>> print(x, x.real, x.units, sep=', ')
    1m, 0.001, 

    >>> l = Quantity('1m', ignore_sf=True)                  # length in meters
    >>> print(l, l.real, l.units, sep=', ')
    1 m, 1.0, m

    >>> d = Quantity('1m', units = 'mile', ignore_sf=True)  # distance in miles
    >>> print(d, d.real, d.units, sep=', ')
    1 mile, 1.0, mile

    >>> t = Quantity('1m', units = 'min', ignore_sf=True)   # duration in minutes
    >>> print(t, t.real, t.units, sep=', ')
    1 min, 1.0, min


Quantity Attributes
"""""""""""""""""""

Finally, you can overwrite :class:`quantiphy.Quantity` attributes to override 
the units, name, or description.

.. code-block:: python

    >>> out_period = Quantity(10*period)
    >>> out_period.units = 's'
    >>> out_period.name = 'output period'
    >>> out_period.desc = 'period at output of frequency divider'
    >>> print(f'{out_period.name} = {out_period} -- {out_period.desc}')
    output period = 100 ns -- period at output of frequency divider

In addition, you can also override the preferences with attributes:

    >>> out_period.spacer = ''
    >>> print(out_period)
    100ns


.. _subclassing Quantity:

Subclassing Quantity
""""""""""""""""""""

You can subclass :class:`quantiphy.Quantity` to make it easier to create 
a particular particular type of quantity, or to create quantities with 
particular qualities.  The following example demonstrates both. It creates 
a subclass for dollars that both sets the units and display preferences.  
Display preferences for currencies are often very different from what you would 
want from physical quantities:

.. code-block:: python

    >>> class Dollars(Quantity):
    ...     units = '$'
    ...     form = 'fixed'
    ...     prec = 2
    ...     strip_zeros = False
    ...     show_commas = True

    >>> cost = Dollars(100_000)
    >>> print(cost)
    $100,000.00

This example creates a special class for bytes.

.. code-block:: python

    >>> class Bytes(Quantity):
    ...     units = 'B'
    ...     form = 'binary'
    ...     accept_binary = True

    >>> memory = Bytes('64KiB')
    >>> print(memory)
    64 KiB

Lastly, this example creates a special class for temperatures. It disallows use 
of 'K' as a scale factor to avoid confusion with Kelvin units.

    >>> class Temperature(Quantity):
    ...     units = 'K'
    ...     input_sf = Quantity.get_pref('input_sf').replace('K', '')

    >>> Tcore = Temperature('15M')
    >>> Tphoto = Temperature('5.3k')
    >>> Tcmb = Temperature('3.18')
    >>> print(Tcore, Tphoto, Tcmb, sep='\n')
    15 MK
    5.3 kK
    3.18 K


.. _scaling upon creation:

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
units (K) and chooses the appropriate converter.  No scaling is done if the 
given units are the same as the desired units. Thus you can use the scaling 
mechanism to convert a collection of data with mixed units to values with 
consistent units.  For example:

.. code-block:: python

    >>> weights = '''
    ...     240 lbs
    ...     230 lb
    ...     100 kg
    ...     210
    ... '''.strip().split('\n')
    >>> for weight in weights:
    ...     w = Quantity(weight, 'lb', scale='lb')
    ...     print(w)
    240 lb
    230 lb
    220.46 lb
    210 lb

QuantiPhy* provides a collection of pre-defined converters for common units:

====== ================================================================
K:     K, F °F, R °R
C, °C: K, C °C, F °F, R °R
m:     km, m, cm, mm, um μm micron, nm, Å angstrom, mi mile miles,
       in inch inches
g:     oz, lb lbs
s:     sec second seconds, min minute minutes, hour hours hr, day days
b:     B
====== ================================================================

The conversions can occur between a pair of units, one from the first column and 
one from the second. They do not occur when both units are only in the second 
column. So for example, it is possible to convert between *g* and *lbs*, but not 
between *oz* and *lb*.  However, if you notice, the units in the second column 
are grouped using commas.  A set of units within commas are considered 
equivalent, meaning that there are multiple names for the same underlying unit.  
For example, *in*, *inch*, and *inches* are all considered equivalent. You can 
convert between equivalent units even though both are found in the second 
column. This feature was used in the above example where *lbs* was converted to 
*lb*.

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

:class:`quantiphy.UnitConversion` supports linear conversions (slope only), 
affine conversions (slope and intercept) and nonlinear conversions.

Notice that the return value of *UnitConversion* was not used. It is enough to 
simply create the *UnitConversion* for it to be available to *Quantity*. So, it 
is normal to not capture the return value of *UnitConversion*. However, there 
are two things you can do with the return value. First you can convert it to 
a string to get a description of the relationship. This is largely used as 
a sanity check:

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
    ...     print(f'{time:9q} {temp:9q}')
          0 s  505.37 K
        600 s  477.59 K
       1.2 ks  455.37 K


Creating a Quantity by Scaling an Existing Quantity
...................................................

The :meth:`quantiphy.Quantity.scale` method scales the value of a quantity and 
then uses the new value to create a new Quantity. For example:

.. code-block:: python

    >>> import math

    >>> h_line = Quantity('1420.405751786 MHz')
    >>> sagan = h_line.scale(math.pi)
    >>> sagan2 = sagan.scale(2)
    >>> print(sagan, sagan2, sep='\n')
    4.4623 GHz
    8.9247 GHz

    >>> type(h_line)
    <class 'quantiphy.Quantity'>

    >>> type(sagan)
    <class 'quantiphy.Quantity'>

Any value that can be passed to the *scale* argument for 
:class:`quantiphy.Quantity` or :meth:`quantiphy.Quantity.render` can be passed 
to the *scale* method. Specifically, the following types are accepted:

float or Quantity:
    The argument scales the underlying value (a new quantity is returned whose 
    value equals the underlying quantity multiplied by scale). In this case the 
    scale is assumed unitless (any units are ignored) and so the units of the 
    new quantity are the same as those of the underlying quantity.

tuple:
    The argument consists of two values. Tthe first value, a float, is treated 
    as a scale factor. The the second value, a string, is taken to be the units 
    of the new quantity.

function:
    The function takes two arguments, the value and the units of the quantity 
    and it returns two values, the value and units of the new value.

string:
    The argument is taken to the be desired units. This value along with the 
    units of the underlying quantity are used to select a known unit conversion, 
    which is applied to create the new value.

    .. code-block:: python

        >>> Tboil_C = Tboil.scale('C')
        >>> print(Tboil_C)
        100 C


Creating a Quantity by Adding to an Existing Quantity
.....................................................

The :meth:`quantiphy.Quantity.add` method adds a contribution to the  value of 
a quantity and then uses the sum to create a new Quantity. For example:

.. code-block:: python

    >>> import math

    >>> total = Quantity(0, '$')
    >>> for contribution in [1.23, 4.56, 7.89]:
    ...     total = total.add(contribution)
    >>> print(total)
    $13.68

When adding quantities, the units of the quantity should match. You can enforce 
this by adding *check_units=True*. If the dimension of your quantities match but 
not the units, you can often use :meth:`quantiphy.Quantity.scale` to get the 
units right:

.. code-block:: python

    >>> m1 = Quantity('1kg')
    >>> m2 = Quantity('1lb')
    >>> m3 = m1.add(m2.scale('g'), check_units=True)
    >>> print(m3)
    1.4536 kg


Accessing Quantity Values
.........................

There are a variety of ways of accessing the value of a quantity. If you are 
just interested in its numeric value, you access it with:

.. code-block:: python

    >>> h_line.real
    1420405751.786

    >>> float(h_line)
    1420405751.786

Or you can simply use a quantity in the same way that you would use any real 
number, meaning that you can use it in expressions and it evaluates to its 
numeric value:

.. code-block:: python

    >>> second_sagan_freq = 2 * math.pi * h_line
    >>> print(second_sagan_freq)
    8924672549.85517

    >>> sagan2 = Quantity(second_sagan_freq, h_line)
    >>> print(sagan2)
    8.9247 GHz

    >>> type(h_line)
    <class 'quantiphy.Quantity'>

    >>> type(second_sagan_freq)
    <class 'float'>

    >>> type(sagan2)
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

The :meth:`quantiphy.Quantity.render` method allows you to control the process 
of converting a quantity to a string. For example:

.. code-block:: python

    >>> h_line.render()
    '1.4204 GHz'

    >>> h_line.render(form='eng')
    '1.4204e9 Hz'

    >>> h_line.render(show_units=False)
    '1.4204G'

    >>> h_line.render(form='eng', show_units=False)
    '1.4204e9'

    >>> h_line.render(prec=6)
    '1.420406 GHz'

    >>> h_line.render(form='fixed', prec=2)
    '1420405751.79 Hz'

    >>> bytes.render(form='binary')
    '1 KiB'

    >>> k.render(negligible=1e-12)
    '0 J/K'


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

    >>> h_line.render(form='eng', prec='full')
    '1.420405751786e9 Hz'

Full precision implies whatever precision was used when specifying the quantity 
if it was specified as a string and if the *keep_components* preference is True.  
Otherwise a fixed number of digits, specified in the *full_prec* preference, is 
used (default=12).  Generally one uses 'full' when generating output that is 
intended to be read by a machine without loss of precision.

An alternative to *render* is :meth:`quantiphy.Quantity.fixed`. It converts the 
quantity to a string in fixed-point format:

.. code-block:: python

    >>> total = Quantity('$11.2M')
    >>> print(total.fixed(prec=2, show_commas=True, strip_zeros=False))
    $11,200,000.00

You can also use :meth:`quantiphy.Quantity.render` to produce a fixed format, 
but it does not support all of the options available with *fixed*:

.. code-block:: python

    >>> print(total.render(form='fixed', prec=2))
    $11200000

Another alternative to *render* is :meth:`quantiphy.Quantity.binary`. It 
converts the quantity to a string that uses binary scale factors:

.. code-block:: python

    >>> mem = Quantity(17_179_869_184, 'B', name='physical memory')
    >>> print(mem.binary())
    16 GiB

Alternatively you can also use *render* to render strings with binary prefixes:

.. code-block:: python

    >>> print(mem.render(form='binary'))
    16 GiB


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

    >>> print(m.render(scale=(0.0022046, 'lb'), form='fixed'))
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

You can also specify the width and alignment.  *Quantiphy* follows the Python 
convention of right justifying numbers by default.

.. code-block:: python

    >>> print('|{:16.6}|'.format(h_line))
    |    1.420406 GHz|

    >>> print('|{:<16.6}|'.format(h_line))
    |1.420406 GHz    |

    >>> print('|{:>16.6}|'.format(h_line))
    |    1.420406 GHz|

    >>> print('|{:^16.6}|'.format(h_line))
    |  1.420406 GHz  |

The general form of the format specifiers supported by quantities is::

   format_spec ::=  [align][#][width][,][.precision][type][scale]

*align* specifies the alignment using one of the following characters:

   ===== =======================================================================
   Align Meaning
   ===== =======================================================================
   >     Right justification.
   <     Left justification.
   ^     Center justification.
   ===== =======================================================================

The hash (#) is a literal hash that when present indicates that trailing zeros 
and radix should not be stripped from the fractional part of the number.

*width* is a literal integer that specifies the minimum width of the string.

The comma (,) is a literal comma that when present indicates that commas should 
be added to the whole part of the mantissa, every three digits.

*precision* is a literal integer that specifies the precision.

And finally, *type* specifies which form should be used when formatting the 
value. The choices include:

   ==== ========================================================================
   Type Meaning
   ==== ========================================================================
        Use default formatting options.
   s    Use default formatting options.
   q    Format using SI scale factors and show the units.
   r    Format using SI scale factors but do not show the units.
   p    Format using fixed-point notation and show the units.
   e    Format using exponent notation but do not show the units.
   f    Format using fixed-point notation but do not show the units.
   b    Format using binary prefixes while showing the units.
   g    Format using fixed-point or exponential notation, whichever is shorter, 
        but do not show the units.
   u    Only include the units.
   n    Only include the name.
   d    Only include the description.
   ==== ========================================================================

You can capitalize any of the format characters that output the value of the 
quantity (any of 'sqrpefg', but not 'und'). If you do, the label will also be 
included.

These format specifiers are generally included in format strings. However, in 
addition, *Quantitphy* provides the :meth:`quantiphy.Quantity.format` method 
that converts a quantity to a string based on a naked format string. For 
example:

.. code-block:: python

    >>> print(h_line.format('.6q'))
    1.420406 GHz

Here is an example of these format types:

.. code-block:: python

    >>> h_line = Quantity('f = 1420.405751786 MHz -- hydrogen line')
    >>> for f in 'sSpPqQrRbBeEfFgGund':
    ...     print(f + ':', h_line.format(f))
    s: 1.4204 GHz
    S: f = 1.4204 GHz -- hydrogen line
    p: 1420405751.786 Hz
    P: f = 1420405751.786 Hz -- hydrogen line
    q: 1.4204 GHz
    Q: f = 1.4204 GHz -- hydrogen line
    r: 1.4204G
    R: f = 1.4204G -- hydrogen line
    b: 1.3229 GiHz
    B: f = 1.3229 GiHz -- hydrogen line
    e: 1.4204e+09
    E: f = 1.4204e+09 -- hydrogen line
    f: 1420405751.786
    F: f = 1420405751.786 -- hydrogen line
    g: 1.4204e+09
    G: f = 1.4204e+09 -- hydrogen line
    u: Hz
    n: f
    d: hydrogen line

The 'q' type specifier is used to explicitly indicate that both the number and 
the units are desired and that SI scale factors should be used, regardless of 
the current preferences.

.. code-block:: python

    >>> print('{:.6q}'.format(h_line))
    1.420406 GHz

Alternately, 'r' can be used to indicate just the number represented using SI 
scale factors is desired, and the units should not be included.

.. code-block:: python

    >>> print('{:r}'.format(h_line))
    1.4204G

The opposite can be achieve using 'p', which includes the units but not use SI 
scale factors:

.. code-block:: python

    >>> print('{:p}'.format(h_line))
    1420405751.786 Hz

The 'p' format is often used with '#' to format currency values:

.. code-block:: python

    >>> print('{:#.2p}'.format(total))
    $11200000.00

    >>> print('{:#,.2p}'.format(total))
    $11,200,000.00

The 'b' format is used to render number with binary scale factors:

.. code-block:: python

    >>> print('{:b}'.format(mem))
    16 GiB

    >>> print('{:B}'.format(mem))
    physical memory = 16 GiB

You can also use the traditional floating point format type specifiers:

.. code-block:: python

    >>> print('{:f}'.format(h_line))
    1420405751.786

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
*label_fmt* is used to add the labeling.

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
    trise = 0

    >>> print('{:E}'.format(trise))
    trise = 1e-08

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
In this case the format code must be specified (use 's' rather than '').

.. code-block:: python

    >>> Tboil = Quantity('Boiling point = 100 °C')
    >>> print('{:S°F}'.format(Tboil))
    Boiling point = 212 °F

    >>> eff_channel_length = Quantity('leff = 14nm')
    >>> print(f'{eff_channel_length:SÅ}')
    leff = 140 Å

    >>> print(f'{mem:bb}')
    128 Gib

This feature can be used to simplify the conversion of the time and temperature 
information back into the original units:

.. code-block:: python

    >>> for time, temp in data:
    ...     print(f'{time:<7smin} {temp:s°F}')
    0 min   450 °F
    10 min  400 °F
    20 min  360 °F

Any format specification that is not recognized by *QuantiPhy* is simply passed 
on to the underlying float. For example:

.. code-block:: python

    >>> total = Quantity(1976794.98, '$')
    >>> print(f'TOTAL: {total:#,.2f}')
    TOTAL: 1,976,794.98


.. index::
   single: constants
   single: physical constants
   single: h (Plank's constant)
   single: ħ (Plank's constant)
   single: k (Boltzmann's constant)
   single: q (elementary charge)
   single: c (speed of light)
   single: 0C (0 Celsius)
   single: eps0 (permittivity of free space)
   single: ε₀ (permittivity of free space)
   single: mu0 (permeability of free space)
   single: μ₀ (permeability of free space)
   single: Z0 (characteristic impedance of free space)

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
    >>> add_constant(Quantity("λₕ: 211.061140539mm // wavelength of hydrogen line"))

    >>> hy_wavelength = Quantity('λₕ')
    >>> print(hy_wavelength.render(show_label=True))
    λₕ = 211.06 mm -- wavelength of hydrogen line

In this case is the name given in the quantity is used when creating the 
constant.  You can also specify an alias as an argument to *add_constant*.

.. code-block:: python

    >>> add_constant(
    ...     Quantity("λₕ = 211.061140539mm # wavelength of hydrogen line"),
    ...     alias='lambda h'
    ... )

    >>> hy_wavelength = Quantity('lambda h')
    >>> print(hy_wavelength.render(show_label=True))
    λₕ = 211.06 mm -- wavelength of hydrogen line

It is not necessary to specify both the name and the alias, one is sufficient; 
the constant is accessible using either.  Notice that the alias does not 
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


.. index::
   single: preferences

.. _preferences:

Preferences
-----------

*QuantiPhy* supports a wide variety of preferences that control its behavior.  
For example, when rendering quantities you can control the number of digits used 
(*prec*), whether SI scale factors are used (*form*), whether the units are 
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
    ...     units = 'C'
    >>> Temperature.set_prefs(prec=1, known_units='K', spacer='')

    >>> class Frequency(Quantity):
    ...     units = 'Hz'
    >>> Frequency.set_prefs(prec=5, spacer='')

    >>> frequencies = []
    >>> for each in '-25.3 999987.7, 25.1  1000207.1, 74.9  1001782.3'.split(','):
    ...     temp, freq = each.split()
    ...     frequencies.append((Temperature(temp),  Frequency(freq)))

    >>> for temp, freq in frequencies:
    ...     print(f'{temp:4}  {freq}')
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
    λₕ = 211.06 mm -- wavelength of hydrogen line

This is often the way to go with quantities that have :index:`logarithmic units`
such as decibels (:index:`dB`) or shannons (Sh) (or the related bit, digits, 
nats, hartleys, etc.). In these cases use of SI scale factors is often 
undesired.

.. code-block:: python

    >>> gain = Quantity(0.25, 'dB')
    >>> print(gain)
    250 mdB

    >>> gain.form = 'fixed'
    >>> print(gain)
    0.25 dB

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

    >>> with Quantity.prefs(form='fixed', show_units=False, prec=2):
    ...     for time, temp in data:
    ...         print('%-7s %s' % (time, temp))
    0       505.37
    600     477.59
    1200    455.37

    >>> print('Final temperature = %s @ %s.' % data[-1][::-1])
    Final temperature = 455.37 K @ 1.2 ks.

Notice that the specified preferences only affected the table, not the final 
printed values, which were rendered outside the *with* statement.


.. index::
   single: localization

.. _localization:

Localization
------------

*Quantiphy* provides 4 preferences that help with localization: *radix*, 
*comma*, *plus*, and *minus*.

*radix*:
    The decimal point; generally ``.`` or ``,``.

*comma*:
    The thousands separator; generally ``,``, ``.``, or the empty string.

*plus*:
    The sign that indicates a positive number; generally ``+`` or ``＋``.
    This only affect the plus sign used on exponents, a plus sign is never added 
    to the front of a number.

*minus*:
    The sign that indicates a negative number; generally ``-`` or ``−``.

By default *QuantiPhy* uses ``.``, ``,``, ``+``, and ``-`` as the defaults.  
These are all simple ASCII characters.  They work as expected for the numbers 
normally used in programming, such as ``-5.17e+06``.

Both *radix* and *comma* affect the way stings are converted to quantities and 
they way quantities are rendered, whereas *plus* and *minus* only affect the way 
quantities are rendered.  When interpreting a string as a number, *QuantiPhy* 
first strips the *comma* character from the string and then replaces the *radix* 
character with ``.``.

If you prefer to use ``,`` for your radix, you generally have two choices. With 
the first, *radix* is set to ``,`` and *comma* to ``.``. This allows you to 
properly read and write numbers like €100.000.000,00 but misinterpretes a number 
if it uses ``.`` as the radix.

.. code-block:: python

    >>> Quantity.set_prefs(radix=',', comma='.')
    >>> q1 = Quantity('€100.000,00')
    >>> q2 = Quantity('€100000.00')
    >>> print(q1, q2, sep='\n')
    €100k
    €10M

With the second, *radix* is set to ``,`` and *comma* to ''. This allows both 
``,`` and ``.`` to be used as the radix, so €100,000 and €100.000 have the same 
value.  However, it fails for numbers that use ``.`` as the thousands separator.

.. code-block:: python

    >>> Quantity.set_prefs(radix=',', comma='')
    >>> q1 = Quantity('€100,000')
    >>> q2 = Quantity('€100.000')
    >>> print(q1, q2, sep='\n')
    €100
    €100

You can automatically adapt to local conventions using the Python *locale* 
package:

.. code-block:: python

    >>> from quantiphy import Quantity
    >>> import locale

    >>> loc_conv = locale.localeconv()
    >>> radix = loc_conv['decimal_point']
    >>> comma = loc_conv['thousands_sep']
    >>> Quantity.set_prefs(radix=radix, comma=comma)

    >>> q = Quantity('€100.000')
    >>> print(q)
    €100

    >>> print(f"radix is '{radix}'\ncomma is '{comma}'")
    radix is '.'
    comma is ''

You can convert from one convention to the other by changing *radix* and *comma* 
on the fly:

    >>> with Quantity.prefs(radix=',', comma='.'):
    ...     q = Quantity('€100.000.000,00')
    >>> with Quantity.prefs(radix='.', comma=','):
    ...     print(f'{q:#,.2p}')
    €100,000,000.00


.. index::
   single: Kelvin/kilo ambiguity

.. _ambiguity:

Ambiguity of Scale Factors and Units
------------------------------------

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
    >>> print(d1.render(form='eng'), d2, sep='\n')
    1e-18 u
    1 nc

    >>> Quantity.set_prefs(known_units='au pc')
    >>> d1 = Quantity('1 au')
    >>> d2 = Quantity('1000 pc')
    >>> print(d1.render(form='eng'), d2, sep='\n')
    1 au
    1 kpc

This same issue comes up for temperature quantities when given in Kelvin. There 
are again several ways to handle this. First you can specify the acceptable 
input scale factors leaving out 'K', ex. *input_sf* = 'TGMkmunpfa', or:

..  code-block:: python

    >>> Quantity.set_prefs(input_sf = Quantity.get_pref('input_sf').replace('K', ''))
    >>> temp = Quantity('100K')
    >>> print(temp.as_tuple())
    (100.0, 'K')

    >>> temp = Quantity('100k')
    >>> print(temp.as_tuple())
    (100000.0, '')

    >>> temp = Quantity('100k', 'K')
    >>> print(temp.as_tuple())
    (100000.0, 'K')

Alternatively, you can specify 'K' as one of the known units. Finally, if you 
know exactly when you will be converting a temperature to a quantity, you can 
specify *ignore_sf* for that specific conversion. The effect is the same either 
way, 'K' is interpreted as a unit rather than a scale factor.


.. index::
   single: tabular data

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

    >>> with Quantity.prefs(number_fmt='{whole:>3}{frac:<4} {units}'):
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
    ...     return '{mantissa:<5} {units}'.format(mantissa=whole+frac, units=units)

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
    ...     return '{:>5} {:<5}'.format(whole+frac, units)

    >>> class Temperature(Quantity):
    ...     units = 'C'
    >>> Temperature.set_prefs(
    ...     prec = 1, known_units = 'K', number_fmt = format_temperature
    ... )

    >>> class Frequency(Quantity):
    ...     units = 'Hz'
    >>> Frequency.set_prefs(prec=5, number_fmt = '{whole:>3}{frac:<6} {units}')

    >>> frequencies = []
    >>> for each in '-25.3 999987.7, 25.1 1000207.1, 74.9 1001782.3'.split(','):
    ...     temp, freq = each.split()
    ...     frequencies.append((Temperature(temp),  Frequency(freq)))

    >>> for temp, freq in frequencies:
    ...     print(temp, freq)
      -25 C     999.988   kHz
       25 C       1.00021 MHz
       75 C       1.00178 MHz


.. index::
   single: extracting quantities from text

.. _extract function:

Extract Quantities
------------------

It is possible to put a collection of quantities in a text string and then use 
the :meth:`quantiphy.Quantity.extract()` method to parse the quantities and 
return them in a dictionary.  For example:

.. code-block:: python

    >>> design_parameters = '''
    ...     Fref (fₒ) = 156 MHz  -- Reference frequency
    ...     Kdet = 88.3 uA       -- Gain of phase detector
    ...     Kvco = 9.07 GHz/V    -- Gain of VCO
    ... '''
    >>> quantities = Quantity.extract(design_parameters)

    >>> Quantity.set_prefs(
    ...     label_fmt = '{n} = {v}',
    ...     label_fmt_full = '{V:<18}  # {d}',
    ...     show_label = 'f',
    ... )
    >>> for k, q in quantities.items():
    ...     print(f'{k}: {q}')
    Fref: fₒ = 156 MHz        # Reference frequency
    Kdet: Kdet = 88.3 uA      # Gain of phase detector
    Kvco: Kvco = 9.07 GHz/V   # Gain of VCO

The string is processed one line at a time and may contain any number of 
quantity definitions.  Blank lines are ignored.  Each non-blank line is passed 
through *assign_rec* to determine if it is recognized as an assignment.  If it 
is recognized, the *assign_rec* named fields (*name*, *qname*, *val*, and 
*desc*) are used when creating the quantity.  The default recognizer allows you 
to separate the name from the value with either '=' or ':'. It allows you to 
separate the value from the description using '--', '//', or '#'. These 
substrings are also used to introduce comments, so you could start a line with 
'#' and it would be treated as a comment.
If the line is not recognized, then it is ignored.

In this example, the first line is nonconforming and so is ignored. The second 
*Kvdo* line is a comment, the comment character and anything beyond is ignored.  
Finally, empty lines are ignored.

.. code-block:: python

    >>> design_parameters = '''
    ...     PLL Design Parameters
    ...
    ...     Fref = 156 MHz      -- Reference frequency
    ...     Kdet = 88.3 uA      -- Gain of phase detector
    ...     Kvco = 9.07 GHz/V   -- Gain of VCO
    ...     -- Kvco = 5 GHz/V     -- Gain of VCO
    ...     N = 128             -- Divide ratio
    ...     Fout = N*Fref "Hz"  -- Output Frequency
    ... '''
    >>> globals().update(Quantity.extract(design_parameters))

    >>> print(f'{Fref:S}\n{Kdet:S}\n{Kvco:S}\n{N:S}\n{Fout:}')
    Fref = 156 MHz      # Reference frequency
    Kdet = 88.3 uA      # Gain of phase detector
    Kvco = 9.07 GHz/V   # Gain of VCO
    N = 128             # Divide ratio
    Fout = 19.968 GHz   # Output Frequency

In this case the output of the :meth:`quantiphy.Quantity.extract()` call is fed 
into globals().update() so as to add the quantities into the module namespace, 
making the quantities accessible as local variables.  This is an example of how 
simulation scripts could be written. The system and simulation parameters would 
be gathered together at the top into a multiline string, which would then be 
read and loaded into the local name space. It allows you to quickly give 
a complete description of a collection of parameters when the goal is to put 
something together quickly in an expressive manner.  Another example of this 
ideas is shown a bit further down where the module docstring is used to contain 
the quantity definitions.

Here is an example that uses this feature to read parameters from a file. This 
is basically the same idea as above, except the design parameters are kept in 
a separate file.  It also subclasses :class:`quantiphy.Quantity` to create 
a version that displays the name and description by default.

.. code-block:: python

    >>> from quantiphy import Quantity, InvalidNumber
    >>> from inform import os_error, fatal, display

    >>> class VerboseQuantity(Quantity):
    ...    show_label = 'f'
    ...    label_fmt = '{n} = {v}'
    ...    label_fmt_full = '{V:<18} -- {d}'

    >>> filename = 'parameters'
    >>> try:
    ...     with open(filename) as f:
    ...         globals().update(VerboseQuantity.extract(f.read()))
    ... except OSError as e:
    ...     fatal(os_error(e))
    ... except InvalidNumber as e:
    ...     fatal(e, culprit=filename)

    >>> display(Fref, Kdet, Kvco, N, Fout, sep='\n')
    Fref = 156 MHz     -- Reference frequency
    Kdet = 88.3 uA     -- Gain of phase detector (Imax)
    Kvco = 9.07 GHz/V  -- Gain of VCO
    N = 128            -- Divide ratio
    Fout = 19.968 GHz  -- Output Frequency

With :meth:`quantiphy.Quantity.extract()` the values of quantities can be given 
as a expression that contains previously defined quantities (or :ref:`physical 
constants <constants>` or select mathematical constants (pi, tau, π, or τ).  You 
can follow an expression with a string to give the units. Finally, you can use 
the *predefined* argument to pass in a dictionary of named values that can be 
used in your expressions.  For example:

.. code-block:: python

    #!/usr/bin/env python3
    >>> __doc__ = """
    ... Simulates a second-order ΔΣ modulator with the following parameter values:
    ...
    ...     Fclk = Fxtal/4 "Hz"                  -- clock frequency
    ...     Fin = 200kHz                         -- input frequency
    ...     Vin = 950mV                          -- input voltage amplitude (peak)
    ...     gain1 = 0.5V/V                       -- gain of first integrator
    ...     gain2 = 0.5V/V                       -- gain of second integrator
    ...     Vmax = 1V                            -- quantizer maximum input voltage
    ...     Vmin = -1V                           -- quantizer minimum input voltage
    ...     levels = 5                           -- quantizer output levels
    ...     Tstop = 2/Fin "s"                    -- simulation stop time
    ...     Tstart = -1/Fin 's'                  -- initial transient interval (discarded)
    ...     file_name = 'out.wave'               -- output filename
    ...     sim_name = f'{Fclk:q} ΔΣ Modulator'  -- simulation name
    ...
    ... The values given above are used in the simulation; no further
    ... modification of the code given below is required when changing
    ... these parameters.
    ... """

    >>> from quantiphy import Quantity

    >>> Fxtal = Quantity('200 MHz')
    >>> parameters = Quantity.extract(__doc__, predefined=dict(Fxtal=Fxtal))
    >>> globals().update(parameters)

    >>> with Quantity.prefs(
    ...     label_fmt = '{n} = {v}',
    ...     label_fmt_full = '{V:<18}  -- {d}',
    ...     show_label = 'f',
    ... ):
    ...     print('Simulation parameters:')
    ...     for k, v in parameters.items():
    ...         try:
    ...             print(f'    {v:Q}')
    ...         except ValueError:
    ...             print(f'    {k} = {v!s}')
    Simulation parameters:
        Fclk = 50 MHz       -- clock frequency
        Fin = 200 kHz       -- input frequency
        Vin = 950 mV        -- input voltage amplitude (peak)
        gain1 = 500 mV/V    -- gain of first integrator
        gain2 = 500 mV/V    -- gain of second integrator
        Vmax = 1 V          -- quantizer maximum input voltage
        Vmin = -1 V         -- quantizer minimum input voltage
        levels = 5          -- quantizer output levels
        Tstop = 10 us       -- simulation stop time
        Tstart = -5 us      -- initial transient interval (discarded)
        file_name = out.wave
        sim_name = 50 MHz ΔΣ Modulator

Notice in this case the parameters were specified and read out of the docstring 
at the top of the file. In this way, the parameters become very easy to set and 
the documentation is always up to date. Ignore the fact that the docstring is 
assigned to *__doc__*. That was a hack that was needed to make the example 
executable from within the documentation.


.. index::
   single: translating quantities in text

.. _translate:

Translating Quantities
----------------------

:meth:`quantiphy.Quantity.all_from_conv_fmt()` recognizes conventionally 
formatted numbers and quantities embedded in text and reformats them using 
:meth:`quantiphy.Quantity.render()`. This is an difficult task in general, and 
so some constraints are placed on the values to make them easier to distinguish.  
Specifically, the units, if given, must be simple and immediately adjacent to 
the number. Units are simple if they only consist of letters and underscores.  
The characters °, Å, Ω and Ʊ are also allowed.  So '47e3Ohms', '50_Ohms' and 
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
    >>> translated_back = Quantity.all_from_si_fmt(translated, form='eng')
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


.. index::
   single: equivalence

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

   >>> Quantity('$10').is_close(Quantity('10 USD'))
   False

   >>> Quantity('$10').is_close(Quantity('10 USD'), check_units=False)
   True


.. index::
   single: infinity
   single: not a number

.. _exceptional values:

Exceptional Values
------------------

*QuantiPhy* supports NaN (not a number) and infinite values:

   >>> inf = Quantity('inf Hz')
   >>> print(inf)
   inf Hz

   >>> nan = Quantity('NaN Hz')
   >>> print(nan)
   NaN Hz

You can test whether the value of the quantity is infinite or is not-a-number
using :meth:`quantiphy.Quantity.is_infinite()` or 
:meth:`quantiphy.Quantity.is_nan()`. These method return a rendered value for 
the number without units if they are true and None otherwise:

.. code-block:: python

   >>> h_line.is_infinite()

   >>> inf.is_infinite()
   'inf'

   >>> h_line.is_nan()

   >>> nan.is_nan()
   'NaN'

The rendered value is affected by the *inf* and *nan* preferences or attributes:

.. code-block:: python

   >>> inf.inf = '∞'
   >>> inf.is_infinite()
   '∞'


.. index::
   single: exceptions

.. _quantiphy exceptions:

Exceptions
----------

The way exceptions are defined in *QuantiPhy* has changed. Initially, the 
standard Python exceptions were used to indicate errors. For example, 
a *ValueError* was raised by :class:`quantiphy.Quantity` if it were passed 
a string it cannot convert into a number.  Now, a variety of *QuantiPhy* 
specific exceptions are used to indicate specific errors. However, these 
exceptions subclass the corresponding Python error for compatibility with 
existing code.  It is recommended that new code catch the *QuantiPhy* specific 
exceptions rather than the generic Python exceptions as their use may be 
deprecated in the future.

*QuantiPhy* employs the following exceptions:

:class:`quantiphy.ExpectedQuantity`:
    Subclass of :class:`quantiphy.QuantiPhyError` and *ValueError*.  Used by 
    :func:`quantiphy.add_constant()`.

    Raised when the value is either not an instance of 
    :class:`quantiphy.Quantity` or a string that can be converted to a quantity.

:class:`quantiphy.IncompatiblePreferences`:
    Subclass of :class:`quantiphy.QuantiPhyError` and *ValueError*.  Used by 
    :class:`quantiphy.Quantity` constructor.

    Raised when comma and radix preference is the same.

:class:`quantiphy.IncompatibleUnits`:
    Subclass of :class:`quantiphy.QuantiPhyError` and *TypeError*.  Used by 
    :meth:`quantiphy.Quantity.add()`.

    Raised when the units of contribution do not match those of underlying 
    quantity.

:class:`quantiphy.InvalidNumber`:
    Subclass of :class:`quantiphy.QuantiPhyError`, *ValueError*, and 
    *TypeError*.  Used by :class:`quantiphy.Quantity()`.

    Raised if the value given could not be converted to a number.

:class:`quantiphy.InvalidRecognizer`:
    Subclass of :class:`quantiphy.QuantiPhyError` and *KeyError*.  Used by 
    :class:`quantiphy.Quantity()`.

    The *assign_rec* preference is expected to be a regular expression that 
    defines one or more named fields, one of which must be *val*. This exception 
    is raised when the current value of *assign_rec* does not satisfy this 
    requirement.

:class:`quantiphy.MissingName`:
    Subclass of :class:`quantiphy.QuantiPhyError` and *NameError*.  Used by 
    :func:`quantiphy.add_constant()`.

    Raised when *alias* was not specified and no name was available from 
    *value*.

:class:`quantiphy.UnknownConversion`:
    Subclass of :class:`quantiphy.QuantiPhyError` and *KeyError*.

    Used by :meth:`quantiphy.UnitConversion.convert()`.

    Raised when the given units are not supported by the underlying class.

    Used by :class:`quantiphy.Quantity()`,
    :meth:`quantiphy.Quantity.scale()`,
    :meth:`quantiphy.Quantity.render()`,
    :meth:`quantiphy.Quantity.fixed()`, and
    :meth:`quantiphy.Quantity.format()`.

    Raised when a unit conversion was requested and there is no corresponding 
    unit converter.

:class:`quantiphy.UnknownFormatKey`:
    Subclass of :class:`quantiphy.QuantiPhyError` and *KeyError*.  Used by 
    :meth:`quantiphy.Quantity.render()`, :meth:`quantiphy.Quantity.fixed()`, and 
    :meth:`quantiphy.Quantity.format()`.

    The *label_fmt* and *label_fmt_full* are expected to be format strings that 
    may interpolate certain named arguments. The valid named arguments are *n* 
    for name, *v* for value, and *d* for description. This exception is raised 
    when some other name is used for an interpolated argument.

:class:`quantiphy.UnknownPreference`:
    Subclass of :class:`quantiphy.QuantiPhyError` and *KeyError*.  Used by 
    :meth:`quantiphy.Quantity.set_prefs()`, 
    :meth:`quantiphy.Quantity.get_pref()`, and 
    :meth:`quantiphy.Quantity.prefs()`.

    Raised when the name given for a preference is unknown.

:class:`quantiphy.UnknownScaleFactor`:
    Subclass of :class:`quantiphy.QuantiPhyError` and *ValueError*.  Used by 
    :class:`quantiphy.Quantity()`, :meth:`quantiphy.Quantity.set_prefs()`, or 
    :meth:`quantiphy.Quantity.prefs()`.

    The *input_sf* preference gives the list of scale factors that should be 
    accepted. This exception is raised if *input_sf* contains an unknown scale 
    factor.

:class:`quantiphy.UnknownUnitSystem`:
    Subclass of :class:`quantiphy.QuantiPhyError` and *KeyError*.  Used by 
    :func:`quantiphy.set_unit_system()`.

    Raised when the name given does not correspond to a known unit system.

*QuantiPhy* defines a common base exception, :class:`quantiphy.QuantiPhyError`, 
that all specific exceptions derive from.  This allows you to simplify your 
exception handling if you are not interested in distinguishing between the 
specific errors:

.. code-block:: python

    >>> from quantiphy import Quantity, QuantiPhyError

    >>> try:
    ...     q = Quantity('tweed')
    ... except QuantiPhyError as e:
    ...     print(str(e))
    tweed: not a valid number.

The alternative would be to catch each error individually:

.. code-block:: python

    >>> from quantiphy import (
    ...     Quantity, InvalidNumber, UnknownScaleFactor,
    ...     UnknownConversion, InvalidRecognizer
    ... )

    >>> try:
    ...     q = Quantity('tweed')
    ... except (InvalidNumber, UnknownScaleFactor, UnknownConversion, InvalidRecognizer) as e:
    ...     print(str(e))
    tweed: not a valid number.

*QuantiPhy* provides uniform access methods for its exceptions. You can access 
all the unnamed arguments passed to the exception using the *args* attribute, 
you can access the named arguments using *kwargs*, and you can create 
a customized message that incorporates the arguments using 
:meth:`quantiphy.QuantiPhyError.render()` method. The argument to *render* is 
a format string that can access both the unnamed and named arguments:

.. code-block:: python

    >>> try:
    ...     q = Quantity('tweed')
    ... except InvalidNumber as e:
    ...     print(e.render('{}: no es un número valido.'))
    ... except UnknownScaleFactor as e:
    ...     print(e.render('factor de escala desconocido.'))
    ... except UnknownConversion as e:
    ...     if 'direction' in e.kwargs:
    ...         direction = e.kwargs['direction']
    ...         if direction == 'to':
    ...             template = 'incapaz de convertir a {}'
    ...         else:  # direction must be 'from'
    ...             template = 'incapaz de convertir de {}'
    ...     else:
    ...         template = 'incapaz de convertir entre {} y {}'
    ...     print(e.render(template))
    ... except InvalidRecognizer as e:
    ...     print(e.render("el reconocedor no contiene la clave 'val'"))
    tweed: no es un número valido.
