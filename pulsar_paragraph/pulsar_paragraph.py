# @author: Evan Anthopoulos
# Version of Pulsar Paragraph program that has output in WIKI format rather than html for upload onto https://pulsars.org.au

import psrqpy
import numpy as np
import pandas as pd

from pulsar_paragraph.load_data import get_data_path
from pulsar_paragraph.default_gates import (
    period_defaults,
    dm_defaults,
    s1400_defaults,
    pb_defaults,
    ecc_defaults,
    age_defaults,
    bsurf_defaults,
    vtrans_defaults,
    minmass_defaults,
)


SURVEY_CODES = {
    "ar1": "the 1st Arecibo Survey",
    "ar2": "the 2nd Arecibo Survey",
    "ar3": "the 3rd Arecibo Survey",
    "ar4": "the 4th Arecibo Survey",
    "ar327": "the Arecibo 327 MHz Drift-Scan Survey",
    "chime": "the CHIME Pulsar Survey",
    "fast_gpps": "the FAST GPPS Survey",
    "fast": "the FAST Survey",
    "fast_mb": "the FAST 19-beam L-Band survey",
    "fast_uwb": "the FAST UWB Survey",
    "fermi": "the Fermi unidentified gamma-ray sources searches",
    "FermiAssoc": "the Fermi unidentified gamma-ray sources searches",
    "FermiBlind": "the Fermi Gamma-ray Observatory blind survey",
    "gbncc": "the Green Bank North Celestial Cap survey",
    "gb1": "the Green Bank Northern Hemisphere survey",
    "gb2": "the Princeton-NRAO survey",
    "gb3": "the Green Bank short-period survey",
    "gb4": "the Green Bank fast pulsar survey",
    "gbt350": "the Green Bank 350 MHz drift-scan survey",
    "ghrss": "the GMRT High Resolution Southern Sky Survey",
    "htru_c": " None",
    "htru_eff": "the Parkes High Time Resolution Universe survey (HTRU) - Effelsberg",
    "htru_i": " None",
    "htru_pks": "the Parkes High Time Resolution Universe survey (HTRU)",
    "jb1": "the Jodrell A survey",
    "jb2": "the Jodrell B survey",
    "lotaas": "the LOFAR Tied Array All-sky Survey",
    "mol1": "the 1st Molonglo survey",
    "mol2": "the 2nd Molonglo Survey",
    "meerkat_trapum": "the MeerKAT TRAPUM survey",
    "misc": "a minor survey",
    "palfa": "the Arecibo Multibeam Survey",
    "pksmb": "the Parkes multibeam pulsar survey",
    "pkshl": "the Parkes high-latitude multibeam pulsar survey",
    "pksngp": "the Parkes deep northern Galactic Plane survey",
    "pkssw": "the Parkes Swinburne intermediate latitude pulsar survey",
    "pks70": "the Parkes Southern Sky survey",
    "pks1": "the Parkes 20-cm survey",
    "pksmb": "the Parkes multibeam pulsar survey",
    "pamb": "the Parkes Perseus Arm multibeam survey",
    "phmb": "the Parkes high-latitude multibeam pulsar survey",
    "pksgc": "the Parkes globular cluster survey",
    "pkspa": "the Parkes Perseus Arm multibeam survey",
    "pks_superb": "the Parkes survey for pulsars and extragalactic radio bursts",
    "SBS_rrat": "the reprocessing of the Swinburne intermediate latitude survey",
    "superb": "the Parkes survey for pulsars and extragalactic radio bursts",
    "fast_crafts": "the FAST Drift Scan Surveys",
    "mwa_smart": "the MWA SMART pulsar survey",
    "pumps": "the Puschino Muktibeam Pulsar Survey",
    "tulipp": "the LOFAR Targetted Search for Polarized Pulsars",
}

