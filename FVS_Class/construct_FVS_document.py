import json

def construct_FVS_document(FVS_scan_lst,out_file_name):
    """
    Creates a MongoDB document object from the list of FVS_Scans
    _id is set to the .out file name (without the .out extension or filepath)
    """
    _id = out_file_name.split('.')[0].split('/')[-1]
    print("_id: ",_id)
    # make a dictionary object of each FVS_Scan
    scan_dicts = []
    for scan in FVS_scan_lst:
        stand_id = scan.stand_id
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
        scan_dict = {stand_id:{
                        'DWDVLOUT':dwdvlout,
                        'CARBREPT':carbrept,
                        'FUELOUT':fuelout,
                        'CANFPROF':canfprof}}
        scan_dicts.append(scan_dict)
    document = {
        '_id': _id
    }
    # add the dictionary objects to the document as their own keys
    for scan_dict in scan_dicts:
        document.update(scan_dict)
    # print(document.keys())
    return document
    # print(json.dumps(document, indent=4))


