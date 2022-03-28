# clear the console
import os
os.system('cls' if os.name == 'nt' else 'clear')

from utils import *
from FVS_Class.FVS_SCAN import *
import mongo_interface

import Configs.config as cfg

import psutil

# if this file is run as a script, run the main function
if __name__ == "__main__":

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
    def memory():
            import os, psutil
            process = psutil.Process(os.getpid())
            return (process.memory_info().rss)/1024  # in kilobytes 

    def test_case():
        # clear the console with os
        os.system('cls' if os.name == 'nt' else 'clear')
        # try:
        # print_dwdvlout_report(cfg.my_out_file)
        # os.system('cls' if os.name == 'nt' else 'clear')
        # print_fuelout_report(cfg.my_out_file)
        # os.system('cls' if os.name == 'nt' else 'clear')
        # print_carbrept(cfg.my_out_file)
        # os.system('cls' if os.name == 'nt' else 'clear')
        # print_canfprof_report(cfg.my_out_file)
        # os.system('cls' if os.name == 'nt' else 'clear')
        FVS_SCANS = get_FVS_scans(cfg.my_out_file)
        mongo_client = mongo_interface.get_client()
        mongo_interface.upload_scans(mongo_client, FVS_SCANS, cfg.my_out_file)
        print("Test Passed")
        # except Exception as e:
        #     print("Test failed")
        #     print(e)
    
    test_case()