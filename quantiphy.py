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
from __future__ import division
import re
import math
try:
    from collections import ChainMap
except ImportError:
    from chainmap import ChainMap
from six import string_types, u, python_2_unicode_compatible

# Utilities {{{1
# is_str {{{2
def is_str(obj):
    """Identifies strings in all their various guises."""
    return isinstance(obj, string_types)

# combine {{{2
def combine(mantissa, sf, units, spacer):
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

# Unit Conversions {{{1
_unit_conversions = {}
def _convert_units(to_units, from_units, value):
    if to_units == from_units:
        return value
    return _unit_conversions[(to_units,from_units)](value)

class UnitConversion(object):
    """
    Create a unit converter.
    """
    def __init__(self, to_units, from_units, slope=1, intercept=0):
        """
        to_units (string or list of strings):
            A collection of units. If given as a single string it is split.

        from_units (string or list of strings):
            A collection of units. If given as a single string it is split.

        slope:
            Scale factor for conversion.

        intercept:
            Conversion offset.

        Forward Conversion:
            The following conversion is applied if the given units are among 
            the from_units and the desired units are among the to_units:

                new_value = given_value*slope + incercept

        Reverse Conversion:
            The following conversion is applied if the given units are among 
            the to_units and the desired units are among the from_units:

                new_value = (given_value - intercept)/slope
        """
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


# Constants {{{1
_user_defined_constants = {}
_predefined_constants = {'mks':{}}
_default_unit_system = 'mks'

def set_unit_system(category):
    global _constants
    _constants = ChainMap(
        _user_defined_constants,
        _predefined_constants[category]
    )

set_unit_system(_default_unit_system)

class Constant(object):
    def __init__(self, value, name=None, unit_systems=None):
        self.name = name
        self.value = value
        if unit_systems:
            for system in unit_systems.split():
                constants = _predefined_constants.get(system, {})
                if name:
                    constants[name] = self.value
                if value.name:
                    constants[value.name] = self.value
                _predefined_constants[system] = constants
        else:
            if name:
                _user_defined_constants[name] = self.value
            if value.name:
                _user_defined_constants[value.name] = self.value
        if not name and not value.name:
            raise NameError('no name specified')

# Settings {{{1
DEFAULTS = {
    'show_si': True,
        # use SI scale factors
    'show_units': True,
        # output units
    'prec': 4,
        # normal precision
    'full_prec': 12,
        # full precision
    'spacer': ' ',
        # spacer between number and units
    'unity_sf': '',
        # what to use as unity scale factor, generally '' or '_'
    'output_sf': 'TGMkmunpfa',
        # the scale factors that should be used when formatting numbers
        # this can be a subset of the available scale factors
    'map_sf': {},
        # use this to change the way individual scale factors are rendered.
        # ex: map_sf={'u': 'μ'} to render micro using mu. Can be a mapping or
        # a function.
    'ignore_sf': False,
        # assume quantity does not employ scale factor when converting from string
    'known_units': [],
        # units with a leading character that could be confused as a scale
        # factor
    'show_label': False,
        # cause render to add name and description by default if given
    'strip_dp': True,
        # strip the decimal points from numbers when rendering even if they can
        # then be mistaken for integers.
    'label_fmt': '{n} = {v}',
        # assignment formatter
        # use {n}, {v}, and {d} to access name, value, and description
        # if two are given as tuple, first is used if desc is present, otherwise
        # second is used. For example, an alternate specification that prints
        # the description if it is available is:
        #     'label_fmt': ('{n} = {v} -- {d}', '{n} = {v}'),
    'assign_rec': r'\A\s*(?:([^=]+)\s*=\s*)?(.*?)(?:\s*--\s*(.*?)\s*)?\Z',
        # assignment recognizer
    'keep_components': True,
        # keep string components
    'reltol': 1e-6,
        # relative tolerance
    'abstol': 1e-12,
        # absolute tolerance
}
CURRENCY_SYMBOLS = '$£€'


# Constants {{{1
__version__ = '1.3.0'
__released__ = '2017-03-19'

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
    'm': ('e-3',  1e-3 ),
    'u': ('e-6',  1e-6 ),
    'μ': ('e-6',  1e-6 ),
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
FORMAT_SPEC = re.compile(r'\A([<>]?)(\d*)(?:\.(\d+))?(?:([qQrRusSeEfFgGdn])([a-zA-Z°ÅΩ℧%][-^/()\w]*)?)?\Z')
#                             ^align ^width    ^prec     ^format            ^units

