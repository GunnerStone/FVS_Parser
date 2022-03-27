from utils import *

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