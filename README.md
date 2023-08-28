# pulsar_paragraph
A python package that can create a human readable summary of a pulsar based on information for the ANTF pulsar catalogue


## Installation

To install this package run:

```
pip install pulsar_paragraph
```

Or clone the git repository and run:

```
pip install .
```

## Usage

To output a summary of a pulsar, use the following command:

```
pulsar_paragraph -p <pulsar_jname>
```

Where pulsar's PSRJ name such as:

```
pulsar_paragraph -p J0437−4715
```

which will output:

```
PSR J0437-4715 is a millisecond pulsar with a period of 5.76 milliseconds and has an extremely low dispersion measure of 2.645 pc/cm^3. It is a very bright pulsar with a 1400 MHz catalogue flux density of 1.502e+05 mJy. PSR J0437-4715 is a Southern Hemisphere pulsar. This pulsar has a period derivative of 5.73e-20. PSR J0437-4715 has a fairly typical orbital period of 5.741 days and a very mildly eccentric orbit with an eccentricity of 0.00002. It is an ancient pulsar with an age of 1.592 Gyr. PSR J0437-4715 has a low magnetic field strength of 5.81e+08 G. It has a high transverse velocity of 104.7 km/s. The estimated distance to J0437-4715 is 156 pc. This pulsar has a low-mass companion with a minimum mass of 0.140 solar masses.
```

If you don't include a pulsar, it will create a summary for each pulsar on the ATNF catalogue.

You can also output the paragraphs to a text file with the -f option:

```
pulsar_paragraph -o <output_file_name>
```