Releases
========

**Latest development release**:
    | Version: 2.6.2
    | Released: 2019-08-14

    - now support Quantity arguments with :meth:`quantiphy.Quantity.extract()`.
    - allow plus and minus signs to be replaced with Unicode equivalents.

**2.5 (2019-01-16)**:
    - added RKM codes example.
    - added *check_value* = 'strict' to :meth:`quantiphy.Quantity.add()`.
    - added backward compatibility for *form* argument of 
      :meth:`quantiphy.Quantity.render()` if it is passed as unnamed argument.
    - made :meth:`quantiphy.Quantity.extract()` a bit more general.
    - reformulated exceptions.
    - added support for binary scale factors and :meth:`quantiphy.Quantity.binary()`.

**2.4 (2018-09-12)**:
    - fixed bug in format that resulted in several format codes ignoring width
    - follow Python convention of right-justifying numbers by default.
    - add Quantity.add() (adds a number to a quantity returning a new quantity)
    - added # alternate form of string formatting.
    - Change *show_si* to *form* (argument on 
      :meth:`quantiphy.Quantity.set_prefs()` and 
      :meth:`quantiphy.Quantity.render()` (*show_si* is now obsolete, use 
      *form='si'* instead).
    - Added concept of equivalent units for unit conversion to documentation.
    - Enhance UnitConversion so that it supports nonlinear conversions.

**2.3 (2018-03-11)**:
    - enhanced :meth:`quantiphy.Quantity.extract()`

      * non-conforming lines are now ignored
      * values may be expressions
      * values need not be quantities
      * can specify a quantity name distinct from dictionary name

    - enhanced the formatting capabilities.

      * added center alignment
      * added *p* format
      * added *show_commas* preference.
      * added *strip_zeros*, *strip_radix* to :meth:`quantiphy.Quantity.render()`
      * added :meth:`quantiphy.Quantity.fixed()` method
      * added :meth:`quantiphy.Quantity.format()` method
      * support any format specifier supported by Python for floats

**2.2 (2017-11-22)**:
    - added :meth:`quantiphy.Quantity.scale()`
    - added :meth:`quantiphy.UnitConversion.convert()`
    - added *strip_zeros*
    - added no-op conversions (units change but value stays the same, ex: $ → USD)

**2.1 (2017-07-30)**:
    The primary focus of this release was on improving the documentation, though 
    there are a few small feature enhancements.

    - added support for SI standard composite units
    - added support for non-breaking space as spacer
    - removed constraint in :meth:`quantiphy.Quantity.extract()` that names must 
      be identifiers

**2.0 (2017-07-15)**:
    This is a 'coming of age' release where the emphasis shifts from finding the 
    right interface to providing an interface that is stable over time. This 
    release includes the first formal documentation and a number of new features 
    and refinements to the API.

    - created formal documentation
    - enhanced *label_fmt* to accept {V}
    - allow quantity to be passed as value to :class:`quantiphy.Quantity`
    - replaced *Quantity.add_to_namespace* with 
      :meth:`quantiphy.Quantity.extract`
    - raise *NameError* rather than *AssertionError* for unknown preferences
    - added :meth:`quantiphy.Quantity.all_from_conv_fmt()` and 
      :meth:`quantiphy.Quantity.all_from_si_fmt()`
    - change *assign_rec* to support more formats
    - changed *Constant()* to :func:`quantiphy.add_constant()`
    - changed the way preferences are implemented
    - changed name of preference methods:
      *set_preferences* → *set_prefs*, *get_preference* → *get_pref*
    - added :meth:`quantiphy.Quantity.prefs()` (preferences context manager)
    - split *label_fmt* preference into two: *label_fmt* and *label_fmt_full*
    - added *show_desc* preference
    - allow *show_label* to be either 'a' or 'f' as well True or False
    - renamed *strip_dp* option to *strip_radix*
    - added *number_fmt* option

**1.3 (2017-03-19)**:
    - reworked constants
    - added unit systems for physical constants

**1.2 (2017-02-24)**:
    - allow digits after decimal point to be optional
    - support underscores in numbers
    - allow options to be monkey-patched on to Quantity objects
    - add *strip_dp* option
    - fix some issues in full precision mode
    - ranamed some options, arguments and methods

**1.1 (2016-11-27)**:
    - added *known_units* preference.
    - added *get_preference* class method.

**1.0 (2016-11-26)**:
    - initial production release.

