from asyncio.windows_events import NULL

# import utils and FVS_Class
import os
import sys
fpath = os.path.join(os.path.dirname(__file__), 'utils')
print("MAGICAL FPATH: {}".format(fpath))
sys.path.append(fpath)
fpath = os.path.join(os.path.dirname(__file__), 'FVS_Class')
sys.path.append(fpath)
from utils import *

# print out the sys path
print("sys.path:", sys.path)

import Configs.config as cfg

class FVS_SCAN:
    def __init__(self, index_lower, index_upper, text):
        self.index_lower = index_lower
        self.index_upper = index_upper

        self.text = text

        # values to set later
        self.stand_id = self.get_STAND_ID()
        self.calibration_statistics = Calibration_Statistics(self.text)

        # It is not guaranteed that DWDVLOUT is present in the text for a given FVS_SCAN
        try:
            self.dwdvlout = DWDVLOUT(self.text)
        except Exception as e:
            self.dwdvlout = None
        
        # It is not guaranteed that CARBREPT is present in the text for a given FVS_SCAN
        try:
            self.carbrept = CARBREPT(self.text)
        except Exception as e:
            self.carbrept = None
        
        # It is not guaranteed that FUELOUT is present in the text for a given FVS_SCAN
        try:
            self.fuelout = FUELOUT(self.text)
        except Exception as e:
            self.fuelout = None

        try:
            self.canfprof = CANFPROF(self.text)
        except Exception as e:
            print(e)
            self.canfprof = None

    
    def get_STAND_ID(self):
        #find the line within the text that contains STAND ID=
        line_numbers = get_line_numbers_containing_word(self.text, 'STAND ID=')

        #get the third word from the line
        line = get_lines(self.text, line_numbers)[0]
        stand_id = get_ith_word_from_line(line, 2)

        return stand_id



class Calibration_Statistics:
    def __init__(self,text):
        self.text = self.get_statistics_text(text)
        self.tree_codes = self.get_tree_codes()
        self.descriptions = self.get_descriptions()
        self.values = self.get_values()

    """ gets the tree codes used within the statistics text"""
    def get_tree_codes(self):
        #find the line that contains the word CALIBRATION STATISTICS
        anchor_line = get_line_numbers_containing_word(self.text, 'CALIBRATION STATISTICS')[0]
        
        # check if first word in line is CALBSTAT (if yes, then the line is not the tree codes line)
        if self.text[anchor_line].split()[0] == 'CALBSTAT':
            # go to the second occuring line that contains CALIBRATION STATISTICS
            anchor_line = get_line_numbers_containing_word(self.text, 'CALIBRATION STATISTICS')[1]

        #get the single line that is 3 below the anchor_line number
        #this line contains the tree codes
        my_line = get_lines(self.text, [anchor_line+3])

        #get the number of occuring tree codes
        num_codes = len(my_line[0].split())
        
        # get all tree codes and return them
        tree_codes = []
        for i in range(num_codes):
            tree_codes.append(my_line[0].split()[i])

        return tree_codes

    """ gets the statistics text from a FVS_SCAN object's text """
    def get_statistics_text(self, text):
        #find the line number that contains the word CALIBRATION STATISTICS
        lower_bound = get_line_numbers_containing_word(text, 'CALIBRATION STATISTICS')[0]

        # check if first word in line is CALBSTAT (if yes, then the line is not the tree codes line)
        if text[lower_bound].split()[0] == 'CALBSTAT':
            # go to the second occuring line that contains CALIBRATION STATISTICS
            lower_bound = get_line_numbers_containing_word(text, 'CALIBRATION STATISTICS')[1]

        #find the line number that contains the word MISTLETOE
        upper_bound = get_line_numbers_containing_word(text, 'MISTLETOE')[0]
        upper_bound += 1 # add 1 to include line with mistletoe

        #get the text between the two line numbers
        statistics_text = get_lines(text, range(lower_bound, upper_bound))
        return statistics_text

    """ gets the values from the statistics text """
    def get_values(self):
        # iteritively get the values and add them to a list of dictionaries with the tree code as the key
        values = []

        # iterate through every line in the statistics text
        for line in self.text:
        
            # check if the current line contains x numbers where x is the number of tree codes
            # get the number of numeric values in the line
            line_values = []
            # iterate through every word in the line
            for word in line.split():
                # check if the word is a number
                if is_number(word):
                    line_values.append(word)
            # if the number of numeric values is the same as the number of tree codes
            # then the line contains the values
            if len(line_values) == len(self.tree_codes):
                # dictionary key is the tree code
                my_Values = {}
                # get each numeric value in the line and associate it with its tree code in a dictionary
                for i, value in enumerate(line_values):
                    my_Values[self.tree_codes[i]] = value
                # add the dictionary to the list of values
                values.append(my_Values)

        return values

    def get_descriptions(self):
        descriptions = []

        ignored_keywords = ['NOTE:','DG']

        #find the line that contains the word CALIBRATION STATISTICS
        lower_bound = get_line_numbers_containing_word(self.text, 'CALIBRATION STATISTICS')[0]
        lower_bound += 5 # add 4 to get to the line after the tree codes line

        #find the line number that contains the word MISTLETOE
        upper_bound = get_line_numbers_containing_word(self.text, 'MISTLETOE')[0]
        upper_bound += 1 # add 1 to include line with mistletoe

        #get the text between the two line numbers
        description_text = get_lines(self.text, range(lower_bound, upper_bound))
        
        description = []
        # iterate through every line in the description text
        for line in description_text:
            numeric_value_found = False
            # read through every word in the line until the word is a number and add it to the list
            for i, word in enumerate(line.split()):
                # check if the first word is a ignored keyword
                if word in ignored_keywords and i == 0:
                    break
                if not is_number(word):
                    description.append(word)
                else:
                    numeric_value_found = True
                    break
            if numeric_value_found == True:
                # convert the list of strings into a string and add it to the list of descriptions
                description = " ".join(description)
                descriptions.append(description)
                description = []

        return descriptions

