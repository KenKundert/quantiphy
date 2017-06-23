.. _examples:

Examples
========

.. _motivation example:

Motivating Example
------------------

*QuantiPhy* is a light-weight package that allows numbers to be combined with 
units into physical quantities.  Physical quantities are very commonly 
encountered when working with real-world systems when numbers are involved. And 
when encountered, the numbers often use SI scale factors to make them easier to 
read and write.  Surprisingly, most computer languages do not support numbers in 
these forms, meaning that when working with physical quantities, one often has 
to choose between using a form that is easy for computers to read or one that is 
easy for humans to read. For example, consider this table of critical 
frequencies needed in jitter tolerance measurements in optical communication:

.. code-block:: python

    >>> table1 = """
    ...     SDH     | Rate          | f1      | f2       | f3      | f4
    ...     --------+---------------+---------+----------+---------+--------
    ...     STM-1   | 155.52 Mb/s   | 500 Hz  | 6.5 kHz  | 65 kHz  | 1.3 MHz
    ...     STM-4   | 622.08 Mb/s   | 1 kHz   | 25 kHz   | 250 kHz | 5 MHz
    ...     STM-16  | 2.48832 Gb/s  | 5 kHz   | 100 kHz  | 1 MHz   | 20 MHz
    ...     STM-64  | 9.95328 Gb/s  | 20 kHz  | 400 kHz  | 4 MHz   | 80 MHz
    ...     STM-256 | 39.81312 Gb/s | 80 kHz  | 1.92 MHz | 16 MHz  | 320 MHz
    ... """

This table was formatted to be easily read by humans. If it were formatted for 
computers, the numbers would be given without units and in exponential notation 
because they have dramatically different sizes. For example, it might look like 
this:

.. code-block:: python

    >>> table2 = """
    ...     SDH     | Rate (b/s)    | f1 (Hz) | f2 (Hz)  | f3 (Hz) | f4 (Hz)
    ...     --------+---------------+---------+----------+---------+--------
    ...     STM-1   | 1.5552e8      | 5e2     | 6.5e3    | 6.5e3   | 1.3e6
    ...     STM-4   | 6.2208e8      | 1e3     | 2.5e3    | 2.5e5   | 5e6
    ...     STM-16  | 2.48832e9     | 5e3     | 1e5      | 1e6     | 2e7
    ...     STM-64  | 9.95328e9     | 2e4     | 4e5      | 4e6     | 8e7
    ...     STM-256 | 3.981312e10   | 8e4     | 1.92e6   | 1.6e7   | 3.20e8
    ... """

This contains the same information, but it is much harder for humans to read and 
interpret.  Often the compromise of partially scaling the numbers can be used to 
make the table easier to interpret:

.. code-block:: python

    >>> table3 = """
    ...     SDH     | Rate (Mb/s)   | f1 (kHz)| f2 (kHz) | f3 (kHz)| f4 (MHz)
    ...     --------+---------------+---------+----------+---------+--------
    ...     STM-1   | 155.52        | 0.5     | 6.5      | 65      | 1.3
    ...     STM-4   | 622.08        | 1       | 2.5      | 250     | 5
    ...     STM-16  | 2488.32       | 5       | 100      | 1000    | 20
    ...     STM-64  | 9953.28       | 20      | 400      | 4000    | 80
    ...     STM-256 | 39813.12      | 80      | 1920     | 16000   | 320
    ... """

This looks cleaner, but it is still involves some effort to interpret because 
the values are distant from their corresponding scaling and units, because the 
large and small values are oddly scaled (0.5 kHz is more naturally given as 
500Hz and 39813 MHz is more naturally given as 39.8 GHz), and because each 
column may have a different scaling factor. While these might seem like minor 
inconveniences on this table, they can become quite annoying as tables become 
larger or more numerous. Fundamentally the issue is that the eyes are naturally 
drawn to the number, but the numbers are not complete, and so the eyes need to 
hunt further.  This problem exists with both tables and graphs. The scaling and 
units for the numbers may be found in the column headings, the axes, the labels, 
the title, the caption, or in the body of the text.  The sheer number of places 
to look can dramatically slow the interpretation of the data. This problem does 
not exist in the first table where each number is complete as it includes both 
its scaling and its units. The eye gets the full picture on the first glance.

This last version of the table represents a very common mistake people make when 
presenting data. They feel that adding units and scale factors to each number 
adds clutter and wastes space and so removes them from the data and places them 
somewhere else. Doing so results in a data that perhaps is visually cleaner but 
is harder for the reader to interpret.  All these tables contain the same 
information, but in the second two tables the readability has been traded off in 
order to make the data easier to read into a computer because in most languages 
there is no easy way to read numbers that have either units or scale factors.

