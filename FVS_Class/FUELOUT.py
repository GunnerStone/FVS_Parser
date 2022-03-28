from utils import *

class FUELOUT:
    def __init__(self, text):
        self.text = self.get_fuelout_text(text)
        self.stand_id = self.get_stand_id()
        self.mgmt_id = self.get_mgmt_id()
        self.fuel_loading_types, self.surface_fuel_loading_types, self.standing_wood_loading_types, self.valid_years, self.valid_surface_fuel_dead_ranges, self.valid_surface_fuel_live_ranges, self.valid_standing_wood_dead_ranges, self.valid_standing_wood_live_ranges, self.report_dict = self.get_report_dict()

        # free up memory
        del self.text

    
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
        end_idx = get_index_of_word_within_line(self.text[lower_bound], word='TOTAL')[0]

        for i in range(start_idx, end_idx):
            valid_surface_fuel_live_ranges.append(self.text[lower_bound].split()[i])

        start_idx = end_idx + 1 # account for the surf total with +1
        end_idx = get_index_of_word_within_line(self.text[lower_bound], word='FOL')[0]

        for i in range(start_idx, end_idx):
            valid_standing_wood_dead_ranges.append(self.text[lower_bound].split()[i])
        
        start_idx = end_idx
        end_idx = get_index_of_word_within_line(self.text[lower_bound], word='TOTAL')[1]

        # append every word after the word FOL to the valid_standing_wood_live_ranges list
        for i in range(start_idx, end_idx):
            valid_standing_wood_live_ranges.append(self.text[lower_bound].split()[i])
        

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
        surface_fuel_total_values = []

        standing_wood_dead_values = []
        standing_wood_live_values = []

        standing_wood_total_values = []
        standing_wood_total_biomass_values = []
        standing_wood_total_cons_values = []
        standing_wood_biomass_removed_values = []

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

            surface_fuel_total_values.append(float(self.text[i].split()[pointer_idx]))

            # increment the pointer_idx
            pointer_idx += 1

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

            # increment the pointer_idx
            pointer_idx += len(valid_standing_wood_live_ranges)

            # grab the total standing wood value
            standing_wood_total_values.append(float(self.text[i].split()[pointer_idx]))

            # increment the pointer_idx
            pointer_idx += 1

            # grab the total biomass value
            standing_wood_total_biomass_values.append(float(self.text[i].split()[pointer_idx]))

            # increment the pointer_idx
            pointer_idx += 1

            # grab the total consumption value
            standing_wood_total_cons_values.append(float(self.text[i].split()[pointer_idx]))

            # increment the pointer_idx
            pointer_idx += 1

            # grab the biomass removed value
            standing_wood_biomass_removed_values.append(float(self.text[i].split()[pointer_idx]))


            """ Append the current year's values to the running list of all years' values"""
            surface_fuel_dead_values.append([float(i) for i in yearly_surface_fuel_dead_values])
            surface_fuel_live_values.append([float(i) for i in yearly_surface_fuel_live_values])
            standing_wood_dead_values.append([float(i) for i in yearly_standing_wood_dead_values])
            standing_wood_live_values.append([float(i) for i in yearly_standing_wood_live_values])
            
        """ Convert values to floats instead of strings """
        # surface_fuel_dead_values = [float(i) for i in surface_fuel_dead_values]
        """ Map values to sub-sub-categories """
        
        sf_df_r_zip_iterrators = []
        sf_lv_r_zip_iterrators = []
        
        sf_surf_r_zip_iterrators = []

        sw_d_r_zip_iterrators = []
        sw_l_r_zip_iterrators = []
        sw_total_r_zip_iterrators = []
        sw_biomass_r_zip_iterrators = []
        sw_cons_r_zip_iterrators = []
        sw_removed_r_zip_iterrators = []


        
        for i in range(len(valid_years)):
            sf_df_r_zip_iterrators.append(dict(zip(valid_surface_fuel_dead_ranges, surface_fuel_dead_values[i])))
            sf_lv_r_zip_iterrators.append(dict(zip(valid_surface_fuel_live_ranges, surface_fuel_live_values[i])))

            sf_surf_r_zip_iterrators.append(dict(zip(['SURF TOTAL'],[surface_fuel_total_values[i]])))

            sw_d_r_zip_iterrators.append(dict(zip(valid_standing_wood_dead_ranges, standing_wood_dead_values[i])))
            sw_l_r_zip_iterrators.append(dict(zip(valid_standing_wood_live_ranges, standing_wood_live_values[i])))

            sw_total_r_zip_iterrators.append(dict(zip(['TOTAL'],[standing_wood_total_values[i]])))
            sw_biomass_r_zip_iterrators.append(dict(zip(['TOTAL BIOMASS'],[standing_wood_total_biomass_values[i]])))
            sw_cons_r_zip_iterrators.append(dict(zip(['TOTAL CONSUMPTION'],[standing_wood_total_cons_values[i]])))
            sw_removed_r_zip_iterrators.append(dict(zip(['BIOMASS REMOVED'],[standing_wood_biomass_removed_values[i]])))


        """ Map sub-sub-categories to subcategories """
        list_of_surface_fuel_subcategories = ['DEAD FUEL','LIVE','SURF TOTAL']
        list_of_standing_wood_subcategories = ['DEAD','LIVE','TOTAL','TOTAL BIOMASS','TOTAL CONSUMPTION','BIOMASS REMOVED']

        subcategory_surface_fuel_dicts = []
        for i in range(len(valid_years)):
            subcategory_surface_fuel_dicts.append(dict.fromkeys(list_of_surface_fuel_subcategories))

        subcategory_standing_wood_dicts = []
        for i in range(len(valid_years)):
            subcategory_standing_wood_dicts.append(dict.fromkeys(list_of_standing_wood_subcategories))

        for i, year in enumerate(valid_years):
            subcategory_surface_fuel_dicts[i]['DEAD FUEL'] = sf_df_r_zip_iterrators[i]
            subcategory_surface_fuel_dicts[i]['LIVE'] = sf_lv_r_zip_iterrators[i]
            subcategory_surface_fuel_dicts[i]['SURF TOTAL'] = surface_fuel_total_values[i]

            subcategory_standing_wood_dicts[i]['DEAD'] = sw_d_r_zip_iterrators[i]
            subcategory_standing_wood_dicts[i]['LIVE'] = sw_l_r_zip_iterrators[i]
            subcategory_standing_wood_dicts[i]['TOTAL'] = standing_wood_total_values[i]
            subcategory_standing_wood_dicts[i]['TOTAL BIOMASS'] = standing_wood_total_biomass_values[i]
            subcategory_standing_wood_dicts[i]['TOTAL CONSUMPTION'] = standing_wood_total_cons_values[i]
            subcategory_standing_wood_dicts[i]['BIOMASS REMOVED'] = standing_wood_biomass_removed_values[i]

        list_of_categories = ['SURFACE FUEL (TONS/ACRE)','STANDING WOOD (TONS/ACRE)']
        category_dicts = []
        for i in range(len(valid_years)):
            category_dicts.append(dict.fromkeys(list_of_categories))
        
        for i, year in enumerate(valid_years):
            category_dicts[i]['SURFACE FUEL (TONS/ACRE)'] = subcategory_surface_fuel_dicts[i]
            category_dicts[i]['STANDING WOOD (TONS/ACRE)'] = subcategory_standing_wood_dicts[i]

            
        top_level_dict = dict.fromkeys(valid_years)            

        for i, key in enumerate(top_level_dict):
            top_level_dict[key] = (category_dicts[i].copy())


        fuel_loading_types = ['SURFACE FUEL','STANDING WOOD']
        surface_fuel_loading_types = ['DEAD FUEL','LIVE']
        standing_wood_loading_types = ['DEAD','LIVE']

        return fuel_loading_types, surface_fuel_loading_types, standing_wood_loading_types, valid_years, valid_surface_fuel_dead_ranges, valid_surface_fuel_live_ranges, valid_standing_wood_dead_ranges, valid_standing_wood_live_ranges, top_level_dict
