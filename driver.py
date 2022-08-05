# clear the console
import os
os.system('cls' if os.name == 'nt' else 'clear')

from utils import *
from FVS_Class.FVS_SCAN import *
from FVS_Class import XY_PROJECTED
from FVS_Class import XY_LATLON
from FVS_Class import ISVALIDOUTPUT
from FVS_Class import VERSION_NUM
import mongo_interface

import Configs.config as cfg
import time


# Gets the line number of the beginning of the desired FVS index
def get_FVS_scans(file_name):
    # get line numbers containing the word STDIDENT
    line_numbers = get_line_numbers_containing_word(file_name, "OPTIONS SELECTED BY INPUT")
    line_numbers.append(len(get_all_lines(file_name)))
    
    """ parsed_outfile stores all extracted information for a given .out file"""
    parsed_outfile = {
        "treatments": [],

        "is_valid_output": False,
        
        # xy projected to albers
        "x_projected": None,
        "y_projected": None,
        # xy projected to latlon
        "x_latlon": None,
        "y_latlon": None,

        "version": None   
    }

    # gather the xy coordinates from the .outfile and store in the parsed dict
    xy_projected = XY_PROJECTED(get_all_lines(file_name))
    xy_latlon = XY_LATLON(get_all_lines(file_name))
    version = VERSION_NUM(get_all_lines(file_name))
    is_valid_output = ISVALIDOUTPUT(get_all_lines(file_name))

    parsed_outfile["is_valid_output"] = is_valid_output.value
    parsed_outfile["x_projected"] = xy_projected.x
    parsed_outfile["y_projected"] = xy_projected.y
    parsed_outfile["x_latlon"] = xy_latlon.x
    parsed_outfile["y_latlon"] = xy_latlon.y
    parsed_outfile["version"] = version.version


    # for every TREATMENT, get the line number of the lower and upper bounds
    for i in range(len(line_numbers)-1):
        my_text = get_lines(file_name, range(line_numbers[i]-1, line_numbers[i+1]-1))
        parsed_outfile["treatments"].append(FVS_SCAN(line_numbers[i]-1,line_numbers[i+1]-1, my_text))

    return parsed_outfile


def main():
    # for every .out file in the out_files folder
    for out_filename in cfg.my_out_files:
        # clear the console
        os.system('cls' if os.name == 'nt' else 'clear')
        # get every FVS Scan object (treatment) parsed from the .out file

        parsed_outfile = get_FVS_scans(out_filename)

        """ start a mongo connection """
        mongo_client = mongo_interface.get_client()
        # upload the FVS_SCANS to the mongo database
        mongo_interface.upload_scans(mongo_client, parsed_outfile, out_filename)

        print("Test Passed for file: {}".format(out_filename))
        # time.sleep(3)

# if this file is run as a script, run the main function
if __name__ == "__main__":
    main()