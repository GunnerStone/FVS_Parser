from utils import *
class CARBREPT:
    def __init__(self, text):
        self.text = self.get_fuelout_text(text)
        self.stand_id = self.get_stand_id()
        self.mgmt_id = self.get_mgmt_id()
        self.valid_years, self.report_dict = self.get_report_dict()


    
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
            aboveground_live_values.append(yearly_aboveground_live_values)
            belowground_values.append(yearly_belowground_values)
            standdead_values.append(yearly_standdead_values)
            forest_values.append(yearly_forest_values)
            totalstandcarbon_values.append(yearly_totalstandcarbon_values)
            totalremovedcarbon_values.append(yearly_totalremovedcarbon_values)
            carbonreleasedfromfire_values.append(yearly_carbonreleasedfromfire_values)


        """ map the data to a dictionary """
        aboveground_live_zip_iterators = []
        belowground_zip_iterators = []
        standdead_zip_iterators = []
        forest_zip_iterators = []
        totalstandcarbon_zip_iterators = []
        totalremovedcarbon_zip_iterators = []
        carbonreleasedfromfire_zip_iterators = []

        # loop through every valid year
        for i in range(len(valid_years)):
            # create a dictionary for the value ranges
            aboveground_live_zip_iterators.append(dict(zip(aboveground_live_indexes, aboveground_live_values[i])))
            belowground_zip_iterators.append(dict(zip(belowground_indexes, belowground_values[i])))
            standdead_zip_iterators.append(dict(zip(standdead_indexes, standdead_values[i])))
            forest_zip_iterators.append(dict(zip(forest_indexes, forest_values[i])))
            totalstandcarbon_zip_iterators.append(dict(zip(totalstandcarbon_indexes, totalstandcarbon_values[i])))
            totalremovedcarbon_zip_iterators.append(dict(zip(totalremovedcarbon_indexes, totalremovedcarbon_values[i])))
            carbonreleasedfromfire_zip_iterators.append(dict(zip(carbonreleasedfromfire_indexes, carbonreleasedfromfire_values[i])))

            
        # create a dictionary for the valid years
        flattened_standdead_values = [item for sublist in standdead_values for item in sublist]
        flattened_totalstandcarbon_values = [item for sublist in totalstandcarbon_values for item in sublist]
        flattened_totalremovedcarbon_values = [item for sublist in totalremovedcarbon_values for item in sublist]
        flattened_carbonreleasedfromfire_values = [item for sublist in carbonreleasedfromfire_values for item in sublist]

        aboveground_live_dict = dict(zip(valid_years, aboveground_live_zip_iterators))
        belowground_dict = dict(zip(valid_years, belowground_zip_iterators))
        standdead_dict = dict(zip(valid_years, flattened_standdead_values))
        forest_dict = dict(zip(valid_years, forest_zip_iterators))
        totalstandcarbon_dict = dict(zip(valid_years, flattened_totalstandcarbon_values))
        totalremovedcarbon_dict = dict(zip(valid_years, flattened_totalremovedcarbon_values))
        carbonreleasedfromfire_dict = dict(zip(valid_years, flattened_carbonreleasedfromfire_values))
        
        # tie the dictionaries together

        carbrept_dict = {
        'Aboveground Live': aboveground_live_dict, 
        'Belowground': belowground_dict, 
        'Stand Dead': standdead_dict, 
        'Forest': forest_dict, 
        'Total Stand Carbon': totalstandcarbon_dict, 
        'Total Removed Carbon': totalremovedcarbon_dict, 
        'Carbon Released from Fire': carbonreleasedfromfire_dict
        }


        return valid_years, carbrept_dict
