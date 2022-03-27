from utils import *

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
