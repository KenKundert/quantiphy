QuantiPhy - Physical Quantities
===============================

| Version: 0.4.0
| Released: 2016-10-26

.. image:: https://img.shields.io/travis/KenKundert/quantiphy/master.svg
    :target: https://travis-ci.org/KenKundert/quantiphy

.. image:: https://img.shields.io/coveralls/KenKundert/quantiphy.svg
    :target: https://coveralls.io/r/KenKundert/quantiphy

.. image:: https://img.shields.io/pypi/v/quantiphy.svg
    :target: https://pypi.python.org/pypi/quantiphy

.. image:: https://img.shields.io/pypi/pyversions/quantiphy.svg
    :target: https://pypi.python.org/pypi/quantiphy/

.. image:: https://img.shields.io/pypi/dd/quantiphy.svg
    :target: https://pypi.python.org/pypi/quantiphy/


Use 'pip install quantiphy' to install. Requires Python2.7 or Python3.3 or 
better.


Introduction
------------

*QuantiPhy* is a light-weight package that allows numbers to be combined with 
units into physical quantities.  Physical quantities are very commonly 
encountered when working with real-world systems when numbers are involved. And 
when encountered, the numbers often use SI scale factors to make them easier to 
read and write. For example, imagine trying to determine the rise time and 
bandwidth of a simple RC circuit:

.. code-block:: python

    >>> from quantiphy import Quantity
    >>> from math import pi

    >>> r = Quantity('1kOhm')
    >>> c = Quantity('1nF')
    >>> tau = Quantity(r*c, 's')
    >>> bw = Quantity(1/(2*pi*tau), 'Hz')
    >>> print('R = {}, C = {} → τ = {}, BW = {}.'.format(r, c, tau, bw))
    R = 1kOhm, C = 1nF → τ = 1us, BW = 159.15kHz.

A quantity is the pairing of a real number and units, though the units are 
optional. The Quantity class is used to combine the pair into a single object, 
and then provides methods to provide access to the pair in useful ways. In the 
above example quantities were created from strings that contained the value and 
unit (ex. '1nF') or from arguments where the value and units were specified 
explicitly (ex. r*c, 's'). Once created, the quantity objects can be treated 
like simple real values, but when printed, their values are presented using SI 
scale factors along with their units.


Quantities
----------

The *Quantity* class is used to create a quantity (an object with both a value 
and units). Normally, creating a quantity takes one or two arguments.  The first 
is taken to be the value, and the second, if given, is taken to be the model, 
which is a source of default values.  More on this in a bit, but for the time 
being you can assume the model is a string that contains the units for the 
quantity.  The value may be given as a float or as a string.  The string may be 
in floating point notation, in scientific notation, or use SI scale factors and 
may include the units.  For example, any of the following ways can be used to 
specify 1ns:

.. code-block:: python

    >>> period = Quantity(1e-9, 's')
    >>> print(period)
    1ns

    >>> period = Quantity('0.000000001 s')
    >>> print(period)
    1ns

    >>> period = Quantity('1e-9s')
    >>> print(period)
    1ns

    >>> period = Quantity('1ns')
    >>> print(period)
    1ns

So far our 1ns is just a value. However, you may also give a name and 
description.  For example:

.. code-block:: python

    >>> period = Quantity('Tclk = 10ns -- clock period')
    >>> print(period.name, '=', period, '#', period.desc)
    Tclk = 10ns # clock period

If you only specify a real number for the value, then the units, name, and 
description do not get values. This is where the second argument, the model, 
helps. It may be another quantity or it may be a string.  Any attributes that 
are not provided by the first argument are taken from the second if available.  
If the second argument is a string, it is split. If it contains one value, that 
value is taken to be the units, if it contains two, those values are taken to be 
the name and units, and it it contains more than two, the remaining values are 
taken to be the description. For example:

.. code-block:: python

    >>> out_period = Quantity(10*period, period)
    >>> print(out_period.name, '=', out_period, '#', out_period.desc)
    Tclk = 100ns # clock period

    >>> freq = Quantity(100e6, 'Hz')
    >>> print(freq)
    100MHz

    >>> freq = Quantity(100e6, 'Fin Hz')
    >>> print(freq.name, '=', freq, '#', freq.desc)
    Fin = 100MHz # 

    >>> freq = Quantity(100e6, 'Fin Hz Input frequency')
    >>> print(freq.name, '=', freq, '#', freq.desc)
    Fin = 100MHz # Input frequency

In addition, you can explicitly specify the units, the name, and the description 
using named arguments. These values override anything specified in the value or 
the model.

