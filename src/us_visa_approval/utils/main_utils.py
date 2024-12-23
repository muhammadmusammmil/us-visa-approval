import os
import sys
import numpy as np
import dill
import yaml
import pandas as pd
from src.us_visa_approval.exception import UsvisaException
from src.us_visa_approval.logger import logging


def read_yaml_file(filepath: str) -> dict:
    try:
        with open(filepath, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise UsvisaException(e, sys) from e
    
def write_yaml_file(filepath: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(filepath):
                os.remove(filepath)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as file:
            yaml.dump(content, file)    
    except Exception as e:
        raise UsvisaException(e, sys) from e
    

def load_object(filepath: str) -> object:
    logging.info("Enterd the load_object method of utils")    

    try:
        with open(filepath, "rb") as file_obj:
            obj = dill.load(file_obj)
        logging.info("Exited the load_object method of utils")
        return obj
    except Exception as e:
        raise UsvisaException(e, sys) from e
    
def save_numpy_array_data(filepath: str, array: np.array):
    try:
        dir_path = os.path.dirname(filepath)
        os.makedirs(dir_path, exist_ok=True)
        with open(filepath, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise UsvisaException(e, sys) from e
    
def load_numpy_array_data(filepath: str) -> np.array:
    try:
        with open(filepath, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise UsvisaException(e, sys) from e
    
def save_object(filepath: str, obj: object) -> None:
    logging.info("Enterd the save_object method of utils")

    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as file_obj:
            dill.dump(file_obj)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise UsvisaException(e, sys) from e
    
def drop_columns(df: pd.DataFrame, col: list) -> pd.DataFrame:
    logging.info("Enterd the drop_columns method of utils")
    try:
        df = df.drop(columns=col, axis=1)
        logging.info("Exited the drop_columns method of utils")
        return df
    except Exception as e:
        raise UsvisaException(e, sys) from e 
        