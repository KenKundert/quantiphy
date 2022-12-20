.. currentmodule:: quantiphy

---------------------
Classes and Functions
---------------------


Quantities
==========

.. autoclass:: Quantity
   :members:

   .. autoclasstoc::


Quantity Functions
------------------

These functions are provided for those that prefer use *QuantiPhy* to convert 
numbers in strings directly to floats, rather than keep the values around as 
:class:`Quantity` objects.

.. autofunction:: as_real
.. autofunction:: as_tuple
.. autofunction:: render
.. autofunction:: fixed
.. autofunction:: binary


Unit Conversion
===============

.. autoclass:: UnitConversion
   :members:

   .. autoclasstoc::


Constants and Unit Systems
==========================

.. autofunction:: add_constant
.. autofunction:: set_unit_system


Exceptions
==========

.. autoexception:: QuantiPhyError
    :members:

.. ignore the following (there is only one method, so no need for TOC)
   .. autoclasstoc::

.. autoexception:: ExpectedQuantity
.. autoexception:: IncompatiblePreferences
.. autoexception:: IncompatibleUnits
.. autoexception:: InvalidNumber
.. autoexception:: InvalidRecognizer
.. autoexception:: MissingName
.. autoexception:: UnknownConversion
.. autoexception:: UnknownFormatKey
.. autoexception:: UnknownPreference
.. autoexception:: UnknownScaleFactor
.. autoexception:: UnknownUnitSystem
