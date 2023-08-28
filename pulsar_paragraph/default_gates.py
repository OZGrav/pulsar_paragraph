def format_float(value, threshold=1e5, decimal_places=2):
    if abs(value) >= threshold:
        return "{:.{}e}".format(value, decimal_places)
    else:
        return "{:.{}f}".format(value, decimal_places)


class VariableGate:
    def __init__(
            self,
            name,
            lower_bound,
            upper_bound,
            descriptor,
            unit,
            factor,
            scientific,
        ):
        self.name = name
        # The minimum value that is required to pass into a specific gate.
        self.lower_bound = lower_bound
        # The maximum value that something can be to pass into specific gate.
        self.upper_bound = upper_bound
        # The descriptor usually containing adjectives, e.g "an extremely young pulsar with a"
        self.descriptor = descriptor
        # Unit for specific value. If left blank, an extra space will result, however this has been taken care of in laws_to_str final "if else" statement.
        self.unit = unit
        # The number that the value will be multiplied by. Leave a value of 1 if you do not want the value changed.
        self.factor = factor
        # Can only be 3 things: "f", "E", or "i", without the quotes. f = float, E = scientific notation, and i = integer, or no decimal places.
        self.scientific = scientific

    def display(self):
        print(f"{format_float(self.lower_bound):8s} > {self.name:7s} > {format_float(self.upper_bound):8s} {self.descriptor:55s} unit: {self.unit:12s} factor:{str(self.factor):5s} {self.scientific}")


def age_defaults():
    return [
        VariableGate(
            name="age",
            lower_bound=0.0,
            upper_bound=1000.0,
            descriptor="an extremely young pulsar with an age of",
            unit="yr",
            factor=1.0,
            scientific="i",
        ),
        VariableGate(
            name="age",
            lower_bound=1000.0,
            upper_bound=2e4,
            descriptor="a fairly young pulsar with an age of",
            unit="yr",
            factor=1.0,
            scientific="i",
        ),
        VariableGate(
            name="age",
            lower_bound=2e4,
            upper_bound=1e5,
            descriptor="a youthful pulsar with an age of",
            unit="kyr",
            factor=0.001,
            scientific="i",
        ),
        VariableGate(
            name="age",
            lower_bound=1e5,
            upper_bound=1e6,
            descriptor="a middle-aged pulsar with an age of",
            unit="Myr",
            factor=1e-06,
            scientific="i",
        ),
        VariableGate(
            name="age",
            lower_bound=1e6,
            upper_bound=1e7,
            descriptor="a fairly old pulsar with an age of",
            unit="Myr",
            factor=1e-06,
            scientific="i",
        ),
        VariableGate(
            name="age",
            lower_bound=1e7,
            upper_bound=1e9,
            descriptor="a very old pulsar with an age of",
            unit="Gyr",
            factor=1e-09,
            scientific="i",
        ),
        VariableGate(
            name="age",
            lower_bound=1e9,
            upper_bound=1e12,
            descriptor="an ancient pulsar with an age of",
            unit="Gyr",
            factor=1e-09,
            scientific="i",
        ),
    ]

def bsurf_defaults():
    return [
        VariableGate(
            name="bsurf",
            lower_bound=0.0,
            upper_bound=1e8,
            descriptor="an extremely low magnetic field strength of",
            unit="G",
            factor=1,
            scientific="E",
        ),
        VariableGate(
            name="bsurf",
            lower_bound=1e8,
            upper_bound=1e9,
            descriptor="a low magnetic field strength of",
            unit="G",
            factor=1,
            scientific="E",
        ),
        VariableGate(
            name="bsurf",
            lower_bound=1e9,
            upper_bound=1e11,
            descriptor="a moderate magnetic field strength of",
            unit="G",
            factor=1,
            scientific="E",
        ),
        VariableGate(
            name="bsurf",
            lower_bound=1e11,
            upper_bound=1e13,
            descriptor="a typical slow pulsar-like magnetic field strength of",
            unit="G",
            factor=1,
            scientific="E",
        ),
        VariableGate(
            name="bsurf",
            lower_bound=1e13,
            upper_bound=1e+99,
            descriptor="a magnetar-like magnetic field strength of",
            unit="G",
            factor=1,
            scientific="E",
        ),
    ]

