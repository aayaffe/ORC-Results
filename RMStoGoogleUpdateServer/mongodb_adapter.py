"""
This file is used to parse RMS file and update a local mongoDB database used in various scoring software.
Created by aayaffe
"""
import subprocess
from pymongo import MongoClient
import json
import urllib.request


def add_certs_to_db(json_url, collection):
    response = urllib.request.urlopen(json_url)
    page = response.read().decode('utf-8-sig')
    parsed = json.loads(page)

    inserted = 0
    for item in parsed["rms"]:
        found = collection.find_one({ "RefNo": item['RefNo'] })
        if not found:
            collection.insert(item)
            inserted+=1
    return inserted
mongod = subprocess.Popen(['mongod'])

client = MongoClient()
db = client.orc_db
certs = db.orccerts
inserted = add_certs_to_db("http://data.orc.org/public/WPub.dll?action=DownRMS&CountryId=ISR&ext=json",certs)

print("Added "+ str(inserted) + " certificates.")
print(str(certs.count()) + " certificates in db")