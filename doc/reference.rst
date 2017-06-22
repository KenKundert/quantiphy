.. _reference manual:

Reference
=========

.. _constants reference:

Constants and Unit Systems
--------------------------

*QuantiPhy* has several built-in constants that are available by specifying 
their name to the *Quantity* class.  These constants are partitioned into two 
*unit systems*: *mks* and *cgs*. Only those constants that are associated with 
the active unit system, or those that are not associated with any unit system, 
are available when creating a new quantity. You can activate a unit system using
:func:`set_unit_system`. You can create your own constants and unit systems 
using the :class:`Constant` class.


.. class:: Constant

    Creates a constant and adds it to the collection of known constants.
    The return value is of no value and should not be used.

    If *unit_systems* is specified, the constant is added to the specified unit 
    systems. In that case, the constant is only available if one of the 
    specified unit systems is active.

    :param value: The value of the constant. Must be a quantity.
    :type value: quantity

    :param name: The name of the constant.
    :type name: string

    :param unit_systems:
        Name or names of the unit systems to which the constant should be
        added.  If given as a string, string will be split at white space to
        create the list. If not given, the constant is not associated with any 
        unit systems and so is always available.
    :type unit_systems: list or string

    Use the Constants class to add additional constants.  Instantiating this 
    class creates the constant and adds it to *QuantiPhy*'s store of constants.
    The return value is generally ignored.

    .. code-block:: python

        >>> from quantiphy import Quantity, Constant
        >>> Constant(Quantity("λh = 211.061140539mm -- wavelength of hydrogen line"))
        <...>
        >>> hy_wavelength = Quantity('λh')
        >>> print(hy_wavelength)
        211.06 mm

        >>> Quantity.set_preferences( label_fmt=('{n} = {v} -- {d}', '{n} = {v}'))
        >>> print(hy_wavelength.render(show_label=True))
        λh = 211.06 mm -- wavelength of hydrogen line

    The constant is accessed by name, which in this case is the name given in the 
    quantity used when creating the constant. You can also specify the name as an 
    argument to *Constant*.

    .. code-block:: python

        >>> from quantiphy import Quantity, Constant

        >>> Constant(
        ...     Quantity("λh = 211.061140539mm -- wavelength of hydrogen line"),
        ...     name='lambda h'
        ... )
        <...>
        >>> hy_wavelength = Quantity('lambda h')
        >>> print(hy_wavelength.render(show_label=True))
        λh = 211.06 mm -- wavelength of hydrogen line

    It is not necessary to specify both names, one is sufficient.  Notice that the 
    name specified as an argument to *Constant* does not actually become part of the 
    constant, it is only used for looking up the constant.

    By default, user defined constants are not associated with a unit system, 
    meaning that they are always available regardless of which unit system is 
    being used.  However, when creating a constant you can specify one or more 
    unit systems for the constant. You need not limit yourself to the predefined 
    'mks' and 'cgs' unit systems.

    .. code-block:: python

        >>> from quantiphy import Quantity, Constant, set_unit_system

        >>> Constant(Quantity(4.80320427e-10, 'Fr'), 'q', 'esu gaussian')
        <...>
        >>> Constant(Quantity(1.602176487e-20, 'abC'), name='q', unit_systems='emu')
        <...>
        >>> q_mks = Quantity('q')
        >>> set_unit_system('cgs')
        >>> q_cgs = Quantity('q')
        >>> set_unit_system('esu')
        >>> q_esu = Quantity('q')
        >>> set_unit_system('gaussian')
        >>> q_gaussian = Quantity('q')
        >>> set_unit_system('emu')
        >>> q_emu = Quantity('q')
        >>> set_unit_system('mks')
        >>> print(q_mks, q_cgs, q_esu, q_gaussian, q_emu, sep='\n')
        160.22e-21 C
        480.32 pFr
        480.32 pFr
        480.32 pFr
        16.022e-21 abC


.. function:: set_unit_system(name)

    Activates a unit system. The default unit system is 'mks'. Calling this 
    function changes the active unit system to the one with the specified name.  
    Only constants associated with the active unit system or not associated with 
    a unit system are available for use.

    :param value: Name of the desired unit system.
    :type value: string

    A *KeyError* is raised if *name* does not correspond to a known unit system.

.. _quantities reference:

Quantities
----------