.. code-block:: python

    >>> out_period = Quantity(
    ...     10*period, period, name='output period',
    ...     desc='period at output of frequency divider'
    ... )
    >>> print(out_period.name, '=', out_period, '#', out_period.desc)
    output period = 100ns # period at output of frequency divider

Finally, you can overwrite the quantities attributes to override the units, 
name, or description.

.. code-block:: python

    >>> out_period = Quantity(10*period)
    >>> out_period.units = 's'
    >>> out_period.name = 'output period'
    >>> out_period.desc = 'period at output of frequency divider'
    >>> print(out_period.name, '=', out_period, '#', out_period.desc)
    output period = 100ns # period at output of frequency divider

From a quantity object, you access its value in various ways:

.. code-block:: python

    >>> h_line = Quantity('1420.405751786 MHz')

    >>> h_line.as_tuple()
    (1420405751.786, 'Hz')

    >>> str(h_line)
    '1.4204GHz'

    >>> h_line.render()
    '1.4204GHz'

    >>> h_line.render(si=False)
    '1.4204e9Hz'

You can also access the value without the units:

.. code-block:: python

    >>> float(h_line)
    1420405751.786

    >>> h_line.render(False)
    '1.4204G'

    >>> h_line.render(False, si=False)
    '1.4204e9'

Or you can access just the units:

.. code-block:: python

    >>> h_line.units
    'Hz'

You can also access the full precision of the quantity:

.. code-block:: python

    >>> h_line.render(prec='full')
    '1.420405751786GHz'

    >>> h_line.render(si=False, prec='full')
    '1.420405751786e9Hz'

Full precision implies whatever precision was used when specifying the quantity 
if it was specified as a string. If it was specified as a real number, then 
a fixed, user controllable number of digits are used (default=12). Generally one 
uses 'full' when generating output that will be read by a machine.

If you specify *fmt* to render, it will generally include the name and perhaps 
the description if they are available. The formatting is controlled by 
'assign_fmt', which is described later. With the default formatting, the 
description is not printed.

.. code-block:: python

    >>> h_line.render(fmt=True)
    '1.4204GHz'

    >>> out_period.render(fmt=True)
    'output period = 100ns'


Quantities As Reals
-------------------

You can use a quantity in the same way that you can use a real number, meaning 
that you can use it in expressions and it will evaluate to its real value::

    >>> period = Quantity('1us')
    >>> print(period)
    1us

    >>> frequency = 1/period
    >>> print(frequency)
    1000000.0

    >>> type(period)
    <class 'quantiphy.Quantity'>

    >>> type(frequency)
    <class 'float'>

Notice that when performing arithmetic operations on quantities the units are 
completely ignored and do not propagate in any way to the newly computed result.


Preferences
-----------

You can adjust some of the behavior of these functions on a global basis using 
*set_preferences*:

.. code-block:: python

   >>> Quantity.set_preferences(prec=2, spacer=' ')
   >>> h_line.render()
   '1.42 GHz'

   >>> h_line.render(prec=4)
   '1.4204 GHz'

Specifying *prec* (precision) as 4 gives 5 digits of precision (you get one more 
digit than the number you specify for precision). Thus, the common range for 
*prec* is from 0 to around 12 to 14 for double precision numbers.

Passing *None* as a value in *set_preferences* returns that preference to its 
default value:

.. code-block:: python

   >>> Quantity.set_preferences(prec=None, spacer=None)
   >>> h_line.render()
   '1.4204GHz'

The available preferences are:

si (bool):
    Use SI scale factors by default. Default is True.

units (bool):
    Output units by default. Default is True.

prec (int):
    Default precision in digits where 0 corresponds to 1 digit, must
    be nonnegative. This precision is used when full precision is not requested.
    Default is 4 digits.

full_prec (int):
    Default full precision in digits where 0 corresponds to 1 digit.
    Must be nonnegative. This precision is used when full precision is requested 
    if the precision is not otherwise known. Default is 12 digits.

spacer (str):
    May be '' or ' ', use the latter if you prefer a space between
    the number and the units. Generally using ' ' makes numbers easier to
    read, particularly with complex units, and using '' is easier to parse.  
    Default is ''.

unity_sf (str):
    The output scale factor for unity, generally '' or '_'.  Default is ''.  
    Generally '' is used if only humans are expected to read the result and '_' 
    is used if you expect to parse the numbers again. Using '_' eliminates the 
    ambiguity between units and scale factors.

output_sf (str):
    Which scale factors to output, generally one would only use familiar scale 
    factors.  Default is 'TGMkmunpfa'.

