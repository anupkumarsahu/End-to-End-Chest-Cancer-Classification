from dataclasses import dataclass
from from_root import from_root

from src.cnnClassifier.config.s3_operations import S3Operation
from src.cnnClassifier.constants import *


@dataclass
class DataIngestionConfig:
    def __init__(self):
        self.S3_OPERATION = (S3Operation(),)
        self.BUCKET_NAME: str = BUCKET_NAME
        self.ZIP_FILE_NAME: str = ZIP_FILE_NAME
        self.DATA_INGESTION_ARTIFACTS_DIR: str = os.path.join(
            from_root(), ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR
        )
        self.CHEST_CT_SCAN_DATA_ARTIFACTS_DIR = os.path.join(
            self.DATA_INGESTION_ARTIFACTS_DIR, DATA_INGESTION_CHEST_CT_SCAN_DATA_DIR
        )
        self.ADENOCARCINOMA_DATA_ARTIFACTS_DIR = os.path.join(
            self.DATA_INGESTION_ARTIFACTS_DIR, DATA_INGESTION_CHEST_CT_SCAN_DATA_DIR, DATA_INGESTION_ADENOCARCINOMA_DIR
        )
        self.NORMAL_DATA_ARTIFACTS_DIR = os.path.join(
            self.DATA_INGESTION_ARTIFACTS_DIR, DATA_INGESTION_CHEST_CT_SCAN_DATA_DIR, DATA_INGESTION_NORMAL_DIR
        )
        # self.TRAIN_DATA_ARTIFACT_DIR = os.path.join(
        #     self.DATA_INGESTION_ARTIFACTS_DIR, DATA_INGESTION_TRAIN_DIR
        # )
        # self.TEST_DATA_ARTIFACT_DIR = os.path.join(
        #     self.DATA_INGESTION_ARTIFACTS_DIR, DATA_INGESTION_TEST_DIR
        # )
        # self.VALID_DATA_ARTIFACT_DIR = os.path.join(
        #     self.DATA_INGESTION_ARTIFACTS_DIR, DATA_INGESTION_VALID_DIR
        # )
        self.ZIP_FILE_DIR = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR)
        self.ZIP_FILE_PATH = os.path.join(
            self.DATA_INGESTION_ARTIFACTS_DIR, self.ZIP_FILE_NAME
        )
        self.UNZIPPED_FILE_PATH = os.path.join(
            self.DATA_INGESTION_ARTIFACTS_DIR, RAW_FILE_NAME
        )
