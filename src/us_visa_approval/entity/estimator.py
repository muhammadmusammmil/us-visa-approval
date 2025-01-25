import sys
import pandas as pd
from sklearn.pipeline import Pipeline
from src.us_visa_approval.exception import UsvisaException
from src.us_visa_approval.logger import logging


class TargetValueMapping:
    def __init__(self):
        self.Certified: int = 0
        self.Denied: int = 1

    def _asdict(self):
        return self.__dict__
    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))
    

class UsVisaModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):

        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        logging.info("Entered predict method of UsVisaModel class")

        try:
            logging.info("Using the trained model to get prediction")

            transformed_feature = self.preprocessing_object.transform(dataframe)

            logging.info("Used the trained model to get prediction")
            return self.trained_model_object.predict(transformed_feature)
        
        except Exception as e:
            raise UsvisaException(e, sys) from e