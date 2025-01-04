import json
import sys

import pandas as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection

from src.us_visa_approval.exception import UsvisaException
from src.us_visa_approval.logger import logging
from src.us_visa_approval.utils.main_utils import read_yaml_file, write_yaml_file
from src.us_visa_approval.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.us_visa_approval.entity.config_entity import DataValidationConfig
from src.us_visa_approval.constant import SCHEMA_FILE_PATH

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(filepath=SCHEMA_FILE_PATH)
        except Exception as e:
            raise UsvisaException(e, sys)
        
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Is required columns present: [{status}]")
            return status
        except Exception as e:
            raise UsvisaException(e, sys)
        
    def is_column_exist(self, df: pd.DataFrame) -> bool:
        try:
            dataframe_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []
            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)

            if len(missing_numerical_columns) > 0:
                logging.info(f'Missing numerical column: {missing_numerical_columns}')

            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)

            if len(missing_categorical_columns) > 0:
                logging.info(f"Missing categorical columns: {missing_categorical_columns}")

            return False if len(missing_numerical_columns)>0 or len(missing_categorical_columns)>0 else True
        
        except Exception as e:
            raise UsvisaException(e, sys)
        

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise UsvisaException(e, sys)
        

    def detect_dataset_drift(self, refrence_df: pd.DataFrame, current_df: pd.DataFrame, ) -> bool:
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])
            data_drift_profile.calculate(refrence_df, current_df)

            report = data_drift_profile.json()
            json_report = json.loads(report)

            write_yaml_file(filepath=self.data_validation_config.drift_report_file_path, content=json_report)

            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]

            logging.info(f"{n_drifted_features}/{n_features} drift detected")
            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]
            return drift_status
        except Exception as e:
            raise UsvisaException(e, sys) from e


    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            validation_err_msg = ""
            logging.info("Starting data validation")
            train_df, test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
                                 DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))
            
            status = self.validate_number_of_columns(dataframe=train_df)
            logging.info(f"All required columns present in training dataframe: {status}")
            if not status:
                validation_err_msg += f"columns are missing in training dataframe."
            status =self.validate_number_of_columns(dataframe=test_df)

            logging.info(f"All required columns present in testing dataframe: {status}")
            if not status:
                validation_err_msg += f"Columns are missing in training dataframe."

            status = self.is_column_exist(df=train_df)

            if not status:
                validation_err_msg += f"Columns are missing in training dataframe."
            status = self.is_column_exist(df=test_df)

            if not status:
                validation_err_msg += f"Columns are missing in test dataframe."

            validation_status = len(validation_err_msg) == 0
            
            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                if drift_status:
                    logging.info(f"Drift detected.")
                    validation_err_msg = "Drift detected"
                else:
                    validation_err_msg = "Drift not detected"

            else:
                logging.info(f"Validation_error: {validation_err_msg}")


            data_validation_aritfact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_err_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            logging.info(f"Data validation artifact: {data_validation_aritfact}")
            return data_validation_aritfact
        except Exception as e:
            raise UsvisaException(e, sys) from e
