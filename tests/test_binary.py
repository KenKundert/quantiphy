# encoding: utf8

# imports {{{1
from quantiphy import Quantity
import pytest

parametrize = pytest.mark.parametrize


# test_reader() {{{1
# test_set {{{2
test_set = """
        0 B;            0 B;            0 B;       0.0000 B;         0.;       0.000000000000 B
        nan;            NaN;            NaN;            NaN;        NaN;                    NaN
      0.5 B;         500 mB;          0.5 B;       0.5000 B;        0.5;       0.500000000000 B
     0.25 B;         250 mB;         0.25 B;       0.2500 B;       0.25;       0.250000000000 B
    0.125 B;         125 mB;        0.125 B;       0.1250 B;      0.125;       0.125000000000 B
   0.0625 B;        62.5 mB;       0.0625 B;       0.0625 B;     0.0625;       0.062500000000 B
        1 B;            1 B;            1 B;       1.0000 B;         1.;       1.000000000000 B
        2 B;            2 B;            2 B;       2.0000 B;         2.;       2.000000000000 B
        4 B;            4 B;            4 B;       4.0000 B;         4.;       4.000000000000 B
        8 B;            8 B;            8 B;       8.0000 B;         8.;       8.000000000000 B
       16 B;           16 B;           16 B;       16.000 B;        16.;       16.00000000000 B
       32 B;           32 B;           32 B;       32.000 B;        32.;       32.00000000000 B
       64 B;           64 B;           64 B;       64.000 B;        64.;       64.00000000000 B
      128 B;          128 B;          128 B;       128.00 B;       128.;       128.0000000000 B
      256 B;          256 B;          256 B;       256.00 B;       256.;       256.0000000000 B
      512 B;          512 B;          512 B;       512.00 B;       512.;       512.0000000000 B
      1 KiB;       1.024 kB;          1 KiB;     1.0000 KiB;        1Ki;     1.000000000000 KiB
      2 KiB;       2.048 kB;          2 KiB;     2.0000 KiB;        2Ki;     2.000000000000 KiB
      4 KiB;       4.096 kB;          4 KiB;     4.0000 KiB;        4Ki;     4.000000000000 KiB
      8 KiB;       8.192 kB;          8 KiB;     8.0000 KiB;        8Ki;     8.000000000000 KiB
     16 KiB;      16.384 kB;         16 KiB;     16.000 KiB;       16Ki;     16.00000000000 KiB
     32 KiB;      32.768 kB;         32 KiB;     32.000 KiB;       32Ki;     32.00000000000 KiB
     64 KiB;      65.536 kB;         64 KiB;     64.000 KiB;       64Ki;     64.00000000000 KiB
    128 KiB;      131.07 kB;        128 KiB;     128.00 KiB;      128Ki;     128.0000000000 KiB
    256 KiB;      262.14 kB;        256 KiB;     256.00 KiB;      256Ki;     256.0000000000 KiB
    512 KiB;      524.29 kB;        512 KiB;     512.00 KiB;      512Ki;     512.0000000000 KiB
      1 MiB;      1.0486 MB;          1 MiB;     1.0000 MiB;        1Mi;     1.000000000000 MiB
      2 MiB;      2.0972 MB;          2 MiB;     2.0000 MiB;        2Mi;     2.000000000000 MiB
      4 MiB;      4.1943 MB;          4 MiB;     4.0000 MiB;        4Mi;     4.000000000000 MiB
      8 MiB;      8.3886 MB;          8 MiB;     8.0000 MiB;        8Mi;     8.000000000000 MiB
     16 MiB;      16.777 MB;         16 MiB;     16.000 MiB;       16Mi;     16.00000000000 MiB
     32 MiB;      33.554 MB;         32 MiB;     32.000 MiB;       32Mi;     32.00000000000 MiB
     64 MiB;      67.109 MB;         64 MiB;     64.000 MiB;       64Mi;     64.00000000000 MiB
    128 MiB;      134.22 MB;        128 MiB;     128.00 MiB;      128Mi;     128.0000000000 MiB
    256 MiB;      268.44 MB;        256 MiB;     256.00 MiB;      256Mi;     256.0000000000 MiB
    512 MiB;      536.87 MB;        512 MiB;     512.00 MiB;      512Mi;     512.0000000000 MiB
      1 GiB;      1.0737 GB;          1 GiB;     1.0000 GiB;        1Gi;     1.000000000000 GiB
      2 GiB;      2.1475 GB;          2 GiB;     2.0000 GiB;        2Gi;     2.000000000000 GiB
      4 GiB;       4.295 GB;          4 GiB;     4.0000 GiB;        4Gi;     4.000000000000 GiB
      8 GiB;      8.5899 GB;          8 GiB;     8.0000 GiB;        8Gi;     8.000000000000 GiB
     16 GiB;       17.18 GB;         16 GiB;     16.000 GiB;       16Gi;     16.00000000000 GiB
     32 GiB;       34.36 GB;         32 GiB;     32.000 GiB;       32Gi;     32.00000000000 GiB
     64 GiB;      68.719 GB;         64 GiB;     64.000 GiB;       64Gi;     64.00000000000 GiB
    128 GiB;      137.44 GB;        128 GiB;     128.00 GiB;      128Gi;     128.0000000000 GiB
    256 GiB;      274.88 GB;        256 GiB;     256.00 GiB;      256Gi;     256.0000000000 GiB
    512 GiB;      549.76 GB;        512 GiB;     512.00 GiB;      512Gi;     512.0000000000 GiB
      1 TiB;      1.0995 TB;          1 TiB;     1.0000 TiB;        1Ti;     1.000000000000 TiB
      2 TiB;       2.199 TB;          2 TiB;     2.0000 TiB;        2Ti;     2.000000000000 TiB
      4 TiB;       4.398 TB;          4 TiB;     4.0000 TiB;        4Ti;     4.000000000000 TiB
      8 TiB;      8.7961 TB;          8 TiB;     8.0000 TiB;        8Ti;     8.000000000000 TiB
     16 TiB;      17.592 TB;         16 TiB;     16.000 TiB;       16Ti;     16.00000000000 TiB
     32 TiB;      35.184 TB;         32 TiB;     32.000 TiB;       32Ti;     32.00000000000 TiB
     64 TiB;      70.369 TB;         64 TiB;     64.000 TiB;       64Ti;     64.00000000000 TiB
    128 TiB;      140.74 TB;        128 TiB;     128.00 TiB;      128Ti;     128.0000000000 TiB
    256 TiB;      281.47 TB;        256 TiB;     256.00 TiB;      256Ti;     256.0000000000 TiB
    512 TiB;      562.95 TB;        512 TiB;     512.00 TiB;      512Ti;     512.0000000000 TiB
      1 PiB;    1.1259e15 B;          1 PiB;     1.0000 PiB;        1Pi;     1.000000000000 PiB
      2 PiB;    2.2518e15 B;          2 PiB;     2.0000 PiB;        2Pi;     2.000000000000 PiB
      4 PiB;    4.5036e15 B;          4 PiB;     4.0000 PiB;        4Pi;     4.000000000000 PiB
      8 PiB;    9.0072e15 B;          8 PiB;     8.0000 PiB;        8Pi;     8.000000000000 PiB
     16 PiB;    18.014e15 B;         16 PiB;     16.000 PiB;       16Pi;     16.00000000000 PiB
     32 PiB;    36.029e15 B;         32 PiB;     32.000 PiB;       32Pi;     32.00000000000 PiB
     64 PiB;    72.058e15 B;         64 PiB;     64.000 PiB;       64Pi;     64.00000000000 PiB
    128 PiB;    144.12e15 B;        128 PiB;     128.00 PiB;      128Pi;     128.0000000000 PiB
    256 PiB;    288.23e15 B;        256 PiB;     256.00 PiB;      256Pi;     256.0000000000 PiB
    512 PiB;    576.46e15 B;        512 PiB;     512.00 PiB;      512Pi;     512.0000000000 PiB
      1 EiB;    1.1529e18 B;          1 EiB;     1.0000 EiB;        1Ei;     1.000000000000 EiB
      2 EiB;    2.3058e18 B;          2 EiB;     2.0000 EiB;        2Ei;     2.000000000000 EiB
      4 EiB;    4.6117e18 B;          4 EiB;     4.0000 EiB;        4Ei;     4.000000000000 EiB
      8 EiB;    9.2234e18 B;          8 EiB;     8.0000 EiB;        8Ei;     8.000000000000 EiB
     16 EiB;    18.447e18 B;         16 EiB;     16.000 EiB;       16Ei;     16.00000000000 EiB
     32 EiB;    36.893e18 B;         32 EiB;     32.000 EiB;       32Ei;     32.00000000000 EiB
     64 EiB;    73.787e18 B;         64 EiB;     64.000 EiB;       64Ei;     64.00000000000 EiB
    128 EiB;    147.57e18 B;        128 EiB;     128.00 EiB;      128Ei;     128.0000000000 EiB
    256 EiB;    295.15e18 B;        256 EiB;     256.00 EiB;      256Ei;     256.0000000000 EiB
    512 EiB;     590.3e18 B;        512 EiB;     512.00 EiB;      512Ei;     512.0000000000 EiB
      1 ZiB;    1.1806e21 B;          1 ZiB;     1.0000 ZiB;        1Zi;     1.000000000000 ZiB
      2 ZiB;    2.3612e21 B;          2 ZiB;     2.0000 ZiB;        2Zi;     2.000000000000 ZiB
      4 ZiB;    4.7224e21 B;          4 ZiB;     4.0000 ZiB;        4Zi;     4.000000000000 ZiB
      8 ZiB;    9.4447e21 B;          8 ZiB;     8.0000 ZiB;        8Zi;     8.000000000000 ZiB
     16 ZiB;    18.889e21 B;         16 ZiB;     16.000 ZiB;       16Zi;     16.00000000000 ZiB
     32 ZiB;    37.779e21 B;         32 ZiB;     32.000 ZiB;       32Zi;     32.00000000000 ZiB
     64 ZiB;    75.558e21 B;         64 ZiB;     64.000 ZiB;       64Zi;     64.00000000000 ZiB
    128 ZiB;    151.12e21 B;        128 ZiB;     128.00 ZiB;      128Zi;     128.0000000000 ZiB
    256 ZiB;    302.23e21 B;        256 ZiB;     256.00 ZiB;      256Zi;     256.0000000000 ZiB
    512 ZiB;    604.46e21 B;        512 ZiB;     512.00 ZiB;      512Zi;     512.0000000000 ZiB
      1 YiB;    1.2089e24 B;          1 YiB;     1.0000 YiB;        1Yi;     1.000000000000 YiB
      2 YiB;    2.4179e24 B;          2 YiB;     2.0000 YiB;        2Yi;     2.000000000000 YiB
      4 YiB;    4.8357e24 B;          4 YiB;     4.0000 YiB;        4Yi;     4.000000000000 YiB
      8 YiB;    9.6714e24 B;          8 YiB;     8.0000 YiB;        8Yi;     8.000000000000 YiB
     16 YiB;    19.343e24 B;         16 YiB;     16.000 YiB;       16Yi;     16.00000000000 YiB
     32 YiB;    38.686e24 B;         32 YiB;     32.000 YiB;       32Yi;     32.00000000000 YiB
     64 YiB;    77.371e24 B;         64 YiB;     64.000 YiB;       64Yi;     64.00000000000 YiB
    128 YiB;    154.74e24 B;        128 YiB;     128.00 YiB;      128Yi;     128.0000000000 YiB
    256 YiB;    309.49e24 B;        256 YiB;     256.00 YiB;      256Yi;     256.0000000000 YiB
    512 YiB;    618.97e24 B;        512 YiB;     512.00 YiB;      512Yi;     512.0000000000 YiB
      1 RiB;    1.2379e27 B;          1 RiB;     1.0000 RiB;        1Ri;     1.000000000000 RiB
      2 RiB;    2.4759e27 B;          2 RiB;     2.0000 RiB;        2Ri;     2.000000000000 RiB
      4 RiB;    4.9518e27 B;          4 RiB;     4.0000 RiB;        4Ri;     4.000000000000 RiB
      8 RiB;    9.9035e27 B;          8 RiB;     8.0000 RiB;        8Ri;     8.000000000000 RiB
     16 RiB;    19.807e27 B;         16 RiB;     16.000 RiB;       16Ri;     16.00000000000 RiB
     32 RiB;    39.614e27 B;         32 RiB;     32.000 RiB;       32Ri;     32.00000000000 RiB
     64 RiB;    79.228e27 B;         64 RiB;     64.000 RiB;       64Ri;     64.00000000000 RiB
    128 RiB;    158.46e27 B;        128 RiB;     128.00 RiB;      128Ri;     128.0000000000 RiB
    256 RiB;    316.91e27 B;        256 RiB;     256.00 RiB;      256Ri;     256.0000000000 RiB
    512 RiB;    633.83e27 B;        512 RiB;     512.00 RiB;      512Ri;     512.0000000000 RiB
      1 QiB;    1.2677e30 B;          1 QiB;     1.0000 QiB;        1Qi;     1.000000000000 QiB
      2 QiB;    2.5353e30 B;          2 QiB;     2.0000 QiB;        2Qi;     2.000000000000 QiB
      4 QiB;    5.0706e30 B;          4 QiB;     4.0000 QiB;        4Qi;     4.000000000000 QiB
      8 QiB;    10.141e30 B;          8 QiB;     8.0000 QiB;        8Qi;     8.000000000000 QiB
     16 QiB;    20.282e30 B;         16 QiB;     16.000 QiB;       16Qi;     16.00000000000 QiB
     32 QiB;    40.565e30 B;         32 QiB;     32.000 QiB;       32Qi;     32.00000000000 QiB
     64 QiB;     81.13e30 B;         64 QiB;     64.000 QiB;       64Qi;     64.00000000000 QiB
    128 QiB;    162.26e30 B;        128 QiB;     128.00 QiB;      128Qi;     128.0000000000 QiB
    256 QiB;    324.52e30 B;        256 QiB;     256.00 QiB;      256Qi;     256.0000000000 QiB
    512 QiB;    649.04e30 B;        512 QiB;     512.00 QiB;      512Qi;     512.0000000000 QiB
   1024 QiB;    1.2981e33 B;   1.2981e+33 B;   1.2981e+33 B; 1.2981e+33;     1.298074214634e+33 B
     -1 KiB;      -1.024 kB;         -1 KiB;    -1.0000 KiB;       -1Ki;    -1.000000000000 KiB
     -1 MiB;     -1.0486 MB;         -1 MiB;    -1.0000 MiB;       -1Mi;    -1.000000000000 MiB
     -1 GiB;     -1.0737 GB;         -1 GiB;    -1.0000 GiB;       -1Gi;    -1.000000000000 GiB
     -1 TiB;     -1.0995 TB;         -1 TiB;    -1.0000 TiB;       -1Ti;    -1.000000000000 TiB
     -1 PiB;   -1.1259e15 B;         -1 PiB;    -1.0000 PiB;       -1Pi;    -1.000000000000 PiB
     -1 EiB;   -1.1529e18 B;         -1 EiB;    -1.0000 EiB;       -1Ei;    -1.000000000000 EiB
     -1 ZiB;   -1.1806e21 B;         -1 ZiB;    -1.0000 ZiB;       -1Zi;    -1.000000000000 ZiB
     -1 YiB;   -1.2089e24 B;         -1 YiB;    -1.0000 YiB;       -1Yi;    -1.000000000000 YiB
     -1 RiB;   -1.2379e27 B;         -1 RiB;    -1.0000 RiB;       -1Ri;    -1.000000000000 RiB
     -1 QiB;   -1.2677e30 B;         -1 QiB;    -1.0000 QiB;       -1Qi;    -1.000000000000 QiB
          h; 662.61e-36 J-s;          0 J-s;     0.0000 J-s;         0.;     0.000000000000 J-s
       hbar; 105.46e-36 J-s;          0 J-s;     0.0000 J-s;         0.;     0.000000000000 J-s
          k; 13.806e-24 J/K;          0 J/K;     0.0000 J/K;         0.;     0.000000000000 J/K
          q;   160.22e-21 C;            0 C;       0.0000 C;         0.;       0.000000000000 C
          c;    299.79 Mm/s;    285.9 Mim/s;   285.90 Mim/s;    285.9Mi;   285.9043674469 Mim/s
         0C;       273.15 K;       273.15 K;       273.15 K;     273.15;       273.1500000000 K
       eps0;    8.8542 pF/m;          0 F/m;     0.0000 F/m;         0.;     0.000000000009 F/m
        mu0;    1.2566 uH/m;          0 H/m;     0.0000 H/m;         0.;     0.000001256637 H/m
         Z0;    376.73 Ohms;    376.73 Ohms;    376.73 Ohms;     376.73;    376.7303136680 Ohms
     1Zippy;        1 Zippy;        1 Zippy;   1.0000 Zippy;         1.;   1.000000000000 Zippy
""".strip()