.. class:: Quantity

    A physical quantity. A real value with units.

    :param value:
        The value of the quantity.  If a string, it may be specified with SI 
        scale factors and units.  For example, the following are all valid: 
        '2.5ns', '1.7 MHz', '1e6ohms', '2.8_V', '1e12 F', '42', '32 ft/s^2', 
        etc.  The string may also contain the name and description of the 
        quantity if they are provided in a way recognizable by *assign_rec*. For 
        example, 'trise = 10ns -- rise time' would work with the default 
        recognizer ('=' separates the name from the value and '--' separates the 
        value from the description).
    :type value: real or string

    :param model:
        Used to pick up any missing attributes (units, name, desc). May be a
        quantity or a string. If it is a quantity, only units is inherited.  If 
        it is a string, it will be split.  Then if there is one item, it is 
        taken to be the units.  If there are two, they are taken to be the name 
        and units.  And if there are three or more, the first two are taken to 
        the be name and units, and the remainder is taken to be the description.
    :type model: quantity or string

    :param units:
        Overrides the units taken from *value* or *model*.
    :type units: string

    :param scale: Scales the given value to form the value of the quantity.

        - If a float, it multiplies the given value to form the desired value.
        - If a tuple, the first value is the multiplier is the second it the 
          desired units.
        - If a function, it is expected to take two arguments: the given value 
          and units, and to return two values in a tuple: the value of the 
          quantity and its units.
        - If a string, it is expected to be the desired units.  In this case the 
          given and desired units are used to look up a :class:`unit conversion 
          <UnitConversion>` that is used to perform the scaling.
    :type scale: float, tuple, function, string

    :param name:
        Overrides the name taken from *value* or *model*.
    :type units: string

    :param ignore_sf:
        Assume the values given in strings do not employ scale factors.  In
        this way, '1m' is interpreted as 1 meter rather than 1 milli and '300K' 
        is interpreted as 300 Kelvin rather than 300 kilo.
    :type ignore_sf: boolean

    :rtype: quantity

    Will produce a ValueError exception if passed a string that cannot be
    converted to a quantity. Will produced a KeyError if a unit conversion
    is requested and there is no corresponding unit converter.

    **Specifying a Value**:

    The *Quantity* class is used to create a quantity (an object with both a value 
    and units). Normally, creating a quantity takes one or two arguments.  The first 
    is taken to be the value, and the second, if given, is taken to be the model, 
    which is a source of default values.  The value may be given as a float or as 
    a string.  The string may be in floating point notation, in scientific notation, 
    or use SI scale factors and may include the units.  For example, any of the 
    following ways can be used to specify 1ns:

    .. code-block:: python

        >>> period = Quantity(1e-9, 's')
        >>> print(period)
        1 ns

        >>> period = Quantity('0.000000001 s')
        >>> print(period)
        1 ns

        >>> period = Quantity('1e-9s')
        >>> print(period)
        1 ns

        >>> period = Quantity('1ns')
        >>> print(period)
        1 ns

    Currency units ($£€) are a bit different than other units, they are placed 
    at the front of the quantity. And like in Python in general, number may 
    contain underscores, which are generally used to make large numbers more 
    readable.

        >>> period = Quantity('$11_200_000')
        >>> print(period)
        $11.2M

    When given as a string, the number may use any of the following scale factors:

        |   Y (10\ :sup:`24`)
        |   Z (10\ :sup:`21`)
        |   E (10\ :sup:`18`)
        |   P (10\ :sup:`15`)
        |   T (10\ :sup:`12`)
        |   G (10\ :sup:`9`)
        |   M (10\ :sup:`6`)
        |   k (10\ :sup:`3`)
        |   _ (1)
        |   c (10\ :sup:`-2`)
        |   % (10\ :sup:`-2`)
        |   m (10\ :sup:`-3`)
        |   u (10\ :sup:`-6`)
        |   μ (10\ :sup:`-6`)
        |   n (10\ :sup:`-9`)
        |   p (10\ :sup:`-12`)
        |   f (10\ :sup:`-15`)
        |   a (10\ :sup:`-18`)
        |   z (10\ :sup:`-21`)
        |   y (10\ :sup:`-24`)

    When specifying the value as a string you may also give a name and 
    description.  This conversion is under the control of the :meth:`assign_rec 
    <Quantity.set_preferences>` preference. For example:

    .. code-block:: python

        >>> period = Quantity('Tclk = 10ns -- clock period')
        >>> print(f'{period.name} = {period}  # {period.desc}')
        Tclk = 10 ns  # clock period

    If given as a string, the value may also be the name of a known constant:

    .. code-block:: python

        >>> k = Quantity('k')
        >>> q = Quantity('q')
        >>> print(k, q, sep='\n')
        13.806e-24 J/K
        160.22e-21 C

    If you only specify a real number for the value, then the units, name, and 
    description do not get values. But even if given as a string, the value may not 
    contain these extra attributes. This is where the second argument, the model, 
    helps.  It may be another quantity or it may be a string.  Any attributes that 
    are not provided by the first argument are taken from the second if available.  
    If the second argument is a string, it is split.  If it contains one value, that 
    value is taken to be the units, if it contains two, those values are taken to be 
    the name and units, and it it contains more than two, the remaining values are 
    taken to be the description.  If the model is a quantity, only the units are 
    inherited. For example:

    .. code-block:: python

        >>> out_period = Quantity(10*period, period)
        >>> print(out_period)
        100 ns

        >>> freq = Quantity(100e6, 'Hz')
        >>> print(freq)
        100 MHz

        >>> freq = Quantity(100e6, 'Fin Hz')
        >>> print(f'{freq:S}')
        Fin = 100 MHz

        >>> freq = Quantity(100e6, 'Fin Hz Input frequency')
        >>> print(f'{freq:S}')
        Fin = 100 MHz -- Input frequency

    In addition, you can explicitly specify the units, the name, and the description 
    using named arguments. These values override anything specified in the value or 
    the model.

    .. code-block:: python

        >>> out_period = Quantity(
        ...     10*period, period, name='output period',
        ...     desc='period at output of frequency divider'
        ... )
        >>> print(f'{out_period:S}')
        output period = 100 ns -- period at output of frequency divider

    Finally, you can overwrite the quantities attributes to override the units, 
    name, or description.

    .. code-block:: python

        >>> out_period = Quantity(10*period)
        >>> out_period.units = 's'
        >>> out_period.name = 'output period'
        >>> out_period.desc = 'period at output of frequency divider'
        >>> print(f'{out_period:S}')
        output period = 100 ns -- period at output of frequency divider

    The following examples demonstrate the various methods for scaling the value 
    before saving it.

    .. code-block:: python

        >>> m = Quantity('50.8', scale=1000, units='g')
        >>> print(m)
        50.8 kg

        >>> m = Quantity('50.8', scale=(1000, 'g'))
        >>> print(m)
        50.8 kg

        >>> def from_dB(value, units=''):
        ...     return 10**(value/20), units[2:]

        >>> Quantity('-100 dBV', scale=from_dB)
        Quantity('10 uV')

        >>> Tboil = Quantity('212 °F', scale='K')
        >>> print(Tboil)
        373.15 K

        >>> d_sun = Quantity('d = 93 Mmiles  -- average distance from Sun to Earth', scale='m')
        >>> print(d_sun)
        149.67 Gm

    When just specifying the desired units to scale, the pair of the given units 
    and the desired units must have a corresponding :class:`unit conversion 
    <UnitConversion>` defined.


    **Accessing Values**:

    There are a variety of ways of accessing the value of a quantity. If you are 
    just interested in its numeric value, you access it with:

    .. code-block:: python

        >>> h_line = Quantity('1420.405751786 MHz')

        >>> h_line.real
        1420405751.786

        >>> float(h_line)
        1420405751.786

    Or you can use a quantity in the same way that you would use any real 
    number, meaning that you can use it in expressions and it will evaluate to 
    its numeric value:

    .. code-block:: python

        >>> period = Quantity('1us')
        >>> print(period)
        1 us

        >>> frequency = 1/period
        >>> print(frequency)
        1000000.0

        >>> type(period)
        <class 'quantiphy.Quantity'>

        >>> type(frequency)
        <class 'float'>

    Notice that when performing arithmetic operations on quantities the units 
    are completely ignored and do not propagate in any way to the newly computed 
    result.

    If you are interested in the units of a quantity, you can use:

    .. code-block:: python

        >>> h_line.units
        'Hz'

    Or you can access both the value and the units, either as a tuple or in 
    a string:

    .. code-block:: python

        >>> h_line.as_tuple()
        (1420405751.786, 'Hz')

        >>> str(h_line)
        '1.4204 GHz'

    The render() method allows you to control the process of converting a quantity 
    to a string. For example:

    .. code-block:: python

        >>> h_line.render()
        '1.4204 GHz'

        >>> h_line.render(show_si=False)
        '1.4204e9 Hz'

    You can also access the full precision of the quantity:

    .. code-block:: python

        >>> h_line.render(prec='full')
        '1.420405751786 GHz'

        >>> h_line.render(show_si=False, prec='full')
        '1.420405751786e9 Hz'

    Full precision implies whatever precision was used when specifying the quantity 
    if it was specified as a string. If it was specified as a real number, then 
    a fixed, user controllable number of digits are used (default=12). Generally one 
    uses 'full' when generating output that will be read by a machine.


    **Format Strings**:

    Quantities can be flexibly interpolated into strings using the string format 
    method or the new format strings. Quantities work with the string and 
    floating point format codes, as well as supporting the normal field width, 
    precision, and alignment modifiers:

    .. code-block:: python

        >>> f'{h_line}'
        '1.4204 GHz'

        >>> f'{h_line:s}'
        '1.4204 GHz'

        >>> f'{h_line:.6}'
        '1.420406 GHz'

        >>> f'|{h_line:15.6}|'
        '|1.420406 GHz   |'

        >>> f'|{h_line:<15.6}|'
        '|1.420406 GHz   |'

        >>> f'|{h_line:>15.6}|'
        '|   1.420406 GHz|'

        >>> f'{h_line:e}'
        '1.4204e+09'

        >>> f'{h_line:f}'
        '1420405751.7860'

        >>> f'{h_line:g}'
        '1.4204e+09'

    When using no format code or the *s* format code, the Quantity preferences 
    such as *show_units* and *show_si* are honored. Quantities also support the 
    *q* (quantity) and *r* (real) format codes that override the preferences.  
    With *q* the units and scale factors are used regardless of the current 
    preferences.  With *r*, the scale factors are used but the units are not 
    included.

    .. code-block:: python

        >>> Quantity.set_preferences(show_units=False)

        >>> f'{h_line}'
        '1.4204G'

        >>> f'{h_line:q}'
        '1.4204 GHz'

        >>> f'{h_line:r}'
        '1.4204G'

        >>> Quantity.set_preferences(show_units=None)

    The *u* format code signifies that only the units should be included, and 
    *d* does the same for the description.

    .. code-block:: python

        >>> mu0 = Quantity('mu0')

        >>> f'{mu0}'
        '1.2566 uH/m'

        >>> f'{mu0:u}'
        'H/m'

        >>> f'{mu0:d}'
        'permeability of free space'

    Quantities also support capitalized versions of most of the format codes, 
    specifically *S*, *E*, *F*, *G*, *Q*, AND *R*. These codes behave as if 
    *show_label* is True.

    .. code-block:: python

        >>> f'{mu0:S}'
        'μ₀ = 1.2566 uH/m -- permeability of free space'

        >>> f'{mu0:E}'
        'μ₀ = 1.2566e-06 -- permeability of free space'

        >>> f'{mu0:F}'
        'μ₀ = 0.0000 -- permeability of free space'

        >>> f'{mu0:G}'
        'μ₀ = 1.2566e-06 -- permeability of free space'

        >>> f'{mu0:Q}'
        'μ₀ = 1.2566 uH/m -- permeability of free space'

        >>> f'{mu0:R}'
        'μ₀ = 1.2566u -- permeability of free space'

    Finally, you can add units after the format code, which causes the units to 
    be scaled to those units if the transformation represents a known unit 
    conversion.

    .. code-block:: python

        >>> eff_channel_length = Quantity('leff = 14nm')
        >>> f'{eff_channel_length:SÅ}'
        'leff = 140 Å'


    **Methods**:

    .. method:: as_tuple()

        :rtype: 2-element tuple

        Returns the numeric value and the units as a tuple.


    .. method:: is_infinite()

        :rtype: boolean

        Returns True if the quantity is infinite, and False otherwise.


    .. method:: is_nan()

        :rtype: boolean

        Returns True if the quantity is *Not a Number*, and False otherwise.

        Will produce a ValueError exception if passed a string that cannot be
        converted to a quantity. Will produced a KeyError if a unit conversion
        is requested and there is no corresponding unit converter.

    .. method:: render()


        :param show_units: Whether the units should be included in the string.
        :type show_units: boolean

        :param show_si: Whether SI scale factors should be used.
        :type show_si: boolean

        :param prec:
            The desired precision (one plus this value is the desired number of
            digits). If specified as 'full', the full original precision is used if 
            the value of the quantity was specified as a string and the 
            *keep_components* preference is set, otherwise the value specified 
            in the :meth:`full_prec <Quantity.set_preferences>` preference is 
            used.
        :type prec: integer or 'full'

        :param show_label:
            Whether :meth:`label_fmt <Quantity.set_preferences>` should be used 
            to include name and perhaps description in the string.
        :type show_label: boolean

        :param scale:
            - If a float, it scales the displayed value (the quantity is multiplied
              by scale before being converted to the sting).
            - If a tuple, the first value, a float, is treated as a scale factor
              and the second value, a string, is take to be the units of the
              displayed value.
            - If a function, it takes two arguments, the value and the units of
              the quantity and it returns two values, the value and units of
              the displayed value.
            - If a string, it is taken to the be desired units. This value along
              with the units of the quantity are used to select a known unit
              conversion, which is applied to create the displayed value.
        :type scale: float, tuple, func, or string

        :rtype: string

        Will produced a KeyError if a unit conversion is requested and there is
        no corresponding unit converter.

        Here are some examples of the use of *render()*.

        .. code-block:: python

            >>> h_line = Quantity('1420.405751786 MHz')

            >>> h_line.render()
            '1.4204 GHz'

            >>> h_line.render(show_units=False)
            '1.4204G'

            >>> h_line.render(show_si=False)
            '1.4204e9 Hz'

            >>> h_line.render(show_units=False, show_si=False)
            '1.4204e9'

            >>> h_line.render(prec=6)
            '1.420406 GHz'

            >>> h_line.render(prec='full')
            '1.420405751786 GHz'

            >>> h_line.render(show_label=True)
            '1.4204 GHz'

            >>> c = Quantity('c')
            >>> c.render(show_label=True)
            'c = 299.79 Mm/s -- speed of light'

            >>> Quantity.set_preferences(label_fmt=('{V:<18}  # {d}', '{n}: {v}'))
            >>> c.render(show_label=True)
            'c: 299.79 Mm/s      # speed of light'

        The following examples demonstrate the various methods for scaling the value 
        before rendering.

        .. code-block:: python

            >>> print('speed of light (cm/s):', c.render(show_units=False, scale=100))
            speed of light (cm/s): 29.979G

            >>> print('speed of light:', c.render(scale=(100, 'cm/s')))
            speed of light: 29.979 Gcm/s

            >>> import math
            >>> def to_dB(value, units):
            ...     return 20*math.log10(value), 'dB'+units

            >>> T = Quantity('100mV')
            >>> print(T.render(scale=to_dB))
            -20 dBV

            >>> duration = Quantity(2700, 's')
            >>> print(duration.render(scale='min'))
            45 min

        When just specifying the desired units to scale, the pair of the given 
        units and the desired units must have a corresponding :class:`unit 
        conversion <UnitConversion>` defined.


    .. method:: is_close()

        Indicates  whether the value of a quantity or real number is equivalent 
        to that of a quantity. The two values need not be identical, they just 
        need to be close to be deemed equivalent. The *reltol* and *abstol* 
        arguments or preferences are used to determine if they are close.

        :param other:
            The value to compare against.
        :type other: quantity or float

        :param reltol:
            The relative tolerance. If not specified. the *reltol* preference is 
            used, which defaults to 1u.
        :type reltol: float

        :param abstol:
            The absolute tolerance.  If not specified. the *abstol* preference is 
            used, which defaults to 1p.
        :type abstol: float

        :param check_units:
            If True (the default) compare the units of the two values, if they 
            differ return False. Otherwise only compare the numeric values, 
            ignoring the units.
        :type check_units: boolean

        :rtype: boolean

        Returns true if ``abs(a - b) <= max(reltol * max(abs(a), abs(b)), abstol)`` 
        where ``a`` and ``b`` represent *other* and the numeric value of the 
        underlying quantity.

        .. code-block:: python

            >>> h_line.is_close(h_line)
            True

            >>> h_line.is_close(h_line + 1)
            True

            >>> h_line.is_close(h_line + 1e4)
            False

        By default, *is_close()* looks at the both the value and the units if the 
        argument has units. In this way if you compare two quantities with 
        different units, the *is_close* test will always fail if their units 
        differ. Use *check_units* to change this behavior.

        .. code-block:: python

            >>> Quantity('10ns').is_close(Quantity('10nm'))
            False

    .. method:: set_preferences()

        Set the default behavior of the class.

        :param show_si:
            :index:`Use SI scale factors <show_si (preference)>` by default.
        :type show_si: boolean

        :param prec:
            :index:`Default precision <prec (preference)>` in digits where 
            0 corresponds to 1 digit.  Must be nonnegative.  This precision is 
            used in digits where when full precision is not required. Default is 
            4.
        :type prec: integer

        :param full_prec:
            :index:`Default full precision <full_prec (preference)>` in digits 
            where 0 corresponds to 1 digit.  Must be nonnegative.  This 
            precision is used when full precision is requested if the precision 
            is not otherwise known. Default is 12.
        :type full_prec: integer

        :param spacer:
            :index:`The spacer text <spacer (preference)>` to be inserted in 
            a string between the numeric value and the scale factor when units 
            are present.  Is generally specified to be '' or 
            ' '; use the latter if you prefer a space between the number and the 
            units. Generally using ' ' makes numbers easier to read, 
            particularly with complex units, and using '' is easier to parse.  
            You could also use a Unicode thin space.
        :type spacer: string

        :param unity_sf:
            :index:`The output scale factor for unity<unity_sf (preference)>`,
            generally '' or '_'. The default is '', but use '_' if you want 
            there to be no ambiguity between units and scale factors. For 
            example, 0.3 would be rendered as '300m', and 300 m would be 
            rendered as '300_m'.
        :type unity_sf: string

        :param output_sf:
            :index:`Which scale factors to output <output_sf (preference)>`,
            generally one would only use familiar
            scale factors. The default is 'TGMkmunpfa', which gets rid or the 
            very large and very small scale factors that many people do not 
            recognize.
        :type output_sf: string

        :param input_sf:
            :index:`Which scale factors to recognize <input_sf (preference)>`
            when reading numbers.  The default is 'YZEPTGMKk_cmuμnpfazy'.  You 
            can use this to ignore the scale factors you never expect to reduce 
            the chance of a scale factor/unit ambiguity.
            For example, if you expect to encounter temperatures in Kelvin and can 
            do without 'K' as a scale factor, you might use 'TGMK_muμnpfa'. This 
            also gets rid of the unusual scale factors.
        :type input_sf: string

        :param ignore_sf:
            :index:`Whether all scale factors should be ignored <ignore_sf 
            (preference)>` by default.
        :type ignore_sf: boolean

        :param map_sf:
            :index:`Use this to change the way individual scale factors are 
            rendered <map_sf (preference)>`, ex: map_sf={'u': 'μ'} to render 
            micro using mu. If a function is given, it takes a single string 
            argument, the nominal scale factor, 
            and returns a string, the desired scale factor.
        :type map_sf: dictionary or function

        :param known_units:
            :index:`List of units that are expected to be used in preference to 
            a scale factor <known_units (preference)>`
            when the leading character could be mistaken as a scale factor.  If 
            a string is given, it is split at white space to form the list. When 
            set, any previous known units are overridden.
        :type known_units: list or string

        :param show_label:
            :index:`Cause <show_label (preference)>`
            render() to add name and description by default if they are 
            available.  By default this is False.
        :type show_label: boolean

        :param strip_dp:
            :index:`When <strip_dp (preference)>`
            rendering, strip the decimal points from numbers even if they can 
            then be mistaken for integers. By default this is True.
        :type strip_dp: boolean

        :param reltol:
            :index:`Relative tolerance <reltol (preference)>`,
            used by is_close() when determining equivalence.  Default is 1e-6.
        :type reltol: float

        :param abstol:
            :index:`Absolute tolerance <abstol (preference)>`,
            used by is_close() when determining equivalence.  Default is 1e-12.
        :type abstol: float

        :param keep_components:
            :index:`indicate <keep_components (preference)>`
            whether components should be kept if quantity value was given as 
            string. Doing so takes a bit of space, but allows the original 
            precision of the number to be recreated when full precision is 
            requested.
        :type keep_components: boolean

        :param label_fmt:
            :index:`Format string for an assignment <label_fmt (preference)>`.
            Will be passed through string .format() method. Format string takes 
            three possible arguments named *n*, *q*, and *d* for the name, value 
            and description.  A typical value is:

                ``'{n} = {v}'``

            You can also pass two format strings as a tuple, The first is used
            if the description is present, otherwise second is used (the second 
            should not contain the *d* argument).  For example:

                ``('{n} = {v} -- {d}', '{n} = {v}')``

            When given as a tuple, there is an additional argument available: 
            *V*.  It should only be used in the first format string and is the 
            quantity formatted with the second string. It is helpful because any 
            argument formatting is applied to the combination, which gives you 
            a way line up the descriptions (see :ref:`thermal voltage example`):

                ('{V:<16}  # {d}', '{n}: {v}')

        :type label_fmt: string or tuple

        :param assign_rec:
            :index:`Regular expression used to recognize an assignment 
            <assign_rec (preference)>`.
            Used in constructor and extract(). By default recognizes the forms:

            .. code-block:: python

                >>> vel = Quantity('vel = 60 m/s')
                >>> print(vel.render(show_label=True))
                vel: 60 m/s

                >>> vel = Quantity('vel = 60 m/s -- velocity')
                >>> print(vel.render(show_label=True))
                vel: 60 m/s         # velocity

                >>> vel = Quantity('vel = 60 m/s # velocity')
                >>> print(vel.render(show_label=True))
                vel: 60 m/s         # velocity

        :type assign_rec: string

        Any values not passed in are left alone. Pass in *None* to reset a value to
        its default value.

        .. code-block:: python

            >>> Quantity.set_preferences(prec=2, spacer='')
            >>> h_line.render()
            '1.42GHz'

            >>> h_line.render(prec=4)
            '1.4204GHz'

        Specifying *prec* (precision) as 4 gives 5 digits of precision (you get one more 
        digit than the number you specify for precision). Thus, the common range for 
        *prec* is from 0 to around 12 to 14 for double precision numbers.

        Passing *None* as a value in *set_preferences* returns that preference to its 
        default value:

        .. code-block:: python

            >>> Quantity.set_preferences(prec=None, spacer=None)
            >>> h_line.render()
            '1.4204 GHz'

        You can override the preferences on an individual quantity by monkey-patching 
        the quantity itself. Doing so overrides the global preferences on that quantity:

        .. code-block:: python

            >>> boltzmann = Quantity('h')
            >>> boltzmann.show_units = False
            >>> boltzmann.show_si = False
            >>> boltzmann.render()
            '662.61e-36'

        *map_sf* can be used to change the way scale factors are rendered.  It is common 
        to switch 'u' with 'μ':

        .. code-block:: python

            >>> period = Quantity('1μs')
            >>> print(period)
            1 us

            >>> Quantity.set_preferences(map_sf={'u': 'μ'})
            >>> print(period)
            1 μs

        You can also use *map_sf* to convert the scale factors to scientific notation 
        (actually it is really engineering notation because the exponents are always 
        a multiple of three):

        .. code-block:: python

            >>> sf_mapper = str.maketrans({
            ...     'e': '×10',
            ...     '-': '⁻',
            ...     '0': '⁰',
            ...     '1': '¹',
            ...     '2': '²',
            ...     '3': '³',
            ...     '4': '⁴',
            ...     '5': '⁵',
            ...     '6': '⁶',
            ...     '7': '⁷',
            ...     '8': '⁸',
            ...     '9': '⁹',
            ... })

            >>> def map_sf(sf):
            ...     return sf.translate(sf_mapper)

            >>> Quantity.set_preferences(map_sf=map_sf)
            >>> h_line.render(show_si=False)
            '1.4204×10⁹ Hz'

        Both of these are common enough so that *QuantiPhy* provides these rendering 
        methods for you.

        .. code-block:: python

            >>> Quantity.set_preferences(map_sf=Quantity.map_sf_to_greek)
            >>> print(period)
            1 μs

            >>> Quantity.set_preferences(map_sf=Quantity.map_sf_to_sci_notation)
            >>> h_line.render(show_si=False)
            '1.4204×10⁹ Hz'

            >>> Quantity.set_preferences(map_sf=None)

    .. method:: get_preference(name)

        You can also access the value of an existing preference.

        This method takes the name of a preference and given above and returns its 
        value.

        A *NameError* is raised if *name* is not the name of a preference.

        A common use for *get_preference* to add additional known units without 
        overriding those already present:

        .. code-block:: python

            >>> known_units = Quantity.get_preference('known_units')
            >>> Quantity.set_preferences(known_units = known_units + ['kat'])


    .. method:: extract()

        Takes a string that contains quantity definitions, one per line, and 
        returns those quantities in a dictionary.

        :param quantities:
            The string that contains the quantities.  This string may contain 
            one definition per line, each of which is parsed by 
            :meth:`assign_rec <Quantity.set_preferences>`.  By default, the 
            lines are assumed to be of the form:

                ``<name> = <value> -- <description>``
            orL

                ``<name> = <value> # <description>``

            *<name>*:
                Must be a valid identifier (ex: c_load).
            *<value>*:
                A number with optional units (ex: 3 or 1pF or 1 kOhm).
                The units need not be a simple identifier (ex: 9.07 GHz/V).
            *<description>*:
                is an optional textual description (ex: Gain of PD (Imax)).

            Any line that does not contain a value is ignores. So with the 
            default *assign_rec* lines with the following form are ignored:

                -- comment

                # comment

        :type quantities: string

        For example:

        .. code-block:: python

            >>> design_parameters = '''
            ...     -- PLL Design Parameters
            ...
            ...     Fref = 156 MHz  -- Reference frequency
            ...     Kdet = 88.3 uA  -- Gain of phase detector (Imax)
            ...     Kvco = 9.07 GHz/V  -- Gain of VCO
            ... '''
            >>> globals().update(Quantity.extract(design_parameters))

            >>> print(f'{Fref:S}\n{Kdet:S}\n{Kvco:S}', sep='\n')
            Fref: 156 MHz       # Reference frequency
            Kdet: 88.3 uA       # Gain of phase detector (Imax)
            Kvco: 9.07 GHz/V    # Gain of VCO

        In this case the output of the extract() call is fed into 
        globals().update() so as to add the quantities into the local namespace.

    .. method:: map_sf_to_sci_notation()

        This is a utility function that would be passed to the *map_sf* preference 
        so that the unknown scale factors would be rendered in scientific notation.
        Use *show_si = False* to rendeer all scale factors in scientific 
        notation.

        :param sf:
            The initial scale factor.
        :type sf: string
        :rtype: string

        To format very large and very small numbers in scientific notation rather 
        than E-notation ...

        .. code-block:: python

            >>> Quantity.set_preferences(map_sf=Quantity.map_sf_to_sci_notation)
            >>> k = Quantity('k')
            >>> print(k)
            13.806×10⁻²⁴ J/K


    .. method:: map_sf_to_greek()

        This is a utility function that would be passed to the *map_sf* preference 
        so that the scale factors that are normally Greek characters (specifically 
        μ) render as Greek characters.

        :param sf:
            The initial scale factor.
        :type sf: string
        :rtype: string

        To format 'u' as 'μ', ...

        .. code-block:: python

            >>> Quantity.set_preferences(map_sf=Quantity.map_sf_to_greek)
            >>> permeability = Quantity('mu0')
            >>> print(permeability)
            1.2566 μH/m


