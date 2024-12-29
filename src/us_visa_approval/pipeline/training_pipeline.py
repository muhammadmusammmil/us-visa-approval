import sys
from src.us_visa_approval.exception import UsvisaException
from src.us_visa_approval.logger import logging
from src.us_visa_approval.componets.data_ingestion import DataIngestion
from src.us_visa_approval.entity.config_entity import DataIngestionConfig
from src.us_visa_approval.entity.artifact_entity import DataIngestionArtifact

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Entered the start data_ingestion methon of TrainingPipeline class")
            logging.info("Getting the data from Mongodb")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initate_data_ingestion()
            logging.info("Got the train_set and test_set from mongodb")
            logging.info("Exited the start_data_ingestion method of TrainingPipeline Class")
            return data_ingestion_artifact
        except Exception as e:
            raise UsvisaException(e, sys) from e
        

    def run_pipeline(self, ) -> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            raise UsvisaException(e, sys)