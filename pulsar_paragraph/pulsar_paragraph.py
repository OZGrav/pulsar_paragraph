# @author: Evan Anthopoulos
# Version of Pulsar Paragraph program that has output in WIKI format rather than html for upload onto https://pulsars.org.au

import psrqpy
import numpy as np
import pandas as pd
import argparse

from pulsar_paragraph.load_data import get_data_path
from pulsar_paragraph.pulsar_classes import PulsarParagraph


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

def is_atnf_value(value):
    """Check if value is a valid ATNF value.

    Parameters
    ----------
    value: str
        The value to check.

    Returns
    -------
    is_atnf_value: bool
        True if value is a valid ATNF value, False otherwise.
    """
    if value == '*':
        return False
    elif np.isnan(value):
        return False
    else:
        return True


def shklovski_pdot_correction(pdot, p, dist, vtrans):
    """Correct pdot for the Shklovski effect.

    pdot: float
        The observed pdot.
    p: float
        The observed period in seconds.
    dist: float
        The distance to the pulsar in kpc.
    vtrans: float
        The transverse velocity of the pulsar in km/s.

    Returns
    -------
    pdot_corrected: float
        The corrected pdot.
    """
    c = 299792458. # m/s
    dist_m = dist * 1e3 * 3.08567758128e16 # convert kpc to m
    vtrans_ms = vtrans * 1e3 # convert km/s to m/s
    return pdot - p * vtrans_ms**2 / ( dist_m * c )


def create_pulsar_paragraph(
        pulsar_names=None,
        query=None,
        pulsar_paragraph=None,
        include_links=False,
    ):
    """Create a paragraph for each pulsar in pulsar_names."""

    if query is None:
        if pulsar_names is None:
            query = psrqpy.QueryATNF().pandas
        else:
            query = psrqpy.QueryATNF(psrs=list(pulsar_names)).pandas
    else:
        # Filter our query to only include pulsars in pulsar_names
        query = query[query['PSRJ'].isin(pulsar_names)]

    if pulsar_paragraph is None:
        pulsar_paragraph = PulsarParagraph()

    pulsars_available = pd.read_csv(get_data_path('pulsars-links_available.csv'), header=None, sep=",", engine='python')
    psrs_available = list(pulsars_available.iloc[:, 0])

    output_paragraphs = []
    for _, row in query.iterrows():
        if is_atnf_value(row['P1']) and is_atnf_value(row['P0']) and is_atnf_value(row['DIST']) and is_atnf_value(row['VTRANS']):
            # Values available for Shklovski correction
            pdot = shklovski_pdot_correction(row['P1'], row['P0'], row['DIST'], row['VTRANS'])
            age = row['P0'] / ( 2 * pdot ) * 3.1688087814029e-8 # convert to years
            bsurf = 3.2e19 * np.sqrt( row['P0'] * pdot )
        else:
            pdot = row['P1']
            age = row['AGE']
            bsurf = row['BSURF']


        period_func_str  = pulsar_paragraph.period.variable_value_to_str( row['P0'])
        dm_func_str      = pulsar_paragraph.dm.variable_value_to_str(     row['DM'])
        age_func_str     = pulsar_paragraph.age.variable_value_to_str(    age)
        bsurf_func_str   = pulsar_paragraph.bsurf.variable_value_to_str(  bsurf)
        pb_func_str      = pulsar_paragraph.pb.variable_value_to_str(     row['PB'])
        ecc_func_str     = pulsar_paragraph.ecc.variable_value_to_str(    row['ECC'])
        minmass_func_str = pulsar_paragraph.minmass.variable_value_to_str(row['MINMASS'])
        s1400_func_str   = pulsar_paragraph.s1400.variable_value_to_str(  row['S1400'])
        vtrans_func_str  = pulsar_paragraph.vtrans.variable_value_to_str( row['VTRANS'])
        dec_func_str     = pulsar_paragraph.dec_law(row['DECJ'])
        p1_func_str      = pulsar_paragraph.p1_to_str(pdot, row['PSRJ'])
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
        if row['PSRJ'] in psrs_available and include_links:
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
                dist_str = f" The estimated distance to {row['PSRJ']} is {dist} pc."
            else:
                dist_str = f" The YMD distance model suggests that the distance to {row['PSRJ']} is {dist} pc, but that is suspicious."
        else:
            dist_str = ''
        # SURVEY
        if survey_func_str is None:
            survey_str = ''
        else:
            if year_str == '':
                survey_str = ''
            else:
                if include_links:
                    survey_str = f" as part of [[https://astronomy.swin.edu.au/~mbailes/encyc/{survey_name}_plots.html|{survey_func_str}]]."
                else:
                    survey_str = f" as part of {survey_func_str}."
        # ORBITAL PERIOD
        if pb_func_str is None:
            pb_str = ''
        else:
            if ecc_func_str is None:
                pb_str = f" PSR {row['PSRJ']} {pb_func_str}."
            else:
                pb_str = f" PSR {row['PSRJ']} {pb_func_str}"
        # ECCENTRICITY
        if ecc_func_str is None:
            ecc_str = ''
        else:
            if pb_str == '':
                ecc_str = f" PSR {row['PSRJ']} {ecc_func_str}."
            else:
                ecc_str = f" and {ecc_func_str}."
        # AGE
        if age_func_str is None:
            age_str = ''
        else:
            if 'PSR' in pb_str:
                age_temp_str = ' It'
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
        # Assosiation
        if assoc_func_str is None:
            assoc_str = ''
        else:
            if 'extragalactic' in assoc_func_str:
                assoc_str = 'It is ' + assoc_func_str
            else:
                assoc_str = assoc_func_str
        # Declination
        if dec_func_str is not None or '' == dec_func_str:
            if s1400_str != '':
                dec_temp_str = f" PSR {row['PSRJ']} "
            else:
                dec_temp_str = ' It '
            if 'extragalactic' in assoc_str or assoc_str == '':
                dec_str = dec_temp_str + 'is a ' + dec_func_str + ' pulsar.'
            elif '47Tuc' in assoc_str or 'and has' in assoc_str:
                dec_str = dec_temp_str + 'is a ' + dec_func_str + ' pulsar '
            else:
                dec_str = dec_temp_str + 'is a ' + dec_func_str + ' pulsar with '
        else:
            dec_str = ''
        # vtrans
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
        output_paragraphs.append(end_str)
    return output_paragraphs

def main():
    parser = argparse.ArgumentParser(description="Creates a human readable summary of a pulsar based on information for the ANTF pulsar catalogue.")

    parser.add_argument("-p", "--pulsar_names", nargs="+", help="List of pulsar names. If none selected will process all pulsars.")
    parser.add_argument("-o", "--output_file", help="Output file name. If none supplied will print to stdout.")
    parser.add_argument("-l", "--include_links", action="store_true", help="Include links to pulsars.org.au and astronomy.swin.edu.au in the descriptions.")

    args = parser.parse_args()

    output_paragraphs = create_pulsar_paragraph(
        pulsar_names=args.pulsar_names,
        include_links=args.include_links,
    )
    if args.output_file:
        with open(args.output_file, 'w') as f:
            for paragraph in output_paragraphs:
                f.write(paragraph + '\n')
    else:
        for paragraph in output_paragraphs:
            print(paragraph)


if __name__ == '__main__':
    main()