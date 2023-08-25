# @author: Evan Anthopoulos
# Version of Pulsar Paragraph program that has output in WIKI format rather than html for upload onto https://pulsars.org.au

import pandas as pd

from pulsar_paragraph.load_data import get_data_path

# This program takes data from the Swinburne supercomputer's pulsar catalogue
# and makes a description for each pulsar in a readable format.

# Important Note: All laws except for survey.law.csv are hardcoded to have 9 columns
# that must be entered in the specified order unless the order is changed.
class Gate:
    def init_gate(self, filename, counter: int):
        row_count, column_count = filename.shape
        lower_bound = float(filename.iloc[counter,0]) # AKA the lower gate, or the least value that is required to pass into a specific gate.
        upper_bound = float(filename.iloc[counter,1]) # AKA the upper gate, or the greatest value that something can be to pass into specific gate.
        g_type = str(filename.iloc[counter,2]) # AKA the descriptor usually containing adjectives, e.g "extremely young pulsar"
        g_format = int(filename.iloc[counter,3]) # # The number of decimal places the output is formatted in.
        g_syntax = str(filename.iloc[counter,4]) # Usually comes after g_type. Is a descriptor of what the specific value is, e.g "with an age of"
        g_prefix = str(filename.iloc[counter,5]) # Comes before g_type, is usually "a" or "an" depending on whether g_type begins with a vowel or consonant.
        g_unit = str(filename.iloc[counter,6]) # Unit for specific value. If left blank, an extra space will result, however this has been taken care of in laws_to_str final "if else" statement.
        g_factor = float(filename.iloc[counter,7]) # The number that the value will be multplied by. Leave a value of 1 if you do not want the value changed.
        g_scientific = str(filename.iloc[counter,8]) # Can only be 3 things: "f", "E", or "i", without the quotes. f = float, E = scientific notation, and i = integer, or no decimal places.
        ngate = [lower_bound,upper_bound,g_type,g_format,g_syntax,g_prefix,g_unit,g_factor,g_scientific]
        return ngate

    # This class creates a gate specifically for survey, as the survey.law.csv is unique
    def init_survey_gate(self, filename, counter: int):
        s_survey_str = str(filename.iloc[counter,0])
        s_survey_name = str(filename.iloc[counter,1])
        sgate = [s_survey_str,s_survey_name]
        return sgate


    class Law:
        # Contains n amount of gates, converts each gate to law, then
        # outputs a string according to the law.

        # This function iterates through the given law.csv and creates a list
        # that has n amount of lists inside of it, depending on how many rows are in the law.csv file.
        def load(self, law_name, law_type):
            g = Gate()
            row_count, column_count = law_name.shape
            n_gate = []
            s_gate = []
            d_gate = []
            if 'survey.law.csv' == str(law_type):
                for i in range(row_count):
                    gate = g.init_survey_gate(law_name, i)
                    s_gate.append(gate)
                return s_gate
            elif 'dec.law.csv' == str(law_type):
                for j in range(row_count):
                    gate = g.init_dec_gate(law_name, j)
                    d_gate.append(gate)
                return d_gate
            else:
                for k in range(row_count):
                    gate = g.init_gate(law_name, k)
                    n_gate.append(gate)
                return n_gate


        # This function is specifically for the surveys. It reads in the surveys from df that and
        # are initialized in init_survey_gate and converts them into lists that are then
        # converted to strings from survey.law.csv.
        def survey_law(self, survey_load, survey_file, survey_type, survey_num: str):
            row_count, column_count = survey_load.shape
            s_law = self.load(survey_load, survey_file)
            survey = str(survey_num).strip()
            final_str = 'None'
            for k in range(row_count):
                if '*' not in survey:
                    if ',' in survey:
                        first_comma = survey.index(',')
                        first_survey = str(survey[:first_comma].strip())
                        for law in s_law:
                            survey_str1 = str(law[0]).strip()
                            survey_name1 = str(law[1])
                            if survey_str1 == first_survey:
                                if 'normal' == survey_type:
                                    final_str = str(survey_name1)
                                elif 'name' == survey_type:
                                    final_str = first_survey
                    else:
                        for law in s_law:
                            survey_str2 = str(law[0]).strip()
                            survey_name2 = str(law[1])
                            if survey_str2 == survey:
                                if 'normal' == survey_type:
                                    final_str = str(survey_name2)
                                elif 'name' == survey_type:
                                    final_str = survey
                else:
                    pass
            return final_str


        # Law that converts dec info to str. Dec info is found in PSR name, e.g J0437-4715, as + or -.
        # Has a function because a law is not necessary. The sentence formatting is at the bottom of the file in an if statement.
        def dec_law(self, dec_num):
            dec = str(dec_num).strip()
            final_str = 'None'
            if '*' not in str(dec):
                        if '+' in dec:
                            final_str = 'Northern Hemisphere'
                        elif '-' in dec:
                            final_str = 'Southern Hemisphere'
            return final_str



        # Converts assoc str to descriptor. Does not have a law because data-type is unique.
        # Breaks the data into lists, then converts data to str depending on data-type. Then, appended to a final str.
        # Does not work for every case, which is why there are some .replace methods at the bottom of file.
        # Final output is of truncated type, aka one/two sentence descriptor max.
        def assoc_to_str(self, df_file, assoc_list, counter: int):
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
            assoc = str(assoc_list[counter]).strip()
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



        # Function that reads in p1 directly from file and outpute a string. Has 3 outcomes depending if p1 is +, -, or 0.
        def p1_to_str(self, p1_list, psr_list, counter: int):
            p1 = str(p1_list[counter])
            if '*' not in p1:
                p1 = float(p1)
                if p1 < 0:
                    p1 = '{:.2e}'.format(p1)
                    p1 = str(p1)
                    return ' This pulsar has an unusual negative period derivative of ' + p1 + '.' + ' Because it is negative, it has no estimate of magnetic field strength or characteristic age.'
                else:
                    p1 = '{:.2e}'.format(p1)
                    p1 = str(p1)
                    return ' This pulsar has a period derivative of ' + p1 + '.'
            else:
                return ' PSR ' + str(psr_list[counter]).strip() + ' has no measured period derivative.'




        # This function takes the list of lists from l.load() and converts it to a string
        # Remember, l.load() calls an init function, so by extension this function does too.
        # It then reads in the data generated by calling those functions (which are from the law.csv files), and outputs a str.
        #    lawcontents: list of comma-separated values
        #    filename: the type of pulsar quantity being dealt with eg Period, DM, year
        #    value: the index of the pulsar's information in the master list
        def laws_to_str(self, lawcontents, filename, value: str) -> str:
            n_law = self.load(lawcontents, filename)
            for law_list in n_law:
                lower_bound = float(law_list[0])
                upper_bound = float(law_list[1])
                l_type = str(law_list[2].strip())
                l_format = int(law_list[3])
                l_syntax = str(law_list[4].strip())
                l_prefix = str(law_list[5].strip())
                l_unit = str(law_list[6].strip())
                l_factor = float(law_list[7])
                l_scientific = str(law_list[8]).strip()
                value = str(value)
                value = value.replace('D', 'E')
                if '*' not in str(value):
                    if lower_bound <= float(value) < upper_bound:
                        if float(value) > 0:
                            if 'f' == l_scientific:
                                value = float(value)
                                value *= l_factor
                                value = round(value, l_format)
                            elif 'E' == l_scientific:
                                value = float(value)
                                value *= l_factor
                                format_str = '{:.' + str(l_format) + 'e}'
                                value = format_str.format(value)
                                value = str(value)
                            if 'i' == l_scientific:
                                value = float(value)
                                value *= l_factor
                                value = round(value, l_format)
                                value = int(value)
                            if float(value) > 0:
                                if l_unit == '':
                                    return l_prefix + ' ' + l_type + ' ' + l_syntax + ' ' +  str(value).strip()
                                else:
                                    return l_prefix + ' ' + l_type + ' ' + l_syntax + ' ' +  str(value).strip() + ' ' + l_unit
                else:
                    return 'None'


