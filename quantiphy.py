# QuantiPhy -- Physical Quantities
# encoding: utf8

# Description {{{1
"""
*QuantiPhy* is a Python library that offers support for physical quantities.  
A quantity is the pairing of a number and a unit of measure that indicates the 
amount of some measurable thing.  *QuantiPhy* provides quantity objects that 
keep the units with the number, making it easy to share them as single object.  
They subclass float and so can be used anywhere a number is appropriate.

*QuantiPhy* naturally supports SI scale factors, which are widely used in 
science and engineering. SI scale factors make it possible to cleanly represent 
both very large and very small quantities in a form that is both easy to read 
and write.  While generally better for humans, no general programming language 
provides direct support for reading or writing quantities with SI scale factors, 
making it difficult to write software that communicates effectively with humans.  
*QuantiPhy* addresses this deficiency, making it natural and simple to both 
input and output physical quantities.
"""

# License {{{1
# Copyright (C) 2016 Kenneth S. Kundert
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].

# Imports {{{1
from __future__ import division
try:
    from collections import ChainMap
except ImportError:  # pragma: no cover
    from chainmap import ChainMap
from six import string_types, python_2_unicode_compatible
import re
import math
import sys

# Utilities {{{1
# is_str {{{2
def is_str(obj):
    # Identifies strings in all their various guises.
    return isinstance(obj, string_types)

# _named_regex {{{2
def named_regex(name, regex):
    return '(?P<%s>%s)' % (name, regex)

# Unit Conversions {{{1
_unit_conversions = {}
def _convert_units(to_units, from_units, value):
    if to_units == from_units:
        return value
    try:
        return _unit_conversions[(to_units,from_units)](value)
    except KeyError:
        raise KeyError(
            "Unable to convert between '%s' and '%s'." % (to_units, from_units)
        )

class UnitConversion(object):
    """
    Creates a unit converter. Just the creation of the converter is sufficient
    to make it available to :class:`Quantity` (the :class:`UnitConversion`
    object itself is normally discarded). Once created, it is automatically
    employed by :class:`Quantity` when a conversion is requested with the given
    units. A forward conversion is performed if the from and to units match, and
    a reversion conversion is performed if they are swapped.

    :arg to_units:
        A collection of units. If given as a single string it is split.
    :type to_units: string or list of strings

    :arg from_units:
        A collection of units. If given as a single string it is split.
    :type from_units: string or list of strings

    :arg float slope:
        Scale factor for conversion.

    :arg float intercept:
        Conversion offset.

    **Forward Conversion**:
    The following conversion is applied if the given units are among the
    *from_units* and the desired units are among the *to_units*:

        *new_value* = *given_value* * *slope* + *intercept*

    **Reverse Conversion**:
    The following conversion is applied if the given units are among 
    the *to_units* and the desired units are among the *from_units*:

        *new_value* = (*given_value* - *intercept*)/*slope*

    Example::

        >>> from quantiphy import Quantity, UnitConversion
        >>> UnitConversion('m', 'pc parsec', 3.0857e16)
        <...>

    This establishes a conversion between meters (m) and parsecs (parsec, pc)
    that can go both ways::

        >>> d_sol = Quantity('5 μpc', scale='m')
        >>> print(d_sol)
        154.28 Gm

        >>> d_ac = Quantity(1.339848, units='pc')
        >>> print(d_ac.render(scale='m'))
        41.344e15 m

    """
    def __init__(self, to_units, from_units, slope=1, intercept=0):
        to_units = to_units.split() if is_str(to_units) else to_units
        from_units = from_units.split() if is_str(from_units) else from_units
        self.slope = slope
        self.intercept = intercept
        for to in to_units:
            for frm in from_units:
                _unit_conversions[(to, frm)] = self._forward
                _unit_conversions[(frm, to)] = self._reverse

    def _forward(self, value):
        return value*self.slope + self.intercept

    def _reverse(self, value):
        return (value - self.intercept)/self.slope

# Temperature conversions {{{2
UnitConversion('C °C', 'C °C')
UnitConversion('C °C', 'K', 1, -273.15)
UnitConversion('C °C', 'F °F', 5/9, -32*5/9)
UnitConversion('C °C', 'R °R', 5/9, -273.15)
# UnitConversion('K', 'C °C', 1, 273.15) -- redundant
UnitConversion('K', 'F °F', 5/9, 273.15 - 32*5/9)
UnitConversion('K', 'R °R', 5/9, 0)

# Distance conversions {{{2
UnitConversion('m', 'km', 1000)
UnitConversion('m', 'cm', 1/100)
UnitConversion('m', 'mm', 1/1000)
UnitConversion('m', 'um μm micron', 1/1000000)
UnitConversion('m', 'nm', 1/1000000000)
UnitConversion('m', 'Å angstrom', 1/10000000000)
UnitConversion('m', 'mi mile miles', 1609.344)

# Mass conversions {{{2
UnitConversion('g', 'lb lbs', 453.59237)
UnitConversion('g', 'oz', 28.34952)

# Time conversions {{{2
UnitConversion('s', 'sec')
UnitConversion('s', 'min', 60)
UnitConversion('s', 'hr hour', 3600)
UnitConversion('s', 'day', 86400)

# Bit conversions {{{2
UnitConversion('b', 'B', 8)

# Constants {{{1
# set_unit_system {{{2
def set_unit_system(unit_system):
    """Activates a unit system.

    The default unit system is 'mks'. Calling this function changes the active
    unit system to the one with the specified name.  Only constants associated
    with the active unit system or not associated with a unit system are
    available for use.

    :arg str unit_system:
        Name of the desired unit system.

    A *KeyError* is raised if *unit_system* does not correspond to a known unit
    system.

    Example::

        >>> from quantiphy import Quantity, set_unit_system
        >>> set_unit_system('cgs')
        >>> print(Quantity('h').render(show_label='f'))
        h = 6.6261e-27 erg-s -- Plank's constant

        >>> set_unit_system('mks')
        >>> print(Quantity('h').render(show_label='f'))
        h = 662.61e-36 J-s -- Plank's constant

    """
    global _active_constants
    _active_constants = ChainMap(
        _constants[None],
        _constants[unit_system]
    )
_default_unit_system = 'mks'
_constants = {None: {}, _default_unit_system: {}}
set_unit_system(_default_unit_system)

# add_constant {{{2
def add_constant(value, alias=None, unit_systems=None):
    """
    Saves a quantity in such a way that it can later be recalled by name when
    creating new quantities.

    :arg quantity value:
        The value of the constant. Must be a quantity or a string that can be
        directly converted to a quantity.

    :arg str alias:
        An alias for the constant. Can be used to access the constant from as an
        alternative to the name given in the value, which itself is optional.
        If the value has a name, specifying this name is optional. If both are
        given, the constant is accessible using either name.

    :arg unit_systems:
        Name or names of the unit systems to which the constant should be added.
        If given as a string, string will be split at white space to create the
        list.  If a constant is associated with a unit system, it is only
        available when that unit system is active. You need not limit yourself
        to the predefined 'mks' and 'cgs' unit systems. Giving a name creates
        the corresponding unit system if it does not already exist.  If
        *unit_systems* is not given, the constant is not associated with a unit
        system, meaning that it is always available regardless of which unit
        system is active.
    :type unit_systems: list or str

    :raises ValueError:
        *value* must be an instance of :class:`Quantity` or it must be a string
        that can be converted to a quantity.

    :raises NameError:
        *alias* was not specified and no name was available from *value*.

    The constant is saved under *name* if given, and under the name contained
    within *value* if available.  It is not necessary to supply both names, one
    is sufficient.

    Example::

        >>> from quantiphy import Quantity, add_constant
        >>> add_constant('f_hy = 1420.405751786 MHz -- Frequency of hydrogen line')
        >>> print(Quantity('f_hy').render(show_label='f'))
        f_hy = 1.4204 GHz -- Frequency of hydrogen line

    """
    if is_str(value):
        value = Quantity(value)
    if not isinstance(value, Quantity):
        raise ValueError('Expected a quantity for value.')
    if not alias and not value.name:
        raise NameError('No name specified.')
    if is_str(unit_systems):
        unit_systems = unit_systems.split()

    # add value to the collection of constants under both names
    if unit_systems:
        for system in unit_systems:
            constants = _constants.get(system, {})
            if alias:
                constants[alias] = value
            if value.name:
                constants[value.name] = value
            _constants[system] = constants
    else:
        if alias:
            _constants[None][alias] = value
        if value.name:
            _constants[None][value.name] = value

