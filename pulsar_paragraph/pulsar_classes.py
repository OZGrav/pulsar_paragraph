import numpy as np



def format_float(value, threshold=1e5, decimal_places=2):
    if abs(value) >= threshold:
        return "{:.{}e}".format(value, decimal_places)
    else:
        return "{:.{}f}".format(value, decimal_places)

def get_conversion_factor(metric_prefix):
    metric_prefixes = {
        'P': 1e15,  # peta
        'T': 1e12,  # tera
        'G': 1e9,   # giga
        'M': 1e6,   # mega
        'k': 1e3,   # kilo
        '' : 1,      # base unit (no prefix)
        'm': 1e-3,  # milli
        'μ': 1e-6,  # micro
        'n': 1e-9,  # nano
        'p': 1e-12, # pico
        'milli': 1e-3,  # milli spelled out for use in milliseconds

        # The following are for converting binary period (days) into others units (hours years)
        "days"  : 1,
        "hours" : 24,
        "years" : 365.25,

    }

    if metric_prefix in metric_prefixes:
        return metric_prefixes[metric_prefix]
    else:
        raise ValueError("Invalid metric prefix")


class VariableGate:
    def __init__(
            self,
            name,
            lower_bound,
            upper_bound,
            descriptor,
            metric_prefix="",
        ):
        self.name = name
        # The minimum value that is required to pass into a specific gate.
        self.lower_bound = lower_bound
        # The maximum value that something can be to pass into specific gate.
        self.upper_bound = upper_bound
        # The descriptor usually containing adjectives, e.g "an extremely young pulsar with a"
        self.descriptor = descriptor
        # The metric prefix. Used to convert to the new units (e.g. G then divide by 1e9)
        self.metric_prefix = metric_prefix

    def display(self):
        print(f"{format_float(self.lower_bound):8s} > {self.name:7s} > {format_float(self.upper_bound):8s} {self.descriptor:55s} unit: {self.metric_prefix}{self.unit:12s}")


class PulsarVariable:
    def __init__(
            self,
            name,
            unit,
            decimal_places=2,
            load_defaults=True
        ):
        self.name = name
        self.unit = unit
        self.decimal_places = decimal_places
        self.gates = []

        if load_defaults:
            self.gates  = gate_default(self.name)

    def add_gate(self, gate):
        self.gates.append(gate)

    def display_gates(self):
        for gate in self.gates:
            gate.display()

    def variable_value_to_str(self,  value: str) -> str:
        if value == "*":
            return None
        if self.name == "s1400":
            # Convert value from mJy to Jy so metric prefixes are handled correctly
            value = float(value) / 1000.0
        for variable_gate in self.gates:
            if variable_gate.lower_bound <= float(value) < variable_gate.upper_bound:
                # Convert to metric prefix units (e.g. G then divide by 1e9)
                converted_value = float(value) / get_conversion_factor(variable_gate.metric_prefix)
                output_str = f"{variable_gate.descriptor} { format_float(converted_value, decimal_places=self.decimal_places) }"
                if f"{variable_gate.metric_prefix}{self.unit}" == "":
                    # No unit so return without a dangling space
                    return output_str
                else:
                    return f"{output_str} {variable_gate.metric_prefix}{self.unit}"



