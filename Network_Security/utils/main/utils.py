import yaml
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
from sklearn.model_selection import GridSearchCV
import os,sys
import pandas as pd 
import numpy as np
#import dill
import pickle
from sklearn.metrics import accuracy_score

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
def load_numpy_array(filepath)->np.array:
    try :
        with open(filepath,'rb')as fileobj:
           return  np.load(fileobj)
    except Exception as ex :
        raise NetworkSecurityException(ex,sys)
def load_object(filepath)->object:
    try :
        if not os.path.exists(filepath):
            raise Exception(f"The file: {filepath} is not exists")
        with open(filepath,'rb') as fileobj:
            print(fileobj)
            return pickle.load(fileobj)
        pass
    except Exception as ex :
        raise NetworkSecurityException(ex,sys)
def evaluate_model(x_train,y_train,x_test,y_test,models,params):
    try :
        report ={}
        for i in range(len(list(models.values()))):
            model=list(models.values())[i]
            para=list(params.values())[i]
            gs=GridSearchCV(model,para,cv=3)
            gs.fit(x_train,y_train)
            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)
            y_train_pred=model.predict(x_train)
            y_test_pred=model.predict(x_test)

            test_model_score=accuracy_score(y_test,y_test_pred)
            report[list(models.keys())[i]]=test_model_score
        return report
    except Exception as ex :
        raise NetworkSecurityException(ex,sys)

        


        

