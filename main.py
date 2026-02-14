import os
import sys
import pandas as pd
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
from Network_Security.entity.config_entity import DataIngestionConfig
from Network_Security.entity.config_entity import TrainingPipelineConfig
from Network_Security.components.data_ingestion import DataIngestion
from Network_Security.entity.config_entity import DataValidationconfig,DataTransformationconfig,ModelTrainerConfig
from Network_Security.components.data_validation import DataValidation
from Network_Security.components.data_transformation import DataTransformation
from Network_Security.components.model_trainer import ModelTrainer


if __name__ == '__main__':
    try:
        dataIngestionConfig = DataIngestionConfig()
        dataingestion = DataIngestion(dataIngestionConfig)
        dataingestionartifacts = dataingestion.initiate_data_ingestion()
        logging.info('data ingestion is done')
        print(dataingestionartifacts)

        datavalidationconfig=DataValidationconfig()
        datavalidation=DataValidation(datavalidationconfig,dataingestionartifacts)
        datavalidationartifacts=datavalidation.intiate_data_validation()
        print(datavalidationartifacts)
        datatranformationconfig=DataTransformationconfig()

        datatranformation=DataTransformation(datatranformationconfig,datavalidationartifacts)
        datatranformationartifacts=datatranformation.initiate_data_transformation()
        print(datatranformationartifacts)

        modeltrainerconfig=ModelTrainerConfig()
        modeltrainer=ModelTrainer(datatranformationartifacts,modeltrainerconfig)
        modeltrainerartifacts=modeltrainer.intiate_model_trainer()
        logging.info("model training is done")

        

    except Exception as ex:
      raise NetworkSecurityException(ex, sys)