class PulsarParagraph:
    def __init__(self):
        self.period = PulsarVariable(
            name="period",
            unit="seconds",
            decimal_places=2,
        )
        self.dm = PulsarVariable(
            name="dm",
            unit="pc/cm^3",
            decimal_places=3,
        )
        self.s1400 = PulsarVariable(
            name="s1400",
            unit="Jy",
            decimal_places=3,
        )
        self.pb = PulsarVariable(
            name="pb",
            unit="",
            decimal_places=3,
        )
        self.ecc = PulsarVariable(
            name="ecc",
            unit="",
            decimal_places=5,
        )
        self.age = PulsarVariable(
            name="age",
            unit="yr",
            decimal_places=3,
        )
        self.bsurf = PulsarVariable(
            name="bsurf",
            unit="G",
            decimal_places=2,
        )
        self.vtrans = PulsarVariable(
            name="vtrans",
            unit="km/s",
            decimal_places=1,
        )
        self.minmass = PulsarVariable(
            name="minmass",
            unit="solar masses",
            decimal_places=3,
        )


    def p1_to_str(self, p1, psr_name):
        """Function that reads in p1 directly from file and output a string. Has 3 outcomes depending if p1 is +, -, or 0.
        """
        if '*' in str(p1):
            return f' PSR {psr_name} has no measured period derivative.'
        elif np.isnan(p1):
            return f' PSR {psr_name} has no measured period derivative.'
        else:
            p1 = float(p1)
            if p1 < 0:
                p1 = '{:.2e}'.format(p1)
                p1 = str(p1)
                return f' This pulsar has an unusual negative period derivative of {p1}. Because it is negative, it has no estimate of implied magnetic field strength or characteristic age.'
            else:
                p1 = '{:.2e}'.format(p1)
                p1 = str(p1)
                return f' This pulsar has a period derivative of {p1}.'


    def dec_law(self, dec):
        """Law that converts dec info to str. Dec info is found in PSR name, e.g J0437-4715, as + or -.
        Has a function because a law is not necessary. The sentence formatting is at the bottom of the file in an if statement.
        """
        dec = str(dec).strip()
        if '*' in str(dec):
            return None
        else:
            if '+' in dec:
                return 'Northern Hemisphere'
            elif '-' in dec:
                return 'Southern Hemisphere'


    def assoc_to_str(self, assoc: int):
        """Converts assoc str to descriptor. Does not have a law because data-type is unique.
        Breaks the data into lists, then converts data to str depending on data-type. Then, appended to a final str.
        Does not work for every case, which is why there are some .replace methods at the bottom of file.
        Final output is of truncated type, aka one/two sentence descriptor max.
        """
        assoc_dict = {
            "EXGAL": "an extragalactic pulsar",
            "SMC": " located in the Small Magellanic Cloud.",
            "XRS": "an associated x-ray source",
            "GRS": "an associated gamma-ray source",
            "SNR": "a supernova remnant",
            "GC": "located in the globular cluster",
            "PWN": " located in the pulsar wind nebula",
            "LMC": " located in the Large Magellanic Cloud.",
            "OPT": "the optical counterpart",
        }
        assoc = str(assoc).strip()
        assoc_str_final = ''
        assoc_str = ''
        assoc_str_temp = ''
        assoc_str_temp2 = ''
        assoc_str2 = ''
        count = 0
        count2 = 0
        exgal_flag = False
        if '*' not in assoc:
            if ',' in assoc:
                assoc_split = assoc.split(',')
                for comma_split in assoc_split:
                    count += 1
                    if ':' in comma_split:
                        colon_split = comma_split.split(':')
                        for item in colon_split:
                            item = str(item).strip()
                            if item in assoc_dict and exgal_flag == True:
                                assoc_str_temp += assoc_dict[item]
                            elif item in assoc_dict and 'EXGAL' == item:
                                assoc_str_temp = assoc_dict[item]
                                exgal_flag = True
                            elif item in assoc_dict:
                                if count < len(assoc_split) and count != 1:
                                    assoc_str_temp += ' and '
                                if 'with' in assoc_str_temp or 'and' in assoc_str_temp:
                                    assoc_str_temp = assoc_dict[item]
                                else:
                                    assoc_str_temp += assoc_dict[item]
                            elif item not in assoc_dict and '[' in item and len(item) > 9:
                                bracket = item.index('[')
                                new_item = item[:bracket]
                                assoc_str_temp += ' ' + '(' + str(new_item) + ')'
                                if count < len(assoc_split)-1:
                                    assoc_str_temp += ', '
                                elif count < len(assoc_split):
                                    assoc_str_temp += ' and '
                                else:
                                    assoc_str_temp += '.'
                            elif item not in assoc_dict and '[' in item:
                                assoc_str_temp = assoc_str_temp.replace('the', 'an')
                                if count < len(assoc_split)-1:
                                    assoc_str_temp += ', '
                                elif count < len(assoc_split):
                                    assoc_str_temp += ' and '
                                else:
                                    assoc_str_temp += '.'
                            elif item not in assoc_dict:
                                if count < len(colon_split):
                                    assoc_str_temp += ' with'
                                assoc_str_temp += ' ' + '(' + str(item) + ')'
                                if count == len(assoc_split):
                                    assoc_str_temp += '.'
                            assoc_str = assoc_str_temp
                    assoc_str_final += assoc_str
            elif ':' in assoc:
                colon_split2 = assoc.split(':')
                for item in colon_split2:
                    count2 += 1
                    item = str(item).strip()
                    if item in assoc_dict and exgal_flag == True:
                        assoc_str_temp2 += assoc_dict[item]
                    elif item in assoc_dict and 'EXGAL' == item:
                        assoc_str_temp2 = assoc_dict[item]
                        exgal_flag = True
                    elif item in assoc_dict:
                        assoc_str_temp2 = ' and has ' + assoc_dict[item]
                    elif item not in assoc_dict and '[' in item and len(item) > 9:
                        bracket = item.index('[')
                        new_item = item[:bracket]
                        assoc_str_temp2 += ' ' + '(' + str(new_item) + ')'
                        if count2 < len(colon_split2):
                            assoc_str_temp2 += ' and has '
                        else:
                            assoc_str_temp2 += '. '
                    elif item not in assoc_dict and '[' in item:
                        assoc_str_temp2 = assoc_str_temp2.replace('the', 'an')
                    elif item not in assoc_dict:
                        assoc_str_temp2 += ' ' + str(item)
                        if count2 < len(colon_split2):
                            assoc_str_temp2 += 'and has '
                        else:
                            assoc_str_temp2 += '. '
                assoc_str2 = assoc_str_temp2
            assoc_str_final += assoc_str2
            return assoc_str_final


