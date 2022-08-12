import json
from datetime import date
from functools import reduce
import time

""" Merges 2 nested dictionaries together"""
def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

def construct_FVS_document(parsed_outfile,out_file_name):
    """
    Creates a MongoDB document object from the parsed_outfile
    _id is set to the .out file name (without the .out extension or filepath)
    """

    scan_dicts = []
    
    for scan in parsed_outfile["treatments"]:
        # get the scan_id
        stand_id = scan.stand_id

        # parse out the treatment id (it is before the '_')
        treatment_num = stand_id.split('_')[0]
        treatment_num = ''.join(x for x in treatment_num if x.isdigit()) # grab the digits

        # parse out the iterration from the scan id (it is after the '_')
        iter_id = int(stand_id.split('_')[-1])
        iteration_num = 'ITER{}'.format(iter_id)

        try:
            dwdvlout = scan.dwdvlout.report_dict
        except AttributeError:
            dwdvlout = {}

        try:
            carbrept = scan.carbrept.report_dict
        except AttributeError:
            carbrept = {}

        try:
            fuelout = scan.fuelout.report_dict
        except AttributeError:
            fuelout = {}

        try:
            canfprof = scan.canfprof.report_dict
        except AttributeError:
            canfprof = {}

        try:
            input_options = scan.input_options.dictionary
        except AttributeError:
            input_options = {}

        scan_dict = {treatment_num:{
                        iteration_num:{
                        'INPUT_OPTIONS':input_options,
                        'DWDVLOUT':dwdvlout,
                        'CARBREPT':carbrept,
                        'FUELOUT':fuelout,
                        'CANFPROF':canfprof}
                        }}
        
        scan_dicts.append(scan_dict)

    # if the coordinates are not present, set the _id to the .out filename
    if parsed_outfile["x_projected"] is None or parsed_outfile["y_projected"] is None:
        _id = "{}".format(out_file_name.split('.')[0].split('/')[-1])
    else:
        _id = "{}__{}__{}".format(parsed_outfile["x_projected"],parsed_outfile["y_projected"],parsed_outfile["version"])

    document = {
        '_id':_id,

        'treatments':{},
        
        'file_name': out_file_name.split('.')[0].split('/')[-1],

        # make a GEOJSON point object from the projected coordinates for Albers
        'projected_coordinates':{
            'type':'Point',
            'coordinates':[ float(parsed_outfile["x_projected"]) if parsed_outfile["x_projected"] is not None else None,
                            float(parsed_outfile["y_projected"]) if parsed_outfile["y_projected"] is not None else None
                            ]
        },
        
        # make GEOJSON point object from the lat/long coordinates
        'location':{
            'type':'Point',
            'coordinates':[ float(parsed_outfile["x_latlon"]) if parsed_outfile["x_latlon"] is not None else None,
                            float(parsed_outfile["y_latlon"]) if parsed_outfile["y_latlon"] is not None else None
                            ]
        },
        
        'is_valid_output': parsed_outfile["is_valid_output"],
        
        'version': parsed_outfile["version"],
        
        'date_uploaded': date.today().strftime("%m/%d/%Y")
    }
    
    # store all the treatments in a treatment dict
    treatment_dict = {}
    for scan in scan_dicts:
        treatment_dict = merge(treatment_dict,scan)
    
    # add the treatment dict to the document
    document['treatments'] = treatment_dict

    return document