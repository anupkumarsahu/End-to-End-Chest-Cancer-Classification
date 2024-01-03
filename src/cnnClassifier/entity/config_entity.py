from dataclasses import dataclass
from pathlib import Path
import sys
from from_root import from_root
from cnnClassifier.entity.artifacts_entity import PrepareBaseModelArtifacts
from cnnClassifier.exception import CNNException

from src.cnnClassifier.config.s3_operations import S3Operation
from src.cnnClassifier.constants import *
from cnnClassifier.logger import logger
from cnnClassifier.utils.common import create_directories, read_yaml


@dataclass
class DataIngestionConfig:
    def __init__(
        self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH
    ):
        self.S3_OPERATION = (S3Operation(),)
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        # create_directories(self.config.artifacts_root)
        
    def prepare_data_ingestion_config(self):
        config = self.config.data_ingestion
        create_directories([config.root_dir])

@dataclass
class PrepareBaseModelConfig:
    def __init__(self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        
        
    def get_prepare_base_model_config(self) -> PrepareBaseModelArtifacts:
        """_summary_

        Returns:
            PrepareBaseModelArtifacts: _description_
        """        
        config = self.config.prepare_base_model
        logger.info(f"Current Directory: {os.getcwd()}")
        os.chdir("../../")
        logger.info(f"Current Directory: {os.getcwd()}")
        
        create_directories([config.root_dir])
        
        prepare_base_model_config = PrepareBaseModelArtifacts(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            updated_base_model_path=Path(config.updated_base_model_path),
            params_image_size=self.params.IMAGE_SIZE,
            params_learning_rate=self.params.LEARNING_RATE,
            params_include_top=self.params.INCLUDE_TOP,
            params_weights=self.params.WEIGHTS,
            params_classes=self.params.CLASSES,
        )
        
        return prepare_base_model_config