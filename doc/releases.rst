.. currentmodule:: quantiphy

Releases
========

Latest development release
--------------------------
| Version: 2.20
| Released: 2024-04-27

- Remove % from *tight_units* list.
- Add spacer keyword argument to :meth:`Quantity.render`,
  :meth:`Quantity.fixed` and :meth:`Quantity.binary`.


2.20 (2024-04-27)
-----------------
- Include full quantities if available in :class:`IncompatibleUnits` errors


2.19 (2023-01-05)
-----------------
- Added new standard SI scale factors (*Q*, *R*, *r*, *q*).
- Subclasses of :class:`Quantity` with units now convert values to the desired 
  units rather than allowing the units of the class to be overridden by those of 
  the value.
- Added scale factor conversion.
- Added quantity functions: :func:`as_real`, :func:`as_tuple`, :func:`render`, 
  :func:`fixed`, and :func:`binary`.
- Fixed rendering of full precision numbers in :meth:`Quantity.fixed()`.
- Added *preferred_units* :class:`Quantity` preference.
- Added “cover” option to *strip_radix* :class:`Quantity` preference.
- Added type hints.


2.18 (2022-08-31)
-----------------
- Support parametrized unit conversions (such as molarity).
- Allow % to act as a scale factor.
- First argument of scaling functions are now guaranteed to be quantities.
- Added :func:`UnitConversion.fixture` decorator function.
- Added :meth:`UnitConversion.activate` method
  (allows overridden converters to be re-activated).


2.17 (2022-04-04)
-----------------
- Refine the list of currency symbols.
- Allows currency symbols to be given before or after the underlying number.
- Allow :class:`Quantity` subclasses to be used in scaling if they have units.


2.16 (2021-12-14)
-----------------
- Add support for — as comment character and make it the default.


2.15 (2021-08-03)
-----------------
- Updated predefined physical constants to CODATA 2018 values.
- Switched to more permissive MIT license.
- Add feet to the available length/distance unit conversions.


2.14 (2021-06-18)
-----------------
- Allow primary argument of :meth:`Quantity.is_close` and :meth:`Quantity.add` 
  to be a string.


2.13 (2020-10-13)
-----------------
- Allow currency symbols in compound units (ex: $/oz or lbs/$).


2.12 (2020-07-25)
-----------------
- Bug fix release.


2.11 (2020-07-19)
-----------------
- Dropping support for all versions of Python older than 3.5.
- Added *sia* form (ASCII only SI scale factors).
- Added *only_e_notation* argument to :meth:`Quantity.all_from_conv_fmt()`.
- Added :meth:`Quantity.reset_prefs()` method.


2.10 (2020-03-2)
----------------
- Added *negligible*, *tight_units*, *nan*, and *inf* preferences.
- Added *negligible* argument to render.
- Added :attr:`Quantity.infinity_symbol` attribute.
- Changed the return values for :meth:`Quantity.is_nan()` and :meth:`Quantity.is_infinite()`.


2.9 (2020-01-28)
----------------
- Made :meth:`Quantity.extract()` more forgiving.
- Support radix and comma processing when converting strings to :class:`Quantity`.


2.8 (2020-01-08)
----------------
- Fix nit in installer (setup.py).


2.7 (2019-12-17)
----------------
- Improve the ability of both :meth:`Quantity.add()` and :meth:`Quantity.scale()` to retain attributes.
- Added *accept_binary* preference.
- Support all preferences as class attributes.
- Allow radix and comma to be replaced by adding *radix* and *comma* preferences.


2.6 (2019-09-24)
----------------
- Now support Quantity arguments with :meth:`Quantity.extract()`.
- Allow plus and minus signs to be replaced with Unicode equivalents.


2.5 (2019-01-16)
----------------
- Added RKM codes example.
- Added *check_value* = 'strict' to :meth:`Quantity.add()`.
- Added backward compatibility for *form* argument of :meth:`Quantity.render()` if it is passed as unnamed argument.
- Made :meth:`Quantity.extract()` a bit more general.
- Reformulated exceptions.
- Added support for binary scale factors and :meth:`Quantity.binary()`.


2.4 (2018-09-12)
----------------
- Fixed bug in format that resulted in several format codes ignoring width
- Follow Python convention of right-justifying numbers by default.
- Add Quantity.add() (adds a number to a quantity returning a new quantity)
- Added # alternate form of string formatting.
- Change *show_si* to *form* (argument on :meth:`Quantity.set_prefs()` and :meth:`Quantity.render()` (*show_si* is now obsolete, use *form='si'* instead).
- Added concept of equivalent units for unit conversion to documentation.
- Enhance UnitConversion so that it supports nonlinear conversions.


2.3 (2018-03-11)
----------------
- Enhanced :meth:`Quantity.extract()`

  * non-conforming lines are now ignored
  * values may be expressions
  * values need not be quantities
  * can specify a quantity name distinct from dictionary name

- Enhanced the formatting capabilities.

  * added center alignment
  * added *p* format
  * added *show_commas* preference.
  * added *strip_zeros*, *strip_radix* to :meth:`Quantity.render()`
  * added :meth:`Quantity.fixed()` method
  * added :meth:`Quantity.format()` method
  * support any format specifier supported by Python for floats


2.2 (2017-11-22)
----------------
- Added :meth:`Quantity.scale()`
- Added :meth:`UnitConversion.convert()`
- Added *strip_zeros*
- Added no-op conversions (units change but value stays the same, ex: $ → USD)


2.1 (2017-07-30)
----------------
The primary focus of this release was on improving the documentation, though 
there are a few small feature enhancements.

- Added support for SI standard composite units
- Added support for non-breaking space as spacer
- Removed constraint in :meth:`Quantity.extract()` that names must be identifiers


2.0 (2017-07-15)
----------------
This is a 'coming of age' release where the emphasis shifts from finding the 
right interface to providing an interface that is stable over time. This 
release includes the first formal documentation and a number of new features 
and refinements to the API.

- Created formal documentation
- Enhanced *label_fmt* to accept {V}
- Allow quantity to be passed as value to :class:`Quantity`
- Replaced *Quantity.add_to_namespace* with :meth:`Quantity.extract`
- Raise *NameError* rather than *AssertionError* for unknown preferences
- Added :meth:`Quantity.all_from_conv_fmt()` and :meth:`Quantity.all_from_si_fmt()`
- Change *assign_rec* to support more formats
- Changed *Constant()* to :func:`add_constant()`
- Changed the way preferences are implemented
- Changed name of preference methods: *set_preferences* → *set_prefs*, *get_preference* → *get_pref*
- Added :meth:`Quantity.prefs()` (preferences context manager)
- Split *label_fmt* preference into two: *label_fmt* and *label_fmt_full*
- Added *show_desc* preference
- Allow *show_label* to be either 'a' or 'f' as well True or False
- Renamed *strip_dp* option to *strip_radix*
- Added *number_fmt* option


1.3 (2017-03-19)
----------------
- Reworked constants
- Added unit systems for physical constants


1.2 (2017-02-24)
----------------
- Allow digits after decimal point to be optional
- Support underscores in numbers
- Allow options to be monkey-patched on to Quantity objects
- Add *strip_dp* option
- Fix some issues in full precision mode
- Ranamed some options, arguments and methods


1.1 (2016-11-27)
----------------
- Added *known_units* preference.
- Added *get_preference* class method.


1.0 (2016-11-26)
----------------
- Initial production release.