class PulsarParagraph:
    def __init__(self, load_defaults=True):
        self.period = []
        self.period_decimal_places = 2

        self.dm = []
        self.dm_decimal_places = 3

        self.s1400 = []
        self.s1400_decimal_places = 3

        self.pb = []
        self.pb_decimal_places = 3

        self.ecc = []
        self.ecc_decimal_places = 3

        self.age = []
        self.age_decimal_places = 3

        self.bsurf = []
        self.bsurf_decimal_places = 2

        self.vtrans = []
        self.vtrans_decimal_places = 1

        self.minmass = []
        self.minmass_decimal_places = 3

        if load_defaults:
            self.period  = period_defaults()
            self.dm      = dm_defaults()
            self.s1400   = s1400_defaults()
            self.pb      = pb_defaults()
            self.ecc     = ecc_defaults()
            self.age     = age_defaults()
            self.bsurf   = bsurf_defaults()
            self.vtrans  = vtrans_defaults()
            self.minmass = minmass_defaults()

    def add_period(self, period):
        self.period.append(period)

    def display_periods(self):
        for period in self.period:
            period.display()

    def add_dm(self, dm):
        self.dm.append(dm)

    def display_dms(self):
        for dm in self.dm:
            dm.display()

    def add_s1400(self, s1400):
        self.s1400.append(s1400)

    def display_s1400s(self):
        for s1400 in self.s1400:
            s1400.display()

    def add_pb(self, pb):
        self.pb.append(pb)

    def display_pbs(self):
        for pb in self.pb:
            pb.display()

    def add_ecc(self, ecc):
        self.ecc.append(ecc)

    def display_eccs(self):
        for ecc in self.ecc:
            ecc.display()

    def add_age(self, age):
        self.age.append(age)

    def display_ages(self):
        for age in self.age:
            age.display()

    def add_bsurf(self, bsurf):
        self.bsurf.append(bsurf)

    def display_bsurfs(self):
        for bsurf in self.bsurf:
            bsurf.display()

    def add_vtrans(self, vtrans):
        self.vtrans.append(vtrans)

    def display_vtranss(self):
        for vtrans in self.vtrans:
            vtrans.display()

    def add_minmass(self, minmass):
        self.minmass.append(minmass)

    def display_minmasss(self):
        for minmass in self.minmass:
            minmass.display()

    def variable_value_to_str(self, variable_gates, value: str) -> str:
        if value == "*":
            return None
        for variable_gate in variable_gates:
            if variable_gate.lower_bound <= float(value) < variable_gate.upper_bound:
                return f"{variable_gate.descriptor} {value * variable_gate.factor} {variable_gate.unit}"


    def p1_to_str(self, p1, psr_name):
        """Function that reads in p1 directly from file and outpute a string. Has 3 outcomes depending if p1 is +, -, or 0.
        """
        if '*' in str(p1):
            return f' PSR {psr_name} has no measured period derivative.'
        else:
            p1 = float(p1)
            if p1 < 0:
                p1 = '{:.2e}'.format(p1)
                p1 = str(p1)
                return f' This pulsar has an unusual negative period derivative of {p1}. Because it is negative, it has no estimate of magnetic field strength or characteristic age.'
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