.. _conversions reference:

Unit Conversions
----------------

.. class:: UnitConversion

    You can add your own unit conversions to *QuantiPhy* by using 
    *UnitConversion*:

    :param to_units:
        A collection of units. If given as a single string it is split.
    :type to_units: string or list of strings


    :param from_units:
        A collection of units. If given as a single string it is split.
    :type from_units: string or list of strings

    :param slope:
        Scale factor for conversion.
    :type slope: float

    :param intercept:
        Conversion offset.
    :type intercept: float

    Forward Conversion:

        The following conversion is applied if the given units are among the 
        *from_units* and the desired units are among the *to_units*:

            ``new_value = given_value*slope + incercept``

    Reverse Conversion:

        The following conversion is applied if the given units are among the 
        *to_units* and the desired units are among the *from_units*:

            ``new_value = (given_value - intercept)/slope``

    For example:

    .. code-block:: python

        >>> from quantiphy import Quantity, UnitConversion

        >>> UnitConversion('m', 'pc parsec', 3.0857e16)
        <...>

        >>> d = Quantity('5 upc', scale='m')
        >>> print(d)
        154.28 Gm

    *UnitConversion* accepts a scale factor and an offset, so can support 
    temperature conversions.  Also, the conversion can occur in either direction:

    .. code-block:: python

        >>> m = Quantity('1 kg', scale='lbs')
        >>> print(m)
        2.2046 lbs

    Unit conversions between the following units are built-in:

    ====== ===============================================================
    K:     K, F, °F, R, °R
    C, °C: K, C, °C, F, °F, R, °R
    m:     km, m, cm, mm, um, μm, micron, nm, Å, angstrom, mi, mile, miles
    g:     oz, lb, lbs
    s:     s, sec, min, hour, hr , day
    ====== ===============================================================

    When using unit conversions it is important to only convert to units without 
    scale factors (such as those in the first column above) when creating 
    a quantity.  If the units used in a quantity includes a scale factor, then it is 
    easy to end up with two scale factors when converting the number to a string 
    (ex: 1 mkm or one milli-kilo-meter).


**Navigation**:

    * :ref:`Overview <overview>`
    * :ref:`Back to top of Reference Manual <reference manual>`
    * :ref:`Examples <examples>`

