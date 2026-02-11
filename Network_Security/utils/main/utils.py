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