def main():

    # Load in main csv file
    df = pd.read_csv(get_data_path('databasev7.csv'),  header=None, sep='~', engine='python')

    # Load in psrs_available file provided by Professor Bailes
    pulsars_available = pd.read_csv(get_data_path('pulsars-links_available.csv'), header=None, sep=",", engine='python')

    # Load in period law csv
    period_file = 'period.law.csv'
    period_law_csv = pd.read_csv(get_data_path(period_file), header=None, sep=',', engine='python')

    # Load in dm law csv
    dm_file = 'dm.law.csv'
    dm_law_csv = pd.read_csv(get_data_path(dm_file), header=None, sep=',', engine='python')

    # Load in age law csv
    age_file = 'age.law.csv'
    age_law_csv = pd.read_csv(get_data_path(age_file), header=None, sep=',', engine='python')

    # Load in bsurf law csv
    bsurf_file = 'bsurf.law.csv'
    bsurf_law_csv = pd.read_csv(get_data_path(bsurf_file), header=None, sep=',', engine='python')

    # Load in minmass law csv
    minmass_file = 'minmass.law.csv'
    minmass_law_csv = pd.read_csv(get_data_path(minmass_file), header=None, sep=',', engine='python')

    # Load in pb law csv
    pb_file = 'pb.law.csv'
    pb_law_csv = pd.read_csv(get_data_path(pb_file), header=None, sep=',', engine='python')

    # Load in ecc law csv
    ecc_file = 'ecc.law.csv'
    ecc_law_csv = pd.read_csv(get_data_path(ecc_file), header=None, sep=',', engine='python')

    #Load in s1400 law csv
    s1400_file = 's1400.law.csv'
    s1400_law_csv = pd.read_csv(get_data_path(s1400_file), header=None, sep=',', engine='python')

    # Load in survey law csv
    survey_file = 'survey.law.csv'
    survey_law_csv = pd.read_csv(get_data_path(survey_file), header=None, sep=',', engine='python')

    # Load in vtrans law csv
    vtrans_file = 'vtrans.law.csv'
    vtrans_law_csv = pd.read_csv(get_data_path(vtrans_file), header=None, sep=',', engine='python')

    # Define which data column within df corresponds to data type
    psr_col = 0
    psrs_available_col = 0
    bname_col = 2
    period_col = 4
    dm_col = 7
    pb_col = 12
    ecc_col = 15
    minmass_col = 18
    age_col = 23
    bsurf_col = 22
    year_col = 11
    survey_col = 10
    s1400_col = 24
    p1_col = 19
    vtrans_col = 51
    assoc_col = 47
    xx_col = 48
    yy_col = 49
    zz_col = 50
    dist_col = 52
    bname_col = 53
    px_col = 54

    # Create lists of data depending on column location within df
    psr_list = df.iloc[:,psr_col]
    bname_list = df.iloc[:,bname_col]
    period_list = df.iloc[:,period_col]
    dm_list = df.iloc[:,dm_col]
    pb_list = df.iloc[:,pb_col]
    ecc_list = df.iloc[:,ecc_col]
    minmass_list = df.iloc[:,minmass_col]
    age_list = df.iloc[:,age_col]
    bsurf_list = df.iloc[:,bsurf_col]
    year_list = df.iloc[:,year_col]
    survey_list = df.iloc[:,survey_col]
    s1400_list = df.iloc[:,s1400_col]
    p1_list = df.iloc[:,p1_col]
    vtrans_list = df.iloc[:,vtrans_col]
    assoc_list = df.iloc[:,assoc_col]
    xx_list = df.iloc[:,xx_col]
    yy_list = df.iloc[:,yy_col]
    zz_list = df.iloc[:,zz_col]
    dist_list = df.iloc[:,dist_col]
    psrs_available = list(pulsars_available.iloc[:, psrs_available_col])


    # Initialize classes
    g = Gate()
    l = g.Law()

    # Create .html file, then initialize start and end strings for the .html file.
    # Call start_str before for loop, call end_str after loop ends to print each one time.
    txt_file = open('pulsar_paragraphs.txt', 'w+')

    # Main Function Loop -- Calls the functions and outputs the paragraph to a .html file.
    # If statements check whether functions return actual data. If not, the string becomes
    # empty, thus only printing if there is actual data to print. The if statements also help to format the output.
    # This is when the final tweaking takes place before outputting the result.
    # Some if statements do unique things, such as the dist if statement, which actually produces a sentence by itself.
    for i in range(len(psr_list)):

        period_func_str = str(l.laws_to_str(period_law_csv, period_file, str(period_list[i])))
        dm_func_str = str(l.laws_to_str(dm_law_csv, dm_file, dm_list[i]))
        age_func_str = str(l.laws_to_str(age_law_csv, age_file, age_list[i]))
        bsurf_func_str = str(l.laws_to_str(bsurf_law_csv, bsurf_file, bsurf_list[i]))
        survey_func_str = str(l.survey_law(survey_law_csv, survey_file, 'normal', str(survey_list[i])))
        survey_name = str(l.survey_law(survey_law_csv, survey_file, 'name', str(survey_list[i])))
        pb_func_str = str(l.laws_to_str(pb_law_csv, pb_file, pb_list[i]))
        ecc_func_str = str(l.laws_to_str(ecc_law_csv, ecc_file, ecc_list[i]))
        minmass_func_str = str(l.laws_to_str(minmass_law_csv, minmass_file, minmass_list[i]))
        s1400_func_str = str(l.laws_to_str(s1400_law_csv, s1400_file, s1400_list[i]))
        dec_func_str = str(l.dec_law(psr_list[i]))
        p1_func_str = str(l.p1_to_str(p1_list, psr_list, i))
        vtrans_func_str = str(l.laws_to_str(vtrans_law_csv, vtrans_file, vtrans_list[i]))
        assoc_func_str = str(l.assoc_to_str(df, assoc_list, i))

        # PERIOD
        if 'None' not in period_func_str:
            if '*' not in str(bname_list[i]).strip():
                bname_str = ' (' + str(bname_list[i]).strip() + ')'
            else:
                bname_str = ''
            if 'None' not in dm_func_str:
                if str(psr_list[i]).strip() in psrs_available:
                    period_str = 'PSR ' + '[[https://pulsars.org.au/fold/meertime/' + str(psr_list[i]).strip() + '|' + str(psr_list[i]).strip() + ']]' + bname_str + ' is ' + period_func_str
                else:
                    # print(str(psr_list[i]), str(i))
                    period_str = 'PSR ' + str(psr_list[i]) + bname_str + 'is ' + period_func_str
            else:
                if str(psr_list[i]).strip() in psrs_available:
                    period_str = 'PSR ' + '[[https://pulsars.org.au/fold/meertime/' + str(psr_list[i]).strip() + '|' + str(psr_list[i]).strip() + ']]' + bname_str + ' is ' + period_func_str + '.'
                else:
                    period_str = 'PSR ' + str(psr_list[i]) + bname_str + 'is ' + period_func_str + '.'
        # DISPERSION MEASURE
        if 'None' not in dm_func_str:
            dm_str = ' and has ' + dm_func_str + '.'
        else:
            dm_str = ''
        # S1400
        if 'None' not in s1400_func_str:
            s1400_str = ' It is ' + s1400_func_str + '.'
        else:
            s1400_str = ''
        # YEAR
        if '*' not in str(year_list[i]):
            if '1089806188' in str(year_list[i]):
                year_str = ''
            elif (survey_func_str == '') or ('None' in survey_func_str):
                year_str = ' PSR ' + str(psr_list[i]) + ' was discovered in ' + str(year_list[i]) + '.'
            else:
                year_str = ' PSR ' + str(psr_list[i]) + 'was discovered in ' + str(year_list[i])
        else:
            year_str = ''
        # DISTANCE
        if '*' not in str(dist_list[i]):
            dist = float(dist_list[i])

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
                dist_str = ' The estimated distance to ' + str(psr_list[i]).strip() + ' is ' + str(dist) + ' pc. '
            else:
                dist_str = ' The YMD distance model suggests that the distance to ' + str(psr_list[i]).strip() + ' is ' + str(dist) + ' pc, but that is suspicious. '
        # SURVEY
        if 'None' not in survey_func_str:
            if year_str == '':
                survey_str = ''
            else:
                survey_str = ' as part of ' + '[[' + 'https://astronomy.swin.edu.au/~mbailes/encyc/' + survey_name + '_plots.html|' + survey_func_str + ']]' + '.'
        else:
            survey_str = ''
        # ORBITAL PERIOD
        if 'None' not in pb_func_str:
            if 'None' not in ecc_func_str:
                pb_str = ' PSR ' + str(psr_list[i]) + pb_func_str
            else:
                pb_str = ' PSR ' + str(psr_list[i]) + pb_func_str + '.'
        else:
            pb_str = ''
        # ECCENTRICITY
        if 'None' not in ecc_func_str:
            if pb_str == '':
                ecc_str = ' PSR ' + str(psr_list[i]) + ecc_func_str + '.'
            else:
                ecc_str = ' and ' + ecc_func_str + '.'
        else:
            ecc_str = ''
        # AGE
        if 'None' not in age_func_str:
            if 'PSR' in pb_str:
                age_temp_str = ' It '
            else:
                age_temp_str = ' PSR ' + str(psr_list[i])
            age_str = age_temp_str + ' is ' + age_func_str + '.'
        else:
            age_str = ''
        if 'None' not in bsurf_func_str:
        # BSURF
            if 'PSR' not in age_str:
                bsurf_str = ' PSR ' + str(psr_list[i]) + ' has ' + bsurf_func_str + '.'
            else:
                bsurf_str = ' It has ' + bsurf_func_str + '.'
        else:
            bsurf_str = ''
        # MINMASS
        if 'None' not in minmass_func_str:
            if '*' not in str(dist_list[i]):
                minmass_str = 'This pulsar has ' + minmass_func_str + '.'
            else:
                minmass_str = ' This pulsar has ' + minmass_func_str + '.'
        else:
            if '*' not in str(dist_list[i]):
                minmass_str = 'This pulsar appears to be solitary.'
            else:
                minmass_str = ' This pulsar appears to be solitary.'
        if 'None' not in assoc_func_str:
            if 'extragalactic' in assoc_func_str:
                assoc_str = 'It is ' + assoc_func_str
            else:
                assoc_str = assoc_func_str
        else:
            assoc_str = ''
        dec_flag = False
        if 'None' not in dec_func_str or '' == dec_func_str:
            if s1400_str != '':
                dec_temp_str = ' PSR ' + str(psr_list[i])
            else:
                dec_temp_str = ' It '
            if 'extragalactic' in assoc_str or assoc_str == '':
                dec_str = dec_temp_str + 'is a ' + dec_func_str + ' pulsar. '
                dec_flag = True
            elif '47Tuc' in assoc_str or 'and has' in assoc_str:
                dec_str = dec_temp_str + 'is a ' + dec_func_str + ' pulsar '
            else:
                dec_str = dec_temp_str + 'is a ' + dec_func_str + ' pulsar with '
        if 'None' not in vtrans_func_str:
            if 'PSR' not in bsurf_str:
                vtrans_str = ' PSR ' + str(psr_list[i]) + ' has ' + vtrans_func_str + '.'
            else:
                vtrans_str = ' It has ' + vtrans_func_str + '.'
        else:
            vtrans_str = ''
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