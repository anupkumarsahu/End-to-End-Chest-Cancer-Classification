from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionArtifacts:
    root_dir: Path
    bucket_name: str
    local_data_file: Path
    unzip_dir: Path
    adenocarcinoma_dir: Path
    normal_dir: Path

@dataclass
class PrepareBaseModelArtifacts:
    root_dir: Path
    base_model_path: Path
    updated_base_model_path: Path
    params_image_size: list
    params_learning_rate: float
    params_include_top: bool
    params_weights: str
    params_classes: int
    
@dataclass
class TrainingConfigArtifacts:
    root_dir: Path
    trained_model_path: Path
    updated_base_model_path: Path
    training_data: Path
    params_epochs: int
    params_batch_size: int
    params_is_augmentation: bool
    params_image_size: list
