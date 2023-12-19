from dataclasses import dataclass


@dataclass
class DataIngestionArtifacts:
    adenocarcinoma_file_path: str
    normal_file_path: str