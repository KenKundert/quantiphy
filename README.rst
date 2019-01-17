QuantiPhy - Physical Quantities
===============================

.. image:: https://img.shields.io/travis/KenKundert/quantiphy/master.svg
    :target: https://travis-ci.org/KenKundert/quantiphy

.. image:: https://img.shields.io/coveralls/KenKundert/quantiphy.svg
    :target: https://coveralls.io/r/KenKundert/quantiphy

.. image:: https://img.shields.io/pypi/v/quantiphy.svg
    :target: https://pypi.python.org/pypi/quantiphy

.. image:: https://img.shields.io/pypi/pyversions/quantiphy.svg
    :target: https://pypi.python.org/pypi/quantiphy/

.. IGNORE: pypi statistics are broken and unlikely to be fixed
    .. image:: https://img.shields.io/pypi/dm/quantiphy.svg
        :target: https://pypi.python.org/pypi/quantiphy/

:Author: Ken Kundert
:Version: 2.5.0
:Released: 2019-01-16


What?
-----

*QuantiPhy* is a Python library that offers support for physical quantities.  
A quantity is the pairing of a number and a unit of measure that indicates the 
amount of some measurable thing.  *QuantiPhy* provides quantity objects that 
keep the units with the number, making it easy to share them as single object.  
They subclass float and so can be used anywhere a real number is appropriate.


Why?
----

*QuantiPhy* naturally supports SI scale factors, which are widely used in 
science and engineering. SI scale factors make it possible to cleanly represent 
both very large and very small quantities in a form that is both easy to read 
and write.  While generally better for humans, no general programming language 
provides direct support for reading or writing quantities with SI scale factors, 
making it difficult to write software that communicates effectively with humans.  
*QuantiPhy* addresses this deficiency, making it natural and simple to both 
input and output physical quantities.


Features
--------

- Flexibly reads amounts with units and SI scale factors.
- Quantities subclass the *float* class and so can be used as conventional 
  numbers.
- Generally includes the units when printing or converting to strings and by 
  default employs SI scale factors.
- Flexible unit conversion and scaling is supported to make it easy to convert 
  to or from any required form.
- Provides a small but extensible collection of physical constants.
- Supports the binary scale factors (*Ki*, *Mi*, etc.) along with the normal SI 
  scale factors (*k*, *M*, etc.).


Alternatives
------------

There are a considerable number of Python packages dedicated to units and 
quantities (`alternatives <https://kdavies4.github.io/natu/seealso.html>`_).  
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


Quick Start
-----------

You can find the documentation on `ReadTheDocs
<https://quantiphy.readthedocs.io>`_.  Install with::

   pip3 install --user quantiphy

Requires Python3.4 or better.  Python2.7 is also supported, however support for 
unicode is weak.

You can find the full documentation `here <https://quantiphy.readthedocs.io>`_.

You use *Quantity* to convert numbers and units in various forms to quantities:

.. code-block:: python

   >>> from quantiphy import Quantity

   >>> Tclk = Quantity(10e-9, 's')
   >>> print(Tclk)
   10 ns

   >>> Fhy = Quantity('1420.405751786 MHz')
   >>> print(Fhy)
   1.4204 GHz

   >>> Rsense = Quantity('1e-4Ω')
   >>> print(Rsense)
   100 uΩ

   >>> cost = Quantity('$11_200_000')
   >>> print(cost)
   $11.2M

   >>> Tboil = Quantity('212 °F', scale='°C')
   >>> print(Tboil)
   100 °C

Once you have a quantity, there are a variety of ways of accessing aspects of 
the quantity:

.. code-block:: python

   >>> Tclk.real
   1e-08

   >>> float(Fhy)
   1420405751.786

   >>> 2*cost
   22400000.0

   >>> Rsense.units
   'Ω'

   >>> str(Tboil)
   '100 °C'

You can use the render method to flexibly convert the quantity to a string:

.. code-block:: python

   >>> Tclk.render()
   '10 ns'

   >>> Tclk.render(show_units=False)
   '10n'

   >>> Tclk.render(form='eng', show_units=False)
   '10e-9'

   >>> Fhy.render(prec=8)
   '1.42040575 GHz'

   >>> Tboil.render(scale='°F')
   '212 °F'

You can use the string format method or the new format strings to flexibly 
incorporate quantity values into strings:

.. code-block:: python

   >>> f'{Fhy}'
   '1.4204 GHz'

   >>> f'{Fhy:.6}'
   '1.420406 GHz'

   >>> f'|{Fhy:<15.6}|'
   '|1.420406 GHz   |'

   >>> f'|{Fhy:>15.6}|'
   '|   1.420406 GHz|'

   >>> f'Boiling point of water: {Tboil:s}'
   'Boiling point of water: 100 °C'

   >>> f'Boiling point of water: {Tboil:s°F}'
   'Boiling point of water: 212 °F'

*QuantiPhy* has many more features and capabilities. For more information, view 
the `documentation <https://quantiphy.readthedocs.io>`_.
