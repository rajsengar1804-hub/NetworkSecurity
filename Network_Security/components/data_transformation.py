import os
import sys
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from Network_Security.entity.config_entity import DataTransformationconfig
from Network_Security.exception.exception import NetworkSecurityException
from Network_Security.logging.logger import logging
from Network_Security.entity.artifact_config import (
    DataValidationArtifact,
    DataTranformationArtifact
)

from Network_Security.constants.training_pipeline import (
    TARGET_COLUMN,
    DATA_TRANSFORMATION_IMPUTER_PARAMS
)
from Network_Security.utils.main.utils import save_numpy_array, save_object


class DataTransformation:
    def __init__(
        self,
        datatransformationconfig: DataTransformationconfig,
        datavalidationartifacts: DataValidationArtifact,
    ):
        try:
            self.datatransformationconfig = datatransformationconfig
            self.datavalidationartifacts = datavalidationartifacts
        except Exception as ex:
            raise NetworkSecurityException(ex, sys)

    @staticmethod
    def read_data_csv(filepath: str) -> pd.DataFrame:
        try:
            return pd.read_csv(filepath)
        except Exception as ex:
            raise NetworkSecurityException(ex, sys)

    def data_transformed_into_object(self) -> Pipeline:
        """
        Creates preprocessing pipeline
        """
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)

            logging.info(
                f"Initialized KNNImputer with params: {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )

            processor = Pipeline(
                steps=[
                    ("KNNImputer", imputer)
                ]
            )

            return processor

        except Exception as ex:
            raise NetworkSecurityException(ex, sys)

    def initiate_data_transformation(self) -> DataTranformationArtifact:
        try:
            logging.info("Starting Data Transformation")

            # Get validated file paths
            train_file_path = self.datavalidationartifacts.valid_train_file_path
            test_file_path = self.datavalidationartifacts.valid_test_file_path

            # Read data
            train_df = self.read_data_csv(train_file_path)
            test_df = self.read_data_csv(test_file_path)

            logging.info("Train and Test data loaded successfully")

            # Separate target and independent features
            train_target = train_df[TARGET_COLUMN]
            train_features = train_df.drop(columns=[TARGET_COLUMN], axis=1)

            test_target = test_df[TARGET_COLUMN]
            test_features = test_df.drop(columns=[TARGET_COLUMN], axis=1)

            # Replace -1 with 0 in target column
            train_target.replace(-1, 0, inplace=True)
            test_target.replace(-1, 0, inplace=True)

            logging.info("Target column processed")

            # Get preprocessing object
            preprocessor = self.data_transformed_into_object()

            # Fit and transform only independent features
            train_features_transformed = preprocessor.fit_transform(train_features)
            test_features_transformed = preprocessor.transform(test_features)

            logging.info("Data transformation completed")

            # Combine features and target
            train_arr = np.c_[train_features_transformed, np.array(train_target)]
            test_arr = np.c_[test_features_transformed, np.array(test_target)]
            save_numpy_array(
                filepath=self.datatransformationconfig.data_transformation_train_file_path,
                array=train_arr,
            )

            save_numpy_array(
                filepath=self.datatransformationconfig.data_transformation_test_file_path,
                array=test_arr,
            )

            save_object(
                file_path=self.datatransformationconfig.data_transformation_preprocessor_file_path,
                obj=preprocessor,
            )
            #model pusher
            save_object("final_model/preprocessor.pkl",preprocessor)

            logging.info("Preprocessor and transformed data saved successfully")

            data_transformation_artifact = DataTranformationArtifact(
                train_numpy_array_filepath=self.datatransformationconfig.data_transformation_train_file_path,
                test_numpy_array_filepath=self.datatransformationconfig.data_transformation_test_file_path,
                preprocessor_pickle_filepath=self.datatransformationconfig.data_transformation_preprocessor_file_path,
            )

            logging.info("Data Transformation Artifact created successfully")

            return data_transformation_artifact

        except Exception as ex:
            raise NetworkSecurityException(ex, sys)
