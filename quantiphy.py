# encoding: utf8
'''
QuantiPhy: Support for Physical Quantities

Utilities for converting to and from physical quantities (numbers with units).
'''

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
import re
import math

# Parameters {{{1
DEFAULTS = {
    'si': True,
        # use si scale factors
    'units': True,
        # output units
    'prec': 4,
        # normal precision
    'full_prec': 12,
        # full precision
    'spacer': '',
        # spacer between number and units
    'unity_sf': '',
        # what to use as unity scale factor, generally '' or '_'
    'output_sf': 'TGMkmunpfa',
        # the scale factors that should be used when formatting numbers
    'ignore_sf': False,
        # assume quantity does not employ scale factor when converting from string
    'fmt': False,
        # cause render to add name and description by default if given
    'assign_fmt': '{n} = {v}',
        # assignment formatter
        # use {n}, {v}, and {d} to access name, value, and description
        # if two are given as tuple, first is used if desc is present, otherwise
        # second is used. For example, an alternate specification that prints
        # the description if it is available is:
        #     'assign_fmt': ('{n} = {v} -- {d}', '{n} = {v}'),
    'assign_rec': r'\A\s*(?:(\w+)\s*=\s*)?(.*?)(?:\s*--\s*(.*?)\s*)?\Z',
        # assignment recognizer
    'keep_components': True,
        # keep string components
    'reltol': 1e-6,
        # relative tolerance
    'abstol': 1e-12,
        # absolute tolerance
}
CURRENCY_SYMBOLS = '$'
CONSTANTS = {
    # value may be given as real number or string. If given as a string then the
    # number of significant figures is used as the full precision.
    'h':    ('6.62606957e-34',  'J-s',  'h',   "Plank's constant"),
    'hbar': (6.62606957e-34/(2*math.pi),
                                'J-s',  'ħ',   "reduced Plank's constant"),
    'k':    ('1.3806488e-23',   'J/K',  'k',   "Boltzmann's constant"),
    'q':    ('1.602176565e-19', 'C',    'q',   "Elementary charge"),
    'c':    ('2.99792458e8',    'm/s',  'c',   "Speed of light"),
    'C0':   ('273.15',          'K',    '0°C', "Zero degrees Celsius in Kelvin"),
    'eps0': ('8.854187817e-12', 'F/m',  'ε₀',  "Permittivity of free space"),
    'mu0':  (4e-7*math.pi,      'H/m',  'μ₀',  "Permeability of free space"),
    'Z0':   ('376.730313461',   'Ohms', 'Z₀',  "Characteristic impedance of free space"),
}


# Constants {{{1
__version__ = '0.2.0'
__released__ = '2016-10-23'

# These mappings are only used when reading numbers
MAPPINGS = {
    'Y': ('e24',  1e24 ),
    'Z': ('e21',  1e21 ),
    'E': ('e18',  1e18 ),
    'P': ('e15',  1e15 ),
    'T': ('e12',  1e12 ),
    'G': ('e9',   1e9  ),
    'M': ('e6',   1e6  ),
    'K': ('e3',   1e3  ),
    'k': ('e3',   1e3  ),
    '_': ('',     1    ),
    '' : ('',     1    ),
    'c': ('e-2',  1e-2 ),  # only available for input, not used in output
    '%': ('e-2',  1e-2 ),  # only available for input, not used in output
    'm': ('e-3',  1e-3 ),
    'u': ('e-6',  1e-6 ),
    'n': ('e-9',  1e-9 ),
    'p': ('e-12', 1e-12),
    'f': ('e-15', 1e-15),
    'a': ('e-18', 1e-18),
    'z': ('e-21', 1e-21),
    'y': ('e-24', 1e-24),
}

# These mappings are only used when writing numbers
BIG_SCALE_FACTORS = 'kMGTPEZY'
    # These must be given in order, one for every three decades.
    # Use k rather than K, because K looks like a temperature when used alone.

SMALL_SCALE_FACTORS = 'munpfazy'
    # These must be given in order, one for every three decades.