# Globals {{{1
__version__ = '2.1.0'
__released__ = '2017-07-30'

# These mappings are only used when reading numbers
# The key for these mappings must be a single character
MAPPINGS = {
    'Y': 'e24',
    'Z': 'e21',
    'E': 'e18',
    'P': 'e15',
    'T': 'e12',
    'G': 'e9',
    'M': 'e6',
    'K': 'e3',
    'k': 'e3',
    '_': 'e0',
    'c': 'e-2',  # only available for input, not used in output
    'm': 'e-3',
    'u': 'e-6',
    'μ': 'e-6',
    'n': 'e-9',
    'p': 'e-12',
    'f': 'e-15',
    'a': 'e-18',
    'z': 'e-21',
    'y': 'e-24',
}

# These mappings are only used when writing numbers
BIG_SCALE_FACTORS = 'kMGTPEZY'
    # These must be given in order, one for every three decades.
    # Use k rather than K, because K looks like a temperature when used alone.

SMALL_SCALE_FACTORS = 'munpfazy'
    # These must be given in order, one for every three decades.

# Regular expression for recognizing and decomposing string .format method codes
FORMAT_SPEC = re.compile(r'\A([<>]?)(\d*)(?:\.(\d+))?(?:([qQrRusSeEfFgGdn])([a-zA-Z°ÅΩ℧%][-^/()\w]*)?)?\Z')
#                             ^align ^width    ^prec     ^format            ^units

# Defaults {{{1
DEFAULTS = {
    'abstol': 1e-12,
    'assign_rec': r'\A\s*((?P<name>[^=:]+)\s*[=:]\s*)?(?P<val>.*?)(\s*(#|--|//)\s*(?P<desc>.*?)\s*)?\Z',
    'full_prec': 12,
    'ignore_sf': False,
    'input_sf': ''.join(MAPPINGS.keys()),
    'keep_components': True,
    'known_units': [],
    'label_fmt': '{n} = {v}',
    'label_fmt_full': '{n} = {v} -- {d}',
    'map_sf': {},
    'number_fmt': None,
    'output_sf': 'TGMkmunpfa',
    'prec': 4,
    'reltol': 1e-6,
    'show_desc': False,
    'show_label': False,
    'show_si': True,
    'show_units': True,
    'spacer': ' ',
    'strip_radix': True,
    'unity_sf': '',
}
CURRENCY_SYMBOLS = '$£€' if sys.version_info.major == 3 else '$'


