# QuantiPhy — Physical Quantities
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

Documentation can be found at https://quantiphy.readthedocs.io.
"""

# MIT License {{{1
# Copyright (C) 2016-2022 Kenneth S. Kundert
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Imports {{{1
import re
import math
import numbers
from collections import ChainMap


# Helpers {{{1
# _named_regex {{{2
def _named_regex(name, regex):
    return '(?P<%s>%s)' % (name, regex)


# _scale {{{2
def _scale(scale, number, units):
    # allow subclasss of Quantity that has units to be the scale
    try:
        if issubclass(scale, Quantity):
            scale = scale.units
    except TypeError:
        pass

    if isinstance(scale, str):
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
    return number, units


# Exceptions {{{1
# QuantiPhyError {{{2
class QuantiPhyError(Exception):
    """QuantiPhy base exception.

    All of the specific QuantiPhy exceptions subclass this exception.
    """
    _template = "{}"

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def render(self, template=None):
        """Convert exception to a string under guidance of format string.

        :arg str template:
            This string, along with the positional and keyword arguments of
            the exception are passed to the Python format() function and the
            result is returned. *template* may also be a list of strings. In
            this case the first string found that renders without error is used.
            If *template* is not given, the exception is rendered with the
            built-in template.
        """
        if not template:
            template = self._template
        if isinstance(template, str):
            templates = [template]
        else:
            templates = template
        for t in templates:
            # use first template for which all arguments are available.
            try:
                msg = t.format(*self.args, **self.kwargs)
                if msg == t and self.args:
                    break
                return msg
            except (IndexError, KeyError):
                continue
        else:
            raise ValueError('No valid template found.')
        culprits = ', '.join(str(a) for a in self.args)
        return '{}: {}'.format(culprits, t)

    def __str__(self):
        return self.render()

    def __repr__(self):
        name = self.__class__.__name__
        kwargs = ['{!s}={!r}'.format(k, v) for k, v in self.kwargs.items()]
        args = ', '.join(repr(a) for a in list(self.args) + kwargs)
        return '{}({})'.format(name, args)


# ExpectedQuantity {{{2
class ExpectedQuantity(QuantiPhyError, ValueError):
    """
    The value is required to be a Quantity or a string that can be converted to
    a Quantity.
    """
    _template = 'expected a quantity for value.'


# IncompatibleUnits {{{2
class IncompatibleUnits(QuantiPhyError, TypeError):
    """
    The units of the contribution do not match those of the underlying quantity.
    """
    _template = '{}: incompatible units.'


# InvalidNumber {{{2
class InvalidNumber(QuantiPhyError, ValueError, TypeError):
    """
    The value given could not be converted to a number.
    """
    _template = "{}: not a valid number."


# InvalidRecognizer {{{2
class InvalidRecognizer(QuantiPhyError, KeyError):
    """
    The *assign_rec* preference is expected to be a regular expression that
    defines one or more named fields, one of which must be *val*. This exception
    is raised when the current value of *assign_rec* does not satisfy this
    requirement.
    """
    _template = "recognizer does not contain 'val' key."


# MissingName {{{2
class MissingName(QuantiPhyError, NameError):
    """
    *alias* was not specified and no name was available from *value*.
    """
    _template = 'no name specified.'


# UnknownConversion {{{2
class UnknownConversion(QuantiPhyError, KeyError):
    """
    The given units are not supported by the underlying class, or a unit
    conversion was requested and there is no corresponding unit converter.
    """
    _template = (
        "unable to convert {direction} '{}'.",
        "unable to convert between '{}' and '{}'.",
    )


# UnknownFormatKey {{{2
class UnknownFormatKey(QuantiPhyError, KeyError):
    """
    The *label_fmt* and *label_fmt_full* are expected to be format strings that
    may interpolate certain named arguments. The valid named arguments are *n*
    for name, *v* for value, and *d* for description. This exception is raised
    when some other name is used for an interpolated argument.
    """
    _template = '{}: unknown format key.'


# UnknownPreference {{{2
class UnknownPreference(QuantiPhyError, KeyError):
    """
    The name given for a preference is unknown.
    """
    _template = '{}: unknown preference.'


# UnknownScaleFactor {{{2
class UnknownScaleFactor(QuantiPhyError, ValueError):
    """
    The *input_sf* preference gives the list of scale factors that should be
    accepted. This exception is raised if *input_sf* contains an unknown scale
    factor.
    """
    _template = "unknown scale factors."


# UnknownUnitSystem {{{2
class UnknownUnitSystem(QuantiPhyError, KeyError):
    """
    The name given does not correspond to a known unit system.
    """
    _template = "{}: unknown unit system."


# IncompatiblePreferences {{{2
class IncompatiblePreferences(QuantiPhyError, ValueError):
    """
    Two preferences are not compatible
    """


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

    :raises UnknownUnitSystem(QuantiPhyError, KeyError):
        *unit_system* does not correspond to a known unit system.

    Example::

        >>> from quantiphy import Quantity, set_unit_system
        >>> set_unit_system('cgs')
        >>> print(Quantity('h').render(show_label='f'))
        h = 6.6261e-27 erg-s — Plank's constant

        >>> set_unit_system('mks')
        >>> print(Quantity('h').render(show_label='f'))
        h = 662.61e-36 J-s — Plank's constant

    """
    global _active_constants
    try:
        _active_constants = ChainMap(
            _constants[None],
            _constants[unit_system]
        )
    except KeyError:
        raise UnknownUnitSystem(unit_system)


_default_unit_system = 'mks'
_constants = {None: {}, _default_unit_system: {}}
_active_constants = {}
set_unit_system(_default_unit_system)


# add_constant {{{2
def add_constant(value, alias=None, unit_systems=None):
    """
    Create a new constant.

    Save a quantity in such a way that it can later be recalled by name when
    creating new quantities.

    :arg quantity value:
        The value of the constant. Must be a quantity or a string that can be
        directly converted to a quantity.

    :arg str alias:
        An alias for the constant. Can be used to access the constant from as an
        alternative to the name given in the value, which itself is optional.
        If the value has a name, specifying this name is optional. If both are
        given, the constant is accessible using either name.  *alias* may also
        be a list of aliases.

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

    :raises ExpectedQuantity(QuantiPhyError, ValueError):
        *value* must be an instance of :class:`Quantity` or it must be
        a string that can be converted to a quantity.

    :raises MissingName(QuantiPhyError, NameError):
        *alias* was not specified and no name was available from *value*.

    The constant is saved under *name* if given, and under the name contained
    within *value* if available.  It is not necessary to supply both names, one
    is sufficient.

    Example::

        >>> from quantiphy import Quantity, add_constant
        >>> add_constant('f_hy = 1420.405751786 MHz — Frequency of hydrogen line')
        >>> print(Quantity('f_hy').render(show_label='f'))
        f_hy = 1.4204 GHz — Frequency of hydrogen line

    """
    if isinstance(value, str):
        value = Quantity(value)
    if not isinstance(value, Quantity):
        raise ExpectedQuantity()
    if not alias and not value.name:
        raise MissingName()
    if isinstance(unit_systems, str):
        unit_systems = unit_systems.split()
    if alias:
        aliases = [alias] if isinstance(alias, str) else alias
    else:
        aliases = []

    # add value to the collection of constants under both names
    if unit_systems:
        for system in unit_systems:
            constants = _constants.get(system, {})
            for a in aliases:
                constants[a] = value
            if value.name:
                constants[value.name] = value
            _constants[system] = constants
    else:
        for a in aliases:
            _constants[None][a] = value
        if value.name:
            _constants[None][value.name] = value


# Globals {{{1
__version__ = '2.17.0'
__released__ = '2022-01-04'
__all__ = '''
    QuantiPhyError
    ExpectedQuantity
    IncompatibleUnits
    InvalidNumber
    InvalidRecognizer
    MissingName
    UnknownConversion
    UnknownFormatKey
    UnknownPreference
    UnknownScaleFactor
    UnknownUnitSystem
    IncompatiblePreferences
    UnitConversion
    set_unit_system
    add_constant
    Quantity
'''.split()

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
    'µ': 'e-6',  # micro
    'μ': 'e-6',  # greek mu
    'n': 'e-9',
    'p': 'e-12',
    'f': 'e-15',
    'a': 'e-18',
    'z': 'e-21',
    'y': 'e-24',
}
BINARY_MAPPINGS = {
    'Yi': 1024*1024*1024*1024*1024*1024*1024*1024,
    'Zi': 1024*1024*1024*1024*1024*1024*1024,
    'Ei': 1024*1024*1024*1024*1024*1024,
    'Pi': 1024*1024*1024*1024*1024,
    'Ti': 1024*1024*1024*1024,
    'Gi': 1024*1024*1024,
    'Mi': 1024*1024,
    'Ki': 1024,
    '_' : 1,
}

# These mappings are only used when writing numbers
BIG_SCALE_FACTORS = 'kMGTPEZY'
    # These must be given in order, one for every three decades.
    # Use k rather than K, because K looks like a temperature when used alone.

SMALL_SCALE_FACTORS = 'munpfazy'
    # These must be given in order, one for every three decades.

# Supported currency symbols (these go on left side of number)
CURRENCY_SYMBOLS = '$€¥£₩₺₽₹Ƀ₿Ξ'

# Unit symbols that are not simple letters.
# Do not include % as it will be picked up when converting text to numbers,
# which is generally not desired (you would end up converting 0.001% to 1m%).
UNIT_SYMBOLS = '°ÅΩƱΩ℧¢$€¥£₩₺₽₹Ƀ₿șΞ'

# Regular expression for recognizing and decomposing string .format method codes
FORMAT_SPEC = re.compile(r'''\A
    ([<^>]?)                            # alignment
    ([#]?)                              # alternate form
    (\d*)                               # width
    (,?)                                # comma
    (?:\.(\d+))?                        # precision
    (?:
        ([qpPQrRbBusSeEfFgGdn])         # format
        ([a-zA-Z%{us}{cs}][-^/()\w]*)?  # units
    )?
\Z'''.format(cs=re.escape(CURRENCY_SYMBOLS), us=re.escape(UNIT_SYMBOLS)), re.VERBOSE)

# Defaults {{{1
DEFAULTS = dict(
    abstol = 1e-12,
    accept_binary = False,
    assign_rec = r'''
        \A((
            (\#|--|//|—).*                           # simple comment
        )|(
            (
                (?P<name>[^(=:]+?)\s*                # name:  [^(=:]+
                (\(\s*(?P<qname>[^)]*?)\s*\)\s*)?    # qname: (.*)
                [=:]\s*                              #        [=:]
            )?
            (?P<val>.+?)                             # value: .+
            (\s*(\#|--|//|—)\s*(?P<desc>.*?))?       # description: (—|--|//|#) .*
        ))\Z
    ''',
    comma = ',',
    form = 'si',
    full_prec = 12,
    ignore_sf = False,
    inf = 'inf',
    input_sf = ''.join(MAPPINGS.keys()),
    keep_components = True,
    known_units = [],
    label_fmt = '{n} = {v}',
    label_fmt_full = '{n} = {v} — {d}',
    map_sf = {},
    minus = '-',
    nan = 'NaN',
    negligible = False,
    number_fmt = None,
    output_sf = 'TGMkmunpfa',
    plus = '+',
    prec = 4,
    radix = '.',
    reltol = 1e-6,
    show_commas = False,
    show_desc = False,
    show_label = False,
    show_units = True,
    spacer = ' ',
    strip_radix = True,
    strip_zeros = True,
    tight_units = ''' % ° ' " ′ ″ '''.split(),
    unity_sf = '',
)

