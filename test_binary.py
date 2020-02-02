# encoding: utf8

data1 = """
         0B;            0 B;            0 B;       0.0000 B;         0.;       0.000000000000 B
        nan;            NaN;            NaN;            NaN;        NaN;                    NaN
       0.5B;         500 mB;          0.5 B;       0.5000 B;        0.5;       0.500000000000 B
      0.25B;         250 mB;         0.25 B;       0.2500 B;       0.25;       0.250000000000 B
     0.125B;         125 mB;        0.125 B;       0.1250 B;      0.125;       0.125000000000 B
    0.0625B;        62.5 mB;       0.0625 B;       0.0625 B;     0.0625;       0.062500000000 B
         1B;            1 B;            1 B;       1.0000 B;         1.;       1.000000000000 B
         2B;            2 B;            2 B;       2.0000 B;         2.;       2.000000000000 B
         4B;            4 B;            4 B;       4.0000 B;         4.;       4.000000000000 B
         8B;            8 B;            8 B;       8.0000 B;         8.;       8.000000000000 B
        16B;           16 B;           16 B;       16.000 B;        16.;       16.00000000000 B
        32B;           32 B;           32 B;       32.000 B;        32.;       32.00000000000 B
        64B;           64 B;           64 B;       64.000 B;        64.;       64.00000000000 B
       128B;          128 B;          128 B;       128.00 B;       128.;       128.0000000000 B
       256B;          256 B;          256 B;       256.00 B;       256.;       256.0000000000 B
       512B;          512 B;          512 B;       512.00 B;       512.;       512.0000000000 B
       1KiB;       1.024 kB;          1 KiB;     1.0000 KiB;       1.Ki;     1.000000000000 KiB
       2KiB;       2.048 kB;          2 KiB;     2.0000 KiB;       2.Ki;     2.000000000000 KiB
       4KiB;       4.096 kB;          4 KiB;     4.0000 KiB;       4.Ki;     4.000000000000 KiB
       8KiB;       8.192 kB;          8 KiB;     8.0000 KiB;       8.Ki;     8.000000000000 KiB
      16KiB;      16.384 kB;         16 KiB;     16.000 KiB;      16.Ki;     16.00000000000 KiB
      32KiB;      32.768 kB;         32 KiB;     32.000 KiB;      32.Ki;     32.00000000000 KiB
      64KiB;      65.536 kB;         64 KiB;     64.000 KiB;      64.Ki;     64.00000000000 KiB
     128KiB;      131.07 kB;        128 KiB;     128.00 KiB;     128.Ki;     128.0000000000 KiB
     256KiB;      262.14 kB;        256 KiB;     256.00 KiB;     256.Ki;     256.0000000000 KiB
     512KiB;      524.29 kB;        512 KiB;     512.00 KiB;     512.Ki;     512.0000000000 KiB
       1MiB;      1.0486 MB;          1 MiB;     1.0000 MiB;       1.Mi;     1.000000000000 MiB
       2MiB;      2.0972 MB;          2 MiB;     2.0000 MiB;       2.Mi;     2.000000000000 MiB
       4MiB;      4.1943 MB;          4 MiB;     4.0000 MiB;       4.Mi;     4.000000000000 MiB
       8MiB;      8.3886 MB;          8 MiB;     8.0000 MiB;       8.Mi;     8.000000000000 MiB
      16MiB;      16.777 MB;         16 MiB;     16.000 MiB;      16.Mi;     16.00000000000 MiB
      32MiB;      33.554 MB;         32 MiB;     32.000 MiB;      32.Mi;     32.00000000000 MiB
      64MiB;      67.109 MB;         64 MiB;     64.000 MiB;      64.Mi;     64.00000000000 MiB
     128MiB;      134.22 MB;        128 MiB;     128.00 MiB;     128.Mi;     128.0000000000 MiB
     256MiB;      268.44 MB;        256 MiB;     256.00 MiB;     256.Mi;     256.0000000000 MiB
     512MiB;      536.87 MB;        512 MiB;     512.00 MiB;     512.Mi;     512.0000000000 MiB
       1GiB;      1.0737 GB;          1 GiB;     1.0000 GiB;       1.Gi;     1.000000000000 GiB
       2GiB;      2.1475 GB;          2 GiB;     2.0000 GiB;       2.Gi;     2.000000000000 GiB
       4GiB;       4.295 GB;          4 GiB;     4.0000 GiB;       4.Gi;     4.000000000000 GiB
       8GiB;      8.5899 GB;          8 GiB;     8.0000 GiB;       8.Gi;     8.000000000000 GiB
      16GiB;       17.18 GB;         16 GiB;     16.000 GiB;      16.Gi;     16.00000000000 GiB
      32GiB;       34.36 GB;         32 GiB;     32.000 GiB;      32.Gi;     32.00000000000 GiB
      64GiB;      68.719 GB;         64 GiB;     64.000 GiB;      64.Gi;     64.00000000000 GiB
     128GiB;      137.44 GB;        128 GiB;     128.00 GiB;     128.Gi;     128.0000000000 GiB
     256GiB;      274.88 GB;        256 GiB;     256.00 GiB;     256.Gi;     256.0000000000 GiB
     512GiB;      549.76 GB;        512 GiB;     512.00 GiB;     512.Gi;     512.0000000000 GiB
       1TiB;      1.0995 TB;          1 TiB;     1.0000 TiB;       1.Ti;     1.000000000000 TiB
       2TiB;       2.199 TB;          2 TiB;     2.0000 TiB;       2.Ti;     2.000000000000 TiB
       4TiB;       4.398 TB;          4 TiB;     4.0000 TiB;       4.Ti;     4.000000000000 TiB
       8TiB;      8.7961 TB;          8 TiB;     8.0000 TiB;       8.Ti;     8.000000000000 TiB
      16TiB;      17.592 TB;         16 TiB;     16.000 TiB;      16.Ti;     16.00000000000 TiB
      32TiB;      35.184 TB;         32 TiB;     32.000 TiB;      32.Ti;     32.00000000000 TiB
      64TiB;      70.369 TB;         64 TiB;     64.000 TiB;      64.Ti;     64.00000000000 TiB
     128TiB;      140.74 TB;        128 TiB;     128.00 TiB;     128.Ti;     128.0000000000 TiB
     256TiB;      281.47 TB;        256 TiB;     256.00 TiB;     256.Ti;     256.0000000000 TiB
     512TiB;      562.95 TB;        512 TiB;     512.00 TiB;     512.Ti;     512.0000000000 TiB
       1PiB;    1.1259e15 B;          1 PiB;     1.0000 PiB;       1.Pi;     1.000000000000 PiB
       2PiB;    2.2518e15 B;          2 PiB;     2.0000 PiB;       2.Pi;     2.000000000000 PiB
       4PiB;    4.5036e15 B;          4 PiB;     4.0000 PiB;       4.Pi;     4.000000000000 PiB
       8PiB;    9.0072e15 B;          8 PiB;     8.0000 PiB;       8.Pi;     8.000000000000 PiB
      16PiB;    18.014e15 B;         16 PiB;     16.000 PiB;      16.Pi;     16.00000000000 PiB
      32PiB;    36.029e15 B;         32 PiB;     32.000 PiB;      32.Pi;     32.00000000000 PiB
      64PiB;    72.058e15 B;         64 PiB;     64.000 PiB;      64.Pi;     64.00000000000 PiB
     128PiB;    144.12e15 B;        128 PiB;     128.00 PiB;     128.Pi;     128.0000000000 PiB
     256PiB;    288.23e15 B;        256 PiB;     256.00 PiB;     256.Pi;     256.0000000000 PiB
     512PiB;    576.46e15 B;        512 PiB;     512.00 PiB;     512.Pi;     512.0000000000 PiB
       1EiB;    1.1529e18 B;          1 EiB;     1.0000 EiB;       1.Ei;     1.000000000000 EiB
       2EiB;    2.3058e18 B;          2 EiB;     2.0000 EiB;       2.Ei;     2.000000000000 EiB
       4EiB;    4.6117e18 B;          4 EiB;     4.0000 EiB;       4.Ei;     4.000000000000 EiB
       8EiB;    9.2234e18 B;          8 EiB;     8.0000 EiB;       8.Ei;     8.000000000000 EiB
      16EiB;    18.447e18 B;         16 EiB;     16.000 EiB;      16.Ei;     16.00000000000 EiB
      32EiB;    36.893e18 B;         32 EiB;     32.000 EiB;      32.Ei;     32.00000000000 EiB
      64EiB;    73.787e18 B;         64 EiB;     64.000 EiB;      64.Ei;     64.00000000000 EiB
     128EiB;    147.57e18 B;        128 EiB;     128.00 EiB;     128.Ei;     128.0000000000 EiB
     256EiB;    295.15e18 B;        256 EiB;     256.00 EiB;     256.Ei;     256.0000000000 EiB
     512EiB;     590.3e18 B;        512 EiB;     512.00 EiB;     512.Ei;     512.0000000000 EiB
       1ZiB;    1.1806e21 B;          1 ZiB;     1.0000 ZiB;       1.Zi;     1.000000000000 ZiB
       2ZiB;    2.3612e21 B;          2 ZiB;     2.0000 ZiB;       2.Zi;     2.000000000000 ZiB
       4ZiB;    4.7224e21 B;          4 ZiB;     4.0000 ZiB;       4.Zi;     4.000000000000 ZiB
       8ZiB;    9.4447e21 B;          8 ZiB;     8.0000 ZiB;       8.Zi;     8.000000000000 ZiB
      16ZiB;    18.889e21 B;         16 ZiB;     16.000 ZiB;      16.Zi;     16.00000000000 ZiB
      32ZiB;    37.779e21 B;         32 ZiB;     32.000 ZiB;      32.Zi;     32.00000000000 ZiB
      64ZiB;    75.558e21 B;         64 ZiB;     64.000 ZiB;      64.Zi;     64.00000000000 ZiB
     128ZiB;    151.12e21 B;        128 ZiB;     128.00 ZiB;     128.Zi;     128.0000000000 ZiB
     256ZiB;    302.23e21 B;        256 ZiB;     256.00 ZiB;     256.Zi;     256.0000000000 ZiB
     512ZiB;    604.46e21 B;        512 ZiB;     512.00 ZiB;     512.Zi;     512.0000000000 ZiB
       1YiB;    1.2089e24 B;          1 YiB;     1.0000 YiB;       1.Yi;     1.000000000000 YiB
       2YiB;    2.4179e24 B;          2 YiB;     2.0000 YiB;       2.Yi;     2.000000000000 YiB
       4YiB;    4.8357e24 B;          4 YiB;     4.0000 YiB;       4.Yi;     4.000000000000 YiB
       8YiB;    9.6714e24 B;          8 YiB;     8.0000 YiB;       8.Yi;     8.000000000000 YiB
      16YiB;    19.343e24 B;         16 YiB;     16.000 YiB;      16.Yi;     16.00000000000 YiB
      32YiB;    38.686e24 B;         32 YiB;     32.000 YiB;      32.Yi;     32.00000000000 YiB
      64YiB;    77.371e24 B;         64 YiB;     64.000 YiB;      64.Yi;     64.00000000000 YiB
     128YiB;    154.74e24 B;        128 YiB;     128.00 YiB;     128.Yi;     128.0000000000 YiB
     256YiB;    309.49e24 B;        256 YiB;     256.00 YiB;     256.Yi;     256.0000000000 YiB
     512YiB;    618.97e24 B;        512 YiB;     512.00 YiB;     512.Yi;     512.0000000000 YiB
    1024YiB;    1.2379e27 B; 1237940039285380274899124224 B; 1237940039285380274899124224.0000 B; 1237940039285380274899124224.; 1237940039285380274899124224.000000000000 B
      -1KiB;      -1.024 kB;         -1 KiB;    -1.0000 KiB;      -1.Ki;    -1.000000000000 KiB
      -1MiB;     -1.0486 MB;         -1 MiB;    -1.0000 MiB;      -1.Mi;    -1.000000000000 MiB
      -1GiB;     -1.0737 GB;         -1 GiB;    -1.0000 GiB;      -1.Gi;    -1.000000000000 GiB
      -1TiB;     -1.0995 TB;         -1 TiB;    -1.0000 TiB;      -1.Ti;    -1.000000000000 TiB
      -1PiB;   -1.1259e15 B;         -1 PiB;    -1.0000 PiB;      -1.Pi;    -1.000000000000 PiB
      -1EiB;   -1.1529e18 B;         -1 EiB;    -1.0000 EiB;      -1.Ei;    -1.000000000000 EiB
      -1ZiB;   -1.1806e21 B;         -1 ZiB;    -1.0000 ZiB;      -1.Zi;    -1.000000000000 ZiB
      -1YiB;   -1.2089e24 B;         -1 YiB;    -1.0000 YiB;      -1.Yi;    -1.000000000000 YiB
          h; 662.61e-36 J-s;          0 J-s;     0.0000 J-s;         0.;     0.000000000000 J-s
       hbar; 105.46e-36 J-s;          0 J-s;     0.0000 J-s;         0.;     0.000000000000 J-s
          k; 13.806e-24 J/K;          0 J/K;     0.0000 J/K;         0.;     0.000000000000 J/K
          q;   160.22e-21 C;            0 C;       0.0000 C;         0.;       0.000000000000 C
          c;    299.79 Mm/s;    285.9 Mim/s;   285.90 Mim/s;    285.9Mi;   285.9043674469 Mim/s
         0C;       273.15 K;       273.15 K;       273.15 K;     273.15;       273.1500000000 K
       eps0;    8.8542 pF/m;          0 F/m;     0.0000 F/m;         0.;     0.000000000009 F/m
        mu0;    1.2566 uH/m;          0 H/m;     0.0000 H/m;         0.;     0.000001256637 H/m
         Z0;    376.73 Ohms;    376.73 Ohms;    376.73 Ohms;     376.73;    376.7303134610 Ohms
     1Zippy;        1 Zippy;        1 Zippy;   1.0000 Zippy;         1.;   1.000000000000 Zippy
""".strip()