# code {{{2
@parametrize(
    "given, expected_1, expected_2, expected_3, expected_4, expected_5",
    [tuple(v.strip() for v in line.split(";")) for line in test_set.splitlines()]
)
def test_reader(given, expected_1, expected_2, expected_3, expected_4, expected_5):
    Quantity.reset_prefs()
    with Quantity.prefs(known_units = 'Zippy'):
        print(
            f'Trying: given={given}:',
            f'expected_1={expected_1},',
            f'expected_2={expected_2},',
            f'expected_3={expected_3},',
            f'expected_4={expected_4},',
            f'expected_5={expected_5}'
        )
        q = Quantity(given, binary=True)

        result = str(q)
        issue = f'{given}: expected “{expected_1}”, got “{result}”.'
        assert expected_1 == result, issue

        result = q.binary()
        issue = f'{given}: expected “{expected_2}”, got “{result}”.'
        assert expected_2 == result, issue

        result = q.binary(prec=4, strip_zeros=False)
        issue = f'{given}: expected “{expected_3}”, got “{result}”.'
        assert expected_3 == result, issue

        result = q.binary(strip_zeros=True, strip_radix=False, show_units=False)
        issue = f'{given}: expected “{expected_4}”, got “{result}”.'
        assert expected_4 == result, issue

        result = q.binary(prec='full', strip_zeros=False)
        issue = f'{given}: expected “{expected_5}”, got “{result}”.'
        assert expected_5 == result, issue

