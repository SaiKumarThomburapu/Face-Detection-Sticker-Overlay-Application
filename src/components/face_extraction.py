import cv2
import numpy as np
from insightface.app import FaceAnalysis
from typing import List
from src.entity.config_entity import FaceExtractionConfig
from src.entity.artifacts import FaceArtifact, FaceExtractionArtifacts

class FaceExtractionComponent:
    def __init__(self):
        self.face_app = None
    
    def initialize_model(self, config: FaceExtractionConfig):
        """Initialize face detection model"""
        self.face_app = FaceAnalysis(name=config.model_name, providers=config.providers)
        self.face_app.prepare(ctx_id=config.ctx_id)
    
    def extract_faces_and_embeddings(self, config: FaceExtractionConfig) -> FaceExtractionArtifacts:
        """Extract faces and embeddings from video"""
        if self.face_app is None:
            self.initialize_model(config)
        
        cap = cv2.VideoCapture(config.video_path)
        all_faces = []
        frame_idx = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                faces = self.face_app.get(frame)
                for face in faces:
                    x1, y1, x2, y2 = face.bbox.astype(int)
                    face_crop = frame[y1:y2, x1:x2]
                    if face_crop.size > 0:
                        emb = face.embedding / np.linalg.norm(face.embedding)
                        face_artifact = FaceArtifact(
                            frame=frame_idx,
                            embedding=emb,
                            crop=face_crop,
                            bbox=(x1, y1, x2, y2)
                        )
                        all_faces.append(face_artifact)
                frame_idx += 1
        finally:
            cap.release()
        
        return FaceExtractionArtifacts(
            faces=all_faces,
            total_frames=frame_idx,
            total_faces=len(all_faces)
        )

