import sys
from src.us_visa_approval.exception import UsvisaException
from src.us_visa_approval.logger import logging
from src.us_visa_approval.componets.data_ingestion import DataIngestion
from src.us_visa_approval.componets.data_validation import DataValidation
from src.us_visa_approval.entity.config_entity import DataIngestionConfig
from src.us_visa_approval.entity.config_entity import DataValidationConfig
from src.us_visa_approval.entity.artifact_entity import DataIngestionArtifact
from src.us_visa_approval.entity.artifact_entity import DataValidationArtifact

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()

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
        


    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataIngestionArtifact:
        logging.info("Enterd the start_data_validation method of TrainingPipeline class")

        try:
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact, data_validation_config=self.data_validation_config)

            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Performed the data validation report")

            logging.info("Exited the start_data_validation method of TrainingPipeline class")

            return data_validation_artifact
        except Exception as e:
            raise UsvisaException(e, sys)from e
        

    def run_pipeline(self, ) -> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise UsvisaException(e, sys)