import sys
from src.us_visa_approval.exception import UsvisaException
from src.us_visa_approval.logger import logging
import os
from src.us_visa_approval.constant import DATABASE_NAME, MONGODB_URL_KEY
import pymongo
import certifi

from urllib.parse import quote_plus




ca = certifi.where()

class MongoDBClient:
    client = None
    def __init__(self, database_name = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongodb_url = os.getenv(MONGODB_URL_KEY)
                if mongodb_url is None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} not set")
                MongoDBClient.client = pymongo.MongoClient(mongodb_url, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection successfully")
        except Exception as e:
            raise UsvisaException(e, sys)