data2 = """
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

from quantiphy import Quantity

def test_reader():
    with Quantity.prefs(known_units = 'Zippy'):
        for line in data1.splitlines():
            v, s1, s2, s3, s4, s5 = [c.strip() for c in line.strip().split(';')]
            print('Trying: v={v}, s1={s1}, s2={s2}, s3={s3}, s4={s4}, s5={s5}'.format(**locals()))
            q = Quantity(v, binary=True)

            res = str(q)
            exp = '{v}: expected <{s1}>, got <{res}>.'.format(**locals())
            assert s1 == res, exp

            res = q.binary()
            exp = '{v}: expected <{s2}>, got <{res}>.'.format(**locals())
            assert s2 == res, exp

            res = q.binary(prec=4, strip_zeros=False)
            exp = '{v}: expected <{s3}>, got <{res}>.'.format(**locals())
            assert s3 == res, exp

            res = q.binary(strip_zeros=True, strip_radix=False, show_units=False)
            exp = '{v}: expected <{s4}>, got <{res}>.'.format(**locals())
            assert s4 == res, exp

            res = q.binary(prec='full', strip_zeros=False)
            exp = '{v}: expected <{s5}>, got <{res}>.'.format(**locals())
            assert s5 == res, exp

def test_writer():
    q = Quantity('mem = 1GiB', binary=True)

    res = str(q)
    exp = '1.0737 GB'
    assert res == exp, res

    res = q.binary()
    exp = '1 GiB'
    assert res == exp, res

    res = q.render(form='binary')
    exp = '1 GiB'
    assert res == exp, res

    res = '{q:b}'.format(**locals())
    exp = '1 GiB'
    assert res == exp, res

    res = q.binary(prec=2, strip_zeros=False)
    exp = '1.00 GiB'
    assert res == exp, res

    res = '{q:#0.2b}'.format(**locals())
    exp = '1.00 GiB'
    assert res == exp, res

    res = q.binary(show_label=True)
    exp = 'mem = 1 GiB'
    assert res == exp, res

    res = '{q:B}'.format(**locals())
    exp = 'mem = 1 GiB'
    assert res == exp, res

    res = q.binary(show_label=True, scale='b')
    exp = 'mem = 8 Gib'
    assert res == exp, res

    res = '{q:Bb}'.format(**locals())
    exp = 'mem = 8 Gib'
    assert res == exp, res

    res = q.binary(strip_zeros=False)
    exp = '1.0000 GiB'
    assert res == exp, res

    res = '{q:#b}'.format(**locals())
    exp = '1.0000 GiB'
    assert res == exp, res

    res = q.binary(strip_zeros=True, strip_radix=False)
    exp = '1. GiB'
    assert res == exp, res

    q = Quantity('1GB', binary=True)

    res = str(q)
    exp = '1 GB'
    assert res == exp, res

    res = q.binary()
    exp = '953.67 MiB'
    assert res == exp, res

    res = '{q:b}'.format(**locals())
    exp = '953.67 MiB'
    assert res == exp, res

    res = q.binary(prec=2)
    exp = '954 MiB'
    assert res == exp, res

    res = '{q:0.2b}'.format(**locals())
    exp = '954 MiB'
    assert res == exp, res

def test_writer_prec():
    for line in data2.splitlines():
        v, p0, p1, p2, p3, p4 = [c.strip() for c in line.strip().split(';')]
        print('Trying: v={v}, p0={p0}, p1={p1}, p2={p2}, p3={p3}, p4={p4}'.format(**locals()))
        q = Quantity(v)

        res = q.binary(prec=0)
        exp = '{v}: expected <{p0}>, got <{res}>.'.format(**locals())
        assert res == p0, exp

        res = q.binary(prec=1)
        exp = '{v}: expected <{p1}>, got <{res}>.'.format(**locals())
        assert res == p1, exp

        res = q.binary(prec=2)
        exp = '{v}: expected <{p2}>, got <{res}>.'.format(**locals())
        assert res == p2, exp

        res = q.binary(prec=3)
        exp = '{v}: expected <{p3}>, got <{res}>.'.format(**locals())
        assert res == p3, exp

        res = q.binary(prec=4)
        exp = '{v}: expected <{p4}>, got <{res}>.'.format(**locals())
        assert res == p4, exp