def dm_defaults():
    return [
        VariableGate(
            name="dm",
            lower_bound=0,
            upper_bound=5.0,
            descriptor="an extremely low dispersion measure of",
            unit="pc/cc",
            factor=1,
            scientific="f",
        ),
        VariableGate(
            name="dm",
            lower_bound=5,
            upper_bound=15.0,
            descriptor="a small dispersion measure of",
            unit="pc/cc",
            factor=1,
            scientific="f",
        ),
        VariableGate(
            name="dm",
            lower_bound=15,
            upper_bound=30.0,
            descriptor="a fairly low dispersion measure of",
            unit="pc/cc",
            factor=1,
            scientific="f",
        ),
        VariableGate(
            name="dm",
            lower_bound=30,
            upper_bound=100.0,
            descriptor="a moderate dispersion measure of",
            unit="pc/cc",
            factor=1,
            scientific="f",
        ),
        VariableGate(
            name="dm",
            lower_bound=100,
            upper_bound=600.0,
            descriptor="a fairly large dispersion measure of",
            unit="pc/cc",
            factor=1,
            scientific="f",
        ),
        VariableGate(
            name="dm",
            lower_bound=600,
            upper_bound=1000.0,
            descriptor="a quite high dispersion measure of",
            unit="pc/cc",
            factor=1,
            scientific="f",
        ),
        VariableGate(
            name="dm",
            lower_bound=1000,
            upper_bound=1e+99,
            descriptor="an extremely high dispersion measure of",
            unit="pc/cc",
            factor=1,
            scientific="f",
        ),
    ]

def ecc_defaults():
    return [
        VariableGate(
            name="ecc",
            lower_bound=0.0,
            upper_bound=1e-06,
            descriptor="an extremely circular orbit with an eccentricity of",
            unit="",
            factor=1,
            scientific="E",
        ),
        VariableGate(
            name="ecc",
            lower_bound=1e-06,
            upper_bound=1e-05,
            descriptor="a very circular orbit with an eccentricity of",
            unit="",
            factor=1,
            scientific="E",
        ),
        VariableGate(
            name="ecc",
            lower_bound=1e-05,
            upper_bound=0.0001,
            descriptor="a very mildly eccentric orbit with an eccentricity of",
            unit="",
            factor=1,
            scientific="E",
        ),
        VariableGate(
            name="ecc",
            lower_bound=0.0001,
            upper_bound=0.01,
            descriptor="a mildly eccentric orbit with an eccentricity of",
            unit="",
            factor=1,
            scientific="E",
        ),
        VariableGate(
            name="ecc",
            lower_bound=0.01,
            upper_bound=0.1,
            descriptor="a reasonably eccentric orbit with an eccentricity of",
            unit="",
            factor=1,
            scientific="f",
        ),
        VariableGate(
            name="ecc",
            lower_bound=0.1,
            upper_bound=0.4,
            descriptor="an eccentric orbit with an eccentricity of",
            unit="",
            factor=1,
            scientific="f",
        ),
        VariableGate(
            name="ecc",
            lower_bound=0.4,
            upper_bound=0.8,
            descriptor="a highly eccentric orbit with an eccentricity of",
            unit="",
            factor=1,
            scientific="f",
        ),
        VariableGate(
            name="ecc",
            lower_bound=0.8,
            upper_bound=1.0,
            descriptor="an extremely eccentric orbit with an eccentricity of",
            unit="",
            factor=1,
            scientific="f",
        ),
    ]