# Regular expression for recognizing identifiers
IDENTIFIER = re.compile(r'\A[_a-zA-Z][\w]*\Z')

# Pattern Definitions {{{1
# Build regular expressions used to recognize quantities
def named_regex(name, regex):
    return '(?P<%s>%s)' % (name, regex)

# components {{{2
sign = named_regex('sign', '[-+]?')
required_digits = r'(?:[0-9][0-9_]*[0-9]|[0-9]+)'  # allow interior underscores
optional_digits = r'(?:[0-9][0-9_]*[0-9]|[0-9]*)'
mantissa = named_regex(
    'mant',
    r'(?:{od}\.?{rd})|(?:{rd}\.?{od})'.format(
        rd = required_digits, od = optional_digits
    ),  # leading or trailing digits are optional, but not both
)
exponent = named_regex('exp', '[eE][-+]?[0-9]+')
scale_factor = named_regex('sf', '[%s]' % ''.join(MAPPINGS))
units = named_regex('units', r'(?:[a-zA-Z°ÅΩ℧%][-^/()\w]*)?')
    # examples: Ohms, V/A, J-s, m/s^2, H/(m-s), Ω, %
    # leading char must be letter to avoid 1.0E-9s -> (1e18, '-9s')
currency = named_regex('currency', '[%s]' % CURRENCY_SYMBOLS)
nan = named_regex('nan', '(?i)inf|nan')

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