ignore_sf (bool):
    Whether scale factors should be ignored by default when converting strings 
    into numbers.  Default is False.

reltol (real):
    Relative tolerance, used by is_close() when determining equivalence. Default 
    is 10\ :sup:`-6`.

abstol (real):
    Absolute tolerance, used by is_close() when determining equivalence. Default 
    is 10\ :sup:`-12`.

keep_components (bool):
    Whether components of number should be kept if the quantities' value was 
    given as string.  Doing so takes a bit of space, but allows the original 
    precision of the number to be recreated when full precision is requested.

assign_fmt (str or tuple):
    Format string for an assignment. Will be passed through string format method 
    to generate a string that includes the quantity name.  Format string takes 
    three possible arguments named n, q, and d for the name, value and 
    description. The default is ``'{n} = {v}'``.

    If two strings are given as a tuple, then the first is used if the 
    description is present and the second used otherwise. For example, an 
    alternate specification that prints the description in the form of a Python 
    comment if it is available is: ``({n} = {v}  # {d}', '{n} = {v}')``.

assign_rec (str):
    Regular expression used to recognize an assignment. Used in Quantity and
    add_to_namespace() to convert a string to a quantity when a name is present.  
    Default recognizes the form:

        "Temp = 300_K -- Temperature".


Ambiguity of Scale Factors and Units
------------------------------------

By default, *QuantiPhy* treats both the scale factor and the units as being 
optional.  With the scale factor being optional, the meaning of some 
specifications can be ambiguous. For example, '1m' may represent 1 milli or it 
may represent 1 meter.  Similarly, '1meter' my represent 1 meter or 
1 milli-eter. To allow you to avoid this ambiguity, *QuantiPhy* accepts '_' as 
the unity scale factor. In this way '1_m' is unambiguously 1 meter. You can 
instruct *QuantiPhy* to output '_' as the unity scale factor by specifying the 
*unity_sf* argument to *set_preferences*:

.. code-block:: python

   >>> Quantity.set_preferences(unity_sf='_')
   >>> l = Quantity(1, 'm')
   >>> print(l)
   1_m

If you need to interpret numbers that have units and are known not to have scale 
factors, you can specify the *ignore_sf* preference:

.. code-block:: python

   >>> Quantity.set_preferences(ignore_sf=True, unity_sf='')
   >>> l = Quantity('1000m')
   >>> l.as_tuple()
   (1000.0, 'm')

   >>> print(l)
   1km

   >>> Quantity.set_preferences(ignore_sf=False)

Exceptional Values
------------------

You can test whether the value of the quantity is infinite or is not-a-number.

.. code-block:: python

   >>> h_line.is_infinite()
   False

   >>> h_line.is_nan()
   False


Equivalence
-----------

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


Physical Constants
------------------

The Quantity class also supports a small number of predefined physical 
constants.

Plank's constant:

.. code-block:: python

   >>> Quantity.set_preferences(
   ...     fmt=True, spacer=' ', assign_fmt=('{n} = {v} -- {d}', '{n} = {v}')
   ... )

   >>> plank = Quantity('h')
   >>> print(plank)
   h = 662.61e-36 J-s -- Plank's constant

   >>> rplank = Quantity('hbar')
   >>> print(rplank)
   ħ = 105.46e-36 J-s -- reduced Plank's constant

Boltzmann's constant:

.. code-block:: python

   >>> boltz = Quantity('k')
   >>> print(boltz)
   k = 13.806e-24 J/K -- Boltzmann's constant

Elementary charge:

.. code-block:: python

   >>> q = Quantity('q')
   >>> print(q)
   q = 160.22e-21 C -- elementary charge

Speed of light:

.. code-block:: python

   >>> c = Quantity('c')
   >>> print(c)
   c = 299.79 Mm/s -- speed of light

Zero degrees Celsius in Kelvin:

.. code-block:: python

   >>> zeroC = Quantity('0C')
   >>> print(zeroC)
   0°C = 273.15 K -- zero degrees Celsius in Kelvin

*QuantiPhy* uses *k* rather than *K* to represent kilo so that you can 
distinguish between kilo and Kelvin.

Permittivity of free space:

.. code-block:: python

   >>> eps0 = Quantity('eps0')
   >>> print(eps0)
   ε₀ = 8.8542 pF/m -- permittivity of free space

Permeability of free space:

.. code-block:: python

   >>> mu0 = Quantity('mu0')
   >>> print(mu0)
   μ₀ = 1.2566 uH/m -- permeability of free space

Characteristic impedance of free space:

.. code-block:: python

   >>> Z0 = Quantity('Z0')
   >>> print(Z0)
   Z₀ = 376.73 Ohms -- characteristic impedance of free space

You can add additional constants by adding them to the CONSTANTS dictionary:

.. code-block:: python

   >>> from quantiphy import Quantity, CONSTANTS
   >>> CONSTANTS['h_line'] = (1.420405751786e9, 'Hz')
   >>> h_line = Quantity('h_line')
   >>> print(h_line)
   1.4204 GHz

The value of the constant may be a tuple or a string. If it is a string, it will 
be interpreted as if it were passed as the primary argument to Quantity. If it 
is a tuple, it may contain up to 4 values, the value, the units, the name, and 
the description. This value may also be a string, and if so it must contain 
a simple number. The benefit of using a string in this case is that *QuantiPhy* 
will recognize the significant figures and use them as the full precision for 
the quantity.

.. code-block:: python

   >>> CONSTANTS['lambda'] = 'λ = 211.0611405389mm -- wavelength of hydrogen line'
   >>> print(Quantity('lambda'))
   λ = 211.06 mm -- wavelength of hydrogen line

   >>> CONSTANTS['lambda'] = (Quantity('c')/h_line,)
   >>> print(Quantity('lambda'))
   211.06m

   >>> CONSTANTS['lambda'] = (Quantity('c')/h_line, 'm')
   >>> print(Quantity('lambda'))
   211.06 mm

   >>> CONSTANTS['lambda'] = (Quantity('c')/h_line, 'm', 'λ')
   >>> print(Quantity('lambda'))
   λ = 211.06 mm

   >>> CONSTANTS['lambda'] = (Quantity('c')/h_line, 'm', 'λ', 'wavelength of hydrogen line')
   >>> print(Quantity('lambda'))
   λ = 211.06 mm -- wavelength of hydrogen line


String Formatting
-----------------

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

   >>> wavelength = Quantity('lambda')
   >>> print('{:n}'.format(wavelength))
   λ

   >>> print('{:d}'.format(wavelength))
   wavelength of hydrogen line

Using the upper case versions of the format codes that print the numerical value 
of the quantity (SQRFEG) to indicate that the name and perhaps description 
should be included as well. They are under the control of the *assign_fmt* 
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

   >>> print('{0:n} = {0:q} ({0:d})'.format(wavelength))
   λ = 211.06 mm (wavelength of hydrogen line)

   >>> print('{:S}'.format(wavelength))
   λ = 211.06 mm -- wavelength of hydrogen line

You can also specify two values to *assign_fmt*, in which case the first is used 
if there is a description and the second used otherwise.

.. code-block:: python

   >>> Quantity.set_preferences(assign_fmt=('{n} = {v} -- {d}', '{n} = {v}'))

   >>> print('{:S}'.format(trise))
   trise = 10 ns

   >>> print('{:S}'.format(wavelength))
   λ = 211.06 mm -- wavelength of hydrogen line


Exceptions
----------

A ValueError is raised if *Quantity* is passed a string it cannot convert into 
a number:

.. code-block:: python

   >>> try:
   ...     q = Quantity('xxx')
   ... except ValueError as err:
   ...     print(err)
   xxx: not a valid number.


Add to Namespace
----------------

It is possible to put a collection of quantities in a text string and then use 
the *add_to_namespace* function to parse the quantities and add them to the 
Python namespace. For example:

.. code-block:: python

   >>> design_parameters = '''
   ...     Fref = 156 MHz  -- Reference frequency
   ...     Kdet = 88.3 uA  -- Gain of phase detector (Imax)
   ...     Kvco = 9.07 GHz/V  -- Gain of VCO
   ... '''
   >>> Quantity.add_to_namespace(design_parameters)

   >>> print(Fref, Kdet, Kvco, sep='\n')
   Fref = 156 MHz -- Reference frequency
   Kdet = 88.3 uA -- Gain of phase detector (Imax)
   Kvco = 9.07 GHz/V -- Gain of VCO

Any number of quantities may be given, with each quantity given on its own line.  
The identifier given to the left '=' is the name of the variable in the local 
namespace that is used to hold the quantity. The text after the '--' is used as 
a description of the quantity.


Subclassing Quantity
--------------------

By subclassing Quantity you can create different sets of default behaviors that 
are active simultaneously. For example:

.. code-block:: python

   >>> class ConventionalQuantity(Quantity):
   ...     pass

   >>> ConventionalQuantity.set_preferences(si=False, units=False)

   >>> period1 = Quantity(1e-9, 's')
   >>> period2 = ConventionalQuantity(1e-9, 's')
   >>> print(period1, period2)
   1 ns 1e-9