class FUELOUT:
    def __init__(self, text):
        self.text = self.get_fuelout_text(text)
        self.stand_id = self.get_stand_id()
        self.mgmt_id = self.get_mgmt_id()
        self.fuel_loading_types, self.surface_fuel_loading_types, self.standing_wood_loading_types, self.valid_years, self.valid_surface_fuel_dead_ranges, self.valid_surface_fuel_live_ranges, self.valid_standing_wood_dead_ranges, self.valid_standing_wood_live_ranges, self.report_dict = self.get_report_dict()


    
    def get_fuelout_text(self, text):
        # find the line number that contains the word ALL fuels report (
        # left parenthesis signifies this is where the values lie, without parenthesis it is the metadata
        lower_bound = get_line_numbers_containing_word(text, 'ALL FUELS REPORT (')[0]
        
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
        fuel_loading_types = ['SURFACE FUEL','STANDING WOOD']
        surface_fuel_loading_types = ['DEAD FUEL','LIVE']
        standing_wood_loading_types = ['DEAD','LIVE']

        """ get the valid ranges """
        valid_surface_fuel_dead_ranges = []
        valid_surface_fuel_live_ranges = []
        valid_standing_wood_dead_ranges = []
        valid_standing_wood_live_ranges = []
        # find the line number that contains the word YEAR
        lower_bound = get_line_numbers_containing_word(self.text, 'YEAR')[0]

        # get the index of the word YEAR
        start_idx = get_index_of_word_within_line(self.text[lower_bound], word='YEAR')[0]

        # get the index of the first word HERB
        end_idx = get_index_of_word_within_line(self.text[lower_bound], word='HERB')[0]

        # get the valid ranges
        # append every word between start_idx and end_idx to the valid_surface_fuel_dead_ranges list
        for i in range(start_idx+1, end_idx):
            valid_surface_fuel_dead_ranges.append(self.text[lower_bound].split()[i])

        start_idx = end_idx
        end_idx = get_index_of_word_within_line(self.text[lower_bound], word='TOTAL')[0]+1

        for i in range(start_idx, end_idx):
            valid_surface_fuel_live_ranges.append(self.text[lower_bound].split()[i])
        
        start_idx = end_idx
        end_idx = get_index_of_word_within_line(self.text[lower_bound], word='FOL')[0]

        for i in range(start_idx, end_idx):
            valid_standing_wood_dead_ranges.append(self.text[lower_bound].split()[i])
        
        # append every word after the word FOL to the valid_standing_wood_live_ranges list
        for i in range(end_idx, len(self.text[lower_bound].split())):
            valid_standing_wood_live_ranges.append(self.text[lower_bound].split()[i])
        
        # manually edit the last element in the list to be SURF TOTAL
        valid_surface_fuel_live_ranges[-1] = 'SURF TOTAL'

        # mannually edit the third from last element in the list to be SURF TOTAL
        valid_standing_wood_live_ranges[-3] = 'TOTAL BIOMASS'
        valid_standing_wood_live_ranges[-2] = 'TOTAL CONS'
        valid_standing_wood_live_ranges[-1] = 'BIOMASS REMOVED'




        """ get the valid years """
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
        surface_fuel_dead_values = []
        surface_fuel_live_values = []
        standing_wood_dead_values = []
        standing_wood_live_values = []

        # lower_bound is still on correct starting line number
        # for every year
        for i in range(lower_bound, lower_bound+len(valid_years)):
            yearly_surface_fuel_dead_values = []
            yearly_surface_fuel_live_values = []
            yearly_standing_wood_dead_values = []
            yearly_standing_wood_live_values = []

            """ Gather the columnal values for the current year """

            # keep track of where we are in the line
            pointer_idx = 1 # value starts at 1 because the first word is the year

            # from the current line, grab all values from the valid_surface_fuel_dead_ranges list
            for j in range(pointer_idx, pointer_idx+len(valid_surface_fuel_dead_ranges)):
                # append values to the yearly_surface_fuel_dead_values list
                yearly_surface_fuel_dead_values.append(self.text[i].split()[j])

            # increment the pointer_idx
            pointer_idx += len(valid_surface_fuel_dead_ranges)

            # from the current line, grab all values from the valid_surface_fuel_live_ranges list
            for j in range(pointer_idx, pointer_idx+len(valid_surface_fuel_live_ranges)):
                # append values to the yearly_surface_fuel_live_values list
                yearly_surface_fuel_live_values.append(self.text[i].split()[j])
            
            # increment the pointer_idx
            pointer_idx += len(valid_surface_fuel_live_ranges)

            # from the current line, grab all values from the valid_standing_wood_dead_ranges list
            for j in range(pointer_idx, pointer_idx+len(valid_standing_wood_dead_ranges)):
                # append values to the yearly_standing_wood_dead_values list
                yearly_standing_wood_dead_values.append(self.text[i].split()[j])

            # increment the pointer_idx
            pointer_idx += len(valid_standing_wood_dead_ranges)

            # from the current line, grab all values from the valid_standing_wood_live_ranges list
            for j in range(pointer_idx, pointer_idx+len(valid_standing_wood_live_ranges)):
                # append values to the yearly_standing_wood_live_values list
                yearly_standing_wood_live_values.append(self.text[i].split()[j])

            """ Append the current year's values to the running list of all years' values"""
            surface_fuel_dead_values.append(yearly_surface_fuel_dead_values)
            surface_fuel_live_values.append(yearly_surface_fuel_live_values)
            standing_wood_dead_values.append(yearly_standing_wood_dead_values)
            standing_wood_live_values.append(yearly_standing_wood_live_values)

        """ map the data to a dictionary """
        surface_fuel_zip_iterators = []
        standing_wood_zip_iterators = []
        surface_fuel_dead_zip_iterators = []
        surface_fuel_live_zip_iterators = []
        standing_wood_dead_zip_iterators = []
        standing_wood_live_zip_iterators = []
        # loop through every valid year
        for i in range(len(valid_years)):
            # create a dictionary for the value ranges
            surface_fuel_dead_zip_iterator = zip(valid_surface_fuel_dead_ranges, surface_fuel_dead_values[i])
            surface_fuel_live_zip_iterator = zip(valid_surface_fuel_live_ranges, surface_fuel_live_values[i])
            standing_wood_dead_zip_iterator = zip(valid_standing_wood_dead_ranges, standing_wood_dead_values[i])
            standing_wood_live_zip_iterator = zip(valid_standing_wood_live_ranges, standing_wood_live_values[i])
            
            
            # append the dictionaries to the list
            surface_fuel_dead_zip_iterators.append(dict(surface_fuel_dead_zip_iterator))
            surface_fuel_live_zip_iterators.append(dict(surface_fuel_live_zip_iterator))
            standing_wood_dead_zip_iterators.append(dict(standing_wood_dead_zip_iterator))
            standing_wood_live_zip_iterators.append(dict(standing_wood_live_zip_iterator))
            
        # create a dictionary for the valid years
        surface_fuel_dead_dict = dict(zip(valid_years, surface_fuel_dead_zip_iterators))
        surface_fuel_live_dict = dict(zip(valid_years, surface_fuel_live_zip_iterators))
        standing_wood_dead_dict = dict(zip(valid_years, standing_wood_dead_zip_iterators))
        standing_wood_live_dict = dict(zip(valid_years, standing_wood_live_zip_iterators))

        # tie the dictionaries together

        fuel_loading_types = ['SURFACE FUEL','STANDING WOOD']
        surface_fuel_loading_types = ['DEAD FUEL','LIVE']
        standing_wood_loading_types = ['DEAD','LIVE']

        fuel_loading_dict = {'SURFACE FUEL': {'DEAD FUEL': surface_fuel_dead_dict, 'LIVE': surface_fuel_live_dict}, 'STANDING WOOD': {'DEAD': standing_wood_dead_dict, 'LIVE': standing_wood_live_dict}}

        return fuel_loading_types, surface_fuel_loading_types, standing_wood_loading_types, valid_years, valid_surface_fuel_dead_ranges, valid_surface_fuel_live_ranges, valid_standing_wood_dead_ranges, valid_standing_wood_live_ranges, fuel_loading_dict



    def get_mgmt_id(self):
        #find the line number that contains the word MGMT ID:
        lower_bound = get_line_numbers_containing_word(self.text, 'MGMT ID:')[0]

        # get index of the word ID: 
        index = get_index_of_word_within_line(self.text[lower_bound], word='ID:')[1]
        index += 1 # add 1 to get the value

        # get the value
        mgmt_id = self.text[lower_bound].split()[index]
        
        return mgmt_id

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



    def get_mgmt_id(self):
        #find the line number that contains the word MGMT ID:
        lower_bound = get_line_numbers_containing_word(self.text, 'MGMT ID:')[0]

        # get index of the word ID: 
        index = get_index_of_word_within_line(self.text[lower_bound], word='ID:')[1]
        index += 1 # add 1 to get the value

        # get the value
        mgmt_id = self.text[lower_bound].split()[index]
        
        return mgmt_id


