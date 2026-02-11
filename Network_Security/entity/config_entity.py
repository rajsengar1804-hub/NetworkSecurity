import os
import sys
from datetime import datetime
from Network_Security.constants import training_pipeline


class TrainingPipelineConfig:
    def __init__(self):
        timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifacts_name = training_pipeline.ARTIFACT_DIR
        self.artifacts_dir = os.path.join(
            self.artifacts_name,
            timestamp
        )


class DataIngestionConfig:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

        self.data_ingestion_dir = os.path.join(
            self.training_pipeline_config.artifacts_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME
        )

        self.feature_store_filepath: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILENAME
        )

        self.training_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TRAIN_FILE_NAME
        )

        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_INGESTED_DIR,
            training_pipeline.TEST_FILE_NAME
        )

        self.train_test_spilt_ratio: float = (
            training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        )

        self.collection_name: str = (
            training_pipeline.DATA_INGESTION_COLLECTION_NAME
        )

        self.database_name: str = (
            training_pipeline.DATA_INGESTION_DATABASE_NAME
        )
class DataValidationconfig:
    def __init__(self):
        self.datavalidationconfig=TrainingPipelineConfig()
        self.data_validation_dir:str=os.path.join(self.datavalidationconfig.artifacts_dir,training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir:str=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir:str=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_data_filepath:str=os.path.join(self.valid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_data_filepath:str=os.path.join(self.valid_data_dir,training_pipeline.TEST_FILE_NAME)
        self.invalid_train_data_filepath:str=os.path.join(self.invalid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_data_filepath:str=os.path.join(self.invalid_data_dir,training_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )

    