# test_writer() {{{1
def test_writer():
    Quantity.reset_prefs()
    q = Quantity('mem = 1GiB', binary=True)

    result = str(q)
    expected = '1.0737 GB'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    result = q.binary()
    expected = '1 GiB'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    result = q.render(form='binary')
    expected = '1 GiB'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    result = f'{q:b}'
    expected = '1 GiB'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    result = q.binary(prec=2, strip_zeros=False)
    expected = '1.00 GiB'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    result = f'{q:#0.2b}'
    expected = '1.00 GiB'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    result = q.binary(show_label=True)
    expected = 'mem = 1 GiB'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    result = f'{q:B}'
    expected = 'mem = 1 GiB'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    result = q.binary(show_label=True, scale='b')
    expected = 'mem = 8 Gib'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    result = f'{q:Bb}'
    expected = 'mem = 8 Gib'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    result = q.binary(strip_zeros=False)
    expected = '1.0000 GiB'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    result = f'{q:#b}'
    expected = '1.0000 GiB'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    result = q.binary(strip_zeros=True, strip_radix=False)
    expected = '1 GiB'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    q = Quantity('1GB', binary=True)

    result = str(q)
    expected = '1 GB'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    result = q.binary()
    expected = '953.67 MiB'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    result = f'{q:b}'
    expected = '953.67 MiB'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    result = q.binary(prec=2)
    expected = '954 MiB'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    result = f'{q:0.2b}'
    expected = '954 MiB'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