# These constants are available to expressions in extract strings.
CONSTANTS = {
    'pi': math.pi,
    'π': math.pi,
    'tau': getattr(math, 'tau', 2*math.pi),
    'τ': getattr(math, 'tau', 2*math.pi),
}


# Quantity class {{{1
class Quantity(float):
    # description {{{2
    """Create a physical quantity.

    A quantity is a number paired with a unit of measure.

    :arg value:
        The value of the quantity.  If a string, it may be the name of a
        pre-defined constant or it may be a number that may be specified with SI
        scale factors and/or units.  For example, the following are all valid:
        '2.5ns', '1.7 MHz', '1e6Ω', '2.8_V', '1e4 m/s', '$10_000', '42', 'ħ',
        etc.  The string may also have name and description if they are provided
        in a way recognizable by *assign_rec*. For example, 'trise: 10ns —
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
        - If a float or quantity, it multiplies by the given value to compute
          the value of the quantity.  If a quantity, the units are ignored.
        - If a tuple, the first value, a float, is treated as a scale factor
          and the second value, a string, is take to be the units of the
          quantity.
        - If a function, it takes two arguments, the given value and the units
          and it returns two values, the value and units of the quantity.
        - If a string, it is taken to the be desired units. This value along
          with the units of the given value are used to select a known unit
          conversion, which is applied to create the quantity.
    :type scale: float, tuple, func, string, or quantity

    :arg str name:
        Overrides the name taken from *value* or *model*.

    :arg str desc:
        Overrides the desc taken from *value* or *model*.

    :arg bool ignore_sf:
        Assume the value given within a string does not employ a scale factors.
        In this way, '1m' is interpreted as 1 meter rather than 1 milli.

    :arg bool binary:
        Allow use of binary scale factors (Ki, Mi, Gi, Ti, Pi, Ei, Zi, Yi).

    :raises UnknownConversion(QuantiPhyError, KeyError):
        A unit conversion was requested and there is no corresponding unit
        converter.

    :raises InvalidRecognizer(QuantiPhyError, KeyError):
        Assignment recognizer (*assign_rec*) does not match at least
        the value (*val*).

    :raises UnknownScaleFactor(QuantiPhyError, ValueError):
        Unknown scale factor.

    :raises InvalidNumber(QuantiPhyError, ValueError, TypeError):
        Not a valid number.

    :raises IncompatiblePreferences(QuantiPhyError, ValueError):
        *radix* and *comma* must differ.

    You can use *Quantity* to create quantities from floats, strings, or other
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
    _provisioned_input_sf = None
        # This must be initialized to None.
        # It is set the first time Quantity is instantiated.

    # these are constants that might be useful to the user
    non_breaking_space = ' '
    narrow_non_breaking_space = ' '
    thin_space = ' '
    plus_sign = '＋'
    minus_sign = '−'
    infinity_symbol = '∞'

    # preferences {{{2
    _initialized = False

    # initialize preferences {{{3
    @classmethod
    def _initialize_preferences(cls):
        if cls._initialized == id(cls):
            return
        cls.reset_prefs()

    # reset preferences {{{3
    @classmethod
    def reset_prefs(cls):
        """Reset preferences

        Resets all preferences to the current preferences of the parent class.
        If there is no parent class, they are reset to their defaults.
        """
        cls._initialized = id(cls)
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
        # description {{{4
        """Set class preferences.

        Any values not passed in are left alone.
        Pass in *None* to reset a preference to its default value.

        :arg float abstol:
            Absolute tolerance, used by :meth:`Quantity.is_close()` when
            determining equivalence.  Default is 10⁻¹².

        :arg bool accept_binary:
            Allow use of binary scale factors (Ki, Mi, Gi, Ti, Pi, Ei, Zi, Yi).
            Default is False.

        :arg str assign_rec:
            Regular expression used to recognize an assignment.  Used in
            constructor and extract(). By default an '=' or ':' separates the
            name from the value and a '—', '--', '#', or '//' separates the
            value from the description, if a description is given. So the
            default recognizes the following forms::

                'vel = 60 m/s'
                'vel = 60 m/s — velocity'
                'vel = 60 m/s -- velocity'
                'vel = 60 m/s # velocity'
                'vel = 60 m/s // velocity'
                'vel: 60 m/s'
                'vel: 60 m/s — velocity'
                'vel: 60 m/s -- velocity'
                'vel: 60 m/s # velocity'
                'vel: 60 m/s // velocity'

            The name, value, and description are identified in the regular
            expression using named groups the names *name*, *val* and *desc*.
            For example::

                assign_req = r'(?P<name>.*+) = (?P<val>.*?) — (?P<desc>.*?)',

            The regular expression is interpreted using the re.VERBOSE flag.

            When used with :meth:`Quantity.extract` there are a few
            more features.

            First, you may also introduce comments using '—', '--', '#', or '//'::

                '— comment'
                '-- comment'
                '# comment'
                '// comment'

            Second, you can specify an alternate name using by placing in within
            parentheses following the name::

                'wavelength (λ) = 21 cm — wavelength of hydrogen line'

            In this case, the name attribute for the quantity will be 'λ' and
            the quantity will be filed in the output dictionary using
            'wavelength' as the key. If the alternate name is not given, then
            'wavelength' is used for the quantity name and dictionary key.

            Third, the value may be an expression involving the previously
            specified values. When doing so, you can specify the units by
            following the value expression with a double-quoted string. The
            expressions may contain numeric literals, previously defined
            quantities, and the constants pi and tau.  For example::

                parameters = Quantity.extract(r'''
                    Fin = 250MHz — frequency of input stimulus
                    Tstop = 10/Fin "s" — simulation stop time
                ''')

            In this example, the value for *Tstop* is given as an expression
            involving *Fin*.

        :arg str comma:
            The character to be used as the thousands separator.  It is very
            common to use a comma, but using a space, period, or an underscore
            can be used.
            For your convenience, you can access a non-breaking space using
            :attr:`Quantity.non_breaking_space`,
            :attr:`Quantity.narrow_non_breaking_space`, or
            :attr:`Quantity.thin_space`.

        :arg str form:
            Specifies the form to use for representing numbers by default.
            Choose from 'si', 'sia', 'eng', 'fixed', and 'binary'. As an
            example, 0.25 A is represented with 250 mA when form is 'si', as
            250e-3 A when form is 'eng', and with 0.25 A when from is 'fixed'.
            'sia' (SI ASCII) is like 'si', but causes *map_sf* to be ignored.
            'binary' is like 'sia', but specifies that binary scale factors be
            used.  Default is 'si'.

        :arg int full_prec:
            Default full precision in digits where 0 corresponds to 1 digit.
            Must be nonnegative.  This precision is used when the full precision
            is requested and the precision is not otherwise known. Default is 12.

        :arg bool ignore_sf:
            Whether all scale factors should be ignored by default when
            recognizing numbers.  Default is False.

        :arg str inf:
            The text to be used to represent infinity.  By default its value is
            'inf', but is often set to '∞' (the unicode infinity symbol).  You
            can access the Unicode infinity symbol using
            :attr:`Quantity.infinity_symbol`.

        :arg str input_sf:
            Which scale factors to recognize when reading numbers.  The default
            is 'YZEPTGMKk_cmuµμnpfazy'.  You can use this to ignore the scale
            factors you never expect to reduce the chance of a scale factor/unit
            ambiguity.  For example, if you expect to encounter temperatures in
            Kelvin and can do without 'K' as a scale factor, you might use
            'TGMK_munpfa'. This also gets rid of the unusual scale factors.

        :arg bool keep_components:
            Indicate whether components should be kept if quantity value was
            given as string. Doing so takes a bit of space, but allows the
            original precision of the number to be recreated when full precision
            is requested.  Default is True.

        :arg known_units:
            List of units that are expected to be used in preference to a scale
            factor when the leading character could be mistaken as a scale
            factor.  If a string is given, it is split at white space to form
            the list. When set, any previous known units are overridden.
            Default is empty.
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

                '{n} = {v} — {d}'    (default)
                '{n} = {v} -- {d}'
                '{n} = {v} # {d}'
                '{n} = {v} // {d}'
                '{n}: {v} — {d}'
                '{n}: {v} -- {d}'
                '{V} — {d}'
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
            given, it takes a single string argument, the nominal scale factor
            (which would be the exponent if no scale factor fits), and returns
            either a string or a tuple. The string is the desired scale factor.
            The tuple consists of the string and a flag. If the flag is True the
            string is treated as an exponent, otherwise it is treated as a scale
            factors. The difference between an exponent and a scale factor is
            that the spacer goes after an exponent and before a scale factor.
            *QuantiPhy* provides two predefined functions intended for use with
            *maps_sf*: :meth:`Quantity.map_sf_to_greek` and
            :meth:`Quantity.map_sf_to_sci_notation`.
            Default is empty.
        :type map_sf: dictionary or function

        :arg str minus:
            The text to be used as the minus sign.  By default its value is '-',
            but is sometimes '−' (the unicode minus sign).  You can access the
            Unicode minus sign using :attr:`Quantity.minus_sign`.

            This preference only affects how numbers are rendered.  Both - and
            the unicode − are always accepted as a minus sign when interpreting
            strings as numbers.

        :arg str nan:
            The text to be used to represent a value that is not-a-number.
            By default its value is 'NaN'.

        :arg negligible:
            If the absolute value of the quantity is equal to or smaller than
            *negligible*, it is rendered as 0.  To make *negligible* a function
            of the units of the quantity, pass a dictionary where the keys are
            the units and the values are the value to use for negligible. A key
            of '' is used for quantities with no units and a key of None
            provides a default value for *negligible* that is used if the units
            of the quantity are not found in the dictionary.
        :type negligible: real or dictionary

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
            *units*) and is expected to return the number as a string.
        :type number_fmt: dictionary or function

        :arg str output_sf:
            Which scale factors to output, generally one would only use familiar
            scale factors. The default is 'TGMkmunpfa', which gets rid or the
            very large ('YZEP') and very small ('zy') scale factors that many
            people do not recognize.

        :arg str radix:
            The character to be used as the radix.  By default it is '.'.

        :arg str plus:
            The text to be used as the plus sign.  By default it is '+',
            but is sometimes '＋' (the unicode full width plus sign) or '' to
            simply eliminate plus signs from numbers.  You can access the
            Unicode full width plus sign using
            :attr:`Quantity.plus_sign`.

            This preference only affects how numbers are rendered.  Both + and
            the unicode ＋ are always accepted as a plus sign when interpreting
            strings as numbers.

            *QuantiPhy* currently does not add leading plus signs to either
            mantissa or exponent, so this setting is ignored.

        :arg int prec:
            Default precision  in digits where 0 corresponds to 1 digit.  Must
            be nonnegative.  This precision is used when the full precision is
            not required. Default is 4.

        :arg float reltol:
            Relative tolerance, used by :meth:`Quantity.is_close()` when
            determining equivalence.  Default is 10⁻⁶.

        :arg bool show_commas:
            When rendering to fixed-point string, add commas to the whole part
            of the mantissa, every three digits. By default this is False.

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

        :arg str spacer:
            The spacer text to be inserted in a string between the numeric value
            and the scale factor when units are present.  Is generally specified
            to be '' or ' '; use the latter if you prefer a space between the
            number and the units. Generally using ' ' makes numbers easier to
            read, particularly with complex units, and using '' is easier to
            parse.  You could also use a Unicode non-breaking space ' '. For
            your convenience, you can access a non-breaking space using
            :attr:`Quantity.non_breaking_space`,
            :attr:`Quantity.narrow_non_breaking_space`, or
            :attr:`Quantity.thin_space`.

            Certain units, as defined using the *tight_units* preference, cause
            the spacer to be suppressed.

        :arg bool strip_radix:
            When rendering, strip the radix (decimal point) if not needed from
            numbers even if they could then be mistaken for integers. If this
            setting is False, the radix is still striped if the number has a
            scale factor. By default this is True.

            Set strip_radix to False when generating output that will be read by
            a parser that distinguishes between integers and reals based on the
            presence of a decimal point.

        :arg bool strip_zeros:
            When rendering, strip off any unneeded zeros from the number. By
            default this is True.

            Set strip_zeros to False when you would like to indicated the
            precision of your numbers based on the number of digits shown.

        :arg list of strings tight_units:
            The spacer is suppressed with these units.
            By default, this is done for: % ° ' " ′ ″.
            Some add °F and °C as well.

        :arg str unity_sf:
            The output scale factor for unity, generally '' or '_'. The default
            is '', but use '_' if you want there to be no ambiguity between
            units and scale factors. For example, 0.3 would be rendered as
            '300m', and 300 m would be rendered as '300_m'.

        :raises UnknownPreference(QuantiPhyError, KeyError):
            Unknown preference.

        :raises UnknownScaleFactor(QuantiPhyError, ValueError):
            Unknown scale factor.

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
        # code {{{4
        cls._initialize_preferences()
        if isinstance(kwargs.get('known_units'), str):
            kwargs['known_units'] = kwargs['known_units'].split()
        for k, v in kwargs.items():
            if k not in DEFAULTS.keys():
                raise UnknownPreference(k)
            if v is None:
                try:
                    del cls._preferences[k]
                except KeyError:
                    # This occurs if pref is not set in first member of chain
                    # could pass, explicitly set to default, or raise
                    # pass does not work with context managers, ends up being a
                    # no-op. raise also does not work with context managers, as
                    # the user can do nothing to avoid the exception.
                    cls._preferences[k] = DEFAULTS[k]
            else:
                cls._preferences[k] = v
        if 'input_sf' in kwargs:
            cls._initialize_recognizers()

    # get preference {{{3
    @classmethod
    def get_pref(cls, name):
        """Get class preference.

        Returns the value of given preference.

        :arg str name:
            Name of the desired preference. See
            :meth:`Quantity.set_prefs()` for list of preferences.

        :raises UnknownPreference(QuantiPhyError, KeyError):
            unknown preference.

        Example::

            >>> Quantity.set_prefs(known_units='au')
            >>> known_units = Quantity.get_pref('known_units')
            >>> known_units.append('pc')
            >>> Quantity.set_prefs(known_units=known_units)
            >>> print(Quantity.get_pref('known_units'))
            ['au', 'pc']

        """
        cls._initialize_preferences()
        try:
            return getattr(cls, name, cls._preferences[name])
        except KeyError:
            raise UnknownPreference(name)

    # preferences {{{3
    # first create a context manager
    class _ContextManager:
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

        :raises UnknownPreference(QuantiPhyError, KeyError):
            Unknown preference.

        :raises UnknownScaleFactor(QuantiPhyError, ValueError):
            Unknown scale factor.
        """
        return cls._ContextManager(cls, kwargs)

    # get attribute {{{3
    def __getattr__(self, name):
        try:
            return self.get_pref(name)
        except KeyError:
            raise AttributeError(name)

    # label formatter {{{3
    def _label(self, value, show_label):
        show_desc = self.show_label if show_label is None else show_label
        if not self.name or not show_desc:
            return value

        if show_desc is True:
            show_desc = self.show_label == 'f' or self.show_desc
        else:
            show_desc = show_desc == 'f'

        try:
            if show_desc and self.desc:
                Value = self.label_fmt.format(n=self.name, v=value)
                label_fmt = self.label_fmt_full
            else:
                Value = value
                label_fmt = self.label_fmt
            return label_fmt.format(n=self.name, v=value, d=self.desc, V=Value)
        except KeyError as e:
            raise UnknownFormatKey(e.args[0])

    # _map_leading_sign {{{2
    def _map_leading_sign(self, value, leading_units=''):
        # maps a leading sign, but only if given
        if math.isnan(self):
            # do not display a sign with NaNs
            return leading_units + value.lstrip('+').lstrip('-')
        if value[0] == '-':
            return self.minus + leading_units + value[1:]
        if value[0] == '+':  # pragma: no cover
            # quantiphy does not currently add leading plus signs to either
            # mantissa or exponent
            return self.plus + leading_units + value[1:]
        return leading_units + value

    # _map_sign {{{2
    def _map_sign(self, value):
        # maps + and - anywhere in the value
        if self.minus != '-':
            value = value.replace('-', self.minus)
        if self.plus != '+':
            value = value.replace('+', self.plus)
        return value

    # _fix_punct {{{2
    def _fix_punct(self, mantissa):
        def replace_char(c):
            if c == '.':
                return self.radix
            elif c == ',':
                return self.comma
            return c
        return ''.join((map(replace_char, mantissa)))

    # _combine {{{2
    def _combine(self, mantissa, sf, units, spacer, sf_is_exp=False):
        if units in self.tight_units:
            spacer = ''
        if self.number_fmt:
            parts = mantissa.split('.')
            whole_part = parts[0]
            frac_part = ''.join(parts[1:])
            if frac_part:
                frac_part = self.radix + frac_part
            if units in CURRENCY_SYMBOLS:
                whole_part = self._map_leading_sign(whole_part, units)
                units = ''
            if sf_is_exp:
                frac_part += sf
                sf = ''
            if callable(self.number_fmt):
                return self.number_fmt(whole_part, frac_part, sf+units)
            return self.number_fmt.format(
                whole=whole_part, frac=frac_part, units=sf+units
            )

        mantissa = self._fix_punct(mantissa.lstrip('+'))
        if units:
            if units in CURRENCY_SYMBOLS:
                # prefix the value with the units
                return self._map_leading_sign(mantissa + sf, units)
            mantissa = self._map_leading_sign(mantissa)
            if sf_is_exp:
                # has an exponent
                return mantissa + sf + spacer + units
            # has a scale factor
            return mantissa + spacer + sf + units
        mantissa = self._map_leading_sign(mantissa)
        return mantissa + sf

    # recognizers {{{2
    @classmethod
    def _initialize_recognizers(cls):
        # Build regular expressions used to recognize quantities

        # identify desired scale factors {{{3
        known_sf = ''.join(MAPPINGS)
        if cls.get_pref('input_sf') is None:  # pragma: no cover
            input_sf = known_sf
        else:
            input_sf = cls.get_pref('input_sf')
            unknown_sf = set(input_sf) - set(known_sf)
            if unknown_sf:
                raise UnknownScaleFactor(*sorted(unknown_sf))
        cls._provisioned_input_sf = input_sf

        def fix_sign(num):
            return num.replace('−', '-').replace('＋', '+')

        # components {{{3
        sign = _named_regex('sign', '[-+−＋]?')
        space = r'[\s ]'  # the space in this regex is a non-breaking space
        required_digits = r'(?:[0-9][0-9_]*[0-9]|[0-9]+)'  # allow interior underscores
        optional_digits = r'(?:[0-9][0-9_]*[0-9]|[0-9]*)'
        mantissa = _named_regex(
            'mant',
            r'(?:{od}\.?{rd})|(?:{rd}\.?{od})'.format(
                rd=required_digits, od=optional_digits
            ),  # leading or trailing digits are optional, but not both
        )
        exponent = _named_regex('exp', '[eE][-+]?[0-9]+')
        scale_factor = _named_regex('sf', '[%s]' % input_sf)
        binary_scale_factor = _named_regex('sf', '%s' % '|'.join(BINARY_MAPPINGS))
        currency = _named_regex('currency', '[%s]' % CURRENCY_SYMBOLS)
        units = _named_regex(
            r'units', r'(?:[a-zA-Z%√{us}{cur}][-^/()\w·⁻⁰¹²³⁴⁵⁶⁷⁸⁹√{us}{cur}]*)?'.format(
                us = re.escape(UNIT_SYMBOLS),
                cur = re.escape(CURRENCY_SYMBOLS),
            )
            # examples: Ohms, V/A, J-s, m/s^2, H/(m-s), Ω, %, m·s⁻², V/√Hz
            # leading char must be letter to avoid 1.0E-9s -> (1e18, '-9s')
        )
        nan = _named_regex('nan', '(?:[iI][nN][fF])|(?:[nN][aA][nN])')

        # number_with_scale_factor {{{3
        number_with_scale_factor = (
            r'{sign}{mantissa}{space}*{scale_factor}{units}'.format(**locals()),
            lambda match: fix_sign(match.group('sign')) + match.group('mant'),
            lambda match: match.group('sf'),
            lambda match: match.group('units')
        )

        # number_with_exponent {{{3
        number_with_exponent = (
            r'{sign}{mantissa}{exponent}{space}*{units}'.format(**locals()),
            lambda match: fix_sign(match.group('sign')) + match.group('mant'),
            lambda match: match.group('exp').lower(),
            lambda match: match.group('units')
        )

        # simple_number {{{3
        # this one must be processed after number_with_scale_factor
        simple_number = (
            r'{sign}{mantissa}{space}*{units}'.format(**locals()),
            lambda match: fix_sign(match.group('sign')) + match.group('mant'),
            lambda match: '',
            lambda match: match.group('units')
        )

        # currency_with_scale_factor {{{3
        currency_with_scale_factor = (
            r'{sign}{currency}{mantissa}{space}*{scale_factor}'.format(**locals()),
            lambda match: fix_sign(match.group('sign')) + match.group('mant'),
            lambda match: match.group('sf'),
            lambda match: match.group('currency')
        )

        # currency_with_exponent {{{3
        currency_with_exponent = (
            r'{sign}{currency}{mantissa}{exponent}'.format(**locals()),
            lambda match: fix_sign(match.group('sign')) + match.group('mant'),
            lambda match: match.group('exp').lower(),
            lambda match: match.group('currency')
        )

        # simple_currency {{{3
        simple_currency = (
            r'{sign}{currency}{mantissa}'.format(**locals()),
            lambda match: fix_sign(match.group('sign')) + match.group('mant'),
            lambda match: '',
            lambda match: match.group('currency')
        )

        # nan_with_units {{{3
        nan_with_units = (
            r'{sign}{nan}{space}+{units}'.format(**locals()),
            lambda match: fix_sign(match.group('sign')) + match.group('nan').lower(),
            lambda match: '',
            lambda match: match.group('units')
        )

        # currency_nan {{{3
        currency_nan = (
            r'{sign}{currency}{nan}'.format(**locals()),
            lambda match: fix_sign(match.group('sign')) + match.group('nan').lower(),
            lambda match: '',
            lambda match: match.group('currency')
        )

        # simple_nan {{{3
        simple_nan = (
            r'{sign}{nan}'.format(**locals()),
            lambda match: fix_sign(match.group('sign')) + match.group('nan').lower(),
            lambda match: '',
            lambda match: ''
        )

        # inf_with_units {{{3
        # the word 'inf' is handled as a nan, this only matches ∞
        inf_with_units = (
            r'{sign}∞{space}*{units}'.format(**locals()),
            lambda match: fix_sign(match.group('sign')) + 'inf',
            lambda match: '',
            lambda match: match.group('units')
        )

        # currency_inf {{{3
        # the word 'inf' is handled as a nan, this only matches ∞
        currency_inf = (
            r'{sign}{currency}∞'.format(**locals()),
            lambda match: fix_sign(match.group('sign')) + 'inf',
            lambda match: '',
            lambda match: match.group('currency')
        )

        # simple_inf {{{3
        # the word 'inf' is handled as a nan, this only matches ∞
        simple_inf = (
            r'{sign}∞'.format(**locals()),
            lambda match: fix_sign(match.group('sign')) + 'inf',
            lambda match: '',
            lambda match: ''
        )

        # number_with_binary_scale_factor {{{3
        number_with_binary_scale_factor = (
            r'{sign}{mantissa}{space}*{binary_scale_factor}{units}'.format(**locals()),
            lambda match: fix_sign(match.group('sign')) + match.group('mant'),
            lambda match: match.group('sf'),
            lambda match: match.group('units')
        )

        # all_number_converters {{{3
        cls.all_number_converters = [
            (re.compile(r'\A\s*{}\s*\Z'.format(pattern)), get_mant, get_sf, get_units)
            for pattern, get_mant, get_sf, get_units in [
                currency_with_exponent, currency_with_scale_factor, simple_currency,
                number_with_exponent, number_with_scale_factor, simple_number,
                nan_with_units, currency_nan, simple_nan,
                inf_with_units, currency_inf, simple_inf,
            ]
        ]

        # sf_free_number_converters {{{3
        cls.sf_free_number_converters = [
            (re.compile(r'\A\s*{}\s*\Z'.format(pattern)), get_mant, get_sf, get_units)
            for pattern, get_mant, get_sf, get_units in [
                currency_with_exponent, simple_currency,
                number_with_exponent, simple_number,
                nan_with_units, currency_nan, simple_nan,
                inf_with_units, currency_inf, simple_inf,
            ]
        ]

        # binary_number_converters {{{3
        cls.binary_number_converters = [
            (re.compile(r'\A\s*{}\s*\Z'.format(pattern)), get_mant, get_sf, get_units)
            for pattern, get_mant, get_sf, get_units in [
                number_with_binary_scale_factor,
            ]
        ]

        # numbers embedded in text {{{3
        smpl_units = '[a-zA-Z_{us}]*'.format(us=re.escape(UNIT_SYMBOLS))
            # may only contain alphabetic characters, ex: V, A, _Ohms, etc.
            # or obvious unicode units, ex: °ÅΩƱ
        sf_or_units = '[a-zA-Z_µ{us}]+'.format(us=re.escape(UNIT_SYMBOLS))
            # must match units or scale factors: add µ, make non-optional
        space = '[   ]?'  # optional non-breaking space (do not use a normal space)
        left_delimit = r'(?:\A|(?<=[^a-zA-Z0-9_.]))'
        right_delimit = r'(?=[^-+−＋0-9]|\Z)'
            # right_delim excludes [-+0-9] to avoid matches with 1e2, 1e-2, 1e+2
            # this is not great because it seems like it should fail for
            # 10uA+20uA.
        cls.embedded_si_notation = re.compile(
            '{left_delimit}{sign}{mantissa}{space}{sf_or_units}{right_delimit}'.format(
                **locals()
            )
        )
        cls.embedded_e_notation = re.compile(
            '{left_delimit}{sign}{mantissa}{exponent}?{space}{smpl_units}{right_delimit}'.format(
                **locals()
            )
        )
        cls.embedded_e_notation_only = re.compile(
            '{left_delimit}{sign}{mantissa}{exponent}{space}{smpl_units}{right_delimit}'.format(
                **locals()
            )
        )

    # constructor {{{2
    def __new__(
        cls, value, model=None, *, units=None, scale=None,
        name=None, desc=None, ignore_sf=None, binary=None
    ):
        if ignore_sf is None:
            ignore_sf = cls.get_pref('ignore_sf')
        if binary is None:
            binary = cls.get_pref('accept_binary')
        data = {}

        # initialize Quantity if required
        if cls._provisioned_input_sf != cls.get_pref('input_sf'):
            cls._initialize_recognizers()

        # process model to get values for name, units, and desc if available
        if model:
            if isinstance(model, str):
                components = model.split(None, 2)
                if len(components) == 1:
                    data['units'] = components[0]
                else:
                    data['name'] = components[0]
                    data['units'] = components[1]
                    if len(components) == 3:
                        data['desc'] = components[2]
            else:
                # data['name'] = getattr(model, 'name', '')
                data['units'] = getattr(model, 'units', '')
                # data['desc'] = getattr(model, 'desc', '')

        def recognize_number(value, ignore_sf):
            comma = cls.get_pref('comma')
            radix = cls.get_pref('radix')
            if comma == radix:
                raise IncompatiblePreferences('comma and radix must differ.')
            if binary and not ignore_sf:
                number_converters = cls.binary_number_converters
                for pattern, get_mant, get_sf, get_units in number_converters:
                    match = pattern.match(
                        value.replace(comma, '').replace(radix, '.')
                    )
                    if match:
                        mantissa = get_mant(match)
                        sf = get_sf(match)
                        units = get_units(match)
                        if sf+units in cls.get_pref('known_units'):
                            sf, units = '', sf+units
                        mantissa = mantissa.replace('_', '')
                        number = float(mantissa) * BINARY_MAPPINGS.get(sf, 1)
                        return number, units, None, ''
            if ignore_sf:
                number_converters = cls.sf_free_number_converters
            else:
                number_converters = cls.all_number_converters
            for pattern, get_mant, get_sf, get_units in number_converters:
                match = pattern.match(
                    value.replace(comma, '').replace(radix, '.')
                )
                if match:
                    mantissa = get_mant(match)
                    sf = get_sf(match)
                    units = get_units(match)
                    if sf+units in cls.get_pref('known_units'):
                        sf, units = '', sf+units
                    mantissa = mantissa.replace('_', '')
                    number = float(mantissa + MAPPINGS.get(sf, sf))
                    return number, units, mantissa, sf
            raise InvalidNumber(value)

        def recognize_all(value):
            try:
                number, u, mantissa, sf = recognize_number(value, ignore_sf)
            except ValueError:
                # not a simple number, try the assignment recognizer
                match = re.match(cls.get_pref('assign_rec'), value, re.VERBOSE)
                if match:
                    args = match.groupdict()
                    n = args.get('name', '')
                    try:
                        val = args['val']
                    except KeyError:
                        raise InvalidRecognizer()
                    if not val:
                        raise
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
        if isinstance(value, str) and value in _active_constants:
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
        elif isinstance(value, str):
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
        if scale or isinstance(scale, numbers.Number):
            original = number
            try:
                number, units = _scale(scale, number, units)
            except TypeError:
                raise InvalidNumber(number)
            if original != number:
                # must erase mantissa which is not out of date
                mantissa = None

        # create the underlying data structure and add attributes as appropriate
        try:
            self = float.__new__(cls, number)
        except TypeError:
            raise InvalidNumber(number)
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
        Returns a representation of the number (sign combined with self.inf) if
        value is infinite and None otherwise.

        Example::

            >>> inf = Quantity('inf Hz')
            >>> inf.is_infinite()
            'inf'

        """
        try:
            value = self._mantissa
        except AttributeError:
            value = str(self.real)
        sign, inf, _ = value.lower().partition('inf')
        if inf == 'inf':
            return sign + self.inf

    # is_nan() {{{2
    def is_nan(self):
        """Test value to determine if quantity is not a number.
        Returns a representation of the number (sign combined with self.nan) if
        value is not a number and None otherwise.

        Example::

            >>> nan = Quantity('-nan Hz')
            >>> nan.is_nan()
            '-NaN'

        """
        try:
            value = self._mantissa
        except AttributeError:
            value = str(self.real)
        sign, nan, _ = value.lower().partition('nan')
        if nan == 'nan':
            return sign + self.nan

    # as_tuple() {{{2
    def as_tuple(self):
        """Return a tuple that contains the value as a float along with its units.

        Example::

            >>> period = Quantity('10ns')
            >>> period.as_tuple()
            (1e-08, 's')

        """
        return self.real, self.units

    # _inherit_attributes() {{{2
    def _inherit_attributes(self, donor):
        # Inherit attributes from the donor except those that represent the
        # value, which may differ from the donor. So that means do not copy the
        # units, the mantissa, or the scale factor.
        self.__dict__.update({
            k: v
            for k, v in donor.__dict__.items()
            if k not in ['units', '_mantissa', '_scale_factor']
        })

    # scale() {{{2
    def scale(self, scale, cls=None):
        """Scale a quantity to create a new quantity.

        :arg scale:
            - If a float, it scales the existing value (a new quantity is
              returned whose value equals the existing quantity multiplied by
              scale. In this case the scale is assumed unitless and so the units
              of the new quantity are the same as those of the existing
              quantity).
            - If a tuple, the first value, a float, is treated as a scale factor
              and the second value, a string, is taken to be the units of the
              new quantity.
            - If a function, it takes two arguments, the value and the units of
              the quantity and it returns two values, the value and units of
              the new value.
            - If a string, it is taken to the be desired units. This value along
              with the units of the quantity are used to select a known unit
              conversion, which is applied to create the new value.
            - If a quantity, the units are ignored and the scale is treated as
              if were specified as a unitless float.
            - If a subclass of :class:`Quantity` that includes units, the units
              are taken to the be desired units and the behavior is the same as
              if a string were given, except that *cls* defaults to the given
              subclass.
        :arg class cls:
            Class to use for return value. If not given, the class of self is
            used unless scale is a subclass of :class:`Quantity`, in which case
            *scale* is used.
        :type scale: real, pair, function, string, or quantity

        :raises UnknownConversion(QuantiPhyError, KeyError):
            A unit conversion was requested and there is no corresponding unit
            converter.

        Example::

            >>> Tf = Tfreeze.scale('°F')
            >>> Tb = Tboil.scale('°F')
            >>> print(Tf, Tb, sep=newline)
            32 °F
            212 °F

        """

        # if subclasss of Quantity is passed as scale, use as cls if not given
        try:
            if issubclass(scale, Quantity) and not cls:
                cls = scale
        except TypeError:
            pass

        number, units = _scale(scale, self.real, self.units)
        if not cls:
            cls = self.__class__
        new = cls(number, units)
        new._inherit_attributes(self)
        return new

    # add() {{{2
    def add(self, addend, check_units=False):
        """Create a new quantity that is the sum of the original and a contribution.

        :arg addend:
            The amount to add to the quantity.
        :type addend: real, quantity, string

        :arg check_units:
            If True, raise an exception if the units of the *addend* are not
            compatible with the underlying quantity. If the *addend* does not
            have units, then it is considered compatible unless *check_units* is
            'strict'.
        :type check_units: boolean or 'strict'

        :raises IncompatibleUnits(QuantiPhyError, TypeError):
            Units of contribution do not match those of underlying quantity.

        Example::

            >>> total = Quantity(0, '$')
            >>> for contribution in [1.23, 4.56, 7.89]:
            ...     total = total.add(contribution)
            >>> print(total)
            $13.68

        """
        if isinstance(addend, str):
            addend = self.__class__(addend)

        try:
            if check_units and self.units != addend.units:
                raise IncompatibleUnits(self.units, addend.units)
        except AttributeError:
            if check_units == 'strict':
                raise IncompatibleUnits(
                    getattr(self, 'units', None),
                    getattr(addend, 'units', None)
                )
        new = self.__class__(self.real + addend, self.units)
        new._inherit_attributes(self)
        return new

    # render() {{{2
    def render(
        self, form=None, show_units=None, prec=None, show_label=None,
        strip_zeros=None, strip_radix=None, scale=None, negligible=None
    ):
        """Convert quantity to a string.

        :arg str form:
            Specifies the form to use for representing numbers by default.
            Choose from 'si', 'sia', 'eng', 'fixed', and 'binary'. As an example
            0.25 A is represented with 250 mA when form is 'si', as 250e-3 A
            when form is 'eng', and with 0.25 A when from is 'fixed'.
            'sia' (SI ASCII) is like 'si', but causes *map_sf* preference to be
            ignored.  'binary' is like 'sia', but specifies that binary scale
            factors be used.  Default is 'si'.

        :arg bool show_units:
            Whether the units should be included in the string.

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

        :arg strip_zeros:
            Remove contiguous zeros from end of fractional part. If not
            specified, the global *strip_zeros* setting is used.
        :type strip_zeros: boolean

        :arg strip_radix:
            Remove radix if there is nothing to the right of it.  If not
            specified, the global *strip_radix* setting is used.
        :type strip_radix: boolean

        :arg scale:
            - If a float or a quantity, it scales the displayed value (the
              quantity is multiplied by scale before being converted to the
              string).  If a quantity, the units are ignored.
            - If a tuple, the first value, a float, is treated as a scale factor
              and the second value, a string, is take to be the units of the
              displayed value.
            - If a function, it takes two arguments, the value and the units of
              the quantity and it returns two values, the value and units of
              the displayed value.
            - If a string, it is taken to the be desired units. This value along
              with the units of the quantity are used to select a known unit
              conversion, which is applied to create the displayed value.
        :type scale: real, pair, function, string, or quantity

        :arg negligible:
            If the absolute value of the quantity is equal to or smaller than
            *negligible*, it is rendered as 0.  To make *negligible* a function
            of the units of the quantity, pass a dictionary where the keys are
            the units and the values are the value to use for negligible. A key
            of '' is used for quantities with no units and a key of None
            provides a default value for *negligible* that is used if the units
            of the quantity are not found in the dictionary.
        :type scale: real or dict

        :raises UnknownConversion(QuantiPhyError, KeyError):
            A unit conversion was requested and there is no corresponding unit
            converter.

        :raises UnknownFormatKey(QuantiPhyError, KeyError):
            'label_fmt' or 'label_fmt_full' contains an unknown format key.

        Example::

            >>> c = Quantity('c')
            >>> print(
            ...     c.render(),
            ...     c.render(form='si'),
            ...     c.render(form='eng'),
            ...     c.render(form='fixed'),
            ...     c.render(show_units=False),
            ...     c.render(prec=6),
            ...     c.render(prec='full'),
            ...     c.render(show_label=True),
            ...     c.render(show_label='f'),
            ...     sep=newline
            ... )
            299.79 Mm/s
            299.79 Mm/s
            299.79e6 m/s
            299792458 m/s
            299.79M
            299.7925 Mm/s
            299.792458 Mm/s
            c = 299.79 Mm/s
            c = 299.79 Mm/s — speed of light

            >>> print(
            ...     Tfreeze.render(scale='°F'),
            ...     Tboil.render(scale='°F'),
            ...     sep=newline
            ... )
            32 °F
            212 °F

        """
        # initialize various options
        form = self.form if form is None else form
        show_units = self.show_units if show_units is None else show_units
        strip_zeros = self.strip_zeros if strip_zeros is None else strip_zeros
        strip_radix = self.strip_radix if strip_radix is None else strip_radix
        negligible = self.negligible if negligible is None else negligible
        units = self.units if show_units else ''
        if prec is None:
            prec = self.prec

        if form == 'fixed':
            return self.fixed(
                prec = prec,
                show_units = show_units,
                show_label = show_label,
                strip_zeros = strip_zeros,
                strip_radix = strip_radix,
                scale = scale
            )
        if form == 'binary':
            return self.binary(
                prec = prec,
                show_units = show_units,
                show_label = show_label,
                strip_zeros = strip_zeros,
                strip_radix = strip_radix,
                scale = scale
            )

        # check for infinities or NaN
        value = self.is_infinite() or self.is_nan()
        if value:
            value = self._combine(value, '', units, ' ')
            return self._label(value, show_label)

        # convert into scientific notation with proper precision
        if prec == 'full' and hasattr(self, '_mantissa') and not scale:
            mantissa = self._mantissa
            if mantissa[0] in '+-':
                sign = '-' if mantissa[0] == '-' else ''
                mantissa = mantissa[1:]
            else:
                sign = ''
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
            whole, frac = mantissa.lstrip('0').split('.')
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
            assert prec >= 0

            # scale if desired
            number = self.real
            if scale or isinstance(scale, numbers.Number):
                number, units = _scale(scale, number, self.units)
                if not show_units:
                    units = ''

            # get components of number
            number = "%.*e" % (prec, number)
            mantissa, exp = number.split("e")
            sign = '-' if mantissa[0] == '-' else ''
            mantissa = mantissa.lstrip('-')
            exp = int(exp)

        if negligible is not False:
            try:
                negligible = negligible.get(self.units, negligible.get(None, -1))
            except AttributeError:
                pass
            if abs(self.real) < negligible:
                mantissa = '0'
                exp = 0
                sign = ''

        #  scale factor
        index = exp // 3
        shift = exp % 3
        eexp = "e" + self._map_leading_sign(str(exp - shift))
        sf = eexp
        sf_is_exp = 'unk'
        if index == 0:
            if units and units not in CURRENCY_SYMBOLS:
                sf = self.unity_sf
            else:
                sf = ''
        elif form in ['si', 'sia', True]:  # True is included for backward compatibility
            if index > 0:
                if index <= len(BIG_SCALE_FACTORS):
                    if BIG_SCALE_FACTORS[index-1] in self.output_sf:
                        sf = BIG_SCALE_FACTORS[index-1]
            else:
                index = -index
                if index <= len(SMALL_SCALE_FACTORS):
                    if SMALL_SCALE_FACTORS[index-1] in self.output_sf:
                        sf = SMALL_SCALE_FACTORS[index-1]
        else:
            assert form in ['eng', False], '{}: unknown form.'.format(form)
                # False is included for backward compatibility

        # render the scale factor if appropriate
        if self.map_sf and form != 'sia':
            try:
                sf = self.map_sf.get(sf, sf)
            except AttributeError:
                sf = self.map_sf(sf)
                if isinstance(sf, tuple):
                    sf, sf_is_exp = sf

        # shift the decimal place as needed
        mantissa = mantissa.replace('.', '')
        if strip_zeros:
            mantissa = mantissa.rstrip('0')
        mantissa += (shift + 1 - len(mantissa))*'0'
        mantissa = sign + mantissa[0:(shift+1)] + '.' + mantissa[(shift+1):]

        # remove trailing decimal point
        if sf or strip_radix:  # could also add 'or units'
            mantissa = mantissa.rstrip('.')
        elif strip_zeros:
            # a trailing radix is not very attractive, so add a zero except if
            # strip_zeros is set, which is where we are trying to retain the
            # number of digits specified by prec to convey the number of
            # significant figures.
            if mantissa[-1] == '.':
                mantissa += '0'

        if sf_is_exp == 'unk':
            sf_is_exp = (sf == eexp)
        value = self._combine(mantissa, sf, units, self.spacer, sf_is_exp)
        return self._label(value, show_label)

    # fixed() {{{2
    def fixed(
        self, show_units=None, prec=None, show_label=None, show_commas=None,
        strip_zeros=None, strip_radix=None, scale=None,
    ):
        """Convert quantity to fixed-point string.

        :arg bool show_units:
            Whether the units should be included in the string.

        :arg prec:
            The desired precision (one plus this value is the desired number of
            digits). If specified as 'full', *full_prec* is used as the number
            of digits (and not the originally specified precision as with
            *render()*).
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

        :arg show_commas:
            Add commas to whole part of mantissa, every three digits. If not
            specified, the global *strip_zeros* setting is used.
        :type commas: boolean

        :arg strip_zeros:
            Remove contiguous zeros from end of fractional part. If not
            specified, the global *strip_zeros* setting is used.
        :type strip_zeros: boolean

        :arg strip_radix:
            Remove radix if there is nothing to the right of it.  If not
            specified, the global *strip_radix* setting is used.
        :type strip_radix: boolean

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
        :type scale: real, pair, function, or string

        :raises UnknownConversion(QuantiPhyError, KeyError):
            A unit conversion was requested and there is no corresponding unit
            converter.

        :raises UnknownFormatKey(QuantiPhyError, KeyError):
            'label_fmt' or 'label_fmt_full' contains an unknown format key.

        Example::

            >>> t = Quantity('Total = $1000000 — the total')
            >>> print(
            ...     t.fixed(),
            ...     t.fixed(show_commas=True),
            ...     t.fixed(show_units=False), sep=newline)
            $1000000
            $1,000,000
            1000000

            >>> print(
            ...     t.fixed(prec=2, strip_zeros=False, show_commas=True),
            ...     t.fixed(prec=6),
            ...     t.fixed(strip_zeros=False, prec=6), sep=newline)
            $1,000,000.00
            $1000000
            $1000000.000000

            >>> print(
            ...     t.fixed(strip_zeros=False, prec='full'),
            ...     t.fixed(show_label=True),
            ...     t.fixed(show_label='f'), sep=newline)
            $1000000.000000000000
            Total = $1000000
            Total = $1000000 — the total

            >>> print(
            ...     t.fixed(scale=(1/10000, 'BTC')),
            ...     t.fixed(scale=(1/1000, 'ETH')),
            ...     t.fixed(scale=(1/1000, 'ETH'), show_units=False), sep=newline)
            100 BTC
            1000 ETH
            1000

        """
        # initialize various options
        show_units = self.show_units if show_units is None else show_units
        show_commas = self.show_commas if show_commas is None else show_commas
        strip_zeros = self.strip_zeros if strip_zeros is None else strip_zeros
        strip_radix = self.strip_radix if strip_radix is None else strip_radix
        units = self.units if show_units else ''
        if prec is None:
            prec = self.prec

        # check for infinities or NaN
        value = self.is_infinite() or self.is_nan()
        if value:
            value = self._combine(value, '', units, ' ')
            return self._label(value, show_label)

        # handle fixed point formatting
        if prec == 'full':
            prec = self.full_prec
        if scale or isinstance(scale, numbers.Number):
            number, units = _scale(scale, float(self), self.units)
            units = units if show_units else ''
        else:
            number = float(self)
        comma = ',' if show_commas else ''
        mantissa = '{0:{1}.{2}f}'.format(number, comma, prec)
        if '.' in mantissa and strip_zeros:
            mantissa = mantissa.rstrip('0')
        if strip_radix:
            mantissa = mantissa.rstrip('.')
        else:
            if '.' not in mantissa:
                mantissa += '.'
        value = self._combine(mantissa, '', units, self.spacer)
        return self._label(value, show_label)

    # binary() {{{2
    def binary(
        self, show_units=None, prec=None, show_label=None,
        strip_zeros=None, strip_radix=None, scale=None,
    ):
        """Convert quantity to string using binary scale factors.

        When in range the number is divided by some integer power of 1024 and
        the appropriate scale factor is added to the quotient, where the scale
        factors are '' for 0 powers of 1024, 'Ki' for 1, 'Mi' for 2, 'Gi' for 3,
        'Ti' for 4, 'Pi' for 5, 'Ei' for 6, 'Zi' for 7 and 'Yi for 8.  Outside
        this range, the number is converted to a string using a simple floating
        point format.

        Within the range the number of significant figures used is equal to
        prec+1.  Outside the range, prec give the number of figures to the right
        of the decimal point.

        :arg bool show_units:
            Whether the units should be included in the string.

        :arg prec:
            The desired precision (number of digits to the right of the radix
            when normalized).  If specified as 'full', *full_prec* is used as
            the number of digits (and not the originally specified precision as
            with render).
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

        :arg strip_zeros:
            Remove contiguous zeros from end of fractional part. If not
            specified, the global *strip_zeros* setting is used.
        :type strip_zeros: boolean

        :arg strip_radix:
            Remove radix if there is nothing to the right of it.  If not
            specified, the global *strip_radix* setting is used.
        :type strip_radix: boolean

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
        :type scale: real, pair, function, or string

        :raises UnknownConversion(QuantiPhyError, KeyError):
            A unit conversion was requested and there is no corresponding unit
            converter.

        :raises UnknownFormatKey(QuantiPhyError, KeyError):
            'label_fmt' or 'label_fmt_full' contains an unknown format key.

        Example::

            >>> t = Quantity('mem = 16 GiB — amount of physical memory', binary=True)
            >>> print(
            ...     t.binary(),
            ...     t.binary(prec=3, strip_zeros=False),
            ...     t.binary(show_label=True, scale='b'), sep=newline)
            16 GiB
            16.00 GiB
            mem = 128 Gib

        """
        # initialize various options
        show_units = self.show_units if show_units is None else show_units
        strip_zeros = self.strip_zeros if strip_zeros is None else strip_zeros
        strip_radix = self.strip_radix if strip_radix is None else strip_radix
        units = self.units if show_units else ''
        if prec is None:
            prec = self.prec
        elif prec == 'full':
            prec = self.full_prec

        # check for infinities or NaN
        value = self.is_infinite() or self.is_nan()
        if value:
            value = self._combine(value, '', units, ' ')
            return self._label(value, show_label)

        # handle scaling
        if scale or isinstance(scale, numbers.Number):
            number, units = _scale(scale, float(self), self.units)
            units = units if show_units else ''
        else:
            number = float(self)

        # format the number with binary scale factors if appropriate
        try:
            from math import log
            base = log(abs(number), 2)//10
            if base < 0:
                raise IndexError
            sf = ('_KMGTPEZY'[int(base)] + 'i')
            sf = sf.replace('_i', self.unity_sf)
            num = '{number:0.{prec}e}'.format(
                number=(number / (2**(10*base))), prec=prec
            )
            # this occasionally rounds up to 1024
            # this can result in 1024 MiB rather than 1 GiB
            mantissa, exp = num.split('e')
            exp = int(exp)
            mantissa += '.'
            whole, frac = mantissa.split('.')[0:2]
            frac += (exp - prec)*'0'
            mantissa = whole + frac[0:exp] + '.' + frac[exp:]
            sf_is_exp = False

        # cannot use binary scale factors, just use float format
        except (IndexError, ValueError):
            num = '{number:0.{prec}f}'.format(number=number, prec=prec)
            if 'e' in num:  # pragma: no cover
                mantissa, exp = num.split('e')
                sf = 'e' + exp
                sf_is_exp = True
            else:
                mantissa = num
                sf = ''
                sf_is_exp = False

        # strip excess digits and radix
        if '.' not in mantissa:
            mantissa += '.'
        if strip_zeros:
            mantissa = mantissa.rstrip('0')
        if strip_radix or (sf and sf_is_exp):
            mantissa = mantissa.rstrip('.')
        value = self._combine(mantissa, sf, units, self.spacer, sf_is_exp)
        return self._label(value, show_label)

    # is_close() {{{2
    def is_close(self, other, reltol=None, abstol=None, check_units=True):
        """
        Are values equivalent?

        Indicates  whether the value of a quantity or real number is equivalent
        to that of a quantity. The two values need not be identical, they just
        need to be close to be deemed equivalent.

        :arg other:
            The value to compare against.
        :type other: quantity, real, or string

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
            ...     c.is_close('299.7925 Mm/s'),       # should pass, is close
            ... )
            True True False True False True

        """
        if isinstance(other, str):
            other = self.__class__(other)

        if check_units:
            other_units = getattr(other, 'units', None)
            if other_units:
                my_units = getattr(self, 'units', None)
                if my_units != other_units:
                    return False
        reltol = self.reltol if reltol is None else reltol
        abstol = self.abstol if abstol is None else abstol
        return math.isclose(
            self.real, float(other), rel_tol=reltol, abs_tol=abstol
        )

    # __str__() {{{2
    def __str__(self):
        return self.render()

    # __repr__() {{{2
    def __repr__(self):
        form = 'eng' if self.ignore_sf else 'si'
        return 'Quantity({!r})'.format(
            self.render(form=form, show_units=True, prec='full', negligible=-1)
        )

    # format() {{{2
    def format(self, template=''):
        """Convert quantity to string under the guidance of a template.

        Supports the normal floating point and string format types as well some
        new ones. If the format code is given in upper case, *label_fmt* is used
        to add the name and perhaps description to the result.

        :arg str template: the format string.

        :raises UnknownFormatKey(QuantiPhyError, KeyError):
            'label_fmt' or 'label_fmt_full' contains an unknown format key.

        :raises UnknownConversion(QuantiPhyError, KeyError):
            A unit conversion was requested and there is no corresponding unit
            converter.


        The format is specified using A#W,.PTU where::

           A   is a character and gives the alignment: either '', '>', '<', or '^'
           #   is a literal hash that if present indicates that
               trailing zeros and radix should not be suppressed from fractional part.
           W   is an integer and gives the width of the final string
           ,   is a literal comma, it indicates that the whole part of the
               mantissa should be partitioned into groups of three digits
               separated by commas
           .P  is a literal period followed by an integer that gives the precision
           T   is a character and gives the type: choose from p, q, r, s, e, f, g, u, n, d, ...
           U   is a string that must match a known unit, it invokes scaling

        Each of these component pieces is optional.

        If::

           q = Quantity('f = 1420.405751786 MHz — hydrogen line')

        then::

           q: quantity [si=y, units=y, label=n] (ex: 1.4204 GHz)
           Q: quantity [si=y, units=y, label=y] (ex: f = 1.4204 GHz)
           r: real [si=y, units=n, label=n] (ex: 1.4204G)
           R: real [si=y, units=n, label=y] (ex: f = 1.4204G)
            : [label=n] (ex: 1.4204 GHz)
           p: fixed-point [fixed=y, units=y, label=n] (ex: 1420405751.7860 Hz)
           P: fixed-point [fixed=y, units=y, label=y] (ex: f = 1420405751.7860 Hz)
           s: string [label=n] (ex: 1.4204 GHz)
           S: string [label=y] (ex: f = 1.4204 GHz)
           e: exponential form [si=n, units=n, label=n] (ex: 1.4204e9)
           E: exponential form [si=n, units=n, label=y] (ex: f = 1.4204e9)
           f: float [label=n] (ex: 1420400000.0000)
           F: float [label=y] (ex: f = 1420400000.0000)
           g: generalized float [label=n] (ex: 1.4204e+09)
           G: generalized float [label=y] (ex: f = 1.4204e+09)
           u: units only (ex: Hz)
           n: name only (ex: f)
           d: description only (ex: hydrogen line)

        """
        match = FORMAT_SPEC.match(template)
        if match:
            align, alt_form, width, comma, prec, ftype, units = match.groups()
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
                return '{0:{1}{2}s}'.format(value, align, width)
            label = ftype.isupper()
            ftype = ftype.lower()
            if ftype in 's':  # note that ftype = '' matches this case
                label = label if ftype else None
                value = self.render(prec=prec, show_label=label, scale=scale)
            elif ftype == 'q':
                value = self.render(
                    form='si', prec=prec, show_units=True, show_label=label,
                    strip_zeros=not alt_form, strip_radix=not alt_form, scale=scale
                )
            elif ftype == 'r':
                value = self.render(
                    form='si', prec=prec, show_units=False, show_label=label,
                    strip_zeros=not alt_form, strip_radix=not alt_form, scale=scale
                )
            elif ftype == 'p':
                value = self.fixed(
                    prec=prec, show_units=True, show_label=label,
                    show_commas=bool(comma), strip_zeros=not alt_form,
                    strip_radix=not alt_form, scale=scale
                )
            elif ftype == 'b':
                value = self.binary(
                    prec=prec, show_units=True, show_label=label,
                    strip_zeros=not alt_form, strip_radix=not alt_form,
                    scale=scale
                )
            else:
                if prec is None:
                    prec = self.prec
                if prec == 'full':
                    prec = self.full_prec
                if ftype == 'g':
                    prec += 1
                if scale:
                    # a hack that includes the scaling
                    value = float(self.render(
                        form='eng', prec='full', show_units=False,
                        show_label=False, scale=scale
                    ))
                else:
                    value = float(self)
                value = '{0:{1}.{2}{3}}'.format(value, comma, prec, ftype)
                value = self._map_leading_sign(value)
                value = self._map_sign(value)
                width = width.lstrip('0')
                    # format function treats 0 as a padding rather than a width
                if self.strip_zeros:
                    if 'e' in value:
                        mantissa, exponent = value.split('e')
                        if '.' in mantissa:
                            mantissa = mantissa.rstrip('0').rstrip('.')
                        value = mantissa + 'e' + exponent
                    elif '.' in value:
                        value = value.rstrip('0').rstrip('.')
                if label:
                    value = self._label(value, True)
            if not align:
                align = '>'  # in python numbers are right-aligned
            return '{0:{1}{2}s}'.format(value, align, width)

        # Not a valid Quantiphy format specifier, so pass it on to float
        return '{0:{1}}'.format(self.real, template)

    __format__ = format

    # extract() {{{2
    @classmethod
    def extract(cls, text, predefined=None, **kwargs):
        r"""Extract quantities.

        Takes a string that contains quantity definitions, one per line, and
        returns those quantities in a dictionary.

        :arg str text:
            The string that contains the quantities, one definition per
            line.  Each is parsed by *assign_rec*. By default, the lines are
            assumed to be of the form::

                [<name> [(<qname>)] = <value>] [— <description>]

            where '=' may be replaced by ':' and '—' (the em-dash) may be
            replaced by '--', '//' or '#'.  In addition, brackets delimit
            optional fields and parentheses represent literal parentheses.  Each
            of the fields are allowed be largely arbitrary strings.

            The brackets indicate that the name/value pair and the description
            is optional.  However, <name> must be given if <value> is given.

            <name>:
                the name is used as a key for the value.

            <qname>:
                the name taken by the quantity.

            <value>:
                A number with optional units (ex: 3 or 1pF or 1 kΩ);
                the units need not be a simple identifier (ex: 9.07 GHz/V).

                The value may also be an expression.  When giving an expression,
                you may follow it with a string surrounded by double quotes,
                which is taken as the units.  For example: Tstop = 5/Fin "s".
                The expressions may only contain value defined previously in the
                same set of definitions, values contained in *predefined*,
                physical constants, the mathematical constants pi and tau
                (2*pi), which may be named π or τ, or number literals without
                scale factors or units. The units should not include a scale
                factor.

                When processing the value, it is passed as an argument to
                Quantity, if cannot be converted to a quantity, then it is
                treated as a Python expression.

            <description>:
                Optional textual description (ex: Frequency of hydrogen line).

            Blank lines and any line that does not contain a value are ignored.
            So with the default *assign_rec*, lines with the following form are
            ignored::

                — comment
                -- comment
                # comment
                // comment

        :arg dict predefined:
            A dictionary of predefined values. When specified, these values
            become available to be used in the expressions that give values to
            the values being defined.  You can use *locals()* as this argument
            to make all local variables available.

            You can specify both values and functions. For example,
            ``predefined=dict(sqrt=sqrt)`` allows ``sqrt`` to be
            used in expressions.

        :arg \**kwargs:
            Any argument that can be passed to Quantity can be passed to this
            function, and are in turn passed to Quantity as the quantities are
            created.  This can be used, for example, to allow the binary scale
            factors.

        :returns:
            a dictionary of quantities for the values specified in the argument.
        :rtype: dict

        Example::

            >>> sagan_frequencies = r'''
            ...     — Carl Sagan's SETI frequencies of high interest
            ...
            ...     f_hy = 1420.405751786 MHz — Hydrogen line frequency
            ...     f_sagan1 = π*f_hy "Hz" — Sagan's first frequency
            ...     f_sagan2 = τ*f_hy "Hz" — Sagan's second frequency
            ... '''
            >>> freqs = Quantity.extract(sagan_frequencies)
            >>> for f in freqs.values():
            ...     print(f.render(show_label='f'))
            f_hy = 1.4204 GHz — Hydrogen line frequency
            f_sagan1 = 4.4623 GHz — Sagan's first frequency
            f_sagan2 = 8.9247 GHz — Sagan's second frequency

            >>> globals().update(freqs)
            >>> print(f_hy, f_sagan1, f_sagan2, sep=newline)
            1.4204 GHz
            4.4623 GHz
            8.9247 GHz

        """
        def _is_quoted(s):
            return (s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")

        if not predefined:
            predefined = {}
        quantities = {}
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            match = re.match(cls.get_pref('assign_rec'), line, re.VERBOSE)
            if match:
                args = match.groupdict()
                name = args.get('name', '')
                qname = args.get('qname', '')
                qname = name if not qname else qname
                value = args['val']
                desc = args.get('desc', '')
                if not name or not value:
                    continue
                name = name.strip()
                try:
                    quantity = cls(value, name=qname, desc=desc, **kwargs)
                except InvalidNumber:

                    # extract the units if given (they are embedded in "")
                    components = value.split()
                    if len(components) >= 2 and _is_quoted(components[-1]):
                        units = components[-1][1:-1]
                        value = ' '.join(components[:-1])
                    else:
                        units = ''

                    # evaluate value as expression
                    symbols = ChainMap(
                        quantities, predefined, _active_constants, CONSTANTS
                    )
                    try:
                        value = eval(value, None, symbols)
                        quantity = cls(value, units=units, name=qname, desc=desc)
                    except InvalidNumber:
                        # not suitable to be a quantity, so just save value
                        quantity = value
                    except SyntaxError:
                        continue
                quantities[name] = quantity
        return quantities

    # map_sf_to_sci_notation() {{{2
    _SCI_NOTATION_MAPPER = {
        ord('e'): '×10',
        ord('+'): '',
        ord('＋'): '',
        ord('-'): '⁻',
        ord('−'): '⁻',
        ord('0'): '⁰',
        ord('1'): '¹',
        ord('2'): '²',
        ord('3'): '³',
        ord('4'): '⁴',
        ord('5'): '⁵',
        ord('6'): '⁶',
        ord('7'): '⁷',
        ord('8'): '⁸',
        ord('9'): '⁹',
        ord('u'): 'µ',
    }

    @staticmethod
    def map_sf_to_sci_notation(sf):
        """Render scale factors in scientific notation.

        Pass this function to *map_sf* preference if you prefer your large and
        small numbers in classic scientific notation. It also causes 'u' to be
        converted to 'µ'. Set *form* to 'eng' to format all numbers in
        scientific notation.

        Example::

            >>> with Quantity.prefs(map_sf=Quantity.map_sf_to_sci_notation, show_label='f'):
            ...     print(
            ...         Quantity('k').render(),
            ...         Quantity('mu0').render(),
            ...         Quantity('mu0').render(form='eng'),
            ...         sep=newline,
            ...     )
            k = 13.806×10⁻²⁴ J/K — Boltzmann's constant
            µ₀ = 1.2566 µH/m — permeability of free space
            µ₀ = 1.2566×10⁻⁶ H/m — permeability of free space

        """
        mapped = sf.translate(Quantity._SCI_NOTATION_MAPPER)
        return mapped, '×' in mapped

    # map_sf_to_greek() {{{2
    @staticmethod
    def map_sf_to_greek(sf):
        """Render scale factors in Greek alphabet if appropriate.

        Pass this dictionary to *map_sf* preference if you prefer µ rather than u.

        Example::

            >>> with Quantity.prefs(map_sf=Quantity.map_sf_to_greek):
            ...     print(Quantity('mu0').render(show_label='f'))
            µ₀ = 1.2566 µH/m — permeability of free space

        """
        # this could just as easily be a simple dictionary, but implement it as
        # a function so that it supports a docstring.
        return {'u': 'µ'}.get(sf, sf)

    # all_from_conv_fmt {{{2
    @classmethod
    def all_from_conv_fmt(cls, text, only_e_notation=False, **kwargs):
        r"""Convert all numbers and quantities from conventional notation.

        Only supports a subset of the conventional formats that *QuantiPhy*
        normally accepts.  For example, leading units (ex. $1M) and embedded
        commas are not supported, and the radix is always '.'.

        There may be a space between the number an units, but it cannot be a
        normal space. Only non-breaking, thin-non-breakn and thin spaces are
        allowed.

        :arg str text:
            A search and replace is performed on this text. The search looks for
            numbers and quantities in floating point or e-notation. They are
            replaced with the same number rendered as a quantity. To be
            recognized any units must be simple (only letters or underscores, no
            digits or symbols) and the units must be immediately adjacent to the
            number.
        :arg bool only_e_notation:
            If true, only numbers that explicitly have exponents are converted
            (1e6Hz is converted, but not 1.6 or 2009).  If False, numbers with
            or without exponents are converted ( 1e6Hz, 1.6 and 2009 are all
            converted.
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
        if only_e_notation:
            regex = cls.embedded_e_notation_only
        else:
            regex = cls.embedded_e_notation
        for match in regex.finditer(text):
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
        r"""Convert all numbers and quantities from SI notation.

        Only supports a subset of the SI formats that *QuantiPhy* normally
        accepts.  For example, leading units (ex. $1M) and embedded commas
        are not supported, and the radix is always '.'.

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

            >>> print(Quantity.all_from_si_fmt(xlated, form='eng'))
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
# Where appropriate, these are the 2018 CODATA values from
# physics.nist.gov/constants.
add_constant(
    Quantity(
        '6.62607015e-34',
        units='J-s',
        name='h',
        desc="Plank's constant"
    ),
    unit_systems='mks'
)
add_constant(
    Quantity(
        '6.62607015e-27',
        units='erg-s',
        name='h',
        desc="Plank's constant"
    ),
    unit_systems='cgs'
)

# Reduced Plank's constant {{{2
add_constant(
    Quantity(
        '1.054571817e-34',
        units='J-s',
        name='ħ',
        desc="reduced Plank's constant"
    ),
    alias='hbar',
    unit_systems='mks'
)
add_constant(
    Quantity(
        '1.054571817e-27',
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
        '1.380649e-23',
        units='J/K',
        name='k',
        desc="Boltzmann's constant"
    ),
    unit_systems='mks'
)
add_constant(
    Quantity(
        '1.380649e-16',
        units='erg/K',
        name='k',
        desc="Boltzmann's constant"
    ),
    unit_systems='cgs'
)

# Elementary charge {{{2
add_constant(
    Quantity(
        '1.602176634e-19',
        units='C',
        name='q',
        desc="elementary charge"
    ),
    unit_systems='mks'
)
add_constant(
    Quantity(
        '4.80320471257e-10',
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
        desc="zero degrees Celsius"
    ),
    alias='0C',
    unit_systems='mks cgs'
)

# Permittivity of free space {{{2
add_constant(
    Quantity(
        '8.8541878128e-12',
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
        1.25663706212e-6,
        units='H/m',
        name='µ₀',
        desc="permeability of free space"
    ),
    alias=['mu0', 'μ₀'],
    unit_systems='mks'
)

# Characteristic impedance of free space {{{2
add_constant(
    Quantity(
        '376.730313668',
        units='Ohms',
        name='Z₀',
        desc="characteristic impedance of free space"
    ),
    alias='Z0',
    unit_systems='mks'
)


# Unit Conversions {{{1
_unit_conversions = {}


# _convert_units() {{{2
def _convert_units(to_units, from_units, value):
    # not intended to be used by the user; if you want this functionality,
    # simply use: Quantity(value, from_units).scale(to_units).

    if to_units == from_units:
        return value
    try:
        return _unit_conversions[(to_units, from_units)](value)
    except KeyError:
        raise UnknownConversion(to_units, from_units)


# UnitConversion class {{{2
class UnitConversion(object):
    """
    Creates a unit converter.

    Just the creation of the converter is sufficient to make it available to
    :class:`Quantity` (the :class:`UnitConversion` object itself is normally
    discarded). Once created, it is automatically employed by :class:`Quantity`
    when a conversion is requested with the given units. A forward conversion is
    performed if the from and to units match, and a reversion conversion is
    performed if they are swapped. A no-op conversion is performed when
    converting one from-unit to another or from one to-unit to another.

    :arg to_units:
        A collection of units. If given as a single string it is split.
        May also be a subclass of :class:`Quantity` if units are defined.
    :type to_units: string or list of strings

    :arg from_units:
        A collection of units. If given as a single string it is split.
        May also be a subclass of :class:`Quantity` if units are defined.
    :type from_units: string or list of strings

    :arg float slope:
        Scale factor for conversion.  You may also pass a function as an
        argument, in which case it is used to perform forward conversions.
        In this case, *intercept* should also be passed a callable.

    :arg float intercept:
        Conversion offset.  You may also pass a function as an argument, in
        which case it is used to perform reverse conversions.  In this case,
        *slope* should also be passed a callable.

    **Forward Conversion**:
    The following conversion is applied if the given units are among the
    *from_units* and the desired units are among the *to_units*:

        *new_value* = *given_value* * *slope* + *intercept*

    Or, if *slope* is callable:

        *new_value* = *slope* (*given_value*)

    In this case the name *slope* is misleading.

    **Reverse Conversion**:
    The following conversion is applied if the given units are among
    the *to_units* and the desired units are among the *from_units*:

        *new_value* = (*given_value* - *intercept*)/*slope*

    Or, if *intercept* is callable:

        *new_value* = *intercept* (*given_value*)

    In this case the name *intercept* is misleading.

    **No-Op Conversion**:
    The following conversion is applied if the given and desired units are both
    found among the from-units or are both found among the to-units.

        *new_value* = *given_value*

    Example::

        >>> from quantiphy import Quantity, UnitConversion
        >>> m2pc = UnitConversion('m', 'pc parsec', 3.0857e16)

    Normally one simply discards the return value of UnitConversion, but if kept
    you can convert it to a string to get a summary of the conversion::

        >>> print(str(m2pc))
        m ← 3.0857e+16*pc

    The act of creating this unit conversion establishes a conversion between
    meters (m) and parsecs (parsec, pc) that is accessible when creating or
    rendering quantities and can go both ways::

        >>> d_sol = Quantity('5 μpc', scale='m')  # forward conversion
        >>> print(d_sol)
        154.28 Gm

        >>> d_ac = Quantity(1.339848, units='pc') # reverse conversion
        >>> print(d_ac.render(scale='m'))
        41.344e15 m

        >>> d_ac = Quantity(1.339848, units='pc') # no-op conversion
        >>> print(f'{d_ac:qparsec}')
        1.3398 parsec

    The conversion can employ both a slope and an intercept, and if you convert
    the converter object to a string, it summarizes the conversion, which can
    help you avoid mistakes::

        >>> conversion = UnitConversion('F', 'C', 1.8, 32)
        >>> print(str(conversion))
        F ← 1.8*C + 32

    You can also use functions to perform the conversions, which is appropriate
    when the conversion is nonlinear (cannot be described with a slope and
    intercept).  For example::

        >>> from quantiphy import UnitConversion, Quantity
        >>> from math import log10

        >>> def from_dB(value):
        ...     return 10**(value/20)

        >>> def to_dB(value):
        ...     return 20*log10(value)

        >>> converter = UnitConversion('V', 'dBV', from_dB, to_dB)
        >>> print(str(converter))
        V ← from_dB(dBV), dBV ← to_dB(V)

        >>> converter = UnitConversion('A', 'dBA', from_dB, to_dB)
        >>> print(str(converter))
        A ← from_dB(dBA), dBA ← to_dB(A)

        >>> print('{:pdBV}, {:pdBV}'.format(Quantity('100mV'), Quantity('10V')))
        -20 dBV, 20 dBV

        >>> print('{:qV}, {:qV}'.format(Quantity('-20 dBV'), Quantity('20 dBV')))
        100 mV, 10 V

        >>> print('{:pdBA}, {:pdBA}'.format(Quantity('100mA'), Quantity('10A')))
        -20 dBA, 20 dBA

        >>> print('{:qA}, {:qA}'.format(Quantity('-20 dBA'), Quantity('20 dBA')))
        100 mA, 10 A

    """

    # constructor {{{3
    def __init__(self, to_units, from_units, slope=1, intercept=0):
        # convert units to lists
        # allow units to be a subclasss of Quantity that has units
        try:
            if issubclass(to_units, Quantity):
                self.to_units = [to_units.units]
        except TypeError:
            self.to_units = to_units.split() if isinstance(to_units, str) else to_units

        try:
            if issubclass(from_units, Quantity):
                self.from_units = [from_units.units]
        except TypeError:
            self.from_units = from_units.split() if isinstance(from_units, str) else from_units

        # convert units to lists and save values
        self.slope = slope
        self.intercept = intercept

        if callable(slope) or callable(intercept):
            # the slope and intercept arguments are actually the forward and
            # reverse conversion functions.
            _forward = slope
            _reverse = intercept
        else:
            _forward = self._forward
            _reverse = self._reverse

        # add to known unit conversion
        for to in self.to_units:
            for frm in self.from_units:
                _unit_conversions[(to, frm)] = _forward
                _unit_conversions[(frm, to)] = _reverse

        # add no-op converters to allow a from-units to be converted to another
        for u1 in self.from_units:
            for u2 in self.from_units:
                if u1 != u2:
                    _unit_conversions[(u1, u2)] = self._no_op

        # add no-op converters to allow a to-units to be converted to another
        for u1 in self.to_units:
            for u2 in self.to_units:
                if u1 != u2:
                    _unit_conversions[(u1, u2)] = self._no_op

    # forward conversion {{{3
    def _forward(self, value):
        return value*self.slope + self.intercept

    # reverse conversion {{{3
    def _reverse(self, value):
        return (value - self.intercept)/self.slope

    # no conversion {{{3
    def _no_op(self, value):
        return value

    # convert {{{3
    def convert(self, value=1, from_units=None, to_units=None):
        """Convert value to quantity with new units.

        A convenience method. Normally it is not needed because once created, a
        unit conversion becomes directly accessible to quantities and can be
        used both when creating or rendering the quantity.

        :arg value:
            The value to convert. May be a real number or a quantity.
            Alternately, may simply be a string, in which case it is taken to be
            the from_units. If the value is not given it is taken to be 1.
        :type arg: real or string or Quantity

        :arg str from_units:
            The units to convert from.
            If not given, the class's first from_units are used.

        :arg str to_units:
            The units to convert to.
            If not given, the class's first to_units are used.

        If the from_units were found among the class's from_units, and the
        to_units were found among the class's to_units, then a forward
        conversion is performed.

        If the from_units were found among the class's to_units, and the
        to_units were found among the class's from_units, then a reverse
        conversion is performed.

        :raises UnknownConversion(QuantiPhyError, KeyError):
            The given units are not supported by the underlying class.

        Example::

            >>> print(str(m2pc))
            m ← 3.0857e+16*pc

            >>> m = m2pc.convert()
            >>> print(str(m))
            30.857e15 m

            >>> pc = m2pc.convert(m)
            >>> print(str(pc))
            1 pc

            >>> m = m2pc.convert(pc)
            >>> print(str(m))
            30.857e15 m

            >>> m2pc.convert(30.857e15, 'm')
            Quantity('1 pc')

            >>> m2pc.convert(1000, 'pc')
            Quantity('30.857e18 m')

            >>> m2pc.convert('pc')
            Quantity('30.857e15 m')

        """
        if isinstance(value, str):
            if not from_units:
                from_units = value
            value = 1
        if from_units is None:
            try:
                from_units = value.units
            except AttributeError:
                pass

        if callable(self.slope) or callable(self.intercept):
            # the slope and intercept arguments are actually the forward and
            # reverse conversion functions.
            _forward = self.slope
            _reverse = self.intercept
        else:
            _forward = self._forward
            _reverse = self._reverse

        if to_units in self.to_units:
            return Quantity(_forward(value), to_units)
        if to_units in self.from_units:
            return Quantity(_reverse(value), to_units)
        if not from_units:
            return Quantity(_forward(value), self.to_units[0])
        if from_units in self.from_units:
            return Quantity(_forward(value), self.to_units[0])
        if from_units in self.to_units:
            return Quantity(_reverse(value), self.from_units[0])
        if to_units:
            raise UnknownConversion(to_units, direction='to')
        raise UnknownConversion(from_units, direction='from')

    # __str__ {{{3
    def __str__(self):
        if callable(self.slope) or callable(self.intercept):
            # using functions to do the conversion, have no good description
            return '{} ← {}({}), {} ← {}({})'.format(
                self.to_units[0], self.slope.__name__, self.from_units[0],
                self.from_units[0], self.intercept.__name__, self.to_units[0]
            )
        if self.intercept:
            return '{} ← {}*{} + {}'.format(
                self.to_units[0], self.slope, self.from_units[0],
                Quantity(self.intercept, self.to_units[0]).render(show_units=False)
            )
        return '{} ← {}*{}'.format(
            self.to_units[0], self.slope, self.from_units[0]
        )


# Temperature conversions {{{2
UnitConversion('C °C', 'C °C')
UnitConversion('C °C', 'K', 1, -273.15)
UnitConversion('C °C', 'F °F', 5/9, -32*5/9)
UnitConversion('C °C', 'R °R', 5/9, -273.15)
# UnitConversion('K', 'C °C', 1, 273.15) — redundant
UnitConversion('K', 'F °F', 5/9, 273.15 - 32*5/9)
UnitConversion('K', 'R °R', 5/9, 0)

# Length/Distance conversions {{{2
UnitConversion('m', 'km', 1000)
UnitConversion('m', 'cm', 1/100)
UnitConversion('m', 'mm', 1/1000)
UnitConversion('m', 'um µm μm micron', 1/1000000)
UnitConversion('m', 'nm', 1/1000000000)
UnitConversion('m', 'Å angstrom', 1/10000000000)
UnitConversion('m', 'mi mile miles', 1609.344)
UnitConversion('m', 'ft feet', 0.3048)
UnitConversion('m', 'in inch inches', 0.0254)

# Mass conversions {{{2
UnitConversion('g', 'lb lbs', 453.59237)
UnitConversion('g', 'oz', 28.34952)

# Time conversions {{{2
UnitConversion('s', 'sec second seconds')
UnitConversion('s', 'min minute minutes', 60)
UnitConversion('s', 'hr hour hours', 3600)
UnitConversion('s', 'day days', 86400)

# Bit conversions {{{2
UnitConversion('b', 'B', 8)
