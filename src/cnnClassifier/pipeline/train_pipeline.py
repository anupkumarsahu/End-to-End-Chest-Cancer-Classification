
import os
import sys
from cnnClassifier.components.data_ingestion import DataIngestion
from cnnClassifier.components.model_trainer import Training
from cnnClassifier.components.prepare_base_model import PrepareBaseModel
from cnnClassifier.config.s3_operations import S3Operation
from cnnClassifier.entity.artifacts_entity import DataIngestionArtifacts, PrepareBaseModelArtifacts, TrainingConfigArtifacts
from cnnClassifier.entity.config_entity import DataIngestionConfig, PrepareBaseModelConfig, TrainingConfig
from cnnClassifier.exception import CNNException
from cnnClassifier.logger import logger
from cnnClassifier.utils.common import create_directories


class TrainPipeline:
    
    def __init__(self):
        self.s3_operations = S3Operation()
        self.data_ingestion_config = DataIngestion(self.s3_operations)
        self.base_model_config = PrepareBaseModelConfig()
        self.train_model_config = TrainingConfig()
        self.s3_operations = S3Operation()
        
    def start_data_ingestion(self) -> DataIngestionArtifacts:
        """_summary_

        Raises:
            CNNException: _description_

        Returns:
            DataIngestionArtifacts: _description_
        """        
        logger.info("Entered the start_data_ingestion method of TrainPipeline class")
        try:
            logger.info("Getting the data from S3 bucket")
            
            data_ingestion_artifact = self.data_ingestion_config.initiate_data_ingestion()
            logger.info("Got the adenocarcinoma and normal from s3")
            logger.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )
            return data_ingestion_artifact
        except Exception as e:
            raise CNNException(e, sys) from e

    def prepare_base_model_config(self) -> PrepareBaseModelArtifacts:
        """_summary_

        Raises:
            CNNException: _description_

        Returns:
            PrepareBaseModelArtifacts: _description_
        """        
        try:
            logger.info("Entered prepare_base_model_config method of TrainPipeline class.")
            logger.info(f"Current directory inside prepare_base_model_config method: {os.getcwd()}")
            prepare_base_model_artifacts = self.base_model_config.get_prepare_base_model_config()

            prepare_base_model = PrepareBaseModel(prepare_base_model_artifacts)
            prepare_base_model.get_base_model()
            prepare_base_model.update_base_model()
        
            logger.info("Exited prepare_base_model_config method of TrainPipeline class.")
        except Exception as e:
            raise CNNException(e, sys) from e
        
    def train_model(self) -> TrainingConfigArtifacts:
        logger.info("Entered train_model method of TrainPipeline class.")
        try:
            logger.info(f"Current directory inside train_model method: {os.getcwd()}")
            train_model_artifacts = self.train_model_config.get_training_config()
            
            training = Training(config=train_model_artifacts)
            training.get_base_model()
            training.train_valid_generator()
            training.train()
            
            logger.info("Exit train_model method of TrainPipeline class.")
        except Exception as e:
            raise e
        
    
    def run_pipeline(self) -> None:
        """_summary_

        Raises:
            CNNException: _description_
        """        
        logger.info("Enter the run_pipeline method of TrainPipeline class")
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            prepare_base_model_artifact = self.prepare_base_model_config()
            train_model = self.train_model()

            logger.info("Exited the run_pipeline method of TrainPipeline class")
        except Exception as e:
            raise CNNException(e, sys) from e