class DWDVLOUT:
    def __init__(self,text):
        self.text = self.get_ddwv_text(text)
        self.stand_id = self.get_stand_id()
        self.mgmt_id = self.get_mgmt_id()
        self.wood_types, self.valid_years, self.valid_ranges, self.report_dict = self.get_report_dict()

    def get_ddwv_text(self, text):
        #find the line number that contains the word DOWN DEAD WOOD VOLUME
        lower_bound = get_line_numbers_containing_word(text, 'DOWN DEAD WOOD VOLUME')[0]
        
        # crop the text to all text after the lower_bound line
        ddwv_text = get_lines(text, range(lower_bound, len(text)))

        # find the first line that contains the word FIRE MODEL VERSION
        upper_bound = get_line_numbers_containing_word(ddwv_text, 'FIRE MODEL VERSION')[0]

        #cop the text to all text in between the bounds
        ddwv_text = get_lines(ddwv_text, range(0, upper_bound))

        return ddwv_text
    
    def get_stand_id(self):
        #find the line number that contains the word STAND ID:
        lower_bound = get_line_numbers_containing_word(self.text, 'STAND ID:')[0]

        # get index of the word ID: 
        index = get_index_of_word_within_line(self.text[lower_bound], word='ID:')[0]
        index += 1 # add 1 to get the value

        # get the value
        stand_id = self.text[lower_bound].split()[index]

        return stand_id
    
    def get_mgmt_id(self):
        #find the line number that contains the word MGMT ID:
        lower_bound = get_line_numbers_containing_word(self.text, 'MGMT ID:')[0]

        # get index of the word ID: 
        index = get_index_of_word_within_line(self.text[lower_bound], word='ID:')[1]
        index += 1 # add 1 to get the value

        # get the value
        mgmt_id = self.text[lower_bound].split()[index]

        return mgmt_id
        
    def get_report_dict(self):
        """
        returns a dictionary with the following keys:
        'HARD': hardwood volume
        'SOFT': softwood volume
        then indexed by the following keys:
        'YEAR': valid years of the report
        then indexed by the following keys:
        'range': valid ranges of the report
        """
        
        """ get the valid ranges """
        valid_ranges = []
        # find the line number that contains the word YEAR
        lower_bound = get_line_numbers_containing_word(self.text, 'YEAR')[0]

        # get the index of the word YEAR
        start_idx = get_index_of_word_within_line(self.text[lower_bound], word='YEAR')[0]

        # get the index of the word TOT
        end_idx = get_index_of_word_within_line(self.text[lower_bound], word='TOT')[0]

        # get the valid ranges
        # append every word between start_idx and end_idx to the valid_ranges list
        for i in range(start_idx+1, end_idx+1):
            valid_ranges.append(self.text[lower_bound].split()[i])
        
        """ get the valid years """
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

        """ get the hardwood volumes """
        hardwood_volumes = []

        # lower_bound is still on correct starting line number
        # read the next nth values where n is the len of valid ranges
        for i in range(lower_bound, lower_bound+len(valid_years)):
            yearly_hardwood_volumes = []
            for j in range(1, len(valid_ranges)+1):
                # get the jth word in the line
                try:
                    word = self.text[i].split()[j]
                    yearly_hardwood_volumes.append(word)
                except:
                    break
            hardwood_volumes.append(yearly_hardwood_volumes)

        """ get the softwood volumes """
        softwood_volumes = []

        # lower_bound is still on correct starting line number
        # read the next nth values where n is the len of valid ranges
        for i in range(lower_bound, lower_bound+len(valid_years)):
            yearly_softwood_volumes = []
            for j in range(len(valid_ranges)+1, len(valid_ranges)+1+len(valid_ranges)+1):
                # get the jth word in the line
                try:
                    word = self.text[i].split()[j] 
                    yearly_softwood_volumes.append(word)
                except:
                    break
            softwood_volumes.append(yearly_softwood_volumes)

        """ map the data to a dictionary """
        hard_zip_iterators = []
        soft_zip_iterators = []
        # loop through every valid year
        for i in range(len(valid_years)):
            # create a dictionary for the value ranges
            hard_zip_iterator = zip(valid_ranges, hardwood_volumes[i])
            soft_zip_iterator = zip(valid_ranges, softwood_volumes[i])

            # append the dictionaries to the list
            hard_zip_iterators.append(dict(hard_zip_iterator))
            soft_zip_iterators.append(dict(soft_zip_iterator))

        # create a dictionary for the valid years
        hard_years_dict = dict(zip(valid_years, hard_zip_iterators))
        soft_years_dict = dict(zip(valid_years, soft_zip_iterators))

        # tie the dictionaries together
        my_wood_types = ['HARD','SOFT']
        my_wood_dict = {'HARD': hard_years_dict, 'SOFT': soft_years_dict}

        return my_wood_types, valid_years, valid_ranges, my_wood_dict
        




    