def minmass_defaults():
    return [
        VariableGate(
            name="minmass",
            lower_bound=0.0,
            upper_bound=0.0001,
            descriptor="a planetary-sized companion with a minimum mass of",
            unit="solar masses",
            factor=1,
            scientific="f",
        ),
        VariableGate(
            name="minmass",
            lower_bound=0.0001,
            upper_bound=0.02,
            descriptor="an extremely low-mass companion with a minimum mass of",
            unit="solar masses",
            factor=1,
            scientific="f",
        ),
        VariableGate(
            name="minmass",
            lower_bound=0.02,
            upper_bound=0.1,
            descriptor="a very low-mass companion with a minimum mass of",
            unit="solar masses",
            factor=1,
            scientific="f",
        ),
        VariableGate(
            name="minmass",
            lower_bound=0.1,
            upper_bound=0.4,
            descriptor="a low-mass companion with a minimum mass of",
            unit="solar masses",
            factor=1,
            scientific="f",
        ),
        VariableGate(
            name="minmass",
            lower_bound=0.4,
            upper_bound=1.0,
            descriptor="a moderate-sized companion with a minimum mass of",
            unit="solar masses",
            factor=1,
            scientific="f",
        ),
        VariableGate(
            name="minmass",
            lower_bound=1.0,
            upper_bound=1000.0,
            descriptor="a very high mass companion with a minimum mass of",
            unit="solar masses",
            factor=1,
            scientific="f",
        ),
    ]

def pb_defaults():
    return [
        VariableGate(
            name="pb",
            lower_bound=0.0,
            upper_bound=0.0833,
            descriptor="has an extremely tight orbital period of just",
            unit="hours",
            factor=24.0,
            scientific="f",
        ),
        VariableGate(
            name="pb",
            lower_bound=0.0833,
            upper_bound=0.5,
            descriptor="has a very tight orbital period of just",
            unit="hours",
            factor=24.0,
            scientific="f",
        ),
        VariableGate(
            name="pb",
            lower_bound=0.5,
            upper_bound=1.0,
            descriptor="has a quite tight orbital period of only",
            unit="hours",
            factor=24.0,
            scientific="f",
        ),
        VariableGate(
            name="pb",
            lower_bound=1.0,
            upper_bound=2.0,
            descriptor="has a reasonably short orbital period of",
            unit="days",
            factor=1.0,
            scientific="f",
        ),
        VariableGate(
            name="pb",
            lower_bound=2.0,
            upper_bound=10.0,
            descriptor="has a fairly typical orbital period of",
            unit="days",
            factor=1.0,
            scientific="f",
        ),
        VariableGate(
            name="pb",
            lower_bound=10.0,
            upper_bound=50.0,
            descriptor="has a quite long orbital period of",
            unit="days",
            factor=1.0,
            scientific="f",
        ),
        VariableGate(
            name="pb",
            lower_bound=50.0,
            upper_bound=365.0,
            descriptor="has a very long orbital period of",
            unit="days",
            factor=1.0,
            scientific="f",
        ),
        VariableGate(
            name="pb",
            lower_bound=365.0,
            upper_bound=1e+99,
            descriptor="has an extremely long orbital period of",
            unit="years",
            factor=0.002737850787,
            scientific="f",
        ),
    ]

def period_defaults():
    return [
        VariableGate(
            name="period",
            lower_bound=0.001,
            upper_bound=0.002,
            descriptor="a very fast millisecond pulsar with a period of",
            unit="milliseconds",
            factor=1000,
            scientific="f",
        ),
        VariableGate(
            name="period",
            lower_bound=0.002,
            upper_bound=0.008,
            descriptor="a millisecond pulsar with a period of",
            unit="milliseconds",
            factor=1000,
            scientific="f",
        ),
        VariableGate(
            name="period",
            lower_bound=0.008,
            upper_bound=0.02,
            descriptor="a relatively slow millisecond pulsar with a period of",
            unit="milliseconds",
            factor=1000,
            scientific="f",
        ),
        VariableGate(
            name="period",
            lower_bound=0.02,
            upper_bound=0.1,
            descriptor="a quite fast pulsar with a period of",
            unit="milliseconds",
            factor=1000,
            scientific="f",
        ),
        VariableGate(
            name="period",
            lower_bound=0.1,
            upper_bound=0.999,
            descriptor="a normal pulsar with a period of",
            unit="milliseconds",
            factor=1000,
            scientific="f",
        ),
        VariableGate(
            name="period",
            lower_bound=1.0,
            upper_bound=2.0,
            descriptor="a normal pulsar with a period of",
            unit="seconds",
            factor=1,
            scientific="f",
        ),
        VariableGate(
            name="period",
            lower_bound=2.0,
            upper_bound=5.0,
            descriptor="a fairly slow pulsar with a period of",
            unit="seconds",
            factor=1,
            scientific="f",
        ),
        VariableGate(
            name="period",
            lower_bound=5.0,
            upper_bound=10.0,
            descriptor="a very slow pulsar with a period of",
            unit="seconds",
            factor=1,
            scientific="f",
        ),
        VariableGate(
            name="period",
            lower_bound=10.0,
            upper_bound=10000.0,
            descriptor="an extremely slow pulsar with a period of",
            unit="seconds",
            factor=1,
            scientific="f",
        ),
    ]

