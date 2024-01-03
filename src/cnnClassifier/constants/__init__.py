import os
from datetime import datetime
from pathlib import Path

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

# Data Ingestion Constants
# ARTIFACTS_DIR = os.path.join("artifacts", TIMESTAMP)
ARTIFACTS_DIR = "artifacts"
BUCKET_NAME = "helmet-object-detection-20112023"
ZIP_FILE_NAME = "Chest-CT-Scan-data.zip"
# ZIP_FILE_NAME = "data.zip"
ANNOTATIONS_COCO_JSON_FILE = "_annotations.coco.json"

RAW_FILE_NAME = "cnnClassifier"

# Data ingestion constants
DATA_INGESTION_ARTIFACTS_DIR = "DataIngestionArtifacts"
DATA_INGESTION_CHEST_CT_SCAN_DATA_DIR = "Chest-CT-Scan-data"
DATA_INGESTION_ADENOCARCINOMA_DIR = "adenocarcinoma"
DATA_INGESTION_NORMAL_DIR = "normal"

# Model Training Constants
TRAINED_AUGMENTATION = True
TRAINED_IMAGE_SIZE = [244, 224, 3]
TRAINED_BATCH_SIZE = 16
TRAINED_INCLUDE_TOP = False
EPOCH = 1
TRAINED_CLASSES = 2
TRAINED_WEIGHTS = "imagenet"
TRAINED_LEARNING_RATE = 0.01
TRAINED_MODEL_DIR = "TrainedModel"
TRAINED_UPDATED_MODEL_DIR = "UpdatedModel"
TRAINED_MODEL_NAME = "base_model.h5"
TRAINED_UPDATED_MODEL_NAME = "base_model_updated.h5"
TRAINED_SHUFFLE = False
TRAINED_NUM_WORKERS = 1


# AWS CONSTANTS
AWS_ACCESS_KEY_ID_ENV_KEY = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_ENV_KEY = "AWS_SECRET_ACCESS_KEY"
REGION_NAME = "us-east-1"

CONFIG_FILE_PATH = Path("config/config.yaml")
PARAMS_FILE_PATH = Path("params.yaml")