# Regular expression for recognizing and decomposing string .format method codes
FORMAT_SPEC = re.compile(r'\A([<>]?)(\d*)(?:\.(\d+))?([qQrRusSeEfFgGdn]?)\Z')

# Pattern Definitions {{{1
# Build regular expressions used to recognize quantities
def named_regex(name, regex):
    return '(?P<%s>%s)' % (name, regex)

# components {{{2
sign = named_regex('sign', '[-+]?')
mantissa = named_regex('mant', r'[0-9]*\.?[0-9]+')
exponent = named_regex('exp', '[eE][-+]?[0-9]+')
scale_factor = named_regex('sf', '[%s]' % ''.join(MAPPINGS))
units = named_regex('units', r'(?:[a-zA-Z][-^/()\w]*)?')
    # examples: Ohms, V/A, J-s, m/s^2, H/(m-s)
    # leading char must be letter to avoid 1.0E-9s -> ('1.0e18', '-9s')
smpl_units = named_regex('units', r'(?:[a-zA-Z_]*)')
    # may only contain alphabetic characters, ex: V, A, Ohms, etc.
currency = named_regex('currency', '[%s]' % CURRENCY_SYMBOLS)
nan = named_regex('nan', '(?i)inf|nan')
left_delimit = r'(?:\A|(?<=[^a-zA-Z0-9_.]))'
right_delimit = r'(?=[^-+0-9_]|\Z)'

# number_with_scale_factor {{{2
number_with_scale_factor = (
    r'{sign}{mantissa}\s*{scale_factor}{units}'.format(**locals()),
    lambda match: match.group('sign') + match.group('mant'),
    lambda match: match.group('sf'),
    lambda match: match.group('units')
)

# number_with_exponent {{{2
number_with_exponent = (
    r'{sign}{mantissa}{exponent}\s*{units}'.format(**locals()),
    lambda match: match.group('sign') + match.group('mant'),
    lambda match: match.group('exp').lower(),
    lambda match: match.group('units')
)

# simple_number {{{2
# this one must be processed after number_with_scale_factor
simple_number = (
    r'{sign}{mantissa}\s*{units}'.format(**locals()),
    lambda match: match.group('sign') + match.group('mant'),
    lambda match: '',
    lambda match: match.group('units')
)

# currency_with_scale_factor {{{2
currency_with_scale_factor = (
    r'{sign}{currency}{mantissa}\s*{scale_factor}'.format(**locals()),
    lambda match: match.group('sign') + match.group('mant'),
    lambda match: match.group('sf'),
    lambda match: match.group('currency')
)

# currency_with_exponent {{{2
currency_with_exponent = (
    r'{sign}{currency}{mantissa}{exponent}'.format(**locals()),
    lambda match: match.group('sign') + match.group('mant'),
    lambda match: match.group('exp').lower(),
    lambda match: match.group('currency')
)

# simple_currency {{{2
simple_currency = (
    r'{sign}{currency}{mantissa}'.format(**locals()),
    lambda match: match.group('sign') + match.group('mant'),
    lambda match: '',
    lambda match: match.group('currency')
)

# nan_with_units {{{2
nan_with_units = (
    r'{sign}{nan}\s+{units}'.format(**locals()),
    lambda match: match.group('sign') + match.group('nan').lower(),
    lambda match: '',
    lambda match: match.group('units')
)

# currency_nan {{{2
currency_nan = (
    r'{sign}{currency}{nan}'.format(**locals()),
    lambda match: match.group('sign') + match.group('nan').lower(),
    lambda match: '',
    lambda match: match.group('currency')
)

# simple_nan {{{2
simple_nan = (
    r'{sign}{nan}'.format(**locals()),
    lambda match: match.group('sign') + match.group('nan').lower(),
    lambda match: '',
    lambda match: ''
)

# all_number_converters {{{2
all_number_converters = [
    (re.compile('\A\s*{}\s*\Z'.format(pattern)), get_mant, get_sf, get_units)
    for pattern, get_mant, get_sf, get_units in [
        number_with_exponent, number_with_scale_factor, simple_number,
        currency_with_exponent, currency_with_scale_factor, simple_currency,
        nan_with_units, currency_nan, simple_nan,
    ]
]

