import os
from datetime import datetime

TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

# Data Ingestion Constants
ARTIFACTS_DIR = os.path.join("artifacts", TIMESTAMP)
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

# AWS CONSTANTS
AWS_ACCESS_KEY_ID_ENV_KEY = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_ENV_KEY = "AWS_SECRET_ACCESS_KEY"
REGION_NAME = "us-east-1"