def s1400_defaults():
    return [
        VariableGate(
            name="s1400",
            lower_bound=0.0,
            upper_bound=0.1,
            descriptor="an extremely faint pulsar with a 1400 MHz catalogue flux density of",
            unit="microJy",
            factor=1000.0,
            scientific="f",
        ),
        VariableGate(
            name="s1400",
            lower_bound=0.1,
            upper_bound=0.5,
            descriptor="a faint pulsar with a 1400 MHz catalogue flux density of",
            unit="mJy",
            factor=1.0,
            scientific="f",
        ),
        VariableGate(
            name="s1400",
            lower_bound=0.5,
            upper_bound=1.0,
            descriptor="a weak pulsar with a 1400 MHz catalogue flux density of",
            unit="mJy",
            factor=1.0,
            scientific="f",
        ),
        VariableGate(
            name="s1400",
            lower_bound=1.0,
            upper_bound=5.0,
            descriptor="a moderately bright pulsar with a 1400 MHz catalogue flux density of",
            unit="mJy",
            factor=1.0,
            scientific="f",
        ),
        VariableGate(
            name="s1400",
            lower_bound=5.0,
            upper_bound=20.0,
            descriptor="a fairly bright pulsar with a 1400 MHz catalogue flux density of",
            unit="mJy",
            factor=1.0,
            scientific="f",
        ),
        VariableGate(
            name="s1400",
            lower_bound=20.0,
            upper_bound=100.0,
            descriptor="a bright pulsar with a 1400 MHz catalogue flux density of",
            unit="mJy",
            factor=1.0,
            scientific="f",
        ),
        VariableGate(
            name="s1400",
            lower_bound=100.0,
            upper_bound=500.0,
            descriptor="a very bright pulsar with a 1400 MHz catalogue flux density of",
            unit="mJy",
            factor=1.0,
            scientific="f",
        ),
        VariableGate(
            name="s1400",
            lower_bound=500.0,
            upper_bound=100000.0,
            descriptor="an extremely bright pulsar with a 1400 MHz catalogue flux density of",
            unit="Jy",
            factor=0.001,
            scientific="f",
        ),
    ]

def vtrans_defaults():
    return [
        VariableGate(
            name="vtrans",
            lower_bound=0,
            upper_bound=10.0,
            descriptor="an extremely low transverse velocity of",
            unit="km/s",
            factor=1,
            scientific="i",
        ),
        VariableGate(
            name="vtrans",
            lower_bound=10,
            upper_bound=30.0,
            descriptor="a low transverse velocity of",
            unit="km/s",
            factor=1,
            scientific="i",
        ),
        VariableGate(
            name="vtrans",
            lower_bound=30,
            upper_bound=100.0,
            descriptor="an intermediate transverse velocity of",
            unit="km/s",
            factor=1,
            scientific="i",
        ),
        VariableGate(
            name="vtrans",
            lower_bound=100,
            upper_bound=300.0,
            descriptor="a high transverse velocity of",
            unit="km/s",
            factor=1,
            scientific="i",
        ),
        VariableGate(
            name="vtrans",
            lower_bound=300,
            upper_bound=500.0,
            descriptor="a very high transverse velocity of",
            unit="km/s",
            factor=1,
            scientific="i",
        ),
        VariableGate(
            name="vtrans",
            lower_bound=500,
            upper_bound=1e+99,
            descriptor="an extremely high transverse velocity of",
            unit="km/s",
            factor=1,
            scientific="i",
        ),
    ]