import pymongo
from pymongo import MongoClient

# add the parent direcoty to the path
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Configs.secrets import mongo_client_name

def get_client():
    client = MongoClient(mongo_client_name)
    return client