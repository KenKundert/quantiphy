Releases
========

1.0 (2016-11-26):
    - Initial production release.

1.1 (2016-11-27):
    - Added *known_units* preference.
    - Added *get_preference* class method.

1.2 (2017-02-24):
    - allow digits after decimal point to be optional
    - support underscores in numbers
    - allow options to be monkey-patched on to Quantity objects
    - add strip_dp option
    - fix some issues in full precision mode
    - ranamed some options, arguments and methods

1.3 (2017-03-19):
    - reworked constants
    - added unit systems for physical constants

1.4 (2017-07-??):
    - created formal documentation
    - enhanced label_fmt to accept {V}
    - allow quantity to be passed as value to Quantity
    - replaced Quantity.add_to_namespace with Quantity.extract
    - raise NameError rather than Assertion for unknown preferences
    - added Quantity.all_from_conv_fmt() and Quantity.all_from_si_fmt()
    - change assign_rec to support more formats
