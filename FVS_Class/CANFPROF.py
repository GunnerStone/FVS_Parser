# import os
# import sys
""" import necessary util functions """
# from utils.get_all_lines import *
# from utils.get_indent_level import *
# from utils.get_index_of_word_within_line import *
# from utils.get_ith_word_from_line import *
# from utils.get_line_numbers_containing_word import *
# from utils.get_lines_with_indent_level import *
# from utils.get_lines import *
# from utils.is_number import *
from utils import *

class CANFPROF:
    def __init__(self, text):
        self.text = self.get_canfprof_text(text)
        self.stand_id = self.get_stand_id()
        self.mgmt_id = self.get_mgmt_id()
        self.valid_years, self.report_dict = self.get_report_dict()
         
    def get_canfprof_text(self, text):
        #find the line number that contains the word POTENTIAL FIRE REPORT (
        lower_bound = get_line_numbers_containing_word(text, 'POTENTIAL FIRE REPORT (')[0]
        
        # crop the text to all text after the lower_bound line
        canfprof_text = get_lines(text, range(lower_bound, len(text)))

        # find the first line that contains the word Structural statistics
        upper_bound = get_line_numbers_containing_word(canfprof_text, 'Structural statistics')[0]

        #cop the text to all text in between the bounds
        canfprof_text = get_lines(canfprof_text, range(0, upper_bound))

        return canfprof_text
    
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
        # Top level keys to index 
        top_level_indexes = ['FLAME LENGTH SURFACE', 
                            '(FT) TOTAL', 
                            'FIRE TYPE',
                            'PROB OF TORCHING',
                            'TORCH INDEX SEVERE MI/HR',
                            'CROWN INDEX SEVERE MI/HR',
                            'CNPY BASE HT FT',
                            'CANPY BULK DENSITY KG/M3',
                            'POTENTIAL MORTALITY',
                            'POTEN. SMOKE']
                            # 'FUEL MODELS']


        # Valid Ranges
        flame_length_surface_range = ['SEV','MOD']
        ft_total_range = ['SEV','MOD']
        fire_type_range = ['S','M']
        prob_torching_range = ['SEV','MOD']
        potential_mortality_range = ['SEV.%BA','MOD.%BA',
                                    'SEV.(TOT CU VOL)','MOD.(TOT CU VOL)']
        poten_smoke_range = ['SEV','MOD']
        

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

        """ get the values """
        flame_length_surface_sev_values = []
        flame_length_surface_mod_values = []
        ft_total_sev_values = []
        ft_total_mod_values = []
        fire_type_sev_values = []
        fire_type_mod_values = []
        prob_torching_sev_values = []
        prob_torching_mod_values = []

        torch_index_sev_mi_hr_values = []
        crown_index_sev_mi_hr_values = []
        cnpy_base_ht_ft_values = []
        canpy_bulk_density_kg_m3_values = []
        
        potential_mortality_sev_ba_values = []
        potential_mortality_mod_ba_values = []
        potential_mortality_sev_tot_values = []
        potential_mortality_mod_tot_values = []

        poten_smoke_sev_values = []
        poten_smoke_mod_values = []


        # lower_bound is still on correct starting line number
        # for every year
        for i in range(lower_bound, lower_bound+len(valid_years)):
            yearly_flame_length_surface_sev_values = []
            yearly_flame_length_surface_mod_values = []
            yearly_ft_total_sev_values = []
            yearly_ft_total_mod_values = []
            yearly_fire_type_sev_values = []
            yearly_fire_type_mod_values = []
            yearly_prob_torching_sev_values = []
            yearly_prob_torching_mod_values = []

            yearly_torch_index_sev_mi_hr_values = []
            yearly_crown_index_sev_mi_hr_values = []
            yearly_cnpy_base_ht_ft_values = []
            yearly_canpy_bulk_density_kg_m3_values = []

            yearly_potential_mortality_sev_ba_values = []
            yearly_potential_mortality_mod_ba_values = []
            yearly_potential_mortality_sev_tot_values = []
            yearly_potential_mortality_mod_tot_values = []

            yearly_poten_smoke_sev_values = []
            yearly_poten_smoke_mod_values = []

            """ Gather the columnal values for the current year """
            # keep track of which column we are looking at
            pointer_idx = 1 # value starts at 1 because the first word is the year

            """ FLAME LENGTH SURFACE """
            # get the value
            value = self.text[i].split()[pointer_idx]
            yearly_flame_length_surface_sev_values.append(value)

            # go over 1 column
            pointer_idx+=1
            value = self.text[i].split()[pointer_idx]
            yearly_flame_length_surface_mod_values.append(value)

            # increment the pointer
            pointer_idx += 1

            """ TOTAL (FT) """
            # get the value
            value = self.text[i].split()[pointer_idx]
            yearly_ft_total_sev_values.append(value)

            # go over 1 column
            pointer_idx+=1
            value = self.text[i].split()[pointer_idx]
            yearly_ft_total_mod_values.append(value)

            # increment the pointer
            pointer_idx += 1

            """ FIRE TYPE """   
            # get the value
            value = self.text[i].split()[pointer_idx]
            yearly_fire_type_sev_values.append(value)

            # go over 1 column
            pointer_idx+=1
            value = self.text[i].split()[pointer_idx]
            yearly_fire_type_mod_values.append(value)

            # increment the pointer
            pointer_idx += 1

            """ PROB OF TORCHING """
            # get the value
            value = self.text[i].split()[pointer_idx]
            yearly_prob_torching_sev_values.append(value)

            # go over 1 column
            pointer_idx+=1
            value = self.text[i].split()[pointer_idx]
            yearly_prob_torching_mod_values.append(value)

            # increment the pointer
            pointer_idx += 1

            """ TORCH INDEX SEVERE MI/HR """
            # get the value
            value = self.text[i].split()[pointer_idx]
            yearly_torch_index_sev_mi_hr_values.append(value)

            # go over 1 column
            pointer_idx+=1

            """ CROWN INDEX SEVERE MI/HR """
            # get the value
            value = self.text[i].split()[pointer_idx]
            yearly_crown_index_sev_mi_hr_values.append(value)

            # go over 1 column
            pointer_idx+=1

            """ CNPY BASE HT FT """
            # get the value
            value = self.text[i].split()[pointer_idx]
            yearly_cnpy_base_ht_ft_values.append(value)

            # go over 1 column
            pointer_idx+=1

            """ CANPY BULK DENSITY KG/M3 """
            # get the value
            value = self.text[i].split()[pointer_idx]
            yearly_canpy_bulk_density_kg_m3_values.append(value)

            # go over 1 column
            pointer_idx+=1

            """ POTENTIAL MORTALITY"""
            # get the value
            value = self.text[i].split()[pointer_idx]
            yearly_potential_mortality_sev_ba_values.append(value)

            # go over 1 column
            pointer_idx+=1

            # get the value
            value = self.text[i].split()[pointer_idx]
            yearly_potential_mortality_mod_ba_values.append(value)

            # go over 1 column
            pointer_idx+=1

            # get the value
            value = self.text[i].split()[pointer_idx]
            yearly_potential_mortality_sev_tot_values.append(value)
            
            # go over 1 column
            pointer_idx+=1

            # get the value
            value = self.text[i].split()[pointer_idx]
            yearly_potential_mortality_mod_tot_values.append(value)

            # go over 1 column
            pointer_idx+=1

            """ POTENTIAL SMOKE """
            # get the value
            value = self.text[i].split()[pointer_idx]
            yearly_poten_smoke_sev_values.append(value)

            # go over 1 column
            pointer_idx+=1

            # get the value
            value = self.text[i].split()[pointer_idx]
            yearly_poten_smoke_mod_values.append(value)

            # increment the pointer
            pointer_idx += 1

            """ Append the current year's values to the running list of all years' values"""
            flame_length_surface_sev_values.append(yearly_flame_length_surface_sev_values)
            flame_length_surface_mod_values.append(yearly_flame_length_surface_mod_values)
            ft_total_sev_values.append(yearly_ft_total_sev_values)
            ft_total_mod_values.append(yearly_ft_total_mod_values)
            fire_type_sev_values.append(yearly_fire_type_sev_values)
            fire_type_mod_values.append(yearly_fire_type_mod_values)
            prob_torching_sev_values.append(yearly_prob_torching_sev_values)
            prob_torching_mod_values.append(yearly_prob_torching_mod_values)
            
            torch_index_sev_mi_hr_values.append(yearly_torch_index_sev_mi_hr_values)
            crown_index_sev_mi_hr_values.append(yearly_crown_index_sev_mi_hr_values)
            cnpy_base_ht_ft_values.append(yearly_cnpy_base_ht_ft_values)
            canpy_bulk_density_kg_m3_values.append(yearly_canpy_bulk_density_kg_m3_values)
            
            potential_mortality_sev_ba_values.append(yearly_potential_mortality_sev_ba_values)
            potential_mortality_mod_ba_values.append(yearly_potential_mortality_mod_ba_values)
            potential_mortality_sev_tot_values.append(yearly_potential_mortality_sev_tot_values)
            potential_mortality_mod_tot_values.append(yearly_potential_mortality_mod_tot_values)

            poten_smoke_sev_values.append(yearly_poten_smoke_sev_values)
            poten_smoke_mod_values.append(yearly_poten_smoke_mod_values)
        

        """ map the data to a dictionary """
        flame_length_surface_zip_iterators = []
        ft_total_zip_iterators = []
        fire_type_zip_iterators = []
        prob_torching_zip_iterators = []

        torch_index_sev_mi_hr_zip_iterators = []
        crown_index_sev_mi_hr_zip_iterators = []
        cnpy_base_ht_ft_zip_iterators = []
        canpy_bulk_density_kg_m3_zip_iterators = []

        potential_mortality_zip_iterators = []

        poten_smoke_zip_iterators = []

        # loop through every valid year
        for i in range(len(valid_years)):
            # create a dictionary for the value ranges
            flame_length_surface_values = flame_length_surface_sev_values[i] + flame_length_surface_mod_values[i]
            flame_length_surface_zip_iterators.append(dict(zip(flame_length_surface_range, flame_length_surface_values)))

            ft_total_values = ft_total_sev_values[i] + ft_total_mod_values[i]
            ft_total_zip_iterators.append(dict(zip(ft_total_range, ft_total_values)))

            fire_type_values = fire_type_sev_values[i] + fire_type_mod_values[i]
            fire_type_zip_iterators.append(dict(zip(fire_type_range, fire_type_values)))

            prob_torching_values = prob_torching_sev_values[i] + prob_torching_mod_values[i]
            prob_torching_zip_iterators.append(dict(zip(prob_torching_range, prob_torching_values)))

            torch_index_sev_mi_hr_zip_iterators.append(dict(zip('TORCH INDEX SEVERE MI/HR', torch_index_sev_mi_hr_values[i])))
            crown_index_sev_mi_hr_zip_iterators.append(dict(zip('CROWN INDEX SEVERE MI/HR', crown_index_sev_mi_hr_values[i])))
            cnpy_base_ht_ft_zip_iterators.append(dict(zip('CNPY BASE HT FT', cnpy_base_ht_ft_values[i])))
            canpy_bulk_density_kg_m3_zip_iterators.append(dict(zip('CANPY BULK DENSITY KG/M3', canpy_bulk_density_kg_m3_values[i])))

            potential_mortality_values = potential_mortality_sev_ba_values[i] + potential_mortality_mod_ba_values[i] + potential_mortality_sev_tot_values[i] + potential_mortality_mod_tot_values[i]
            potential_mortality_zip_iterators.append(dict(zip(potential_mortality_range, potential_mortality_values)))

            poten_smoke_values = poten_smoke_sev_values[i] + poten_smoke_mod_values[i]
            poten_smoke_zip_iterators.append(dict(zip(poten_smoke_range, poten_smoke_values)))

            
        # flatten out the 1 deep indexed lists
        flattened_torch_index_sev_mi_hr_values = [item for sublist in torch_index_sev_mi_hr_values for item in sublist]
        flattened_crown_index_sev_mi_hr_values = [item for sublist in crown_index_sev_mi_hr_values for item in sublist]
        flattened_cnpy_base_ht_ft_values = [item for sublist in cnpy_base_ht_ft_values for item in sublist]
        flattened_canpy_bulk_density_kg_m3_values = [item for sublist in canpy_bulk_density_kg_m3_values for item in sublist]
        
        # create the dictionaries
        flame_length_surface_dict = dict(zip(valid_years, flame_length_surface_zip_iterators))
        ft_total_dict = dict(zip(valid_years, ft_total_zip_iterators))
        fire_type_dict = dict(zip(valid_years, fire_type_zip_iterators))
        prob_torching_dict = dict(zip(valid_years, prob_torching_zip_iterators))

        torch_index_sev_mi_hr_dict = dict(zip(valid_years, flattened_torch_index_sev_mi_hr_values))
        crown_index_sev_mi_hr_dict = dict(zip(valid_years, flattened_crown_index_sev_mi_hr_values))
        cnpy_base_ht_ft_dict = dict(zip(valid_years, flattened_cnpy_base_ht_ft_values))
        canpy_bulk_density_kg_m3_dict = dict(zip(valid_years, flattened_canpy_bulk_density_kg_m3_values))

        potential_mortality_dict = dict(zip(valid_years, potential_mortality_zip_iterators))

        poten_smoke_dict = dict(zip(valid_years, poten_smoke_zip_iterators))

        """ create the dataframe """
        # tie the dictionaries together

        canfprof_dict = {
        'FLAME LENGTH SURFACE': flame_length_surface_dict,
        '(FT) TOTAL': ft_total_dict,
        'FIRE TYPE': fire_type_dict,
        'PROB OF TORCHING': prob_torching_dict,
        
        'TORCH INDEX SEVERE MI/HR': torch_index_sev_mi_hr_dict,
        'CROWN INDEX SEVERE MI/HR': crown_index_sev_mi_hr_dict,
        'CNPY BASE HT FT': cnpy_base_ht_ft_dict,
        'CANPY BULK DENSTY KG/M3': canpy_bulk_density_kg_m3_dict,

        'POTENTIAL MORALITY': potential_mortality_dict,

        'POTENTIAL SMOKE': poten_smoke_dict

        }


        return valid_years, canfprof_dict