def main():
    pulsars_available = pd.read_csv(get_data_path('pulsars-links_available.csv'), header=None, sep=",", engine='python')
    psrs_available = list(pulsars_available.iloc[:, 0])
    txt_file = open('pulsar_paragraphs.txt', 'w+')

    # Main Function Loop -- Calls the functions and outputs the paragraph to a .html file.
    # If statements check whether functions return actual data. If not, the string becomes
    # empty, thus only printing if there is actual data to print. The if statements also help to format the output.
    # This is when the final tweaking takes place before outputting the result.
    # Some if statements do unique things, such as the dist if statement, which actually produces a sentence by itself.

    #query = psrqpy.QueryATNF(version=ATNF_VER).pandas
    pulsar_paragraph = PulsarParagraph()
    query = psrqpy.QueryATNF().pandas
    for index, row in query.iterrows():
        period_func_str  = pulsar_paragraph.variable_value_to_str(pulsar_paragraph.period,  row['P0'])
        dm_func_str      = pulsar_paragraph.variable_value_to_str(pulsar_paragraph.dm,      row['DM'])
        age_func_str     = pulsar_paragraph.variable_value_to_str(pulsar_paragraph.age,     row['AGE'])
        bsurf_func_str   = pulsar_paragraph.variable_value_to_str(pulsar_paragraph.bsurf,   row['BSURF'])
        pb_func_str      = pulsar_paragraph.variable_value_to_str(pulsar_paragraph.pb,      row['PB'])
        ecc_func_str     = pulsar_paragraph.variable_value_to_str(pulsar_paragraph.ecc,     row['ECC'])
        minmass_func_str = pulsar_paragraph.variable_value_to_str(pulsar_paragraph.minmass, row['MINMASS'])
        s1400_func_str   = pulsar_paragraph.variable_value_to_str(pulsar_paragraph.s1400,   row['S1400'])
        vtrans_func_str  = pulsar_paragraph.variable_value_to_str(pulsar_paragraph.vtrans,  row['VTRANS'])
        dec_func_str     = pulsar_paragraph.dec_law(row['DECJ'])
        p1_func_str      = pulsar_paragraph.p1_to_str(row['P1'], row['PSRJ'])
        assoc_func_str   = pulsar_paragraph.assoc_to_str(row['ASSOC'])
        if type(row['SURVEY']) == str:
            survey_name      = row['SURVEY'].split(',')[0]
            survey_func_str  = SURVEY_CODES[survey_name]
        else:
            survey_func_str  = None

        # Name
        if '*' == row['PSRB'] or type(row['PSRB']) == float:
            bname_str = ''
        else:
            bname_str = f" ({row['PSRB']})"
        if row['PSRJ'] in psrs_available:
            period_str = f"PSR [[https://pulsars.org.au/fold/meertime/{row['PSRJ']}|{row['PSRJ']}]]{bname_str} is {period_func_str}"
        else:
            period_str = f"PSR {row['PSRJ']}{bname_str} is {period_func_str}"

        # DISPERSION MEASURE
        if dm_func_str is None:
            dm_str = '.'
        else:
            dm_str = ' and has ' + dm_func_str + '.'
        # S1400
        if s1400_func_str is None:
            s1400_str = ''
        else:
            s1400_str = ' It is ' + s1400_func_str + '.'
        # YEAR
        if '*' == row['DATE'] or type(row['DATE']) == float:
            year_str = ''
        else:
            if '1089806188' in str(row['DATE']):
                year_str = ''
            elif (survey_func_str == '') or (survey_func_str is None):
                year_str = f" PSR {row['PSRJ']} was discovered in {row['DATE']}."
            else:
                year_str = f" PSR {row['PSRJ']} was discovered in {row['DATE']}"
        # DISTANCE
        if '*' not in str(row['DIST']) and not np.isnan(row['DIST']):
            dist = float(row['DIST'])

            # For globular clusters
            if '47Tuc' in assoc_func_str:
                dist = 4.5
            elif 'M10' in assoc_func_str:
                dist = 4.4
            elif 'M13' in assoc_func_str:
                dist = 7.1
            elif 'M14' in assoc_func_str:
                dist = 9.3
            elif 'M15' in assoc_func_str:
                dist = 10.4
            elif 'M22' in assoc_func_str:
                dist = 3.2
            elif 'M28' in assoc_func_str:
                dist = 5.5
            elif 'M2' in assoc_func_str:
                dist = 11.5
            elif 'M30' in assoc_func_str:
                dist = 8.1
            elif 'NGC5272' in assoc_func_str:
                dist = 10.2
            elif 'M4' in assoc_func_str:
                dist = 2.2
            elif 'M53' in assoc_func_str:
                dist = 17.9
            elif 'M5' in assoc_func_str:
                dist = 7.5
            elif 'M62' in assoc_func_str:
                dist = 6.8
            elif 'M71' in assoc_func_str:
                dist = 4.0
            elif 'NGC1851' in assoc_func_str:
                dist = 12.1
            elif 'NGC5986' in assoc_func_str:
                dist = 10.4
            elif 'NGC6341' in assoc_func_str:
                dist = 8.3
            elif 'NGC6397' in assoc_func_str:
                dist = 2.3
            elif 'NGC6440' in assoc_func_str:
                dist = 8.5
            elif 'NGC6441' in assoc_func_str:
                dist = 11.6
            elif 'NGC6517' in assoc_func_str:
                dist = 10.6
            elif 'NGC6522' in assoc_func_str:
                dist = 7.7
            elif 'NGC6539' in assoc_func_str:
                dist = 7.8
            elif 'NGC6544' in assoc_func_str:
                dist = 3.0
            elif 'NGC6624' in assoc_func_str:
                dist = 7.9
            elif 'NGC6652' in assoc_func_str:
                dist = 10.0
            elif 'NGC_6712' in assoc_func_str:
                dist = 6.9
            elif 'NGC6749' in assoc_func_str:
                dist = 7.9
            elif 'NGC6752' in assoc_func_str:
                dist = 4.0
            elif 'NGC6760' in assoc_func_str:
                dist = 7.4
            elif 'OmegaCen' in assoc_func_str:
                dist = 5.2
            elif 'Ter5' in assoc_func_str:
                dist = 6.9
            elif 'NGC6342' in assoc_func_str:
                dist = 8.5
            dist = int(float(dist) * 1000)
            if float(dist) < 15000:
                dist_str = f" The estimated distance to {row['PSRJ']} is {dist} pc. "
            else:
                dist_str = f" The YMD distance model suggests that the distance to {row['PSRJ']} is {dist} pc, but that is suspicious. "
        # SURVEY
        if survey_func_str is None:
            survey_str = ''
        else:
            if year_str == '':
                survey_str = ''
            else:
                survey_str = f" as part of [[https://astronomy.swin.edu.au/~mbailes/encyc/{survey_name}_plots.html|{survey_func_str}]]."
        # ORBITAL PERIOD
        if pb_func_str is None:
            pb_str = ''
        else:
            if ecc_func_str is None:
                pb_str = f" PSR {row['PSRJ']}{pb_func_str}."
            else:
                pb_str = f" PSR {row['PSRJ']}{pb_func_str}"
        # ECCENTRICITY
        if ecc_func_str is None:
            ecc_str = ''
        else:
            if pb_str == '':
                ecc_str = f" PSR {row['PSRJ']}{ecc_func_str}."
            else:
                ecc_str = f" and {ecc_func_str}."
        # AGE
        if age_func_str is None:
            age_str = ''
        else:
            if 'PSR' in pb_str:
                age_temp_str = ' It '
            else:
                age_temp_str = f" PSR {row['PSRJ']}"
            age_str = f"{age_temp_str} is {age_func_str}."
        # BSURF
        if bsurf_func_str is None:
            bsurf_str = ''
        else:
            if 'PSR' in age_str:
                bsurf_str = f" It has {bsurf_func_str}."
            else:
                bsurf_str = f" PSR {row['PSRJ']} has {bsurf_func_str}."
        # MINMASS
        if minmass_func_str is None:
            minmass_str = 'This pulsar appears to be solitary.'
        else:
            minmass_str = 'This pulsar has ' + minmass_func_str + '.'
        if '*' == row['DIST'] or type(row['DIST']) == float:
            minmass_str = f" {minmass_str}"
        if assoc_func_str is None:
            assoc_str = ''
        else:
            if 'extragalactic' in assoc_func_str:
                assoc_str = 'It is ' + assoc_func_str
            else:
                assoc_str = assoc_func_str
        dec_flag = False
        if dec_func_str is not None or '' == dec_func_str:
            if s1400_str != '':
                dec_temp_str = ' PSR ' + row['PSRJ']
            else:
                dec_temp_str = ' It '
            if 'extragalactic' in assoc_str or assoc_str == '':
                dec_str = dec_temp_str + 'is a ' + dec_func_str + ' pulsar. '
                dec_flag = True
            elif '47Tuc' in assoc_str or 'and has' in assoc_str:
                dec_str = dec_temp_str + 'is a ' + dec_func_str + ' pulsar '
            else:
                dec_str = dec_temp_str + 'is a ' + dec_func_str + ' pulsar with '
        if vtrans_func_str is None:
            vtrans_str = ''
        else:
            if 'PSR' not in bsurf_str:
                vtrans_str = ' PSR ' + row['PSRJ'] + ' has ' + vtrans_func_str + '.'
            else:
                vtrans_str = ' It has ' + vtrans_func_str + '.'
        # Adjustments to end_str because assoc function is not perfect.
        end_str = period_str + dm_str + s1400_str + dec_str + assoc_str + p1_func_str + pb_str + ecc_str + age_str + bsurf_str + vtrans_str + dist_str + minmass_str + year_str + survey_str
        if '(47Tuc)an' in end_str:
            end_str = end_str.replace('(47Tuc)an', '47Tuc with an')
            if 'with 47Tuc' in end_str:
                end_str = end_str.replace('with 47Tuc', '47Tuc')
        if 'and has located' in end_str:
            end_str = end_str.replace('and has located', 'located')
        if '.an' in end_str:
            end_str = end_str.replace('.an extragalactic pulsar located in the Small Magellanic Cloud.', ' with ')
        if 'with and' in end_str:
            end_str = end_str.replace('with and', 'and')
        if 'J0537-6910' in end_str or 'J0540-6919' in end_str:
            end_str = end_str.replace('.an extragalactic pulsar located in the Large Magellanic Cloud.', ', and has ')
            end_str = end_str.replace('It is a gamma-ray source (4FGL_J0540.3-6920), an extragalactic pulsar located in the Large Magellanic Cloud.an extragalactic pulsar located in the Large Magellanic Cloud.', 'It is an extragalactic pulsar located in the Large Magellanic Cloud, with a gamma-ray source (4FGL_J0540.3-6920) and ')
        if 'a gamma-ray source (4FGL_J0540.3-6920), an extragalactic pulsar located in the Large Magellanic Cloud,' in end_str:
            end_str = end_str.replace('a gamma-ray source (4FGL_J0540.3-6920), an extragalactic pulsar located in the Large Magellanic Cloud,', 'an extragalactic pulsar located in the Large Magellanic Cloud with a gamma-ray source (4FGL_J0540.3-6920)')
        if '(?)' in end_str:
            end_str = end_str.replace('(?)','')
        if ')a ' in end_str:
            end_str = end_str.replace(')a', ') a')
        if ')an' in end_str:
            end_str = end_str.replace(')an', ') an')
        if 'and located' in end_str or 'and  located' in end_str:
            end_str = end_str.replace ('and located', 'and is located')
            end_str = end_str.replace ('and  located', 'and is located')
        if ', located' or ',  located' in end_str:
            end_str = end_str.replace (', located', ', is located')
            end_str = end_str.replace (',  located', ', is located')
        if 'and an' in end_str or 'and  an' in end_str:
            end_str = end_str.replace ('and an', 'and has an')
            end_str = end_str.replace ('and  an', 'and has an')
        if ' ()' in end_str:
            end_str = end_str.replace(' ()', '')
        if ' with (' in end_str or '  with  ('in end_str or '  with (' in end_str or ' with  (' in end_str:
            end_str = end_str.replace(' with (', ' (')
            end_str = end_str.replace('  with (', ' (')
            end_str = end_str.replace(' with  (', ' (')
            end_str = end_str.replace('  with  (', ' (')
        if 'with located' in end_str or ' with  located in end_str':
            end_str = end_str.replace('with located', 'located')
            end_str = end_str.replace('with  located', 'located')
        if ') an' in end_str or ')  an' in end_str:
            end_str = end_str.replace(') an', ') and an')
            end_str = end_str.replace(')  an', ') and an')
        if ') a ' in end_str or ')  a ' in end_str:
            end_str = end_str.replace(') a ', ') and a ')
            end_str = end_str.replace(')  a ', ') and a ')
        if 'the optical counterpart.' in end_str:
            end_str = end_str.replace('the optical counterpart', 'an optical counterpart')
        if 'and  and' in end_str or 'and and' in end_str:
            end_str = end_str.replace('and and', 'and')
            end_str = end_str.replace('and  and', 'and')
        if ' and a supernova remnant (Vela)' in end_str:
            end_str = end_str.replace(' and a supernova remnant (Vela)', '')
        if ' and an associated x-ray source (Swift_J063343.8+063223)' in end_str:
            end_str = end_str.replace( 'and an associated x-ray source (Swift_J063343.8+063223)', '')
        if ' and an associated gamma-ray source (HESS_J1023-575)' in end_str:
            end_str = end_str.replace(' and an associated gamma-ray source (HESS_J1023-575)', '')
        if ')) and an optical counterpart' in end_str:
            end_str = end_str.replace('and an', 'with an')
        if ' and an associated gamma-ray source (1AGL_J)' in end_str:
            end_str = end_str.replace(' and an associated gamma-ray source (1AGL_J)', '')
        if 'It is an associated gamma-ray source' in end_str:
            end_str = end_str.replace('It is an associated gamma-ray source', 'It has an associated gamma-ray source')
        print(end_str, file = txt_file)

    txt_file.close()


if __name__ == '__main__':
    main()