# Quantity class {{{1
@python_2_unicode_compatible
class Quantity(float):
    # class attributes {{{2
    # defaults
    show_si = DEFAULTS['show_si']
    show_units = DEFAULTS['show_units']
    prec = DEFAULTS['prec']
    full_prec = DEFAULTS['full_prec']
    spacer = DEFAULTS['spacer']
    unity_sf = DEFAULTS['unity_sf']
    output_sf = DEFAULTS['output_sf']
    map_sf = DEFAULTS['map_sf']
    keep_components = DEFAULTS['keep_components']
    ignore_sf = DEFAULTS['ignore_sf']
    known_units = DEFAULTS['known_units']
    show_label = DEFAULTS['show_label']
    strip_dp = DEFAULTS['strip_dp']
    label_fmt = DEFAULTS['label_fmt']
    assign_rec = DEFAULTS['assign_rec']
    reltol = DEFAULTS['reltol']
    abstol = DEFAULTS['abstol']
        # These class attributes act as defaults for the instances. However,
        # when accessing these values the code always goes through self.
        # This allows the user to monkey-patch the instances to provide local
        # overrides to these values.

    units = ''  # do not change these
    name = ''
    desc = ''
        # These are used as the default values for these three attributes.
        # Putting them here means that the instances do not need to contain
        # these values if not specified, but yet they can always be accessed.

    # constructor {{{2
    def __new__(
        cls, value, model=None, units=None, scale=None,
        name=None, desc=None, ignore_sf=None
    ):
        """Physical Quantity
        A real quantity with units.

        value (real or string):
            The value of the quantity.  If a string, it may be specified with SI
            scale factors and units.  For example, the following are all valid:
                2.5ns, 1.7 MHz, 1e6ohms, 2.8_V, 1e12 F, 42, etc.
            String may also have name and description if they are provided in a
            way recognizable by assign_rec. For example,
                trise = 10ns -- rise time
            would work with the default recognizer.
        model (quantity or string):
            Used to pick up any missing attibutes (units, name, desc). May be a
            quantity or a string. If it is a string, it will be split. Then if
            there is one item, it is take to be the units. If there are two,
            they are taken to be the name and units.  And if there are three or
            more, the first two are taken to the be name and units, and the
            remainder is take to be the description.
        units (string):
            Overrides the units taken from the value or model.
        name (string):
            Overrides the name taken from the value or model.
        desc (string):
            Overrides the desc taken from the value or model.
        ignore_sf (bool):
            Assume the values given in strings do not employ scale factors.  In
            this way, '1m' will be interpreted as 1 meter rather than 1 milli.

        Will produce a ValueError exception if passed a string that cannot be
        converted to a quantity. Will produced a KeyError if a unit conversion
        is requested and there is no corresponding unit converter.
        """

        ignore_sf = cls.ignore_sf if ignore_sf is None else ignore_sf
        data = {}

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
                data['name'] = getattr(model, 'name', '')
                data['units'] = getattr(model, 'units', '')
                data['desc'] = getattr(model, 'desc', '')

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
                    if sf+units in cls.known_units:
                        sf, units = '', sf+units
                    mantissa = mantissa.replace('_', '')
                    number = float(mantissa + MAPPINGS.get(sf, [sf])[0])
                    return number, units, mantissa, sf
            else:
                raise ValueError('%s: not a valid number' % value)

        def recognize_all(value):
            try:
                number, u, mantissa, sf = recognize_number(value, ignore_sf)
            except ValueError:
                # not a simple number, try the assignment recognizer
                match = re.match(cls.assign_rec, value)
                if match:
                    n, val, d = match.groups()
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
        if is_str(value):
            constant = _constants.get(value)
            if constant:
                number = float(constant)
                mantissa = getattr(constant, '_mantissa', None)
                sf = getattr(constant, '_scale_factor', None)
                if constant.units:
                    data['units'] = constant.units
                if constant.name:
                    data['name'] = constant.name
                if constant.desc:
                    data['desc'] = constant.desc
            else:
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

        if cls.keep_components:
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
        '''Test value to determine if it is infinite.'''
        try:
            value = self._mantissa
        except AttributeError:
            value = str(self.real)
        return value.lower() in ['inf', '-inf', '+inf']

    # is_nan() {{{2
    def is_nan(self):
        '''Test value to determine if it is not a number.'''
        try:
            value = self._mantissa
        except AttributeError:
            value = str(self.real)
        return value.lower() in ['nan', '-nan', '+nan']

    # as_tuple() {{{2
    def as_tuple(self):
        "Returns a tuple that contains the value as a float along with its units."
        return self.real, self.units

    # render() {{{2
    def render(
        self, show_units=None, show_si=None, prec=None, show_label=None,
        scale=None
    ):
        """Convert quantity to a string

        show_units (bool):
            Whether the units should be included in the string.
        show_si (bool):
            Whether SI scale factors should be used.
        prec (int or 'full'):
            The desired precision (one plus this value is the desired number of
            digits). If specified as full, the full original precision is used.
        show_label (bool):
            Whether label_fmt should be used to include name and perhaps
            description in string.
        scale (float, tuple, func, or string):
            If a float, it scales the displayed value (the quantity is multiplied
                by scale before being converted to the sting).
            If a tuple, the first value, a float, is treated as a scale factor
                and the second value, a string, is take to be the units of the
                displayed value.
            If a function, it takes two arguments, the value and the units of
                the quantity and it returns two values, the value and units of
                the displayed value.
            If a string, it is taken to the be desired units. This value along
                with the units of the quantity are used to select a known unit
                conversion, which is applied to create the displayed value.

        Will produced a KeyError if a unit conversion is requested and there is
        no corresponding unit converter.
        """


        use_fmt = self.show_label if show_label is None else show_label
        if use_fmt and self.label_fmt and self.name:
            def format(value):
                if is_str(self.label_fmt):
                    label_fmt = self.label_fmt
                elif self.desc:
                    label_fmt = self.label_fmt[0]
                else:
                    label_fmt = self.label_fmt[1]
                return label_fmt.format(n=self.name, v=value, d=self.desc)
        else:
            format = lambda x: x

        # initialize units and si
        show_units = self.show_units if show_units is None else show_units
        units = self.units if show_units else ''
        show_si = self.show_si if show_si is None else show_si

        # check for infinities or NaN
        if self.is_infinite() or self.is_nan():
            return format(combine(str(self.real), '', units, ' '))

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
                    exp = int(MAPPINGS.get(sf, [sf])[0].lstrip('e'))
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
                sf = self.map_sf.__func__(sf)

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
        if sf or show_units or self.strip_dp:
            mantissa = mantissa.rstrip(".")
        else:
            if mantissa[-1] == '.':
                mantissa += '0'

        return format(combine(mantissa, sf, units, self.spacer))

    # is_close() {{{2
    def is_close(self, other, reltol=None, abstol=None, check_units=True):
        '''Use abstol and reltol to determine if a value is close.'''
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
        new ones. If the format code is given in upper case, label_fmt is used
        to add the name and perhaps description to the result.

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
                    raise NotImplementedError(ftype)
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
                    name = getattr(self, 'name', '')
                    desc = getattr(self, 'desc', '')
                    if is_str(self.label_fmt):
                        label_fmt = self.label_fmt
                    elif desc:
                        label_fmt = self.label_fmt[0]
                    else:
                        label_fmt = self.label_fmt[1]
                    value = label_fmt.format(n=name, v=value, d=desc)
            return '{0:{1}{2}s}'.format(value, align, width)
        else:
            # unrecognized format, just provide something reasonable
            return self.render()


    # set_preferences() {{{2
    @classmethod
    def set_preferences(cls, **kwargs):
        """Set class preferences

        show_si (bool):
            Use SI scale factors by default.
        show_units (bool):
            Output units by default.
        prec (int):
            Default precision in digits where 0 corresponds to 1 digit. Must
            be nonnegative. This precision is used when full precision is not
            required.
        full_prec (int):
            Default full precision in digits where 0 corresponds to 1 digit,
            must be nonnegative. This precision is used when full precision is
            requested if the precision is not otherwise known.
        spacer (str):
            May be '' or ' ', use the latter if you prefer a space between the
            number and the units. Generally using ' ' makes numbers easier to
            read, particularly with complex units, and using '' is easier to
            parse.
        unity_sf (str):
            The output scale factor for unity, generally '' or '_'.
        output_sf (str):
            Which scale factors to output, generally one would only use familiar
            scale factors.
        map_sf (dict or funct):
            Use this to change the way individual scale factors are rendered,
            ex: map_sf={'u': 'μ'} to render micro using mu. If a function is
            given, it takes a single string argument, the nominal scale factor,
            and returns a string, the desired scale factor.
        ignore_sf (bool):
            Whether scale factors should be ignored by default.
        known_units (list or string):
            List of units that are expected to be used for which the leading
            character could be mistaken as a scale factor.  If a string is
            given, it is split at white space to form the list.
        show_label (bool):
            Cause render() to add name and description by default if they are
            given.
        strip_dp (bool):
            When rendering, strip the decimal points from numbers even if they
            can then be mistaken for integers.
        reltol (real):
            Relative tolerance, used by is_close() when determining equivalence.
        abstol (real):
            Absolute tolerance, used by is_close() when determining equivalence.
        keep_components (bool):
            Indicate whether components should be kept if quantity value was
            given as string. Doing so takes a bit of space, but allows the
            original precision of the number to be recreated when full precision
            is requested.
        label_fmt (str):
            Format string for an assignment. Will be passed through string
            .format() method. Format string takes three possible arguments named
            n, q, and d for the name, value and description.  The default is
                '{n} = {v}'
            You can also pass two format strings as a tuple, The first is used
            if desc is present, otherwise second is used. For example,
                ('{n} = {v} -- {d}', '{n} = {v}'),
        assign_rec (str):
            Regular expression used to recognize an assignment. Used in
            add_to_namespace(). Default recognizes the form
                "Temp = 300_K -- Ambient temperature".

        Any value not passed in are left alone. Pass in None to reset a value to
        its default value.
        """

        for key, value in kwargs.items():
            assert key in DEFAULTS, ('%s: unknown.' % key)
            if value is None:
                # attributes that were passed as None are to be returned to
                # their default value
                if cls == Quantity:
                    # this is base class, override value with the default value
                    setattr(cls, key, DEFAULTS[key])
                else:
                    # delete the attribute so value of parent class is used.
                    delattr(cls, key)
            else:
                # override with the desired value
                if key in ['known_units'] and is_str(value):
                    value = value.split()
                setattr(cls, key, value)

    # get_preference() {{{2
    @classmethod
    def get_preference(cls, key):
        """Get class preference

        name (str):
            Name of the desired preference. Choose from: show_si, show_units,
            prec, full_prec, spacer, unity_sf, output_sf, map_sf, ignore_sf,
            known_units, show_label, reltol, abstol, keep_components, label_fmt,
            assign_rec.
        """
        assert key in DEFAULTS, ('%s: unknown.' % key)
        return getattr(cls, key)

    # add_to_namespace() {{{2
    @classmethod
    def add_to_namespace(cls, quantities):
        """ Add to Namespace

        Takes a string that contains quantity definitions and places those
        quantities in the calling namespace. The string may contain one
        definition per line, each of which is parsed by assign_rec. By default,
        the lines are assumed to be of the form:

            <name> = <value> -- <description>

        <name> must be a valid identifier (ex: c_load).
        <value> is a number with optional units (ex: 3 or 1pF or 1 kOhm).
            The units need not be a simple identifier (ex: 9.07 GHz/V).
        <description> is an optional textual description (ex: Gain of PD (Imax)).
        """
        # Access the namespace of the calling frame
        import inspect
        import keyword
        frame = inspect.stack()[1][0]
        namespace = frame.f_globals

        for line in quantities.splitlines():
            match = re.match(cls.assign_rec, line)
            if match:
                name, value, desc = match.groups()
                if not value:
                    continue
                if not name:
                    raise ValueError('{}: no variable name given.'.format(line))
                name = name.strip()
                quantity = cls(value, name=name, desc=desc)
                if IDENTIFIER.match(name) and not keyword.iskeyword( name):
                    namespace[name] = quantity
                else:  # pragma: no cover
                    raise ValueError('{}: not a valid identifier.'.format(name))
            else:  # pragma: no cover
                raise ValueError('{}: not a valid number'.format(line))

    # map_sf_to_sci_notation() {{{2
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

        Pass this function to map_sf preference if you prefer your large and
        small numbers is classic scientific notation.
        """
        # The explicit references to unicode here and in _SCI_NOTATION_MAPPER are
        # for backward compatibility with python2. They can be removed when
        # python2 support is dropped.
        return u(sf).translate(Quantity._SCI_NOTATION_MAPPER)

    # map_sf_to_greek() {{{2
    @staticmethod
    def map_sf_to_greek(sf):
        '''Render scale factors in Greek alphabet if appropriate.

        Pass this dictionary to map_sf preference if you prefer μ rather than u.
        '''
        # this could just as easily be a simple dictionary, but implement it as
        # a function so that it supports a docstring.
        return {'u': 'μ'}.get(sf, sf)


# Predefined Constants {{{1
# Plank's constant {{{2
Constant(Quantity(
    '6.626070040e-34',
    units='J-s',
    name='h',
    desc="Plank's constant"
), unit_systems='mks')

Constant(Quantity(
    '6.626070040e-27',
    units='erg-s',
    name='h',
    desc="Plank's constant"
), unit_systems='cgs')

# Reduced Plank's constant {{{2
Constant(Quantity(
    '1.054571800e-34',
    units='J-s',
    name='ħ',
    desc="reduced Plank's constant"
), name='hbar', unit_systems='mks')

Constant(Quantity(
    '1.054571800e-27',
    units='erg-s',
    name='ħ',
    desc="reduced Plank's constant"
), name='hbar', unit_systems='cgs')

# Boltzmann's constant {{{2
Constant(Quantity(
    '1.38064852e-23',
    units='J/K',
    name='k',
    desc="Boltzmann's constant"
), unit_systems='mks')

Constant(Quantity(
    '1.38064852e-16',
    units='erg/K',
    name='k',
    desc="Boltzmann's constant"
), unit_systems='cgs')

# Elementary charge {{{2
Constant(Quantity(
    '1.6021766208e-19',
    units='C',
    name='q',
    desc="elementary charge"
), unit_systems='mks')

Constant(Quantity(
    '4.80320425e-10',
    units='Fr',
    name='q',
    desc="elementary charge"
), unit_systems='cgs')

# Speed of light {{{2
Constant(Quantity(
    '2.99792458e8',
    units='m/s',
    name='c',
    desc="speed of light"
), unit_systems='mks cgs')

# Zero degrees Celsius in Kelvin {{{2
Constant(Quantity(
    '273.15',
    units='K',
    name='0°C',
    desc="zero degrees Celsius in Kelvin"
), name='0C', unit_systems='mks cgs')

# Permittivity of free space {{{2
Constant(Quantity(
    '8.854187817e-12',
    units='F/m',
    name='ε₀',
    desc="permittivity of free space"
), name='eps0', unit_systems='mks')

# Permeability of free space {{{2
Constant(Quantity(
    4e-7*math.pi,
    units='H/m',
    name='μ₀',
    desc="permeability of free space"
), name='mu0', unit_systems='mks')

# Characteristic impedance of free space {{{2
Constant(Quantity(
    '376.730313461',
    units='Ohms',
    name='Z₀',
    desc="characteristic impedance of free space"
), name='Z0', unit_systems='mks')
