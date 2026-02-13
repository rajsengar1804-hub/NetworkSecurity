import yaml
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
import os,sys
import pandas as pd 
import numpy as np
#import dill
import pickle

def read_yaml_file(filepath:str)->dict:
    try :
        with open(filepath,"rb") as fileobj:
             return yaml.safe_load(fileobj)
        
    except Exception as ex :
        raise NetworkSecurityException(ex,sys)
def write_yaml_file(filepath:str,content:pd.DataFrame):
    try :
         with open(filepath,'w')as fileobj:
             yaml.dump(content,fileobj)
    except Exception as ex :
        raise NetworkSecurityException(ex,sys)
    
def save_numpy_array(filepath: str, array: np.array) -> None:
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "wb") as file_obj:
            np.save(file_obj, array)

    except Exception as ex:
        raise NetworkSecurityException(ex, sys)

def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise NetworkSecurityException(e, sys)

