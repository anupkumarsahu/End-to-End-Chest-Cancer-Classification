import os
import shutil
import sys
from zipfile import ZipFile

from cnnClassifier.config import s3_operations
from cnnClassifier.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from cnnClassifier.entity.artifacts_entity import DataIngestionArtifacts
from cnnClassifier.exception import CNNException
from cnnClassifier.logger import logger
from cnnClassifier.utils.common import create_directories, read_yaml
from cnnClassifier.config.s3_operations import S3Operation


class DataIngestion:
    """docstring for DataIngestion."""

    def __init__(
        self,
        s3_operations: S3Operation,
        config_filepath=CONFIG_FILE_PATH,
        params_filepath=PARAMS_FILE_PATH,
    ):
        self.s3_operation = s3_operations

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        # create_directories(self.config.artifacts_root)

    def get_data_from_s3(self):
        """_summary_

        Raises:
            CNNException: _description_
        """
        try:
            logger.info("Entered the get_data_from_s3 method of Data ingestion class")

            logger.info(f"Chest CT-Scan folder {self.config.data_ingestion.root_dir}")
            
            if os.path.isdir(self.config.data_ingestion.unzip_dir):
                shutil.rmtree(self.config.data_ingestion.unzip_dir)

            os.makedirs(self.config.data_ingestion.root_dir, exist_ok=True)

            logger.info(
                f"Zip file name: {self.config.data_ingestion.local_data_file}, is the file available: {os.path.isfile(self.config.data_ingestion.local_data_file)}"
            )
            if not os.path.isfile(self.config.data_ingestion.local_data_file):
                self.s3_operation.read_data_from_s3(
                    self.config.data_ingestion.zip_file_name,
                    self.config.data_ingestion.bucket_name,
                    self.config.data_ingestion.local_data_file,
                    self.config.data_ingestion.root_dir,
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
            with ZipFile(self.config.data_ingestion.local_data_file, "r") as zip_ref:
                # zip_ref.extractall(self.config.data_ingestion.unzip_dir)
                zip_ref.extractall()

            logger.info("Exited the unzip_and_clean method of Data ingestion class")

            return (
                self.config.data_ingestion.adenocarcinoma_dir,
                self.config.data_ingestion.normal_dir,
            )
        except Exception as e:
            raise CNNException(e, sys) from e
        
    def prepare_data_ingestion_config(self):
        config = self.config.data_ingestion
        create_directories([config.root_dir])

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
            self.prepare_data_ingestion_config()
            
            self.get_data_from_s3()

            logger.info("Fetched the data from S3 bucket")

            adenocarcinoma_file_path, normal_file_path = self.unzip_and_clean()
            logger.info(
                f"Unzipped file and splited into adenocarcinoma: {adenocarcinoma_file_path} and normal: {normal_file_path}"
            )

            logger.info(
                "Exited the initiate_data_ingestion method of Data ingestion class"
            )

        except Exception as e:
            raise CNNException(e, sys) from e
