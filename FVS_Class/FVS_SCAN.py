from utils import *
from .CalibrationStats import *
from .DWDVLOUT import *
from .CARBREPT import *
from .FUELOUT import *
from .CANFPROF import *
from .INPUT_OPTIONS import *


class FVS_SCAN:
    def __init__(self, index_lower, index_upper, text):
        self.index_lower = index_lower
        self.index_upper = index_upper

        self.text = text

        # values to set later
        self.stand_id = self.get_STAND_ID()
        try:
            self.calibration_statistics = Calibration_Statistics(self.text)
        except Exception as e:
            print("{}: Error on calibration statistics: ".format(self.stand_id), e)
            self.calibration_statistics = None
            
        # It is not guaranteed that DWDVLOUT is present in the text for a given FVS_SCAN
        try:
            self.dwdvlout = DWDVLOUT(self.text)
        except Exception as e:
            print("{}: Error on DWDVLOUT: ".format(self.stand_id), e)
            self.dwdvlout = None
        
        # It is not guaranteed that CARBREPT is present in the text for a given FVS_SCAN
        try:
            self.carbrept = CARBREPT(self.text)
        except Exception as e:
            print("{}: Error on CARBREPT: ".format(self.stand_id), e)
            self.carbrept = None
        
        # It is not guaranteed that FUELOUT is present in the text for a given FVS_SCAN
        try:
            self.fuelout = FUELOUT(self.text)
        except Exception as e:
            print("{}: Error on FUELOUT: ".format(self.stand_id), e)
            self.fuelout = None

        # It is not guaranteed that CANFPROF is present in the text for a given FVS_SCAN
        try:
            self.canfprof = CANFPROF(self.text)
        except Exception as e:
            print("{}: Error on CANFPROF: ".format(self.stand_id), e)
            self.canfprof = None

        try:
            self.input_options = INPUT_OPTIONS(self.text)
        except Exception as e:
            print("{}: Error on INPUT_OPTIONS: ".format(self.stand_id), e)
            self.input_options = None

        # free up memory by removing unnecessary text
        del self.text
   
    def get_STAND_ID(self):
        #find the line within the text that contains STAND ID=
        line_numbers = get_line_numbers_containing_word(self.text, 'STAND ID=')

        #get the third word from the line
        line = get_lines(self.text, line_numbers)[0]
        stand_id = get_ith_word_from_line(line, 2)

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

    def get_mgmt_id(self):
        #find the line number that contains the word MGMT ID:
        lower_bound = get_line_numbers_containing_word(self.text, 'MGMT ID:')[0]

        # get index of the word ID: 
        index = get_index_of_word_within_line(self.text[lower_bound], word='ID:')[1]
        index += 1 # add 1 to get the value

        # get the value
        mgmt_id = self.text[lower_bound].split()[index]
        
        return mgmt_id