# sf_free_number_converters {{{2
sf_free_number_converters = [
    (re.compile('\A\s*{}\s*\Z'.format(pattern)), get_mant, get_sf, get_units)
    for pattern, get_mant, get_sf, get_units in [
        number_with_exponent, simple_number,
        currency_with_exponent, simple_currency,
        nan_with_units, currency_nan, simple_nan,
    ]
]
# recognize_number() {{{2
def recognize_number(value, ignore_sf):
    if ignore_sf:
        number_converters = sf_free_number_converters
    else:
        number_converters = all_number_converters
    for pattern, get_mant, get_sf, get_units in number_converters:
        match = pattern.match(value)
        if match:
            mantissa = get_mant(match)
            sf = get_sf(match)
            sf = sf if sf != '_' else ''
            units = get_units(match)
            number = float(mantissa + MAPPINGS.get(sf, [sf])[0])
            return number, units, mantissa, sf
    else:
        raise ValueError('%s: not a valid number.' % value)

# Utilities {{{1
# is_str {{{2
from six import string_types
def is_str(obj):
    """Identifies strings in all their various guises."""
    return isinstance(obj, string_types)

# _combine {{{2
def _combine(mantissa, sf, units, spacer):
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

# Quantity class {{{1
class Quantity(float):
    # Defaults
    _si = DEFAULTS['si']
    _units = DEFAULTS['units']
    _prec = DEFAULTS['prec']
    _full_prec = DEFAULTS['full_prec']
    _spacer = DEFAULTS['spacer']
    _unity_sf = DEFAULTS['unity_sf']
    _output_sf = DEFAULTS['output_sf']
    _keep_components = DEFAULTS['keep_components']
    _ignore_sf = DEFAULTS['ignore_sf']
    _fmt = DEFAULTS['fmt']
    _assign_fmt = DEFAULTS['assign_fmt']
    _assign_rec = DEFAULTS['assign_rec']
    _reltol = DEFAULTS['reltol']
    _abstol = DEFAULTS['abstol']

    units = ''  # do not change these
    name = ''
    desc = ''
        # these used as the default values for these three attributes. Putting
        # them here means that the instances do not need to contain these values
        # if not specified, but yet they can always be accessed

    # constructor {{{2
    def __new__(
        cls, value, model=None, units=None, name=None, desc=None, ignore_sf=None
    ):
        """Physical Quantity
        A real quantity with units.

        value (real or string): the value of the quantity.
            If a string, it may be specified with SI scale factors and units.
            For example, the following are all valid:
                2.5ns, 1.7 MHz, 1e6ohms, 2.8_V, 1e12 F, 42, etc.
            String may also have name and description if they are provided in a
            way recognizable by assign_rec. For example,
                trise = 10ns -- rise time
            would work with the default recognizer.
        model (quantity or string): used to pick up any missing attibutes
            (units, name, desc). May be a quantity or a string. If it is a string,
            it will be split. Then if there is one item, it is take to be the
            units. If there are two, they are taken to be the name and units.
            And if there are three or more, the first two are taken to the be
            name and units, and the remainder is take to be the description.
        units (string): overrides the units taken from the value or model.
        name (string): overrides the name taken from the value or model.
        desc (string): overrides the desc taken from the value or model.
        ignore_sf (bool): assume the values given in strings do not employ scale
            factors.  In this way, '1m' will be interpreted as 1 meter rather
            than 1 milli.
        """
        ignore_sf = cls._ignore_sf if ignore_sf is None else ignore_sf

        def recognize_all(value):
            nonlocal name, units, desc, mantissa, sf
            try:
                number, u, mantissa, sf = recognize_number(value, ignore_sf)
            except ValueError:
                # not a simple number, try the assignment recognizer
                match = re.match(cls._assign_rec, value)
                if match:
                    n, val, d = match.groups()
                    number, u, mantissa, sf = recognize_number(val, ignore_sf)
                    if name is None:
                        name = n
                    if desc is None:
                        desc = d
                else:
                    raise
            if units is None:
                units = u
            return number

        # process the value
        if is_str(value):
            if value in CONSTANTS:
                value = CONSTANTS[value]
                if is_str(value):
                    number = recognize_all(value)
                else:
                    number = value[0]
                    if is_str(number):
                        number, _, mantissa, sf = recognize_number(number, True)
                    if len(value) > 1 and not units:
                        units = value[1]
                    if len(value) > 2 and not name:
                        name = value[2]
                    if len(value) > 3 and not desc:
                        desc = value[3]
            else:
                number = recognize_all(value)
        else:
            number = value

        # process model to get values for name, units, and desc if still empty
        if is_str(model):
            components = model.split(maxsplit=2)
            if len(components) == 1:
                units = components[0] if units is None else units
            else:
                name = components[0] if name is None else name
                units = components[1] if units is None else units
                if len(components) == 3:
                    desc = components[2] if desc is None else desc
        else:
            name = getattr(model, 'name', None) if name is None else name
            units = getattr(model, 'units', None) if units is None else units
            desc = getattr(model, 'desc', None) if desc is None else desc

        # create the underlying data structure and add attributes as appropriate
        self = float.__new__(cls, number)
        if units:
            self.units = units
        if name:
            self.name = name
        if desc:
            self.desc = desc

        if cls._keep_components:
            try:
                # if we got a string, keep the pieces so we can reconstruct it
                # exactly as it was given.
                if mantissa:
                    self._mantissa = mantissa
                    self._scale_factor = sf
            except NameError:
                pass
        return self

    # is_infinte() {{{2
    def is_infinite(self):
        try:
            value = self._mantissa
        except AttributeError:
            value = str(self.real)
        return value.lower() in ['inf', '-inf', '+inf']

    # is_nan() {{{2
    def is_nan(self):
        try:
            value = self._mantissa
        except AttributeError:
            value = str(self.real)
        return value.lower() in ['nan', '-nan', '+nan']

    # as_tuple() {{{2
    def as_tuple(self):
        "Returns a tuple that contains the value as a float and the units."
        return self.real, self.units

    # render() {{{2
    def render(self, units=None, si=None, prec=None, fmt=None):
        "Returns the quantity as a string."

        use_fmt = self._fmt if fmt is None else fmt
        if use_fmt and self._assign_fmt and self.name:
            def format(value):
                if is_str(self._assign_fmt):
                    assign_fmt = self._assign_fmt
                elif self.desc:
                    assign_fmt = self._assign_fmt[0]
                else:
                    assign_fmt = self._assign_fmt[1]
                return assign_fmt.format(n=self.name, v=value, d=self.desc)
        else:
            format = lambda x: x

        # initialize units and si
        use_units = self._units if units is None else units
        units = self.units if use_units else ''
        si = self._si if si is None else si

        # check for infinities or NaN
        if self.is_infinite() or self.is_nan():
            return format(_combine(str(self.real), '', units, ' '))

        # convert into scientific notation with proper precision
        if prec is None:
            prec = self._prec
        if prec == 'full' and hasattr(self, '_mantissa'):
            mantissa = self._mantissa
            sf = self._scale_factor
            try:
                exp = int(sf)
            except ValueError:
                if sf:
                    exp = int(MAPPINGS.get(sf, [sf])[0].lstrip('e'))
                else:
                    exp = 0

            # normalize the mantissa
            mantissa += '' if '.' in mantissa else '.'
            whole, frac = mantissa.split('.')
            mantissa = whole[0] + '.' + whole[1:] + frac
            exp += len(whole) - 1
        else:
            # determine precision
            if prec == 'full':
                prec = self._full_prec
            assert (prec >= 0)

            # get components of number
            number = "%.*e" % (prec, self.real)
            mantissa, exp = number.split("e")
            exp = int(exp)

        #  scale factor
        index = exp // 3
        shift = exp % 3
        sf = "e%d" % (exp - shift)
        if index == 0:
            if units and units not in CURRENCY_SYMBOLS and not self._spacer:
                sf = self._unity_sf
            else:
                sf = ''
        elif si:
            if (index > 0):
                if index <= len(BIG_SCALE_FACTORS):
                    if BIG_SCALE_FACTORS[index-1] in self._output_sf:
                        sf = BIG_SCALE_FACTORS[index-1]
            else:
                index = -index
                if index <= len(SMALL_SCALE_FACTORS):
                    if SMALL_SCALE_FACTORS[index-1] in self._output_sf:
                        sf = SMALL_SCALE_FACTORS[index-1]

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
        mantissa = mantissa.rstrip(".")

        return format(_combine(mantissa, sf, units, self._spacer))

    # is_close() {{{2
    def is_close(self, other):
        try:
            return math.isclose(
                self.real, float(other),
                rel_tol=self._reltol, abs_tol=self._abstol
            )
        except AttributeError:
            delta = abs(self.real-float(other))
            reference = max(abs(self.real), abs(float(other)))
            return delta <= max(self._reltol * reference, self._abs_tol)

    # __float__() {{{2
    def __float__(self):
        return self.real

    # __str__() {{{2
    def __str__(self):
        return self.render()

    # __repr__() {{{2
    def __repr__(self):
        si = False if self._ignore_sf else None
        return 'Quantity({!r})'.format(self.render(units=True, si=si, prec='full'))

    # __format__() {{{2
    def __format__(self, fmt):
        """Convert quantity to string for Python string format function.

        Supports the normal floating point and string format types as well some
        new ones. If the format code is given in upper case, assign_fmt is used
        to add the name and perhaps description to the result.

        The format is specified using AW.PT where:
        A is character and gives the alignment: either '', '>', or '<'
        W is integer and gives the width
        P is integer and gives the precision
        T is char and gives the type: choose from q, r, s, e, f, g, u, n, d, ...
           q = quantity [si=y, units=y, fmt=n] (ex: 1.4204GHz)
           Q = quantity [si=y, units=y, fmt=y] (ex: f = 1.4204GHz)
           r = real [si=y, units=n, fmt=n] (ex: 1.4204G)
           R = real [si=y, units=n, fmt=y] (ex: f = 1.4204G)
             = string [] (ex: 1.4204GHz)
           s = string [fmt=n] (ex: 1.4204GHz)
           S = string [fmt=y] (ex: f = 1.4204GHz)
           e = exponential form [si=n, units=n, fmt=n] (ex: 1.4204e9)
           E = exponential form [si=n, units=n, fmt=y] (ex: f = 1.4204e9)
           f = float [na] (ex: 1420400000.0000)
           F = float [na] (ex: f = 1420400000.0000)
           g = float [na] (ex: 1.4204e+09)
           G = float [na] (ex: f = 1.4204e+09)
           u = units [na] (ex: Hz)
           n = name [na] (ex: f)
           d = description [na] (ex: hydrogen line)
        """
        match = FORMAT_SPEC.match(fmt)
        if match:
            align, width, prec, ftype = match.groups()
            prec = int(prec) if prec else None
            if ftype and ftype in 'dnu':
                if ftype == 'u':
                    value = self.units
                elif ftype == 'n':
                    value = getattr(self, 'name', '')
                elif ftype == 'd':
                    value = getattr(self, 'desc', '')
                else:
                    raise AssertionError(ftype)
                return '{0:{1}{2}s}'.format(value, align, width)
            fmt = ftype.isupper()
            if ftype in 'sS':  # note that ftype = '' matches this case
                fmt = fmt if ftype else None
                value = self.render(prec=prec, fmt=fmt)
            elif ftype in 'qQ':
                value = self.render(prec=prec, si=True, units=True, fmt=fmt)
            elif ftype in 'rR':
                value = self.render(prec=prec, si=True, units=False, fmt=fmt)
            else:
                if prec is None:
                    prec = self._prec
                if ftype in 'gG':
                    prec += 1
                value = '{0:.{1}{2}}'.format(self.real, prec, ftype.lower())
                if ftype.isupper():
                    name = getattr(self, 'name', '')
                    desc = getattr(self, 'desc', '')
                    if is_str(self._assign_fmt):
                        assign_fmt = self._assign_fmt
                    elif desc:
                        assign_fmt = self._assign_fmt[0]
                    else:
                        assign_fmt = self._assign_fmt[1]
                    value = assign_fmt.format(n=name, v=value, d=desc)
            return '{0:{1}{2}s}'.format(value, align, width)
        else:
            return self.render()


    # set_preferences() {{{2
    @classmethod
    def set_preferences(cls, **kwargs):
        """Set Class Preferences

        si (bool): Use SI scale factors by default.
        units (bool): Output units by default.
        prec (int): Default precision in digits where 0 corresponds to 1 digit. Must
            be nonnegative. This precision is used when full precision is not
            required.
        full_prec (int): Default full precision in digits where 0 corresponds to 1
            digit, must be nonnegative. This precision is used when full precision
            is requested if the precision is not otherwise known.
        spacer (str): May be '' or ' ', use the latter if you prefer a space between
            the number and the units. Generally using ' ' makes numbers easier to
            read, particularly with complex units, and using '' is easier to parse.
        unity_sf (str): The output scale factor for unity, generally '' or '_'.
        output_sf (str): Which scale factors to output, generally one would only use
            familiar scale factors.
        ignore_sf (bool): Whether scale factors should be ignored by default.
        fmt (bool): Cause render() to add name and description by default they are given.
        reltol (real): relative tolerance, used by is_close() when determining
            equivalence.
        abstol (real): absolute tolerance, used by is_close() when determining
            equivalence.
        keep_components (bool): indicate whether components should be kept if
            quantity value was given as string. Doing so takes a bit of space, but
            allows the original precision of the number to be recreated when full
            precision is requested.
        assign_fmt (str): Format string for an assignment. Will be passed through
            string .format method. Format string takes three possible arguments
            named n, q, and d for the name, value and description.  The default is
                '{n} = {v}'
            You can also pass two format strings as a tuple, The first is used
            if desc is present, otherwise second is used. For example,
                ('{n} = {v} -- {d}', '{n} = {v}'),
        assign_rec (str): Regular expression used to recognize an assignment. Used
            in add_to_namespace(). Default recognizes the form
                "Temp = 300_K -- Ambient temperature".
        reltol (real): relative tolerance.
        abstol (real): absolute tolerance.

        Any value not passed in are left alone. Pass in None to reset it to its
        default value.
        """

        for key, value in kwargs.items():
            lkey = '_' + key
            if value is None:
                # attributes that were passed as None are to be returned to
                # their default value
                if cls == Quantity:
                    # this is base class, override value with the default value
                    setattr(cls, lkey, DEFAULTS[key])
                else:
                    # delete the attribute so value of parent class is used.
                    delattr(cls, lkey)
            else:
                # override with the desired value
                setattr(cls, lkey, value)

# add_to_namespace() {{{2
    @classmethod
    def add_to_namespace(cls, quantities):
        """ Add to Namespace

        Takes a string that contains quantity definitions and places those
        quantities in the calling namespace. The string may contain one
        definition per line, of the form:
            <name> = <value> -- <description>

        <name> must be a valid identifier (ex: c_load).
        <value> is a number with optional units (ex: 3 or 1pF or 1 kOhm).
            The units need not be a simple identifier (ex: 9.07 GHz/V).
        <description> is an optional textual description (ex: Gain of PD (Imax)).
        """
        # Access the namespace of the calling frame
        import inspect
        frame = inspect.stack()[1][0]
        namespace = frame.f_globals

        for line in quantities.splitlines():
            match = re.match(cls._assign_rec, line)
            if match:
                name, value, desc = match.groups()
                if not value:
                    continue
                if not name:
                    raise ValueError('{}: no variable name given.'.format(line))
                quantity = Quantity(value, name=name, desc=desc)
                namespace[name] = quantity
            else:  # pragma: no cover
                raise ValueError('{}: not a valid number.'.format(line))
