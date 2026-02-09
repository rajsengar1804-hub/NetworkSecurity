import os 
import sys 
from Network_Security.logging import logger
from Network_Security.exception.exception import NetworkSecurityException

import pymongo
import json
from dotenv import load_dotenv
import pandas as pd 
import numpy as np 

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi 
ca = certifi.where()


class Networkdataextract:
    def __init__(self, filepath, database, collection):
        try:
            self.filepath = filepath
            self.database = database
            self.collection = collection
        except Exception as ex:
            raise NetworkSecurityException(ex, sys)

    def convert_to_json(self):
        try:
            df = pd.read_csv(self.filepath)
            df.reset_index(drop=True, inplace=True)

            records=list(json.loads(df.T.to_json()).values())
            logger.logging.info("data convert into json")
            return records

        except Exception as ex:
            raise NetworkSecurityException(ex, sys)

    def insert_data_mongodb(self, records):
        try:
            self.records = records
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)

            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)
            logger.logging.info("data insert into mongodb")
            return len(self.records)
        except Exception as ex:
            raise NetworkSecurityException(ex, sys)


if __name__ == '__main__':
    FILE_PATH = "E:/NETWORK SECURITY/NETWORK_DATA/phispine1.csv"
    DATABASE = "NETWORKS"
    Collection = "NetworkData"

    networkobj = Networkdataextract(FILE_PATH, DATABASE, Collection)
    records = networkobj.convert_to_json()
    print(records)

    no_of_records = networkobj.insert_data_mongodb(records)
    print(no_of_records)
