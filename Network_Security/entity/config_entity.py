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