*QuanitiPhy* makes it easy to read and generate numbers with units and scale 
factors so you do not have to choose between human and computer readability.  
For example, the above tables could be read with the following code (it must be 
tweaked somewhat to handle tables 2 and 3):

.. code-block:: python

    >>> from quantiphy import Quantity

    >>> sdh = []
    >>> lines = table1.strip().split('\n')
    >>> for line in lines[2:]:
    ...     fields = line.split('|')
    ...     name = fields[0].strip()
    ...     rate = Quantity(fields[1])
    ...     critical_freqs = [Quantity(f) for f in fields[2:]]
    ...     sdh.append((name, rate, critical_freqs))

    >>> for name, rate, freqs in sdh:
    ...     print('{:8s}: {:12s} {:9s} {:9s} {:9s} {}'.format(name, rate, *freqs))
    STM-1   : 155.52 Mb/s  500 Hz    6.5 kHz   65 kHz    1.3 MHz
    STM-4   : 622.08 Mb/s  1 kHz     25 kHz    250 kHz   5 MHz
    STM-16  : 2.4883 Gb/s  5 kHz     100 kHz   1 MHz     20 MHz
    STM-64  : 9.9533 Gb/s  20 kHz    400 kHz   4 MHz     80 MHz
    STM-256 : 39.813 Gb/s  80 kHz    1.92 MHz  16 MHz    320 MHz


    >>> for name, rate, freqs in sdh:
    ...     print('{:8s}: {:.4e} {:.4e} {:.4e} {:.4e} {:.4e}'.format(name, rate, *(1*f for f in freqs)))
    STM-1   : 1.5552e+08 5.0000e+02 6.5000e+03 6.5000e+04 1.3000e+06
    STM-4   : 6.2208e+08 1.0000e+03 2.5000e+04 2.5000e+05 5.0000e+06
    STM-16  : 2.4883e+09 5.0000e+03 1.0000e+05 1.0000e+06 2.0000e+07
    STM-64  : 9.9533e+09 2.0000e+04 4.0000e+05 4.0000e+06 8.0000e+07
    STM-256 : 3.9813e+10 8.0000e+04 1.9200e+06 1.6000e+07 3.2000e+08

The code first reads the data and then produces two outputs.  The first output 
shows that quantities can be displayed in easily readable forms with their units 
and the second output shows that the values are easily accessible for 
computation (the use of ``1*f`` is not necessary to be able to see the results 
in exponential notation, rather it is there to demonstrate that it is easy to do 
calculations on Quantities).

:class:`quantiphy.Quantity` is used to convert a number string, such as '155.52 
Mb/s' into an internal representation that includes the value and the units: 
155.52e6 and 'b/s'.  The scaling factor is properly interpreted. Once a value is 
converted to a Quantity, it can be treated just like a normal float. The main 
difference occurs when it is time to convert it back to a string. When doing so, 
the scale factor and units are included by default.


.. _thermal voltage example:

Thermal Voltage Example
-----------------------

In this example, quantities are used to represent all of the values used to 
compute the thermal voltage: *Vt = kT/q*.

.. code-block:: python

    >>> from quantiphy import Quantity
    >>> Quantity.set_preferences(
    ...     show_label=True,
    ...     label_fmt=('{V:<18}  # {d}', '{n} = {v}')
    ... )

    >>> T = Quantity(300, 'T K ambient temperature')
    >>> k = Quantity('k')
    >>> q = Quantity('q')
    >>> Vt = Quantity(k*T/q, 'Vt V thermal voltage')

    >>> print(T, k, q, Vt, sep='\n')
    T = 300 K           # ambient temperature
    k = 13.806e-24 J/K  # Boltzmann's constant
    q = 160.22e-21 C    # elementary charge
    Vt = 25.852 mV      # thermal voltage

The first part of this example imports :class:`quantiphy.Quantity` and sets the 
*label_fmt* preference to display both the value and the description when upper 
case format codes are used. *label_fmt* is given as a tuple of two strings, the 
first will be used when the description is present, the second is used when it 
is not. In the first string, the ``{V:<16}`` is replaced by the expansion of the 
second string, left justified with a field width of 16, and the ``{d}`` is 
replaced by the description. On the second string the ``{n}`` is replaced by the 
*name* and ``{v}`` is replaced by the value (numeric value and units).

