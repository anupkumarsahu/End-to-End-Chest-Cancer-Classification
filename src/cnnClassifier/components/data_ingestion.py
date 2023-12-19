import os
import sys
from zipfile import ZipFile
from cnnClassifier.entity.artifacts_entity import DataIngestionArtifacts

from cnnClassifier.entity.config_entity import DataIngestionConfig
from cnnClassifier.config.s3_operations import S3Operation
from cnnClassifier.exception import CNNException
from cnnClassifier.logger import logger


class DataIngestion:
    """docstring for DataIngestion."""

    def __init__(
        self, data_ingestion_config: DataIngestionConfig, s3_operations: S3Operation
    ):
        self.data_ingestion_config = data_ingestion_config
        self.s3_operations = s3_operations

    def get_data_from_s3(self):
        """_summary_

        Raises:
            CNNException: _description_
        """
        try:
            logger.info("Entered the get_data_from_s3 method of Data ingestion class")
            os.makedirs(
                self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR, exist_ok=True
            )

            self.s3_operations.read_data_from_s3(
                self.data_ingestion_config.ZIP_FILE_NAME,
                self.data_ingestion_config.BUCKET_NAME,
                self.data_ingestion_config.ZIP_FILE_PATH,
            )

            logger.info("Exited the get_data_from_s3 method of Data ingestion class")
        except Exception as e:
            raise CNNException(e, sys) from e

    def unzip_and_clean(self):
        """_summary_

        Raises:
            CNNException: _description_

        Returns:
            _type_: _description_
        """
        logger.info("Entered the unzip_and_clean method of Data ingestion class")

        try:
            with ZipFile(self.data_ingestion_config.ZIP_FILE_PATH, "r") as zip_ref:
                zip_ref.extractall(self.data_ingestion_config.ZIP_FILE_DIR)
            
            logger.info("Exited the unzip_and_clean method of Data ingestion class")

            return (
                self.data_ingestion_config.ADENOCARCINOMA_DATA_ARTIFACTS_DIR,
                self.data_ingestion_config.NORMAL_DATA_ARTIFACTS_DIR,
            )
        except Exception as e:
            raise CNNException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        """_summary_

        Raises:
            CNNException: _description_

        Returns:
            DataIngestionArtifacts: _description_
        """        
        logger.info(
            "Entered the initiate_data_ingestion method of Data ingestion class"
        )

        try:
            self.get_data_from_s3()

            logger.info("Fetched the data from S3 bucket")

            adenocarcinoma_file_path, normal_file_path = self.unzip_and_clean()
            logger.info("Unzipped file and splited into adenocarcinoma and normal")

            data_ingestion_artifact = DataIngestionArtifacts(
                adenocarcinoma_file_path=adenocarcinoma_file_path,
                normal_file_path=normal_file_path,
            )

            logger.info(
                "Exited the initiate_data_ingestion method of Data ingestion class"
            )
            logger.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise CNNException(e, sys) from e
