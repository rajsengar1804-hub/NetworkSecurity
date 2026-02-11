import os 
import sys 
import pandas as pd 
import numpy as np 
from Network_Security.entity.config_entity import DataValidationconfig
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.entity.artifact_config import DataingestionArtifacts
from Network_Security.logging.logger import logging
from Network_Security.entity.artifact_config import DataValidationArtifact
from Network_Security.constants.training_pipeline import SCHEMA_FILE_PATH
from Network_Security.utils.main.utils import read_yaml_file,write_yaml_file
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self,datavalidationconfig:DataValidationconfig,
                 dataingestionartifacts:DataingestionArtifacts):
        try: 
          self.datavalidationconfig=datavalidationconfig
          self.dataingestionartifacts=dataingestionartifacts
          self.schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as ex :
           raise NetworkSecurityException(ex,sys)
    @staticmethod
    def read_data(filepath:str)->pd.DataFrame:
       try :
          df=pd.read_csv(filepath)
          return df
       except Exception as ex :
          raise NetworkSecurityException(ex,sys)
    def validate_no_of_columns(self,dataframe:pd.DataFrame)->bool:
       number_of_column=len(self.schema_config['columns'])
       logging.info(f"Number of columns in schema ={number_of_column}")
       logging.info(f"Number of columns in dataframe ={len(dataframe.columns)}")
       if number_of_column==len(dataframe.columns):
          return True 
       else :
          return False
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        report ={}
        status =True
        try :
          for col in base_df:
              d1=base_df[col]
              d2=current_df[col]
              is_same_dist=ks_2samp(d1,d2)
              if threshold<=is_same_dist.pvalue:
                  is_found=False
              else :
                  status =False
                  is_found=True
              report.update({col:{
                      "p_value":float(is_same_dist.pvalue),
                      "drift_status":is_found
                      }})

          drift_report_file_path = self.datavalidationconfig.drift_report_file_path
          dir_path = os.path.dirname(drift_report_file_path)
          os.makedirs(dir_path,exist_ok=True)
          write_yaml_file(filepath=drift_report_file_path,content=report)
        except Exception as ex :
            raise NetworkSecurityException(ex,sys)
    def intiate_data_validation(self)->DataValidationArtifact:
       try :
        train_file_path=self.dataingestionartifacts.trained_file_path
        test_file_path=self.dataingestionartifacts.test_file_path

        trained_dataframe=DataValidation.read_data(train_file_path)
        test_dataframe=DataValidation.read_data(test_file_path)
        status=self.validate_no_of_columns(trained_dataframe)
        if not status:
                error_message=f"Train dataframe does not contain all columns.\n"
        status = self.validate_no_of_columns(dataframe=test_dataframe)
        if not status:
                error_message=f"Test dataframe does not contain all columns.\n"
        status=self.detect_dataset_drift(base_df=trained_dataframe,current_df=test_dataframe,threshold=0.05)
        dir_path=os.path.dirname(self.datavalidationconfig.valid_train_data_filepath)
        os.makedirs(dir_path,exist_ok=True)
        trained_dataframe.to_csv(
                self.datavalidationconfig.valid_train_data_filepath, index=False, header=True

            )

        test_dataframe.to_csv(
                self.datavalidationconfig.valid_test_data_filepath, index=False, header=True
            )
        



        
        return DataValidationArtifact(
            validation_status=status,
            valid_train_file_path=self.datavalidationconfig.valid_train_data_filepath,
            valid_test_file_path=self.datavalidationconfig.valid_test_data_filepath,
            invalid_train_file_path=None,
            invalid_test_file_path=None,
            drift_report_file_path=self.datavalidationconfig.drift_report_file_path
        )
        
       except Exception as ex :
          raise NetworkSecurityException(ex,sys)
       

       
       
          