def gate_default(variable_name):
    gate_defaults = {
        "age" : [
            VariableGate(
                name="age",
                lower_bound=0.0,
                upper_bound=1000.0,
                descriptor="an extremely young pulsar with an estimated age of",
            ),
            VariableGate(
                name="age",
                lower_bound=1000.0,
                upper_bound=2e4,
                descriptor="a fairly young pulsar with an estimated age of",
            ),
            VariableGate(
                name="age",
                lower_bound=2e4,
                upper_bound=1e5,
                descriptor="a youthful pulsar with an estimated age of",
                metric_prefix="k",
            ),
            VariableGate(
                name="age",
                lower_bound=1e5,
                upper_bound=1e6,
                descriptor="a middle-aged pulsar with an estimated age of",
                metric_prefix="M",
            ),
            VariableGate(
                name="age",
                lower_bound=1e6,
                upper_bound=1e7,
                descriptor="a fairly old pulsar with an estimated age of",
                metric_prefix="M",
            ),
            VariableGate(
                name="age",
                lower_bound=1e7,
                upper_bound=1e9,
                descriptor="a very old pulsar with an estimated age of",
                metric_prefix="G",
            ),
            VariableGate(
                name="age",
                lower_bound=1e9,
                upper_bound=1e12,
                descriptor="an ancient pulsar with an estimated age of",
                metric_prefix="G",
            ),
        ],
        "bsurf" : [
            VariableGate(
                name="bsurf",
                lower_bound=0.0,
                upper_bound=1e8,
                descriptor="an extremely low implied magnetic field strength of",
            ),
            VariableGate(
                name="bsurf",
                lower_bound=1e8,
                upper_bound=1e9,
                descriptor="a low implied magnetic field strength of",
            ),
            VariableGate(
                name="bsurf",
                lower_bound=1e9,
                upper_bound=1e11,
                descriptor="a moderate implied magnetic field strength of",
            ),
            VariableGate(
                name="bsurf",
                lower_bound=1e11,
                upper_bound=1e13,
                descriptor="a typical slow pulsar-like implied magnetic field strength of",
            ),
            VariableGate(
                name="bsurf",
                lower_bound=1e13,
                upper_bound=1e+99,
                descriptor="a magnetar-like implied magnetic field strength of",
            ),
        ],
        "dm" : [
            VariableGate(
                name="dm",
                lower_bound=0,
                upper_bound=5.0,
                descriptor="an extremely low dispersion measure of",
            ),
            VariableGate(
                name="dm",
                lower_bound=5,
                upper_bound=15.0,
                descriptor="a small dispersion measure of",
            ),
            VariableGate(
                name="dm",
                lower_bound=15,
                upper_bound=30.0,
                descriptor="a fairly low dispersion measure of",
            ),
            VariableGate(
                name="dm",
                lower_bound=30,
                upper_bound=100.0,
                descriptor="a moderate dispersion measure of",
            ),
            VariableGate(
                name="dm",
                lower_bound=100,
                upper_bound=600.0,
                descriptor="a fairly large dispersion measure of",
            ),
            VariableGate(
                name="dm",
                lower_bound=600,
                upper_bound=1000.0,
                descriptor="a quite high dispersion measure of",
            ),
            VariableGate(
                name="dm",
                lower_bound=1000,
                upper_bound=1e+99,
                descriptor="an extremely high dispersion measure of",
            ),
        ],
        "ecc" : [
            VariableGate(
                name="ecc",
                lower_bound=0.0,
                upper_bound=1e-06,
                descriptor="an extremely circular orbit with an eccentricity of",
            ),
            VariableGate(
                name="ecc",
                lower_bound=1e-06,
                upper_bound=1e-05,
                descriptor="a very circular orbit with an eccentricity of",
            ),
            VariableGate(
                name="ecc",
                lower_bound=1e-05,
                upper_bound=0.0001,
                descriptor="a very mildly eccentric orbit with an eccentricity of",
            ),
            VariableGate(
                name="ecc",
                lower_bound=0.0001,
                upper_bound=0.01,
                descriptor="a mildly eccentric orbit with an eccentricity of",
            ),
            VariableGate(
                name="ecc",
                lower_bound=0.01,
                upper_bound=0.1,
                descriptor="a reasonably eccentric orbit with an eccentricity of",
            ),
            VariableGate(
                name="ecc",
                lower_bound=0.1,
                upper_bound=0.4,
                descriptor="an eccentric orbit with an eccentricity of",
            ),
            VariableGate(
                name="ecc",
                lower_bound=0.4,
                upper_bound=0.8,
                descriptor="a highly eccentric orbit with an eccentricity of",
            ),
            VariableGate(
                name="ecc",
                lower_bound=0.8,
                upper_bound=1.0,
                descriptor="an extremely eccentric orbit with an eccentricity of",
            ),
        ],
        "minmass" : [
            VariableGate(
                name="minmass",
                lower_bound=0.0,
                upper_bound=0.0001,
                descriptor="a planetary-sized companion with a minimum mass of",
            ),
            VariableGate(
                name="minmass",
                lower_bound=0.0001,
                upper_bound=0.02,
                descriptor="an extremely low-mass companion with a minimum mass of",
            ),
            VariableGate(
                name="minmass",
                lower_bound=0.02,
                upper_bound=0.1,
                descriptor="a very low-mass companion with a minimum mass of",
            ),
            VariableGate(
                name="minmass",
                lower_bound=0.1,
                upper_bound=0.4,
                descriptor="a low-mass companion with a minimum mass of",
            ),
            VariableGate(
                name="minmass",
                lower_bound=0.4,
                upper_bound=1.0,
                descriptor="a moderate-sized companion with a minimum mass of",
            ),
            VariableGate(
                name="minmass",
                lower_bound=1.0,
                upper_bound=1000.0,
                descriptor="a very high mass companion with a minimum mass of",
            ),
        ],
        "pb" : [
            VariableGate(
                name="pb",
                lower_bound=0.0,
                upper_bound=0.0833,
                descriptor="has an extremely tight orbital period of just",
                metric_prefix="hours",
            ),
            VariableGate(
                name="pb",
                lower_bound=0.0833,
                upper_bound=0.5,
                descriptor="has a very tight orbital period of just",
                metric_prefix="hours",
            ),
            VariableGate(
                name="pb",
                lower_bound=0.5,
                upper_bound=1.0,
                descriptor="has a quite tight orbital period of only",
                metric_prefix="hours",
            ),
            VariableGate(
                name="pb",
                lower_bound=1.0,
                upper_bound=2.0,
                descriptor="has a reasonably short orbital period of",
                metric_prefix="days",
            ),
            VariableGate(
                name="pb",
                lower_bound=2.0,
                upper_bound=10.0,
                descriptor="has a fairly typical orbital period of",
                metric_prefix="days",
            ),
            VariableGate(
                name="pb",
                lower_bound=10.0,
                upper_bound=50.0,
                descriptor="has a quite long orbital period of",
                metric_prefix="days",
            ),
            VariableGate(
                name="pb",
                lower_bound=50.0,
                upper_bound=365.0,
                descriptor="has a very long orbital period of",
                metric_prefix="days",
            ),
            VariableGate(
                name="pb",
                lower_bound=365.0,
                upper_bound=1e+99,
                descriptor="has an extremely long orbital period of",
                metric_prefix="years",
            ),
        ],
        "period" : [
            VariableGate(
                name="period",
                lower_bound=0.001,
                upper_bound=0.002,
                descriptor="a very fast millisecond pulsar with a period of",
                metric_prefix="milli",
            ),
            VariableGate(
                name="period",
                lower_bound=0.002,
                upper_bound=0.008,
                descriptor="a millisecond pulsar with a period of",
                metric_prefix="milli",
            ),
            VariableGate(
                name="period",
                lower_bound=0.008,
                upper_bound=0.02,
                descriptor="a relatively slow millisecond pulsar with a period of",
                metric_prefix="milli",
            ),
            VariableGate(
                name="period",
                lower_bound=0.02,
                upper_bound=0.1,
                descriptor="a quite fast pulsar with a period of",
                metric_prefix="milli",
            ),
            VariableGate(
                name="period",
                lower_bound=0.1,
                upper_bound=0.999,
                descriptor="a normal pulsar with a period of",
                metric_prefix="milli",
            ),
            VariableGate(
                name="period",
                lower_bound=1.0,
                upper_bound=2.0,
                descriptor="a normal pulsar with a period of",
            ),
            VariableGate(
                name="period",
                lower_bound=2.0,
                upper_bound=5.0,
                descriptor="a fairly slow pulsar with a period of",
            ),
            VariableGate(
                name="period",
                lower_bound=5.0,
                upper_bound=10.0,
                descriptor="a very slow pulsar with a period of",
            ),
            VariableGate(
                name="period",
                lower_bound=10.0,
                upper_bound=10000.0,
                descriptor="an extremely slow pulsar with a period of",
            ),
        ],
        "s1400" : [
            VariableGate(
                name="s1400",
                lower_bound=0.0,
                upper_bound=1e-6,
                descriptor="an extremely faint pulsar with a 1400 MHz catalogue flux density of",
                metric_prefix="μ",
            ),
            # Redundant description to output the correct metric_prefix
            VariableGate(
                name="s1400",
                lower_bound=1e-6,
                upper_bound=1e-4,
                descriptor="an extremely faint pulsar with a 1400 MHz catalogue flux density of",
                metric_prefix="μ",
            ),
            VariableGate(
                name="s1400",
                lower_bound=1e-4,
                upper_bound=5e-4,
                descriptor="a faint pulsar with a 1400 MHz catalogue flux density of",
                metric_prefix="m",
            ),
            VariableGate(
                name="s1400",
                lower_bound=5e-4,
                upper_bound=1e-3,
                descriptor="a weak pulsar with a 1400 MHz catalogue flux density of",
                metric_prefix="m",
            ),
            VariableGate(
                name="s1400",
                lower_bound=1e-3,
                upper_bound=5e-3,
                descriptor="a moderately bright pulsar with a 1400 MHz catalogue flux density of",
                metric_prefix="m",
            ),
            VariableGate(
                name="s1400",
                lower_bound=5e-3,
                upper_bound=2e-2,
                descriptor="a fairly bright pulsar with a 1400 MHz catalogue flux density of",
                metric_prefix="m",
            ),
            VariableGate(
                name="s1400",
                lower_bound=2e-2,
                upper_bound=0.1,
                descriptor="a bright pulsar with a 1400 MHz catalogue flux density of",
                metric_prefix="m",
            ),
            VariableGate(
                name="s1400",
                lower_bound=0.1,
                upper_bound=0.5,
                descriptor="a very bright pulsar with a 1400 MHz catalogue flux density of",
                metric_prefix="m",
            ),
            VariableGate(
                name="s1400",
                lower_bound=0.5,
                upper_bound=1e99,
                descriptor="an extremely bright pulsar with a 1400 MHz catalogue flux density of",
            ),
        ],
        "vtrans" : [
            VariableGate(
                name="vtrans",
                lower_bound=0,
                upper_bound=10.0,
                descriptor="an extremely low transverse velocity of",
            ),
            VariableGate(
                name="vtrans",
                lower_bound=10,
                upper_bound=30.0,
                descriptor="a low transverse velocity of",
            ),
            VariableGate(
                name="vtrans",
                lower_bound=30,
                upper_bound=100.0,
                descriptor="an intermediate transverse velocity of",
            ),
            VariableGate(
                name="vtrans",
                lower_bound=100,
                upper_bound=300.0,
                descriptor="a high transverse velocity of",
            ),
            VariableGate(
                name="vtrans",
                lower_bound=300,
                upper_bound=500.0,
                descriptor="a very high transverse velocity of",
            ),
            VariableGate(
                name="vtrans",
                lower_bound=500,
                upper_bound=1e+99,
                descriptor="an extremely high transverse velocity of",
            ),
        ]
    }
    return gate_defaults[variable_name]