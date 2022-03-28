from utils import *
class CARBREPT:
    def __init__(self, text):
        self.text = self.get_fuelout_text(text)
        self.stand_id = self.get_stand_id()
        self.mgmt_id = self.get_mgmt_id()
        self.valid_years, self.report_dict = self.get_report_dict()

        # free up memory
        del self.text
    
    def get_fuelout_text(self, text):
        # find the line number that contains the word STAND CARBON REPORT
        # left parenthesis signifies this is where the values lie, without parenthesis it is the metadata
        lower_bound = get_line_numbers_containing_word(text, 'STAND CARBON REPORT')[0]
        
        # crop the text to all text after the lower_bound line
        fuelout_text = get_lines(text, range(lower_bound, len(text)))

        # find the first line that contains the word FIRE MODEL VERSION
        upper_bound = get_line_numbers_containing_word(fuelout_text, 'FIRE MODEL VERSION')[0]

        #rcop the text to all text in between the bounds
        fuelout_text = get_lines(fuelout_text, range(0, upper_bound))

        return fuelout_text
        
    def get_mgmt_id(self):
        #find the line number that contains the word MGMT ID:
        lower_bound = get_line_numbers_containing_word(self.text, 'MGMT ID:')[0]

        # get index of the word ID: 
        index = get_index_of_word_within_line(self.text[lower_bound], word='ID:')[1]
        index += 1 # add 1 to get the value

        # get the value
        mgmt_id = self.text[lower_bound].split()[index]

        return mgmt_id

    def get_stand_id(self):
        #find the line number that contains the word STAND ID:
        lower_bound = get_line_numbers_containing_word(self.text, 'STAND ID:')[0]

        # get index of the word ID: 
        index = get_index_of_word_within_line(self.text[lower_bound], word='ID:')[0]
        index += 1 # add 1 to get the value

        # get the value
        stand_id = self.text[lower_bound].split()[index]

        return stand_id
    
    def get_report_dict(self):
        # Top level keys to index 
        top_level_indexes = ['Aboveground Live', 'Belowground', 'Forest',]


        # Valid Ranges
        aboveground_live_indexes = [    'Total',
                                        'Merch']       
        belowground_indexes = [ 'Live',
                                'Dead']
        forest_indexes = [  'DDW',
                            'Floor',
                            'Shb/Hrb']

        # Valid Standalone ranges (no toplevel index required)
        standdead_indexes = ['Stand Dead']
        totalstandcarbon_indexes = ['Total Stand Carbon']
        totalremovedcarbon_indexes = ['Total Removed Carbon']
        carbonreleasedfromfire_indexes = ['Carbon Released From Fire']

        

        """ get the valid years """
        # find the line number that contains the word YEAR
        lower_bound = get_line_numbers_containing_word(self.text, 'YEAR')[0]
        valid_years = []
        lower_bound += 2 # year values start 2 lines below the year line

        # Assume the valid years are the first word in the line until the end of the report
        # get the first word in the line and append to valid_years
        for i in range(lower_bound, len(self.text)):
            try:
                year = self.text[i].split()[0]
            except:
                break
            valid_years.append(year)

        """ get the SURFACE_FUEL values """
        aboveground_live_values = []
        belowground_values = []
        standdead_values = []
        forest_values = []
        totalstandcarbon_values = []
        totalremovedcarbon_values = []
        carbonreleasedfromfire_values = []

        # lower_bound is still on correct starting line number
        # for every year
        for i in range(lower_bound, lower_bound+len(valid_years)):
            yearly_aboveground_live_values = []
            yearly_belowground_values = []
            yearly_standdead_values = []
            yearly_forest_values = []
            yearly_totalstandcarbon_values = []
            yearly_totalremovedcarbon_values = []
            yearly_carbonreleasedfromfire_values = []

            """ Gather the columnal values for the current year """

            # keep track of where we are in the line
            pointer_idx = 1 # value starts at 1 because the first word is the year

            """ Aboveground Live value collection """
            # iterate through the aboveground live indexes
            for j in range(pointer_idx, pointer_idx+len(aboveground_live_indexes)):
                # get the value
                value = self.text[i].split()[j]

                # append to the yearly list
                yearly_aboveground_live_values.append(value)

            # increment the pointer
            pointer_idx += len(aboveground_live_indexes)

            """ Belowground value collection """
            # iterate through the belowground indexes
            for j in range(pointer_idx, pointer_idx+len(belowground_indexes)):
                # get the value
                value = self.text[i].split()[j]

                # append to the yearly list
                yearly_belowground_values.append(value)

            # increment the pointer
            pointer_idx += len(belowground_indexes)

            """ Standing Dead value collection """
            # iterate through the belowground indexes
            for j in range(pointer_idx, pointer_idx+1): #increment by 1 because there is only one value
                # get the value
                value = self.text[i].split()[j]

                # append to the yearly list
                yearly_standdead_values.append(value)

            # increment the pointer
            pointer_idx += 1

            """ Forest value collection """
            # iterate through the forest indexes
            for j in range(pointer_idx, pointer_idx+len(forest_indexes)):
                # get the value
                value = self.text[i].split()[j]

                # append to the yearly list
                yearly_forest_values.append(value)

            # increment the pointer
            pointer_idx += len(forest_indexes)

            """ Total Stand Carbon value collection """
            # iterate through the totalstandcarbon indexes
            for j in range(pointer_idx, pointer_idx+1): #increment by 1 because there is only one value
                # get the value
                value = self.text[i].split()[j]

                # append to the yearly list
                yearly_totalstandcarbon_values.append(value)
            
            # increment the pointer
            pointer_idx += 1
            
            """ Total Removed Carbon value collection """
            # iterate through the totalremovedcarbon indexes
            for j in range(pointer_idx, pointer_idx+1): #increment by 1 because there is only one value
                # get the value
                value = self.text[i].split()[j]

                # append to the yearly list
                yearly_totalremovedcarbon_values.append(value)

            # increment the pointer
            pointer_idx += 1

            """ Carbon Released from Fire value collection """
            # iterate through the carbonreleased indexes
            for j in range(pointer_idx, pointer_idx+1): #increment by 1 because there is only one value
                # get the value
                value = self.text[i].split()[j]
                
                # append to the yearly list
                yearly_carbonreleasedfromfire_values.append(value)

            # increment the pointer
            pointer_idx += 1

            """ Append the current year's values to the running list of all years' values"""
            aboveground_live_values.append([float(i) for i in yearly_aboveground_live_values])
            belowground_values.append([float(i) for i in yearly_belowground_values])
            standdead_values.append([float(i) for i in yearly_standdead_values])
            forest_values.append([float(i) for i in yearly_forest_values])
            totalstandcarbon_values.append([float(i) for i in yearly_totalstandcarbon_values])
            totalremovedcarbon_values.append([float(i) for i in yearly_totalremovedcarbon_values])
            carbonreleasedfromfire_values.append([float(i) for i in yearly_carbonreleasedfromfire_values])
            
        ag_zip_iterrators = []
        bg_zip_iterrators = []
        sd_zip_iterrators = []
        f_zip_iterrators = []
        tsc_zip_iterrators = []
        trc_zip_iterrators = []
        crf_zip_iterrators = []

        for i in range(len(valid_years)):
            ag_zip_iterrators.append(dict(zip(aboveground_live_indexes, aboveground_live_values[i])))
            bg_zip_iterrators.append(dict(zip(belowground_indexes, belowground_values[i])))
            # sd_zip_iterrators.append(dict(zip(['Stand Dead'], standdead_values[i])))
            f_zip_iterrators.append(dict(zip(forest_indexes, forest_values[i])))
            # tsc_zip_iterrators.append(dict(zip(['Total Stand Carbon'], [totalstandcarbon_values[i]])))
            # trc_zip_iterrators.append(dict(zip(['Total Removed Carbon'], [totalremovedcarbon_values[i]])))
            # crf_zip_iterrators.append(dict(zip(['Carbon Released from Fire'], [carbonreleasedfromfire_values[i]])))
        
        list_of_categories = ['Aboveground Live', 'Belowground', 'Stand Dead', 'Forest', 'Total Stand Carbon', 'Total Removed Carbon', 'Carbon Released from Fire']
        category_dicts = []
        for i in range(len(valid_years)):
            category_dicts.append(dict.fromkeys(list_of_categories))
        
        for i, year in enumerate(valid_years):
            category_dicts[i]['Aboveground Live'] = ag_zip_iterrators[i]
            category_dicts[i]['Belowground'] = bg_zip_iterrators[i]
            category_dicts[i]['Stand Dead'] = standdead_values[i][0]
            category_dicts[i]['Forest'] = f_zip_iterrators[i]
            category_dicts[i]['Total Stand Carbon'] = totalstandcarbon_values[i][0]
            category_dicts[i]['Total Removed Carbon'] = totalremovedcarbon_values[i][0]
            category_dicts[i]['Carbon Released from Fire'] = carbonreleasedfromfire_values[i][0]

        top_level_dict = dict.fromkeys(valid_years)

        for i, key in enumerate(top_level_dict):
            top_level_dict[key] = (category_dicts[i].copy())       

   
        return valid_years, top_level_dict