The second part defines four quantities. The first is given in a very specific 
way to avoid the ambiguity between units and scale factors. In this case, the 
temperature is given in Kelvin (K), and normally if the temperature were given 
as the string '300 K', the units would be confused for the scale factor. As 
mentioned in :ref:`ambiguity` the 'K' would be treated as a scale factor unless 
you took explicit steps. In this case, this issue is circumvented by specifying 
the units in the model along with the name and description. The model is also 
used when creating *Vt* to specify the name, units, and description.

The last part simply prints the four values. It uses the :S format specification 
to indicated that the full quantity description should be printed. In this case, 
since all the quantities have descriptions, the first string in *label_fmt* is 
used to format the output.


.. _disk usage example:

Disk Usage Example
------------------

Here is a simple example that uses *QuantiPhy*. It runs the *du* command, which 
prints out the disk usage of files and directories.  The results from *du* are 
gathered and then sorted by size and then the size and name of each item is 
printed.

Quantity is used to scale the filesize reported by *du* from KB to B. Then the 
list of files is sorted by size. Here we are exploiting the fact that quantities 
act like floats, and so the sorting can be done with no extra effort.  Finally, 
the ability to render to a number with a scale factor and units is used when 
presenting the results.

.. code-block:: python

    #!/usr/bin/env python3
    # runs du and sorts the output while suppressing any error messages from du

    from quantiphy import Quantity
    from inform import display, fatal, os_error
    from shlib import Run
    import sys

    try:
        du = Run(['du'] + sys.argv[1:], modes='WEO1')

        files = []
        for line in du.stdout.split('\n'):
            if line:
                size, filename = line.split('\t', 1)
                files += [(Quantity(size, scale=(1000, 'B')), filename)]

        files.sort(key=lambda x: x[0])

        for each in files:
            display(*each, sep='\t')

    except OSError as err:
        fatal(os_error(err))
    except KeyboardInterrupt:
        display('dus: killed by user.')


.. _matplotlib example:

MatPlotLib Example
------------------

In this example *QuantiPhy* is used to create easy to read axis labels in 
MatPlotLib. It uses NumPy to do a spectral analysis of a signal and then 
produces an SVG version of the results using MatPlotLib.

.. code-block:: python

    #!/usr/bin/env python3

    import numpy as np
    from numpy.fft import fft, fftfreq, fftshift
    import matplotlib as mpl
    mpl.use('SVG')
    from matplotlib.ticker import FuncFormatter
    import matplotlib.pyplot as pl
    from quantiphy import Quantity
    Quantity.set_preferences(prec=2)

    # define the axis formatting routines
    def freq_fmt(val, pos):
        return Quantity(val, 'Hz').render()
    freq_formatter = FuncFormatter(freq_fmt)

    def volt_fmt(val, pos):
        return Quantity(val, 'V').render()
    volt_formatter = FuncFormatter(volt_fmt)

    # read the data from delta-sigma.smpl
    data = np.fromfile('delta-sigma.smpl', sep=' ')
    time, wave = data.reshape((2, len(data)//2), order='F')

    # print out basic information about the data
    timestep = Quantity(time[1] - time[0], 's')
    nonperiodicity = Quantity(wave[-1] - wave[0], 'V')
    points = len(time)
    period = Quantity(timestep * len(time), 's')
    freq_res = Quantity(1/period, 'Hz')
    print('timestep:', timestep)
    print('nonperiodicity:', nonperiodicity)
    print('timepoints:', points)
    print('period:', period)
    print('freq resolution:', freq_res)

    # create the window
    window = np.kaiser(len(time), 11)/0.37
        # beta=11 corresponds to alpha=3.5 (beta = pi*alpha)
        # the processing gain with alpha=3.5 is 0.37
    windowed = window*wave

    # transform the data into the frequency domain
    spectrum = 2*fftshift(fft(windowed))/len(time)
    freq = fftshift(fftfreq(len(wave), timestep))

    # generate graphs of the resulting spectrum
    fig = pl.figure()
    ax = fig.add_subplot(111)
    ax.plot(freq, np.absolute(spectrum))
    ax.set_yscale('log')
    ax.xaxis.set_major_formatter(freq_formatter)
    ax.yaxis.set_major_formatter(volt_formatter)
    pl.savefig('spectrum.svg')
    ax.set_xlim((0, 1e6))
    ax.set_ylim((1e-7, 1))
    pl.savefig('spectrum-zoomed.svg')

This script produces the following textual output::

    timestep: 20 ns
    nonperiodicity: 2.3 pV
    timepoints: 28k
    period: 560 us
    freq resolution: 1.79 kHz

And the following is one of the two graphs produced:

..  image:: spectrum-zoomed.png

Notice the axis labels in the generated graph.  Use of *QuantiPhy* makes the 
widely scaled units compact and easy to read.
