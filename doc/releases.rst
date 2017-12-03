Releases
========

**1.0 (2016-11-26)**:
    - Initial production release.

**1.1 (2016-11-27)**:
    - Added *known_units* preference.
    - Added *get_preference* class method.

**1.2 (2017-02-24)**:
    - allow digits after decimal point to be optional
    - support underscores in numbers
    - allow options to be monkey-patched on to Quantity objects
    - add strip_dp option
    - fix some issues in full precision mode
    - ranamed some options, arguments and methods

**1.3 (2017-03-19)**:
    - reworked constants
    - added unit systems for physical constants

**2.0 (2017-07-15)**:
    This is a 'coming of age' release where the emphasis shifts from finding the 
    right interface to providing an interface that is stable over time. This 
    release includes the first formal documentation and a number of new features 
    and refinements to the API.

    - created formal documentation
    - enhanced label_fmt to accept {V}
    - allow quantity to be passed as value to Quantity
    - replaced Quantity.add_to_namespace with Quantity.extract
    - raise NameError rather than Assertion for unknown preferences
    - added Quantity.all_from_conv_fmt() and Quantity.all_from_si_fmt()
    - change assign_rec to support more formats
    - changed Constant() to add_constant()
    - changed the way preferences are implemented
    - changed name of preference methods:
      set_preferences -> set_prefs, get_preference -> get_pref
    - added Quantity.prefs() (preferences context manager)
    - split label_fmt preference into two: label_fmt and label_fmt_full
    - added show_desc preference
    - allow show_label to be either 'a' or 'f' as well True or False
    - renamed strip_dp option to strip_radix
    - added number_fmt option


**2.1 (2017-07-30)**:
    The primary focus of this release was on improving the documentation, though 
    there are a few small feature enhancements.

    - added support for SI standard composite units
    - added support for non-breaking space as spacer
    - removed constraint in extract() that names must be identifiers

**2.2 (2017-11-22)**:
    - added Quantity.scale()
    - added UnitConversion.convert()
    - added strip_zeros
    - added no-op conversions (units change but value stays the same: ex. $->USD)

**Latest development release**:
    | Version: 2.2.3
    | Released: 2017-12-02