# Quantity class {{{1
@python_2_unicode_compatible
class Quantity(float):
    # description {{{2
    """Create a Physical Quantity

    A quantity is a number paired with a unit of measure.

    :arg value:
        The value of the quantity.  If a string, it may be the name of a
        pre-defined constant or it may be a number that may be specified with SI
        scale factors and/or units.  For example, the following are all valid:
        '2.5ns', '1.7 MHz', '1e6Ω', '2.8_V', '1e4 m/s', '$10_000', '42', 'ħ',
        etc.  The string may also have name and description if they are provided
        in a way recognizable by *assign_rec*. For example, 'trise: 10ns --
        rise time' or 'trise = 10ns # rise time' would work with the default
        recognizer.
    :type value: real, string or quantity

    :arg model:
        Used to pick up any missing attibutes (*units*, *name*, *desc*). May be a
        quantity or a string. If model is a quantity, only its units would be
        taken. If model is a string, it is split. Then, if there is one
        item, it is taken to be *units*. If there are two, they are taken
        to be *name* and *units*.  And if there are three or more, the first
        two are taken to the be *name* and *units*, and the remainder is taken
        to be *description*.
    :type model: quantity or string

    :arg str units:
        Overrides the units taken from *value* or *model*.

    :arg scale:
        - If a float, it multiplies by the given value to compute the value of
          the quantity.
        - If a tuple, the first value, a float, is treated as a scale factor
          and the second value, a string, is take to be the units of the
          quantity.
        - If a function, it takes two arguments, the given value and the units 
          and it returns two values, the value and units of the quantity.
        - If a string, it is taken to the be desired units. This value along
          with the units of the given value are used to select a known unit
          conversion, which is applied to create the quantity.
    :type scale: float, tuple, func, or string):

    :arg str name:
        Overrides the name taken from *value* or *model*.

    :arg str desc:
        Overrides the desc taken from *value* or *model*.

    :arg bool ignore_sf:
        Assume the value given within a string does not employ a scale factors.
        In this way, '1m' is interpreted as 1 meter rather than 1 milli.

    :raises KeyError:
        A unit conversion was requested and there is no corresponding unit
        converter or assignment recognizer (*assign_rec*) does not match at least
        the value (*val*).

    :raises ValueError:
        A string was passed that cannot be converted to a quantity.

    You can use *Quantity* to create quantities from floats, strings, or other
    quantities.  If a float is given, *model* or *units* would be used to
    specify the units.

    Examples::

        >>> from quantiphy import Quantity
        >>> from math import pi, tau
        >>> newline = '''
        ... '''

        >>> fhy = Quantity('1420.405751786 MHz')
        >>> sagan = Quantity(pi*fhy, 'Hz')
        >>> sagan2 = Quantity(tau*fhy, fhy)
        >>> print(fhy, sagan, sagan2, sep=newline)
        1.4204 GHz
        4.4623 GHz
        8.9247 GHz

    You can use *scale* to scale the number or convert to different units when
    creating the quantity.

    Examples::

        >>> Tfreeze = Quantity('273.15 K', ignore_sf=True, scale='°C')
        >>> print(Tfreeze)
        0 °C

        >>> Tboil = Quantity('212 °F', scale='°C')
        >>> print(Tboil)
        100 °C

    """

    # constants (do not change these) {{{2
    units = ''
    name = ''
    desc = ''
        # These are used as the default values for these three attributes.
        # Putting them here means that the instances do not need to contain
        # these values if not specified, but yet they can always be accessed.
    all_number_converters = None
    sf_free_number_converters = None
        # These must be initialized to None, but will be set the first time
        # Quantity is instantiated.
    non_breaking_space = ' '

    # preferences {{{2
    _initialized = set()

    # _initialize_preferences {{{3
    @classmethod
    def _initialize_preferences(cls):
        if id(cls) in cls._initialized:
            return
        cls._initialized.add(id(cls))
        if cls == Quantity:
            prefs = DEFAULTS
        else:
            parent = cls.__mro__[1]
                # for some reason I cannot get super to work right
            prefs = parent._preferences
        # copy dict so any changes made to parent's preferences do not affect us
        prefs = dict(prefs)
        cls._preferences = ChainMap({}, prefs)
            # use chain to support use of contexts
            # put empty map in as first so user never accidentally deletes or
            # changes one of the initial preferences

    # set preferences {{{3
    @classmethod
    def set_prefs(cls, **kwargs):
        """Set class preferences.

        Any values not passed in are left alone.
        Pass in *None* to reset a preference to its default value.

        :arg float abstol:
            Absolute tolerance, used by :meth:`Quantity.is_close()` when
            determining equivalence.  Default is 10⁻¹².


        :arg str assign_rec:
            Regular expression used to recognize an assignment.  Used in
            constructor and extract(). By default an '=' or ':' separates the
            name from the value and a '--', '#' or '//' separates the value from
            the description, if a description is given. So the default
            recognizes the following forms::

                'vel = 60 m/s'
                'vel = 60 m/s -- velocity'
                'vel = 60 m/s # velocity'
                'vel = 60 m/s // velocity'
                'vel: 60 m/s'
                'vel: 60 m/s -- velocity'
                'vel: 60 m/s # velocity'
                'vel: 60 m/s // velocity'

            The name, value, and description are identified in the regular
            expression using named groups the names *name*, *val* and *desc*.
            For example::

                assign_req = r'(?P<name>.*+) = (?P<val>.*?) -- (?P<desc>.*?)',

        :arg int full_prec:
            Default full precision in digits where 0 corresponds to 1 digit.
            Must be nonnegative.  This precision is used when the full precision
            is requested and the precision is not otherwise known. Default is 12.

        :arg bool ignore_sf:
            Whether all scale factors should be ignored by default when
            recognizing numbers.

        :arg str input_sf:
            Which scale factors to recognize when reading numbers.  The default
            is 'YZEPTGMKk_cmuμnpfazy'.  You can use this to ignore the scale
            factors you never expect to reduce the chance of a scale factor/unit
            ambiguity.  For example, if you expect to encounter temperatures in
            Kelvin and can do without 'K' as a scale factor, you might use
            'TGMK_munpfa'. This also gets rid of the unusual scale factors.

        :arg bool keep_components:
            Indicate whether components should be kept if quantity value was
            given as string. Doing so takes a bit of space, but allows the
            original precision of the number to be recreated when full precision
            is requested.

        :arg known_units:
            List of units that are expected to be used in preference to a scale
            factor when the leading character could be mistaken as a scale
            factor.  If a string is given, it is split at white space to form
            the list. When set, any previous known units are overridden.
        :type known_units: list or string

        :arg str label_fmt:
            Format string used when label is requested if the quantity does not
            have a description or if the description was not requested (if
            *show_desc* is False).  Is passed through string .format() method.
            Format string takes two possible arguments named *n* and *v*
            for the name and value.  A typical values include::

                '{n} = {v}'    (default)
                '{n}: {v}'

        :arg str label_fmt_full:
            Format string used when label is requested if the quantity 
            has a description and the description was requested (if
            *show_desc* is True).  Is passed through string .format() method.
            Format string takes four possible arguments named *n*, *v*, *d* and *V*
            for the name, value, description, and value as formatted by *label_fmt*.
            Typical value include::

                '{n} = {v} --  {d}'    (default)
                '{n} = {v} # {d}'
                '{n} = {v} // {d}'
                '{n}: {v} -- {d}'
                '{V} -- {d}'
                '{V:<20}  # {d}'

            The last example shows the *V* argument with alignment and width
            modifiers.  In this case the modifiers apply to the name and value
            after being they are combined with the *label_fmt*. This is
            typically done when printing several quantities, one per line,
            because it allows you to line up the descriptions.

        :arg map_sf:
            Use this to change the way individual scale factors are rendered,
            ex: map_sf={'u': 'μ'} to render micro using mu. If a function is
            given, it takes a single string argument, the nominal scale factor,
            and returns a string, the desired scale factor. *QuantiPhy* provides
            two predefined functions intended for use with *maps_sf*:
            :meth:`Quantity.map_sf_to_greek` and
            :meth:`Quantity.map_sf_to_sci_notation`.
        :type map_sf: dictionary or function

        :arg number_fmt:
            Format string used to convert the components of the number into the
            number itself.  Normally this is not necessary. However, it can be
            used to perform special formatting that is helpful when aligning
            numbers in tables.  It allows you to specify the widths and
            alignments of the individual components. There are three named
            components: *whole*, *frac*, and *units*.  *whole* contains the
            portion of the mantissa to the left of the radix (decimal point). It
            is the whole mantissa if there is no radix. It also includes the
            sign and the leading units (currency symbols), if any. *frac*
            contains the radix and the fractional part.  It also contains the
            exponent if the number has one. *units* contains the scale factor
            and units.  The following value can be used to align both the radix
            and the units, and give the number a fixed width::

                number_fmt = '{whole:>3s}{frac:<4s} {units:<3s}'

            The various widths and alignments could be adjusted to fit a variety
            of needs.

            It is also possible to specify a function as *number_fmt*, in which
            case it is passed the three values in order (*whole*, *frac* and
            *units*) and it expected to return the number as a string.
        :type number_fmt: dictionary or function

        :arg str output_sf:
            Which scale factors to output, generally one would only use familiar
            scale factors. The default is 'TGMkmunpfa', which gets rid or the
            very large ('YZEP') and very small ('zy') scale factors that many
            people do not recognize.

        :arg int prec:
            Default precision  in digits where 0 corresponds to 1 digit.  Must
            be nonnegative.  This precision is used when the full precision is
            not required. Default is 4.

        :arg float reltol:
            Relative tolerance, used by :meth:`Quantity.is_close()` when
            determining equivalence.  Default is 10⁻⁶.

        :arg bool show_desc:
            Whether the description should be shown if it is available when
            showing the label.  By default *show_desc* is False.

            .. deprecated:: 2.1
               Use ``show_label='f'`` instead.

        :arg show_label:
            Add the name and possibly the description when rendering a quantity
            to a string.  Either *label_fmt* or *label_fmt_full* is used to
            label the quantity.

            - Neither is used if *show_label* is False,
            - otherwise *label_fmt* is used if quantity does not have a
              description or if *show_label* is 'a' (short for abbreviated),
            - otherwise *label_fmt_full* is used if *show_desc* is True or
              *show_label* is 'f' (short for full).
        :type show_label: 'f', 'a', or bool

        :arg bool show_si:
            Use SI scale factors by default. If this is not set, engineering
            format is used.  Engineering format is normal E-notation except that
            the exponents are constrained to be a multiple of 3.

        :arg str spacer:
            The spacer text to be inserted in a string between the numeric value
            and the scale factor when units are present.  Is generally specified
            to be '' or ' '; use the latter if you prefer a space between the
            number and the units. Generally using ' ' makes numbers easier to
            read, particularly with complex units, and using '' is easier to
            parse.  You could also use a Unicode non-breaking space ' '. For
            your convenience, you can access a non-breaking space using
            Quantity.non_breaking_space.

        :arg bool strip_radix:
            When rendering, strip the radix (decimal point) from numbers even if they
            can then be mistaken for integers. By default this is True.

        :arg str unity_sf:
            The output scale factor for unity, generally '' or '_'. The default
            is '', but use '_' if you want there to be no ambiguity between
            units and scale factors. For example, 0.3 would be rendered as
            '300m', and 300 m would be rendered as '300_m'.

        :raises KeyError: unknown preference.

        Example::

            >>> mu0 = Quantity('mu0')
            >>> print(mu0)
            1.2566 uH/m

            >>> Quantity.set_prefs(prec=6, map_sf={'u': 'μ'})
            >>> print(mu0)
            1.256637 μH/m

            >>> Quantity.set_prefs(prec=None, map_sf=None)
            >>> print(mu0)
            1.2566 uH/m

        """
        cls._initialize_preferences()
        if is_str(kwargs.get('known_units')):
            kwargs['known_units'] = kwargs['known_units'].split()
        for k, v in kwargs.items():
            if k not in DEFAULTS.keys():
                 raise KeyError(k)
            if v is None:
                try:
                    del cls._preferences[k]
                except KeyError:
                    # This occurs if pref is not set in first member of chain
                    # could pass, explicitly set to default, or raise
                    pass
            else:
                cls._preferences[k] = v
        if 'input_sf' in kwargs:
            cls._initialize_recognizers()

    # get preference {{{3
    @classmethod
    def get_pref(cls, name):
        """Get class preference

        Returns the value of given preference.

        :arg str name:
            Name of the desired preference. See
            :meth:`Quantity.set_prefs()` for list of preferences.

        :raises KeyError: unknown preference.

        Example::

            >>> Quantity.set_prefs(known_units='au')
            >>> known_units = Quantity.get_pref('known_units')
            >>> known_units.append('pc')
            >>> Quantity.set_prefs(known_units=known_units)
            >>> print(Quantity.get_pref('known_units'))
            ['au', 'pc']

        """
        cls._initialize_preferences()
        return cls._preferences[name]

    # preferences {{{3
    # first create a context manager
    class ContextManager:
        def __init__(self, cls, kwargs):
            self.cls = cls
            self.kwargs = kwargs
        def __enter__(self):
            cls = self.cls
            cls._initialize_preferences()
            cls._preferences = cls._preferences.new_child()
            cls.set_prefs(**self.kwargs)
        def __exit__(self, *args):
            self.cls._preferences = self.cls._preferences.parents

    # now, return the context manager
    @classmethod
    def prefs(cls, **kwargs):
        """Set class preferences.

        This is just like :meth:`Quantity.set_prefs()`, except it is designed to
        work as a context manager, meaning that it is meant to be used with
        Python's *with* statement. It allows preferences to be set to new values
        temporarily. They are reset upon exiting the *with* statement. For
        example::

            >>> with Quantity.prefs(ignore_sf=True):
            ...     t = Quantity('600_000 K')
            >>> t_bad = Quantity('600_000 K')
            >>> print(t, t_bad, sep=newline)
            600 kK
            600M

        See :meth:`Quantity.set_prefs()` for list of available arguments.

        :raises KeyError: unknown preference.
        """
        return cls.ContextManager(cls, kwargs)

    # get attribute {{{3
    def __getattr__(self, name):
        try:
            return self.get_pref(name)
        except KeyError:
            raise AttributeError(name)

    # label formatter {{{3
    def _label(self, value, show_label):
        show_label = self.show_label if show_label is None else show_label
        if not show_label or not self.name:
            return value
        Value = value
        if self.desc and show_label != 'a' and (show_label == 'f' or self.show_desc):
            Value = self.label_fmt.format(n=self.name, v=value)
            label_fmt = self.label_fmt_full
        else:
            label_fmt = self.label_fmt
        return label_fmt.format(n=self.name, v=value, d=self.desc, V=Value)

    # _combine {{{2
    def _combine(self, mantissa, sf, units, spacer):
        if self.number_fmt:
            parts = mantissa.split('.')
            whole_part = parts[0]
            frac_part = ''.join(parts[1:])
            if frac_part:
                frac_part = '.' + frac_part
            if units in CURRENCY_SYMBOLS:
                if whole_part[0] == '-':
                    whole_part = '-' + units + whole_part[1:]
                else:
                    whole_part = units + whole_part
                units = ''
            if sf not in MAPPINGS:
                frac_part += sf
                sf = ''
            if callable(self.number_fmt):
                return self.number_fmt(whole_part, frac_part, sf+units)
            return self.number_fmt.format(
                whole=whole_part, frac=frac_part, units=sf+units
            )

        mantissa = mantissa.lstrip('+')
        if units:
            if units in CURRENCY_SYMBOLS:
                # prefix the value with the units
                if mantissa[0] == '-':
                    # if negative, the sign goes before the currency symbol
                    return '-' + units + mantissa[1:] + sf
                else:
                    return units + mantissa + sf
            else:
                if sf in MAPPINGS:
                    # has a scale factor
                    return mantissa + spacer + sf + units
                else:
                    # has an exponent
                    return mantissa + sf + spacer + units
        else:
            return mantissa + sf

    # recognizers {{{2
    @classmethod
    def _initialize_recognizers(cls):
        # Build regular expressions used to recognize quantities

        # identify desired scale factors {{{3
        known_sf = ''.join(MAPPINGS)
        if cls.get_pref('input_sf') is None: # pragma: no cover
            input_sf = known_sf
        else:
            input_sf = cls.get_pref('input_sf')
            unknown_sf = set(input_sf) - set(known_sf)
            if unknown_sf:
                unknown_sf = ', '.join(sorted(unknown_sf))
                raise ValueError('%s: unknown scale factors.' % unknown_sf)

        # components {{{3
        sign = named_regex('sign', '[-+]?')
        space = r'[\s ]'  # the space in this regex is a non-breaking space
        required_digits = r'(?:[0-9][0-9_]*[0-9]|[0-9]+)'  # allow interior underscores
        optional_digits = r'(?:[0-9][0-9_]*[0-9]|[0-9]*)'
        mantissa = named_regex(
            'mant',
            r'(?:{od}\.?{rd})|(?:{rd}\.?{od})'.format(
                rd = required_digits, od = optional_digits
            ),  # leading or trailing digits are optional, but not both
        )
        exponent = named_regex('exp', '[eE][-+]?[0-9]+')
        scale_factor = named_regex('sf', '[%s]' % input_sf)
        units = named_regex('units', r'(?:[a-zA-Z°ÅΩ℧%][-^/()\w·⁻⁰¹²³⁴⁵⁶⁷⁸⁹]*)?')
            # examples: Ohms, V/A, J-s, m/s^2, H/(m-s), Ω, %, m·s⁻²
            # leading char must be letter to avoid 1.0E-9s -> (1e18, '-9s')
        currency = named_regex('currency', '[%s]' % CURRENCY_SYMBOLS)
        nan = named_regex('nan', '(?i)inf|nan')

        # number_with_scale_factor {{{3
        number_with_scale_factor = (
            r'{sign}{mantissa}{space}*{scale_factor}{units}'.format(**locals()),
            lambda match: match.group('sign') + match.group('mant'),
            lambda match: match.group('sf'),
            lambda match: match.group('units')
        )

        # number_with_exponent {{{3
        number_with_exponent = (
            r'{sign}{mantissa}{exponent}{space}*{units}'.format(**locals()),
            lambda match: match.group('sign') + match.group('mant'),
            lambda match: match.group('exp').lower(),
            lambda match: match.group('units')
        )

        # simple_number {{{3
        # this one must be processed after number_with_scale_factor
        simple_number = (
            r'{sign}{mantissa}{space}*{units}'.format(**locals()),
            lambda match: match.group('sign') + match.group('mant'),
            lambda match: '',
            lambda match: match.group('units')
        )

        # currency_with_scale_factor {{{3
        currency_with_scale_factor = (
            r'{sign}{currency}{mantissa}{space}*{scale_factor}'.format(**locals()),
            lambda match: match.group('sign') + match.group('mant'),
            lambda match: match.group('sf'),
            lambda match: match.group('currency')
        )

        # currency_with_exponent {{{3
        currency_with_exponent = (
            r'{sign}{currency}{mantissa}{exponent}'.format(**locals()),
            lambda match: match.group('sign') + match.group('mant'),
            lambda match: match.group('exp').lower(),
            lambda match: match.group('currency')
        )

        # simple_currency {{{3
        simple_currency = (
            r'{sign}{currency}{mantissa}'.format(**locals()),
            lambda match: match.group('sign') + match.group('mant'),
            lambda match: '',
            lambda match: match.group('currency')
        )

        # nan_with_units {{{3
        nan_with_units = (
            r'{sign}{nan}{space}+{units}'.format(**locals()),
            lambda match: match.group('sign') + match.group('nan').lower(),
            lambda match: '',
            lambda match: match.group('units')
        )

        # currency_nan {{{3
        currency_nan = (
            r'{sign}{currency}{nan}'.format(**locals()),
            lambda match: match.group('sign') + match.group('nan').lower(),
            lambda match: '',
            lambda match: match.group('currency')
        )

        # simple_nan {{{3
        simple_nan = (
            r'{sign}{nan}'.format(**locals()),
            lambda match: match.group('sign') + match.group('nan').lower(),
            lambda match: '',
            lambda match: ''
        )

        # all_number_converters {{{3
        cls.all_number_converters = [
            (re.compile('\A\s*{}\s*\Z'.format(pattern)), get_mant, get_sf, get_units)
            for pattern, get_mant, get_sf, get_units in [
                number_with_exponent, number_with_scale_factor, simple_number,
                currency_with_exponent, currency_with_scale_factor, simple_currency,
                nan_with_units, currency_nan, simple_nan,
            ]
        ]

        # sf_free_number_converters {{{3
        cls.sf_free_number_converters = [
            (re.compile('\A\s*{}\s*\Z'.format(pattern)), get_mant, get_sf, get_units)
            for pattern, get_mant, get_sf, get_units in [
                number_with_exponent, simple_number,
                currency_with_exponent, simple_currency,
                nan_with_units, currency_nan, simple_nan,
            ]
        ]

        # numbers embedded in text {{{3
        smpl_units = '[a-zA-Z_°ÅΩ℧]*'
            # may only contain alphabetic characters, ex: V, A, _Ohms, etc.
            # or obvious unicode units, ex: °ÅΩ℧
        sf_or_units = '[a-zA-Z_μ°ÅΩ℧]+'
            # must match units or scale factors: add μ, make non-optional
        space = '[ ]?'  # optional non-breaking space (do not use a normal space)
        left_delimit = r'(?:\A|(?<=[^a-zA-Z0-9_.]))'
        right_delimit = r'(?=[^-+0-9]|\Z)'
            # right_delim excludes [-+0-9] to avoid matches with 1e2, 1e-2, 1e+2
            # this is not great because it seems like it should fail for
            # 10uA+20uA, but it does not and I don't know why.
        cls.embedded_si_notation = re.compile(
            '{left_delimit}{mantissa}{space}{sf_or_units}{right_delimit}'.format(
                **locals()
            )
        )
        cls.embedded_e_notation = re.compile(
            '{left_delimit}{mantissa}{exponent}?{space}{smpl_units}{right_delimit}'.format(
                **locals()
            )
        )

    # constructor {{{2
    def __new__(
        cls, value, model=None, units=None, scale=None,
        name=None, desc=None, ignore_sf=None
    ):
        if ignore_sf is None:
            ignore_sf = cls.get_pref('ignore_sf')
        data = {}

        # intialize Quantity if required
        if not cls.all_number_converters or not cls.sf_free_number_converters:
            cls._initialize_recognizers()

        # process model to get values for name, units, and desc if available
        if model:
            if is_str(model):
                components = model.split(None, 2)
                if len(components) == 1:
                    data['units'] = components[0]
                else:
                    data['name'] = components[0]
                    data['units'] = components[1]
                    if len(components) == 3:
                        data['desc'] = components[2]
            else:
                #data['name'] = getattr(model, 'name', '')
                data['units'] = getattr(model, 'units', '')
                #data['desc'] = getattr(model, 'desc', '')

        def recognize_number(value, ignore_sf):
            if ignore_sf:
                number_converters = cls.sf_free_number_converters
            else:
                number_converters = cls.all_number_converters
            for pattern, get_mant, get_sf, get_units in number_converters:
                match = pattern.match(value)
                if match:
                    mantissa = get_mant(match)
                    sf = get_sf(match)
                    units = get_units(match)
                    if sf+units in cls.get_pref('known_units'):
                        sf, units = '', sf+units
                    mantissa = mantissa.replace('_', '')
                    number = float(mantissa + MAPPINGS.get(sf, sf))
                    return number, units, mantissa, sf
            else:
                raise ValueError('%s: not a valid number.' % value)

        def recognize_all(value):
            try:
                number, u, mantissa, sf = recognize_number(value, ignore_sf)
            except ValueError:
                # not a simple number, try the assignment recognizer
                match = re.match(cls.get_pref('assign_rec'), value)
                if match:
                    args = match.groupdict()
                    n = args.get('name', '')
                    val = args['val']
                    d = args.get('desc', '')
                    number, u, mantissa, sf = recognize_number(val, ignore_sf)
                    if n:
                        data['name'] = n.strip()
                    if d:
                        data['desc'] = d.strip()
                else:
                    raise
            if u:
                data['units'] = u
            return number, mantissa, sf

        # process the value
        if is_str(value) and value in _active_constants:
            value = _active_constants[value]
        if isinstance(value, Quantity):
            number = float(value)
            mantissa = getattr(value, '_mantissa', None)
            sf = getattr(value, '_scale_factor', None)
            if value.units:
                data['units'] = value.units
            if value.name:
                data['name'] = value.name
            if value.desc:
                data['desc'] = value.desc
        elif is_str(value):
            number, mantissa, sf = recognize_all(value)
        else:
            number = value

        # resolve units, name and description
        if not units:
            units = data.get('units')
        if not name:
            name = data.get('name')
        if not desc:
            desc = data.get('desc')

        # perform specified conversion if requested
        if scale:
            original = number
            if is_str(scale):
                # if scale is string, it contains the units to convert from
                number = _convert_units(scale, units, number)
                units = scale
            else:
                try:
                    # otherwise, it might be a function
                    number, units = scale(number, units)
                except TypeError:
                    try:
                        # otherwise, assume it is a scale factor and units
                        multiplier, units = scale
                    except TypeError:
                        # otherwise, assume it is just a scale factor
                        multiplier = scale
                    number *= multiplier
            if original != number:
                # must erase mantissa which is not out of date
                mantissa = None

        # create the underlying data structure and add attributes as appropriate
        self = float.__new__(cls, number)
        if units:
            self.units = units
        if name:
            self.name = name
        if desc:
            self.desc = desc

        if cls.get_pref('keep_components'):
            try:
                # If we got a string, keep the pieces so we can reconstruct it
                # exactly as it was given. Needed for 'full' precision.
                if mantissa:
                    self._mantissa = mantissa
                    self._scale_factor = sf
            except NameError:
                pass
        return self

    # is_infinte() {{{2
    def is_infinite(self):
        """Test value to determine if quantity is infinite.

        Example::

            >>> inf = Quantity('inf Hz')
            >>> inf.is_infinite()
            True

        """
        try:
            value = self._mantissa
        except AttributeError:
            value = str(self.real)
        return value.lower() in ['inf', '-inf', '+inf']

    # is_nan() {{{2
    def is_nan(self):
        """Test value to determine if quantity is not a number.

        Example::

            >>> nan = Quantity('NaN Hz')
            >>> nan.is_nan()
            True

        """
        try:
            value = self._mantissa
        except AttributeError:
            value = str(self.real)
        return value.lower() in ['nan', '-nan', '+nan']

    # as_tuple() {{{2
    def as_tuple(self):
        """Returns a tuple that contains the value as a float along with its units.

        Example::

            >>> period = Quantity('10ns')
            >>> period.as_tuple()
            (1e-08, 's')

        """
        return self.real, self.units

    # render() {{{2
    def render(
        self, show_units=None, show_si=None, prec=None, show_label=None,
        scale=None
    ):
        """Convert quantity to a string.

        :arg bool show_units:
            Whether the units should be included in the string.

        :arg bool show_si:
            Whether SI scale factors should be used.  If true, SI scale factors
            are used if the appropriate scale factor is available, otherwise
            engineering format is used. If false, engineering format is used for
            all numbers.  Engineering format is normal E-notation except that
            the exponents are constrained to be a multiple of 3.

        :arg prec:
            The desired precision (one plus this value is the desired number of
            digits). If specified as 'full', the full original precision is used.
        :type prec: integer or 'full'

        :arg show_label:
            Add the name and possibly the description when rendering a quantity
            to a string.  Either *label_fmt* or *label_fmt_full* is used to
            label the quantity.

            - neither is used if *show_label* is False,
            - otherwise *label_fmt* is used if quantity does not have a
              description or if *show_label* is 'a' (short for abbreviated),
            - otherwise *label_fmt_full* is used if *show_desc* is True or
              *show_label* is 'f' (short for full).
        :type show_label: 'f', 'a', or boolean

        :arg scale:
            - If a float, it scales the displayed value (the quantity is
              multiplied by scale before being converted to the string).
            - If a tuple, the first value, a float, is treated as a scale factor
              and the second value, a string, is take to be the units of the
              displayed value.
            - If a function, it takes two arguments, the value and the units of
              the quantity and it returns two values, the value and units of
              the displayed value.
            - If a string, it is taken to the be desired units. This value along
              with the units of the quantity are used to select a known unit
              conversion, which is applied to create the displayed value.
        :type scale: real, pair, function, or string:

        :raises KeyError:
            A unit conversion was requested and there is no corresponding unit
            converter.

        Example::

            >>> c = Quantity('c')
            >>> print(
            ...     c.render(),
            ...     c.render(show_units=False),
            ...     c.render(show_si=False),
            ...     c.render(prec=6),
            ...     c.render(prec='full'),
            ...     c.render(show_label=True),
            ...     c.render(show_label='f'),
            ...     sep=newline
            ... )
            299.79 Mm/s
            299.79M
            299.79e6 m/s
            299.7925 Mm/s
            299.792458 Mm/s
            c = 299.79 Mm/s
            c = 299.79 Mm/s -- speed of light

            >>> print(
            ...     Tfreeze.render(scale='°F'),
            ...     Tboil.render(scale='°F'),
            ...     sep=newline
            ... )
            32 °F
            212 °F

        """

        # initialize units and si
        show_units = self.show_units if show_units is None else show_units
        units = self.units if show_units else ''
        show_si = self.show_si if show_si is None else show_si

        # check for infinities or NaN
        if self.is_infinite() or self.is_nan():
            value = self._combine(str(self.real), '', units, ' ')
            return self._label(value, show_label)

        # convert into scientific notation with proper precision
        if prec is None:
            prec = self.prec
        if prec == 'full' and hasattr(self, '_mantissa') and not scale:
            mantissa = self._mantissa
            sf = self._scale_factor

            # convert scale factor to integer exponent
            try:
                exp = int(sf)
            except ValueError:
                if sf:
                    exp = int(MAPPINGS.get(sf, sf).lstrip('e'))
                else:
                    exp = 0

            # add decimal point to mantissa if missing
            mantissa += '' if '.' in mantissa else '.'
            # strip off leading zeros and break into components
            whole, frac = mantissa.strip('0').split('.')
            if whole == '':
                # no whole part, remove leading zeros from fractional part
                orig_len = len(frac)
                frac = frac.lstrip('0')
                if frac:
                    whole = frac[:1]
                    frac = frac[1:]
                    exp -= orig_len - len(frac)
                else:
                    # stripping off zeros left us with nothing, this must be 0
                    whole = '0'
                    frac = ''
                    exp = 0
            # normalize the mantissa
            mantissa = whole[0] + '.' + whole[1:] + frac
            exp += len(whole) - 1
        else:
            # determine precision
            if prec == 'full':
                prec = self.full_prec
            assert (prec >= 0)

            # scale if desired
            number = self.real
            if scale:
                if is_str(scale):
                    # if scale is string, it contains the units to convert to
                    number = _convert_units(scale, self.units, number)
                    units = scale
                else:
                    try:
                        # otherwise, it might be a function
                        number, units = scale(number, self.units)
                    except TypeError:
                        try:
                            # otherwise, assume it is a scale factor and units
                            multiplier, units = scale
                        except TypeError:
                            # otherwise, assume it is just a scale factor
                            multiplier = scale
                        number *= multiplier
                if not show_units:
                    units = ''

            # get components of number
            number = "%.*e" % (prec, number)
            mantissa, exp = number.split("e")
            exp = int(exp)

        #  scale factor
        index = exp // 3
        shift = exp % 3
        sf = "e%d" % (exp - shift)
        if index == 0:
            if units and units not in CURRENCY_SYMBOLS:
                sf = self.unity_sf
            else:
                sf = ''
        elif show_si:
            if (index > 0):
                if index <= len(BIG_SCALE_FACTORS):
                    if BIG_SCALE_FACTORS[index-1] in self.output_sf:
                        sf = BIG_SCALE_FACTORS[index-1]
            else:
                index = -index
                if index <= len(SMALL_SCALE_FACTORS):
                    if SMALL_SCALE_FACTORS[index-1] in self.output_sf:
                        sf = SMALL_SCALE_FACTORS[index-1]

        # render the scale factor if approprite
        if self.map_sf:
            try:
                sf = self.map_sf.get(sf, sf)
            except AttributeError:
                sf = self.map_sf(sf)

        # move decimal point as needed
        if shift:
            mantissa += '00'
            whole, frac = mantissa.split('.')
            if shift == 1:
                 mantissa = whole + frac[0:1] + '.' + frac[1:]
            else:
                 mantissa = whole + frac[0:2] + '.' + frac[2:]

        # remove trailing zeros (except if mantissa does not contain a .)
        if mantissa.find('.') >= 0:
            mantissa = mantissa.rstrip("0")

        # remove trailing decimal point
        if sf or show_units or self.strip_radix:
            mantissa = mantissa.rstrip(".")
        else:
            if mantissa[-1] == '.':
                mantissa += '0'

        value =  self._combine(mantissa, sf, units, self.spacer)
        return self._label(value, show_label)

    # is_close() {{{2
    def is_close(self, other, reltol=None, abstol=None, check_units=True):
        '''
        Are values equivalent?

        Indicates  whether the value of a quantity or real number is equivalent
        to that of a quantity. The two values need not be identical, they just
        need to be close to be deemed equivalent.

        :arg other:
            The value to compare against.
        :type other: quantity or real

        :arg float reltol:
            The relative tolerance.
            If not specified. the *reltol* preference is 
            used, which defaults to 1u.

        :arg float abstol:
            The absolute tolerance.  If not specified. the *abstol* preference is 
            used, which defaults to 1p.

        :arg bool check_units:
            If True (the default), and if *other* is a quantity, compare the
            units of the two values, if they differ return False. Otherwise only
            compare the numeric values, ignoring the units.

        :returns:
            Returns true if ``abs(a - b) <= max(reltol * max(abs(a), abs(b)), abstol)``
            where ``a`` and ``b`` represent *other* and the numeric value of the
            underlying quantity.
        :rtype: bool

        Example::

            >>> print(
            ...     c.is_close(c),                     # should pass, is identical
            ...     c.is_close(c+1),                   # should pass, is close
            ...     c.is_close(c+1e4),                 # should fail, not close
            ...     c.is_close(Quantity(c+1, 'm/s')),  # should pass, is close
            ...     c.is_close(Quantity(c+1, 'Hz')),   # should fail, wrong units
            ... )
            True True False True False

        '''
        if check_units:
            other_units = getattr(other, 'units', None)
            if other_units:
                my_units = getattr(self, 'units', None)
                if my_units != other_units:
                    return False
        reltol = self.reltol if reltol is None else reltol
        abstol = self.abstol if abstol is None else abstol
        try:
            return math.isclose(
                self.real, float(other), rel_tol=reltol, abs_tol=abstol
            )
        except AttributeError:  # pragma: no cover
            # used by python3.4 and earlier
            delta = abs(self.real-float(other))
            reference = max(abs(self.real), abs(float(other)))
            return delta <= max(reltol * reference, abstol)

    # __str__() {{{2
    def __str__(self):
        return self.render()

    # __repr__() {{{2
    def __repr__(self):
        show_si = False if self.ignore_sf else None
        return 'Quantity({!r})'.format(
            self.render(show_units=True, show_si=show_si, prec='full')
        )

    # __format__() {{{2
    def __format__(self, template):
        """Convert quantity to string for Python string format function.

        Supports the normal floating point and string format types as well some
        new ones. If the format code is given in upper case, *label_fmt* is used
        to add the name and perhaps description to the result.

        :arg str template: the format string.
        :raises ValueError: unknown format code.

        The format is specified using AW.PT where:
        A is character and gives the alignment: either '', '>', or '<'
        W is integer and gives the width
        P is integer and gives the precision
        T is char and gives the type: choose from q, r, s, e, f, g, u, n, d, ...
           q = quantity [si=y, units=y, label=n] (ex: 1.4204GHz)
           Q = quantity [si=y, units=y, label=y] (ex: f = 1.4204GHz)
           r = real [si=y, units=n, label=n] (ex: 1.4204G)
           R = real [si=y, units=n, label=y] (ex: f = 1.4204G)
             = string [] (ex: 1.4204GHz)
           s = string [label=n] (ex: 1.4204GHz)
           S = string [label=y] (ex: f = 1.4204GHz)
           e = exponential form [si=n, units=n, label=n] (ex: 1.4204e9)
           E = exponential form [si=n, units=n, label=y] (ex: f = 1.4204e9)
           f = float [na] (ex: 1420400000.0000)
           F = float [na] (ex: f = 1420400000.0000)
           g = float [na] (ex: 1.4204e+09)
           G = float [na] (ex: f = 1.4204e+09)
           u = units [na] (ex: Hz)
           n = name [na] (ex: f)
           d = description [na] (ex: hydrogen line)

        """
        match = FORMAT_SPEC.match(template)
        if match:
            align, width, prec, ftype, units = match.groups()
            scale = units if units else None
            prec = int(prec) if prec else None
            ftype = ftype if ftype else ''
            if ftype and ftype in 'dnu':
                if ftype == 'u':
                    value = scale if scale else self.units
                elif ftype == 'n':
                    value = getattr(self, 'name', '')
                elif ftype == 'd':
                    value = getattr(self, 'desc', '')
                else:  # pragma: no cover
                    raise ValueError(
                        "Unknown format code '%s' for object of type 'Quantity'." % ftype
                    )
                return '{0:{1}{2}s}'.format(value, align, width)
            label = ftype.isupper()
            if ftype in 'sS':  # note that ftype = '' matches this case
                label = label if ftype else None
                value = self.render(prec=prec, show_label=label, scale=scale)
            elif ftype in 'qQ':
                value = self.render(
                    prec=prec, show_si=True, show_units=True, show_label=label,
                    scale=scale
                )
            elif ftype in 'rR':
                value = self.render(
                    prec=prec, show_si=True, show_units=False, show_label=label,
                    scale=scale
                )
            else:
                if scale:
                    # this is a hack that will include the scaling
                    value = float(self.render(
                        prec='full', show_si=False, show_units=False,
                        show_label=False, scale=scale
                    ))
                else:
                    value = float(self)
                if prec is None:
                    prec = self.prec
                if prec == 'full':
                    prec = self.full_prec
                if ftype in 'gG':
                    prec += 1
                value = '{0:.{1}{2}}'.format(value, prec, ftype.lower())
                if ftype.isupper():
                    value = self._label(value, True)
            return '{0:{1}{2}s}'.format(value, align, width)
        else:
            # unrecognized format, just provide something reasonable
            return self.render()

    # extract() {{{2
    @classmethod
    def extract(cls, text):
        """Extract quantities

        Takes a string that contains quantity definitions, one per line, and 
        returns those quantities in a dictionary.

        :arg str quantities:
            The string that contains the quantities, one definition per
            line.  Each is parsed by *assign_rec*. By default, the lines are
            assumed to be of the form::

                [<name> = <value>]
                [<name> = <value>] [-- <description>]
                [<name> = <value>] [# <description>]
                [<name> = <value>] [// <description>]
                [<name>: <value>]
                [<name>: <value>] [-- <description>]
                [<name>: <value>] [# <description>]
                [<name>: <value>] [// <description>]

            The brackets indicate that the name/value pair and the description
            is optional.  However, <name> must be given if <value> is given.

            <name>: the name is used as a key for the value.

            <value>: A number with optional units (ex: 3 or 1pF or 1 kOhm),
            the units need not be a simple identifier (ex: 9.07 GHz/V).

            <description>: Optional textual description (ex: Gain of PD (Imax)).

            Blank lines and any line that does not contain a value are ignored.
            So with the default *assign_rec*, lines with the following form are
            ignored::

                -- comment

                # comment
                // comment

        :returns:
            a dictionary of quantities for the values specified in the argument.
        :rtype: dict

        :raises ValueError:
            Value is not a valid number or was not given a name.

        Example::

            >>> sagan_frequencies = r'''
            ...     -- Carl Sagan's SETI frequencies of high interest
            ...
            ...     f_hy = 1420.405751786 MHz -- Hydrogen line frequency
            ...     f_sagan1 = 4462.336274928 MHz -- Sagan's first frequency: pi*f_hy
            ...     f_sagan2 = 8924.672549855 MHz -- Sagan's second frequency: 2*pi*f_hy
            ... '''
            >>> freqs = Quantity.extract(sagan_frequencies)
            >>> for f in freqs.values():
            ...     print(f.render(show_label='f'))
            f_hy = 1.4204 GHz -- Hydrogen line frequency
            f_sagan1 = 4.4623 GHz -- Sagan's first frequency: pi*f_hy
            f_sagan2 = 8.9247 GHz -- Sagan's second frequency: 2*pi*f_hy

            >>> globals().update(freqs)
            >>> print(f_hy, f_sagan1, f_sagan2, sep=newline)
            1.4204 GHz
            4.4623 GHz
            8.9247 GHz

        """
        import keyword
        quantities = {}
        for line in text.splitlines():
            match = re.match(cls.get_pref('assign_rec'), line)
            if match:
                args = match.groupdict()
                name = args.get('name', '')
                value = args['val']
                desc = args.get('desc', '')
                if not value:
                    continue
                if not name:
                    raise ValueError('{}: name not given.'.format(line))
                name = name.strip()
                quantity = cls(value, name=name, desc=desc)
                quantities[name] = quantity
            else:  # pragma: no cover
                raise ValueError('{}: not a valid number.'.format(line))
        return quantities

    # map_sf_to_sci_notation() {{{2
    # The explicit references to unicode here is for backward compatibility with
    # python2. It can be removed when python2 support is dropped.
    _SCI_NOTATION_MAPPER = {
        ord(u'e'): u'×10',
        ord(u'+'): u'',
        ord(u'-'): u'⁻',
        ord(u'0'): u'⁰',
        ord(u'1'): u'¹',
        ord(u'2'): u'²',
        ord(u'3'): u'³',
        ord(u'4'): u'⁴',
        ord(u'5'): u'⁵',
        ord(u'6'): u'⁶',
        ord(u'7'): u'⁷',
        ord(u'8'): u'⁸',
        ord(u'9'): u'⁹',
        ord(u'u'): u'μ',
    }

    @staticmethod
    def map_sf_to_sci_notation(sf):
        """ Render scale factors in scientific notation

        Pass this function to *map_sf* preference if you prefer your large and
        small numbers in classic scientific notation. It also causes 'u' to be
        converted to 'μ'. Set *show_si* False to format all numbers in
        scientific notation.

        Example::

            >>> with Quantity.prefs(map_sf=Quantity.map_sf_to_sci_notation):
            ...     print(
            ...         Quantity('k').render(show_label='f'),
            ...         Quantity('mu0').render(show_label='f'),
            ...         sep=newline,
            ...     )
            k = 13.806×10⁻²⁴ J/K -- Boltzmann's constant
            μ₀ = 1.2566 μH/m -- permeability of free space

        """
        return sf.translate(Quantity._SCI_NOTATION_MAPPER)

    # map_sf_to_greek() {{{2
    @staticmethod
    def map_sf_to_greek(sf):
        '''Render scale factors in Greek alphabet if appropriate.

        Pass this dictionary to *map_sf* preference if you prefer μ rather than u.

        Example::

            >>> with Quantity.prefs(map_sf=Quantity.map_sf_to_greek):
            ...     print(Quantity('mu0').render(show_label='f'))
            μ₀ = 1.2566 μH/m -- permeability of free space

        '''
        # this could just as easily be a simple dictionary, but implement it as
        # a function so that it supports a docstring.
        return {'u': 'μ'}.get(sf, sf)

    # all_from_conv_fmt {{{2
    @classmethod
    def all_from_conv_fmt(cls, text, **kwargs):
        """Convert all numbers and quantities from conventional notation.

        :arg str text:
            A search and replace is performed on this text. The search looks for
            numbers and quantities in floating point or e-notation. They are
            replaced with the same number rendered as a quantity. To be
            recognized any units must be simple (only letters or underscores, no
            digits or symbols) and the units must be immediately adjacent to the
            number.
        :arg \**kwargs:
            By default the numbers are rendered using the currently active
            preferences, but any valid argument to :meth:`Quantity.render()` can
            be passed in to control the rendering.
        :returns:
            A copy of *text* where all numbers that were formatted
            conventionally have been reformatted.
        :rtype: str

        Example::

            >>> text = 'Applying stimulus @ 2.05000e-05s: V(in) = 5.00000e-01V.'
            >>> with Quantity.prefs(spacer=''):
            ...     xlated = Quantity.all_from_conv_fmt(text)
            ...     print(xlated)
            Applying stimulus @ 20.5us: V(in) = 500mV.

        """
        out = []
        start = 0
        for match in cls.embedded_e_notation.finditer(text):
            end = match.start(0)
            number = match.group(0)
            try:
                number = Quantity(number).render(**kwargs)
            except ValueError:  # pragma: no cover
                # something unexpected happened
                # but this is not essential, so ignore it
                pass
            out.append(text[start:end] + number)
            start = match.end(0)
        return ''.join(out) + text[start:]

    # all_from_si_fmt {{{2
    @classmethod
    def all_from_si_fmt(cls, text, **kwargs):
        """Convert all numbers and quantities from SI notation.

        :arg str text:
            A search and replace is performed on this text. The search looks for
            numbers and quantities formatted in SI notation (must have either a
            scale factor or units or both).  They are replaced with the same
            number rendered as a quantity. To be recognized any units must be
            simple (only letters or underscores, no digits or symbols) and the
            units must be immediately adjacent to the number.
        :arg \**kwargs:
            By default the numbers are rendered using the currently active
            preferences, but any valid argument to :meth:`Quantity.render()` can
            be passed in to control the rendering.
        :returns:
            A copy of *text* where all numbers that were formatted with SI scale
            factors have been reformatted.
        :rtype: str

        Example::

            >>> print(Quantity.all_from_si_fmt(xlated))
            Applying stimulus @ 20.5 us: V(in) = 500 mV.

            >>> print(Quantity.all_from_si_fmt(xlated, show_si=False))
            Applying stimulus @ 20.5e-6 s: V(in) = 500e-3 V.

        """
        out = []
        start = 0
        for match in cls.embedded_si_notation.finditer(text):
            end = match.start(0)
            number = match.group(0)
            try:
                number = Quantity(number).render(**kwargs)
            except ValueError:  # pragma: no cover
                # something unexpected happened
                # but this is not essential, so ignore it
                pass
            out.append(text[start:end] + number)
            start = match.end(0)
        return ''.join(out) + text[start:]