# test_writer_prec() {{{1
# test_set {{{2
test_set = """
     931.32 pB;        0 B;        0 B;        0 B;        0 B;        0 B
     1.8626 nB;        0 B;        0 B;        0 B;        0 B;        0 B
     3.7253 nB;        0 B;        0 B;        0 B;        0 B;        0 B
     7.4506 nB;        0 B;        0 B;        0 B;        0 B;        0 B
     14.901 nB;        0 B;        0 B;        0 B;        0 B;        0 B
     29.802 nB;        0 B;        0 B;        0 B;        0 B;        0 B
     59.605 nB;        0 B;        0 B;        0 B;        0 B;        0 B
     119.21 nB;        0 B;        0 B;        0 B;        0 B;        0 B
     238.42 nB;        0 B;        0 B;        0 B;        0 B;        0 B
     476.84 nB;        0 B;        0 B;        0 B;        0 B;        0 B
     953.67 nB;        0 B;        0 B;        0 B;        0 B;        0 B
     1.9073 uB;        0 B;        0 B;        0 B;        0 B;        0 B
     3.8147 uB;        0 B;        0 B;        0 B;        0 B;        0 B
     7.6294 uB;        0 B;        0 B;        0 B;        0 B;        0 B
     15.259 uB;        0 B;        0 B;        0 B;        0 B;        0 B
     30.518 uB;        0 B;        0 B;        0 B;        0 B;        0 B
     61.035 uB;        0 B;        0 B;        0 B;        0 B;   0.0001 B
     122.07 uB;        0 B;        0 B;        0 B;        0 B;   0.0001 B
     244.14 uB;        0 B;        0 B;        0 B;        0 B;   0.0002 B
     488.28 uB;        0 B;        0 B;        0 B;        0 B;   0.0005 B
     976.56 uB;        0 B;        0 B;        0 B;    0.001 B;    0.001 B
     1.9531 mB;        0 B;        0 B;        0 B;    0.002 B;    0.002 B
     3.9062 mB;        0 B;        0 B;        0 B;    0.004 B;   0.0039 B
     7.8125 mB;        0 B;        0 B;     0.01 B;    0.008 B;   0.0078 B
     15.625 mB;        0 B;        0 B;     0.02 B;    0.016 B;   0.0156 B
      31.25 mB;        0 B;        0 B;     0.03 B;    0.031 B;   0.0312 B
       62.5 mB;        0 B;      0.1 B;     0.06 B;    0.062 B;   0.0625 B
        125 mB;        0 B;      0.1 B;     0.12 B;    0.125 B;    0.125 B
        250 mB;        0 B;      0.2 B;     0.25 B;     0.25 B;     0.25 B
        500 mB;        0 B;      0.5 B;      0.5 B;      0.5 B;      0.5 B
           1 B;        1 B;        1 B;        1 B;        1 B;        1 B
           2 B;        2 B;        2 B;        2 B;        2 B;        2 B
           4 B;        4 B;        4 B;        4 B;        4 B;        4 B
           8 B;        8 B;        8 B;        8 B;        8 B;        8 B
          16 B;       20 B;       16 B;       16 B;       16 B;       16 B
          32 B;       30 B;       32 B;       32 B;       32 B;       32 B
          64 B;       60 B;       64 B;       64 B;       64 B;       64 B
         128 B;      100 B;      130 B;      128 B;      128 B;      128 B
         256 B;      300 B;      260 B;      256 B;      256 B;      256 B
         512 B;      500 B;      510 B;      512 B;      512 B;      512 B
      1.024 kB;      1 KiB;      1 KiB;      1 KiB;      1 KiB;      1 KiB
      2.048 kB;      2 KiB;      2 KiB;      2 KiB;      2 KiB;      2 KiB
      4.096 kB;      4 KiB;      4 KiB;      4 KiB;      4 KiB;      4 KiB
      8.192 kB;      8 KiB;      8 KiB;      8 KiB;      8 KiB;      8 KiB
     16.384 kB;     20 KiB;     16 KiB;     16 KiB;     16 KiB;     16 KiB
     32.768 kB;     30 KiB;     32 KiB;     32 KiB;     32 KiB;     32 KiB
     65.536 kB;     60 KiB;     64 KiB;     64 KiB;     64 KiB;     64 KiB
     131.07 kB;    100 KiB;    130 KiB;    128 KiB;    128 KiB;    128 KiB
     262.14 kB;    300 KiB;    260 KiB;    256 KiB;    256 KiB;    256 KiB
     524.29 kB;    500 KiB;    510 KiB;    512 KiB;    512 KiB;    512 KiB
     1.0486 MB;      1 MiB;      1 MiB;      1 MiB;      1 MiB;      1 MiB
     2.0972 MB;      2 MiB;      2 MiB;      2 MiB;      2 MiB;      2 MiB
     4.1943 MB;      4 MiB;      4 MiB;      4 MiB;      4 MiB;      4 MiB
     8.3886 MB;      8 MiB;      8 MiB;      8 MiB;      8 MiB;      8 MiB
     16.777 MB;     20 MiB;     16 MiB;     16 MiB;     16 MiB;     16 MiB
     33.554 MB;     30 MiB;     32 MiB;     32 MiB;     32 MiB;     32 MiB
     67.109 MB;     60 MiB;     64 MiB;     64 MiB;     64 MiB;     64 MiB
     134.22 MB;    100 MiB;    130 MiB;    128 MiB;    128 MiB;    128 MiB
     268.44 MB;    300 MiB;    260 MiB;    256 MiB;    256 MiB;    256 MiB
     536.87 MB;    500 MiB;    510 MiB;    512 MiB;    512 MiB;    512 MiB
     1.0737 GB;   1000 MiB;   1000 MiB;   1020 MiB;   1024 MiB;   1024 MiB
     2.1475 GB;      2 GiB;      2 GiB;      2 GiB;      2 GiB;      2 GiB
      4.295 GB;      4 GiB;      4 GiB;      4 GiB;      4 GiB;      4 GiB
     8.5899 GB;      8 GiB;      8 GiB;      8 GiB;      8 GiB;      8 GiB
      17.18 GB;     20 GiB;     16 GiB;     16 GiB;     16 GiB;     16 GiB
      34.36 GB;     30 GiB;     32 GiB;     32 GiB;     32 GiB;     32 GiB
     68.719 GB;     60 GiB;     64 GiB;     64 GiB;     64 GiB;     64 GiB
     137.44 GB;    100 GiB;    130 GiB;    128 GiB;    128 GiB;    128 GiB
     274.88 GB;    300 GiB;    260 GiB;    256 GiB;    256 GiB;    256 GiB
     549.76 GB;    500 GiB;    510 GiB;    512 GiB;    512 GiB;    512 GiB
    1.09955 TB;      1 TiB;      1 TiB;      1 TiB;      1 TiB;      1 TiB
      2.199 TB;      2 TiB;      2 TiB;      2 TiB;      2 TiB;      2 TiB
      4.398 TB;      4 TiB;      4 TiB;      4 TiB;      4 TiB;      4 TiB
     8.7961 TB;      8 TiB;      8 TiB;      8 TiB;      8 TiB;      8 TiB
     17.592 TB;     20 TiB;     16 TiB;     16 TiB;     16 TiB;     16 TiB
     35.184 TB;     30 TiB;     32 TiB;     32 TiB;     32 TiB;     32 TiB
     70.369 TB;     60 TiB;     64 TiB;     64 TiB;     64 TiB;     64 TiB
     140.74 TB;    100 TiB;    130 TiB;    128 TiB;    128 TiB;    128 TiB
     281.47 TB;    300 TiB;    260 TiB;    256 TiB;    256 TiB;    256 TiB
     562.95 TB;    500 TiB;    510 TiB;    512 TiB;    512 TiB;    512 TiB
     1.1259 PB;      1 PiB;      1 PiB;      1 PiB;      1 PiB;      1 PiB
     2.2518 PB;      2 PiB;      2 PiB;      2 PiB;      2 PiB;      2 PiB
     4.5036 PB;      4 PiB;      4 PiB;      4 PiB;      4 PiB;      4 PiB
     9.0072 PB;      8 PiB;      8 PiB;      8 PiB;      8 PiB;      8 PiB
     18.014 PB;     20 PiB;     16 PiB;     16 PiB;     16 PiB;     16 PiB
     36.029 PB;     30 PiB;     32 PiB;     32 PiB;     32 PiB;     32 PiB
     72.058 PB;     60 PiB;     64 PiB;     64 PiB;     64 PiB;     64 PiB
     144.12 PB;    100 PiB;    130 PiB;    128 PiB;    128 PiB;    128 PiB
     288.23 PB;    300 PiB;    260 PiB;    256 PiB;    256 PiB;    256 PiB
     576.46 PB;    500 PiB;    510 PiB;    512 PiB;    512 PiB;    512 PiB
    1.15295 EB;      1 EiB;      1 EiB;      1 EiB;      1 EiB;      1 EiB
     2.3058 EB;      2 EiB;      2 EiB;      2 EiB;      2 EiB;      2 EiB
     4.6117 EB;      4 EiB;      4 EiB;      4 EiB;      4 EiB;      4 EiB
     9.2234 EB;      8 EiB;      8 EiB;      8 EiB;      8 EiB;      8 EiB
     18.447 EB;     20 EiB;     16 EiB;     16 EiB;     16 EiB;     16 EiB
     36.893 EB;     30 EiB;     32 EiB;     32 EiB;     32 EiB;     32 EiB
     73.787 EB;     60 EiB;     64 EiB;     64 EiB;     64 EiB;     64 EiB
     147.57 EB;    100 EiB;    130 EiB;    128 EiB;    128 EiB;    128 EiB
     295.15 EB;    300 EiB;    260 EiB;    256 EiB;    256 EiB;    256 EiB
      590.3 EB;    500 EiB;    510 EiB;    512 EiB;    512 EiB;    512 EiB
     1.1806 ZB;      1 ZiB;      1 ZiB;      1 ZiB;      1 ZiB;      1 ZiB
     2.3612 ZB;      2 ZiB;      2 ZiB;      2 ZiB;      2 ZiB;      2 ZiB
     4.7224 ZB;      4 ZiB;      4 ZiB;      4 ZiB;      4 ZiB;      4 ZiB
     9.4447 ZB;      8 ZiB;      8 ZiB;      8 ZiB;      8 ZiB;      8 ZiB
     18.889 ZB;     20 ZiB;     16 ZiB;     16 ZiB;     16 ZiB;     16 ZiB
     37.779 ZB;     30 ZiB;     32 ZiB;     32 ZiB;     32 ZiB;     32 ZiB
     75.558 ZB;     60 ZiB;     64 ZiB;     64 ZiB;     64 ZiB;     64 ZiB
     151.12 ZB;    100 ZiB;    130 ZiB;    128 ZiB;    128 ZiB;    128 ZiB
     302.23 ZB;    300 ZiB;    260 ZiB;    256 ZiB;    256 ZiB;    256 ZiB
     604.46 ZB;    500 ZiB;    510 ZiB;    512 ZiB;    512 ZiB;    512 ZiB
    1.20895 YB;      1 YiB;      1 YiB;      1 YiB;      1 YiB;      1 YiB
     2.4179 YB;      2 YiB;      2 YiB;      2 YiB;      2 YiB;      2 YiB
     4.8357 YB;      4 YiB;      4 YiB;      4 YiB;      4 YiB;      4 YiB
     9.6714 YB;      8 YiB;      8 YiB;      8 YiB;      8 YiB;      8 YiB
     19.343 YB;     20 YiB;     16 YiB;     16 YiB;     16 YiB;     16 YiB
     38.686 YB;     30 YiB;     32 YiB;     32 YiB;     32 YiB;     32 YiB
     77.371 YB;     60 YiB;     64 YiB;     64 YiB;     64 YiB;     64 YiB
     154.74 YB;    100 YiB;    130 YiB;    128 YiB;    128 YiB;    128 YiB
     309.49 YB;    300 YiB;    260 YiB;    256 YiB;    256 YiB;    256 YiB
     618.97 YB;    500 YiB;    510 YiB;    512 YiB;    512 YiB;    512 YiB
    1.23795 RB;      1 RiB;      1 RiB;      1 RiB;      1 RiB;      1 RiB
     2.4759 RB;      2 RiB;      2 RiB;      2 RiB;      2 RiB;      2 RiB
     4.9518 RB;      4 RiB;      4 RiB;      4 RiB;      4 RiB;      4 RiB
     9.9035 RB;      8 RiB;      8 RiB;      8 RiB;      8 RiB;      8 RiB
     19.807 RB;     20 RiB;     16 RiB;     16 RiB;     16 RiB;     16 RiB
     39.614 RB;     30 RiB;     32 RiB;     32 RiB;     32 RiB;     32 RiB
     79.228 RB;     60 RiB;     64 RiB;     64 RiB;     64 RiB;     64 RiB
     158.46 RB;    100 RiB;    130 RiB;    128 RiB;    128 RiB;    128 RiB
     316.91 RB;    300 RiB;    260 RiB;    256 RiB;    256 RiB;    256 RiB
     633.83 RB;    500 RiB;    510 RiB;    512 RiB;    512 RiB;    512 RiB
     1.2677 QB;      1 QiB;      1 QiB;      1 QiB;      1 QiB;      1 QiB
     2.5353 QB;      2 QiB;      2 QiB;      2 QiB;      2 QiB;      2 QiB
     5.0706 QB;      4 QiB;      4 QiB;      4 QiB;      4 QiB;      4 QiB
    10.1412 QB;      8 QiB;      8 QiB;      8 QiB;      8 QiB;      8 QiB
     20.282 QB;     20 QiB;     16 QiB;     16 QiB;     16 QiB;     16 QiB
     40.565 QB;     30 QiB;     32 QiB;     32 QiB;     32 QiB;     32 QiB
      81.13 QB;     60 QiB;     64 QiB;     64 QiB;     64 QiB;     64 QiB
     162.26 QB;    100 QiB;    130 QiB;    128 QiB;    128 QiB;    128 QiB
     324.52 QB;    300 QiB;    260 QiB;    256 QiB;    256 QiB;    256 QiB
     649.04 QB;    500 QiB;    510 QiB;    512 QiB;    512 QiB;    512 QiB
     1298.1 QB;    1e+33 B;  1.3e+33 B;  1.3e+33 B;1.298e+33 B;1.2981e+33 B
     2596.1 QB;    3e+33 B;  2.6e+33 B;  2.6e+33 B;2.596e+33 B;2.5961e+33 B
     5192.3 QB;    5e+33 B;  5.2e+33 B; 5.19e+33 B;5.192e+33 B;5.1923e+33 B
      10385 QB;    1e+34 B;    1e+34 B; 1.04e+34 B;1.038e+34 B;1.0385e+34 B
          1 uB;        0 B;        0 B;        0 B;        0 B;        0 B
         10 uB;        0 B;        0 B;        0 B;        0 B;        0 B
        100 uB;        0 B;        0 B;        0 B;        0 B;   0.0001 B
          1 mB;        0 B;        0 B;        0 B;    0.001 B;    0.001 B
         10 mB;        0 B;        0 B;     0.01 B;     0.01 B;     0.01 B
        100 mB;        0 B;      0.1 B;      0.1 B;      0.1 B;      0.1 B
           1 B;        1 B;        1 B;        1 B;        1 B;        1 B
          10 B;       10 B;       10 B;       10 B;       10 B;       10 B
         100 B;      100 B;      100 B;      100 B;      100 B;      100 B
          1 kB;     1000 B;     1000 B;     1000 B;     1000 B;     1000 B
         10 kB;     10 KiB;    9.8 KiB;   9.77 KiB;  9.766 KiB; 9.7656 KiB
        100 kB;    100 KiB;     98 KiB;   97.7 KiB;  97.66 KiB; 97.656 KiB
          1 MB;   1000 KiB;    980 KiB;    977 KiB;  976.6 KiB; 976.56 KiB
""".strip()