# Gets the line number of the beginning of the desired FVS index
def get_FVS_scans(file_name):
    # get line numbers containing the word STDIDENT
    line_numbers = get_line_numbers_containing_word(file_name, "STDIDENT")
    line_numbers.append(len(get_all_lines(file_name)))

    FVS_SCANS = []
    # for every FVS run, get the line number of the lower and upper bounds
    for i in range(len(line_numbers)-1):
        my_text = get_lines(file_name, range(line_numbers[i]-1, line_numbers[i+1]-1))
        FVS_SCANS.append(FVS_SCAN(line_numbers[i]-1,line_numbers[i+1]-1, my_text))
    return FVS_SCANS

if __name__ == "__main__":

    def print_dwdvlout_report(file_name):
        #
        FVS_SCANS = get_FVS_scans(file_name)
        for scan in FVS_SCANS:
            # print the stand id
            print(scan.stand_id)

            
            # print the DOWN DEAD WOOD VOLUME REPORT
            if scan.dwdvlout is not None:
                wood_types = scan.dwdvlout.wood_types
                years = scan.dwdvlout.valid_years
                ranges = scan.dwdvlout.valid_ranges
                report_dict = scan.dwdvlout.report_dict

                print("DOWN DEAD WOOD VOLUME REPORT")
                
                for type in wood_types:
                    print("")
                    print("ESTIMATED DOWN WOOD VOLUME (CUFT/ACRE) BY SIZE CLASS (INCHES) FOR " + type + " WOOD")
                    my_ranges = "      "
                    for range in ranges:
                        my_ranges += (str("{0:10}".format(range) + " "))
                    print(my_ranges)
                    for year in years:
                        my_str = (year + ": ")
                        for range in ranges:
                            my_str += (str("{0:10}".format(report_dict[type][year][range])) + " ")
                        print(my_str)
                
            print("\n")
    def print_calibration_statistics(file_name):
        FVS_SCANS = get_FVS_scans(file_name)
        for scan in FVS_SCANS:
            # print the stand id
            print(scan.stand_id)
            # print calibration statistics
            for i in range(len(scan.calibration_statistics.descriptions)):
                # description of statistic
                print(scan.calibration_statistics.descriptions[i])

                # value of statistic for all tree codes
                print(scan.calibration_statistics.values[i])
    
    def print_carbrept(file_name):
        FVS_SCANS = get_FVS_scans(file_name)
        for scan in FVS_SCANS:
            # print the stand id
            print(scan.stand_id)
            if scan.carbrept is not None:
                # print carbrept
                report_dict = scan.carbrept.report_dict

                fo_keys = report_dict.keys()
                so_keys = scan.carbrept.valid_years
                abovegroundlive_keys = list(report_dict['Aboveground Live'][so_keys[0]].keys())
                belowground_keys = list(report_dict['Belowground'][so_keys[0]].keys())
                forest_keys = list(report_dict['Forest'][so_keys[0]].keys())

                print("--------------------------------------------------------------------------------")
                print("STAND CARBON REPORT for STAND ID: " + scan.stand_id + " ALL VARIABLES ARE RPORTED IN TONS/ACRE")
                print("--------------------------------------------------------------------------------")
                print("Aboveground Live: ")
                header = "      "
                for key in abovegroundlive_keys:
                    header += (str("{0:10}".format(key) + " "))
                print(header)
                for year in so_keys:
                    my_str = (year + ": ")
                    for key in abovegroundlive_keys:
                        my_str += (str("{0:10}".format(report_dict['Aboveground Live'][year][key])) + " ")
                    print(my_str)

                print("-----------------------------------------")
                print("Belowground: ")
                header = "      "
                for key in belowground_keys:
                    header += (str("{0:10}".format(key) + " "))
                print(header)
                for year in so_keys:
                    my_str = (year + ": ")
                    for key in belowground_keys:
                        my_str += (str("{0:10}".format(report_dict['Belowground'][year][key])) + " ")
                    print(my_str)
                
                print("-----------------------------------------")
                print("Stand Dead: ")
                for year in so_keys:
                    my_str = (year + ": ")
                    my_str += (str("{0:10}".format(report_dict['Stand Dead'][year])) + " ")
                    print(my_str)
                
                print("-----------------------------------------")
                print("Forest: ")
                header = "      "
                for key in forest_keys:
                    header += (str("{0:10}".format(key) + " "))
                print(header)
                for year in so_keys:
                    my_str = (year + ": ")
                    for key in forest_keys:
                        my_str += (str("{0:10}".format(report_dict['Forest'][year][key])) + " ")
                    print(my_str)

                print("-----------------------------------------")
                print("Total Stand Carbon: ")
                for year in so_keys:
                    my_str = (year + ": ")
                    my_str += (str("{0:10}".format(report_dict['Total Stand Carbon'][year])) + " ")
                    print(my_str)

                print("-----------------------------------------")
                print("Total Removed Carbon: ")
                for year in so_keys:
                    my_str = (year + ": ")
                    my_str += (str("{0:10}".format(report_dict['Total Removed Carbon'][year])) + " ")
                    print(my_str)
                
                print("-----------------------------------------")
                print("Carbon Released from Fire: ")
                for year in so_keys:
                    my_str = (year + ": ")
                    my_str += (str("{0:10}".format(report_dict['Carbon Released from Fire'][year])) + " ")
                    print(my_str)
                


    def print_fuelout_report(file_name):
        #
        FVS_SCANS = get_FVS_scans(file_name)
        for scan in FVS_SCANS:
            # print the stand id
            print(scan.stand_id)

            
            # print the ALL FUELS REPORT
            if scan.fuelout is not None:
                fuel_loading_types = scan.fuelout.fuel_loading_types
                surface_fuel_loading_types = scan.fuelout.surface_fuel_loading_types
                standing_wood_loading_types = scan.fuelout.standing_wood_loading_types
                valid_years = scan.fuelout.valid_years
                valid_surface_fuel_dead_ranges = scan.fuelout.valid_surface_fuel_dead_ranges
                valid_surface_fuel_live_ranges = scan.fuelout.valid_surface_fuel_live_ranges
                valid_standing_wood_dead_ranges = scan.fuelout.valid_standing_wood_dead_ranges
                valid_standing_wood_live_ranges = scan.fuelout.valid_standing_wood_live_ranges
                report_dict = scan.fuelout.report_dict


                for i, type in enumerate(fuel_loading_types):
                    print("ALL FUELS REPORT for " + str(type) + " in (TONS/ACRE)")
                    keys = list(report_dict[type].keys())
                    
                    my_ranges = "      "
                    if i == 0:
                        header = ("      " + str("{0:15}".format(str(keys[0]))))
                        for _ in range(0,len(valid_surface_fuel_dead_ranges)-1):
                            header += str("{0:15}".format(""))
                        header +=str(keys[1])

                        print(header) 

                        for label in valid_surface_fuel_dead_ranges:
                            my_ranges += (str("{0:14}".format(label) + " "))
                        for label in valid_surface_fuel_live_ranges:
                            my_ranges += (str("{0:14}".format(label) + " "))
                    else:
                        header = ("      " + str("{0:15}".format(str(keys[0]))))
                        for _ in range(0,len(valid_standing_wood_dead_ranges)-1):
                            header += str("{0:15}".format(""))
                        header +=str(keys[1])

                        print(header)
                        for label in valid_standing_wood_dead_ranges:
                            my_ranges += (str("{0:14}".format(label) + " "))
                        for label in valid_standing_wood_live_ranges:
                            my_ranges += (str("{0:14}".format(label) + " "))
                    print(my_ranges)
                    for year in valid_years:
                        my_str = (year + ": ")
                        if i == 0:
                            for label in valid_surface_fuel_dead_ranges:
                                my_str += (str("{0:14}".format(report_dict[type][keys[0]][year][label])) + " ")
                            for label in valid_surface_fuel_live_ranges:
                                my_str += (str("{0:14}".format(report_dict[type][keys[1]][year][label])) + " ")
                        else:
                            for label in valid_standing_wood_dead_ranges:
                                my_str += (str("{0:14}".format(report_dict[type][keys[0]][year][label])) + " ")
                            for label in valid_standing_wood_live_ranges:
                                my_str += (str("{0:14}".format(report_dict[type][keys[1]][year][label])) + " ")
                        
                        print(my_str)
                    print()
                
            print("\n")
    def print_canfprof_report(filename):
        #
        FVS_SCANS = get_FVS_scans(filename)
        for scan in FVS_SCANS:
            # print the stand id
            print(scan.stand_id)

            # print the CANFPROF REPORT
            if scan.canfprof is not None:
                valid_years = scan.canfprof.valid_years
                report_dict = scan.canfprof.report_dict

                print("CANFPROF REPORT EXISTS")

                for key in report_dict.keys():
                    print(key)
                    has_printed_subsubkey = False

                    for subkey in report_dict[key].keys():
                        curr_year = str(subkey)
                        try:
                            
                            # print out the subsub keys (attributes/tags)
                            if not has_printed_subsubkey:
                                my_line = "      "
                                for subsubkey in report_dict[key][subkey].keys():
                                    my_line+=("{0:20}".format(str(subsubkey)) + " ")

                                print(my_line)
                            has_printed_subsubkey = True
                            # print out the current year
                            my_line = str(curr_year+": ")

                            # print out the current year's values
                            for subsubkey in report_dict[key][subkey].keys():
                                my_line += "{0:20}".format((report_dict[key][subkey][subsubkey])) + " "
                            print(my_line)
                        except:
                            # if exception occurs, then it has a single value
                            my_line = str(curr_year+": ")
                            my_line+="{0:20}".format((report_dict[key][subkey])) + " "
                            print(my_line)
                    print()
            break

            print("\n") 
    # print_dwdvlout_report("ws11treat4rep.out")
    # print_fuelout_report("ws11treat4rep.out")
    # print_carbrept("ws11treat4rep.out")
    print_canfprof_report(cfg.my_out_file)