# Predefined Constants {{{1
# Plank's constant {{{2
add_constant(
    Quantity(
        '6.626070040e-34',
        units='J-s',
        name='h',
        desc="Plank's constant"
    ),
    unit_systems='mks'
)
add_constant(
    Quantity(
        '6.626070040e-27',
        units='erg-s',
        name='h',
        desc="Plank's constant"
    ),
    unit_systems='cgs'
)

# Reduced Plank's constant {{{2
add_constant(
    Quantity(
        '1.054571800e-34',
        units='J-s',
        name='ħ',
        desc="reduced Plank's constant"
    ),
    alias='hbar',
    unit_systems='mks'
)
add_constant(
    Quantity(
        '1.054571800e-27',
        units='erg-s',
        name='ħ',
        desc="reduced Plank's constant"
    ),
    alias='hbar',
    unit_systems='cgs'
)

# Boltzmann's constant {{{2
add_constant(
    Quantity(
        '1.38064852e-23',
        units='J/K',
        name='k',
        desc="Boltzmann's constant"
    ),
    unit_systems='mks'
)
add_constant(
    Quantity(
        '1.38064852e-16',
        units='erg/K',
        name='k',
        desc="Boltzmann's constant"
    ),
    unit_systems='cgs'
)

# Elementary charge {{{2
add_constant(
    Quantity(
        '1.6021766208e-19',
        units='C',
        name='q',
        desc="elementary charge"
    ),
    unit_systems='mks'
)
add_constant(
    Quantity(
        '4.80320425e-10',
        units='Fr',
        name='q',
        desc="elementary charge"
    ),
    unit_systems='cgs'
)

# Speed of light {{{2
add_constant(
    Quantity(
        '2.99792458e8',
        units='m/s',
        name='c',
        desc="speed of light"
    ),
    unit_systems='mks cgs'
)

# Zero degrees Celsius in Kelvin {{{2
add_constant(
    Quantity(
        '273.15',
        units='K',
        name='0°C',
        desc="zero degrees Celsius in Kelvin"
    ),
    alias='0C',
    unit_systems='mks cgs'
)

# Permittivity of free space {{{2
add_constant(
    Quantity(
        '8.854187817e-12',
        units='F/m',
        name='ε₀',
        desc="permittivity of free space"
    ),
    alias='eps0',
    unit_systems='mks'
)

# Permeability of free space {{{2
add_constant(
    Quantity(
        4e-7*math.pi,
        units='H/m',
        name='μ₀',
        desc="permeability of free space"
    ),
    alias='mu0',
    unit_systems='mks'
)

# Characteristic impedance of free space {{{2
add_constant(
    Quantity(
        '376.730313461',
        units='Ohms',
        name='Z₀',
        desc="characteristic impedance of free space"
    ),
    alias='Z0',
    unit_systems='mks'
)