# code {{{2
@parametrize(
    "given, expected_1, expected_2, expected_3, expected_4, expected_5",
    [tuple(v.strip() for v in line.split(";")) for line in test_set.splitlines()]
)
def test_writer_prec(given, expected_1, expected_2, expected_3, expected_4, expected_5):
    Quantity.reset_prefs()
    print(
        f'Trying: given={given}:',
        f'expected_1={expected_1},',
        f'expected_2={expected_2},',
        f'expected_3={expected_3},',
        f'expected_4={expected_4},',
        f'expected_5={expected_5}'
    )
    q = Quantity(given)

    result = q.binary(prec=0)
    issue = f'{given}: expected “{expected_1}”, got “{result}”.'
    assert result == expected_1, issue

    result = q.binary(prec=1)
    issue = f'{given}: expected “{expected_2}”, got “{result}”.'
    assert result == expected_2, issue

    result = q.binary(prec=2)
    issue = f'{given}: expected “{expected_3}”, got “{result}”.'
    assert result == expected_3, issue

    result = q.binary(prec=3)
    issue = f'{given}: expected “{expected_4}”, got “{result}”.'
    assert result == expected_4, issue

    result = q.binary(prec=4)
    issue = f'{given}: expected “{expected_5}”, got “{result}”.'
    assert result == expected_5, issue


