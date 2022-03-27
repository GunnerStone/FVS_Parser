import pymongo
from pymongo import MongoClient


client = pymongo.MongoClient("mongodb+srv://GSTONE:Gooberthecat123@cluster0.ucvcm.mongodb.net/FVS_Scans?retryWrites=true&w=majority")
db = client["FVS_Scans"]
collection = db["Scan1"]

collection.insert_one({})