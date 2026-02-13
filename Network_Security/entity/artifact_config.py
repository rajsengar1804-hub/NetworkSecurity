from dataclasses import dataclass 
@dataclass
class DataingestionArtifacts:
    trained_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str
@dataclass
class DataTranformationArtifact:
    train_numpy_array_filepath:str
    test_numpy_array_filepath:str
    preprocessor_pickle_filepath:str
