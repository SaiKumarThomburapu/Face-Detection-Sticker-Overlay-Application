from dataclasses import dataclass
from typing import List, Optional

@dataclass
class FaceExtractionConfig:
    video_path: str
    model_name: str
    providers: List[str]
    ctx_id: int = 0

@dataclass
class ClusteringConfig:
    eps: float
    min_samples: int
    metric: str

@dataclass
class VideoProcessingConfig:
    input_video_path: str
    sticker_path: str
    output_path: str
    fps: int
    codec: str

@dataclass
class AudioProcessingConfig:
    original_video_path: str
    video_no_audio_path: str
    output_video_path: str
    temp_audio_path: str

@dataclass
class UploadConfig:
    session_id: str
    session_path: str
    video_path: str
    sticker_path: str

@dataclass
class RenderConfig:
    session_id: str
    cluster_ids: List[int]
    video_path: str
    sticker_path: str
    output_path: str
    final_output_path: str

