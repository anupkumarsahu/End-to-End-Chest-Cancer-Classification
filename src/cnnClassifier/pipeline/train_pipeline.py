
import sys
from cnnClassifier.components.data_ingestion import DataIngestion
from cnnClassifier.config.s3_operations import S3Operation
from cnnClassifier.entity.artifacts_entity import DataIngestionArtifacts
from cnnClassifier.entity.config_entity import DataIngestionConfig
from cnnClassifier.exception import CNNException
from cnnClassifier.logger import logger


class TrainPipeline:
    
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.s3_operations = S3Operation()
        
    def start_data_ingestion(self) -> DataIngestionArtifacts:
        logger.info("Entered the start_data_ingestion method of TrainPipeline class")
        try:
            logger.info("Getting the data from S3 bucket")
            
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config,
                s3_operations=S3Operation(),
            )
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logger.info("Got the adenocarcinoma and normal from s3")
            logger.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )
            return data_ingestion_artifact
        except Exception as e:
            raise CNNException(e, sys) from e

    def run_pipeline(self) -> None:
        logger.info("Enter the run_pipeline method of TrainPipeline class")
        try:
            data_ingestion_artifact = self.start_data_ingestion()

            logger.info("Exited the run_pipeline method of TrainPipeline class")
        except Exception as e:
            raise CNNException(e, sys) from e