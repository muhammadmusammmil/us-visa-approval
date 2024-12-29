import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from src.us_visa_approval.logger import logging
from src.us_visa_approval.exception import UsvisaException
from src.us_visa_approval.entity.config_entity import DataIngestionConfig
from src.us_visa_approval.entity.artifact_entity import DataIngestionArtifact
from src.us_visa_approval.data_acces.usvisa_data import UsvisaData


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):

        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise UsvisaException(e, sys)
        

    def export_data_into_feature_store(self) -> pd.DataFrame:
        try:
            logging.info("Collecting data from mongodb")
            usvisa_data = UsvisaData()
            dataframe = usvisa_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            logging.info(f"Shape of dataframe: {dataframe.shape}")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"saving exported data into feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise UsvisaException(e, sys)
        

    def split_data_as_train_test(self, dataframe: pd.DataFrame) -> None:
        logging.info("Enterd split data as train test method of DataIngestion class")

        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on dataframe")
            logging.info("Exited split data s train test method of DataIngestion class")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info("Export train test file path")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)

            logging.info(f"Exported train and test file path.")
        except Exception as e:
            raise UsvisaException(e, sys) from e
        



    def initate_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entered initiate_data_ingestion method of DataIngestion class")
        try:
            dataframe = self.export_data_into_feature_store()
            logging.info("Got the data from mongodb")

            self.split_data_as_train_test(dataframe=dataframe)
            logging.info("performed train test split on the dataset")

            logging.info("Exited initiate_data_ingestion method of DataIngestion class")

            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                            test_file_path=self.data_ingestion_config.test_file_path)
            
            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise UsvisaException(e, sys) from e
        
