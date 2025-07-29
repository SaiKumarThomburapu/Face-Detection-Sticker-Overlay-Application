from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import numpy as np

@dataclass
class FaceArtifact:
    frame: int
    embedding: np.ndarray
    crop: np.ndarray
    bbox: tuple

@dataclass
class FaceExtractionArtifacts:
    faces: List[FaceArtifact]
    total_frames: int
    total_faces: int

@dataclass
class ClusteringArtifacts:
    clusters: Dict[int, List[FaceArtifact]]
    cluster_count: int
    noise_faces: int

@dataclass
class PreviewArtifacts:
    preview_paths: Dict[int, str]
    cluster_ids: List[int]

@dataclass
class VideoProcessingArtifacts:
    output_video_path: str
    processed_frames: int
    overlay_count: int

@dataclass
class AudioProcessingArtifacts:
    final_output_path: str
    has_audio: bool
    audio_merged: bool

@dataclass
class SessionArtifacts:
    session_id: str
    video_path: str
    sticker_path: str
    clusters: Dict[int, List[FaceArtifact]]
    preview_paths: Dict[int, str]

@dataclass
class UploadArtifacts:
    session_artifacts: SessionArtifacts
    cluster_ids: List[int]
    message: str

@dataclass
class RenderArtifacts:
    final_video_path: str
    session_id: str
    processed_clusters: List[int]
    message: str

