import json
from functools import reduce

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

def construct_FVS_document(FVS_scan_lst,out_file_name):
    """
    Creates a MongoDB document object from the list of FVS_Scans
    _id is set to the .out file name (without the .out extension or filepath)
    """
    _id = out_file_name.split('.')[0].split('/')[-1]
    print("_id: ",_id)
    # make a dictionary object of each FVS_Scan
    scan_dicts = []
    print("num of FVS scans: ",len(FVS_scan_lst))
    for scan in FVS_scan_lst:
        # get the scan_id
        stand_id = scan.stand_id
        # parse out the treatment id (it is before the '_')
        treatment_num = stand_id.split('_')[0]
        # parse out the iterration from the scan id (it is after the '_')
        iter_id = int(stand_id.split('_')[-1])
        iteration_num = 'ITER{}'.format(iter_id)
        # print("treatment: {} with iteration: {}".format(treatment_num,iteration_num))
        try:
            dwdvlout = scan.dwdvlout.report_dict
            # print("dwdvlout found!")
        except AttributeError:
            dwdvlout = {}
            # print("dwdvlout not found!")
        try:
            carbrept = scan.carbrept.report_dict
            # print("carbrept found!")
        except AttributeError:
            carbrept = {}
            # print("carbrept not found!")
        try:
            fuelout = scan.fuelout.report_dict
            # print("fuelout found!")
        except AttributeError:
            fuelout = {}
            # print("fuelout not found!")
        try:
            canfprof = scan.canfprof.report_dict
            # print("canfprof found!")
        except AttributeError:
            canfprof = {}
            # print("canfprof not found!")
        scan_dict = {treatment_num:{iteration_num:{
                        'DWDVLOUT':dwdvlout,
                        'CARBREPT':carbrept,
                        'FUELOUT':fuelout,
                        'CANFPROF':canfprof}}}
        
        scan_dicts.append(scan_dict)
        # print("appended scan_dict: ",scan_dict)
    document = {
        '_id': _id
    }
    
    for scan in scan_dicts:
        document = merge(document,scan)

    return document