# test_writer_cover() {{{1
def test_writer_cover():
    Quantity.reset_prefs()

    q = Quantity('mem = 0.5B', binary=True)
    result = q.binary(strip_radix='cover', strip_zeros=True, prec=5)
    expected = '0.5 B'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    q = Quantity('mem = 8B', binary=True)
    result = q.binary(strip_radix='cover', strip_zeros=True, prec=5)
    expected = '8.0 B'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    q = Quantity('mem = 64 B', binary=True)
    result = q.binary(strip_radix='cover', strip_zeros=True, prec=5)
    expected = '64.0 B'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    q = Quantity('mem = 512 B', binary=True)
    result = q.binary(strip_radix='cover', strip_zeros=True, prec=5)
    expected = '512.0 B'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

    q = Quantity('mem = 4,096 B', binary=True)
    result = q.binary(strip_radix='cover', strip_zeros=True, prec=5)
    expected = '4 KiB'
    assert result == expected, f'{given}: expected “{expected}”, got “{result}”.'

if __name__ == '__main__':
    # As a debugging aid allow the tests to be run on their own, outside pytest.
    # This makes it easier to see and interpret and textual output.

    defined = dict(globals())
    for k, v in defined.items():
        if callable(v) and k.startswith('test_'):
            print()
            print('Calling:', k)
            print((len(k)+9)*'=')
            v()
