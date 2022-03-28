import json
from FVS_Class import construct_FVS_document
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Configs.secrets import mongo_client_database
from Configs.secrets import mongo_client_collection
# takes the FVS_Scans object and uploads it to the mongo database
def upload_scans(client, scans, out_filename):
    post = construct_FVS_document(scans, out_filename)
    db = client[mongo_client_database]
    collection = db[mongo_client_collection]

    # update the document if it already exists
    results = collection.update_one({'_id': post['_id']},{'$set': post}, upsert=True)
    return