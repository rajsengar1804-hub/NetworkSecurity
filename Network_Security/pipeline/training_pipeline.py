import os ,sys
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
from Network_Security.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationconfig,DataValidationconfig,
    ModelTrainerConfig
)
from Network_Security.entity.artifact_config import (
    DataingestionArtifacts,DataTranformationArtifact,
    DataValidationArtifact,ModelTrainerArtifact
)
from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.components.data_validation import DataValidation
from Network_Security.components.data_transformation import DataTransformation
from Network_Security.components.model_trainer import ModelTrainer

class Training_pipeline:
    def __init__(self):
        pass
    def start_data_ingestion(self):
        try :
            dataIngestionConfig = DataIngestionConfig()
            dataingestion = DataIngestion(dataIngestionConfig)
            dataingestionartifacts = dataingestion.initiate_data_ingestion()
            logging.info('data ingestion is done')
            print(dataingestionartifacts)
            return dataingestionartifacts
        except Exception as ex :
            raise NetworkSecurityException(ex,sys)
    def start_data_validation(self):
        try :
            datavalidationconfig=DataValidationconfig()
            dataingestionartifacts=self.start_data_ingestion()
            datavalidation=DataValidation(datavalidationconfig,dataingestionartifacts)
            datavalidationartifacts=datavalidation.intiate_data_validation()
            print(datavalidationartifacts)
            return datavalidationartifacts
        except Exception as ex :
            raise NetworkSecurityException(ex,sys)
    def start_data_tranformation(self):
        try :
            datavalidationartifacts=self.start_data_validation()
            datatranformationconfig=DataTransformationconfig()
            datatranformation=DataTransformation(datatranformationconfig,datavalidationartifacts)
            datatranformationartifacts=datatranformation.initiate_data_transformation()
            print(datatranformationartifacts)
            return datatranformationartifacts
        except Exception as ex :
            raise NetworkSecurityException(ex,sys)
    def start_data_model_trainer(self):
        try :
            datatransformationartifacts=self.start_data_tranformation()
            modeltrainerconfig=ModelTrainerConfig()
            modeltrainer=ModelTrainer(datatransformationartifacts,modeltrainerconfig)
            modeltrainerartifacts=modeltrainer.intiate_model_trainer()
            logging.info("model training is done")
            return modeltrainerartifacts
        except Exception as ex :
            raise NetworkSecurityException(ex,sys)
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation()
            data_transformation_artifact=self.start_data_tranformation()
            model_trainer_artifact=self.start_data_model_trainer()
            logging.info("training is done successfully")
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    
    
    
        
        