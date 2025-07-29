import cv2
import numpy as np
from typing import Dict, List
from src.entity.config_entity import VideoProcessingConfig
from src.entity.artifacts import FaceArtifact, VideoProcessingArtifacts

class VideoProcessingComponent:
    def __init__(self):
        pass
    
    def overlay_sticker(self, frame: np.ndarray, bbox: tuple, sticker_img: np.ndarray) -> np.ndarray:
        """Overlay sticker on face in frame"""
        x1, y1, x2, y2 = bbox
        h, w = frame.shape[:2]
        
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)
        
        face_w = x2 - x1
        face_h = y2 - y1
        
        if face_w <= 0 or face_h <= 0:
            return frame
        
        try:
            sticker_resized = cv2.resize(sticker_img, (face_w, face_h))
            
            if sticker_resized.shape[2] == 4:  # Has alpha channel
                alpha_s = sticker_resized[:, :, 3] / 255.0
                alpha_l = 1.0 - alpha_s
                
                for c in range(3):
                    frame[y1:y2, x1:x2, c] = (
                        alpha_s * sticker_resized[:, :, c] +
                        alpha_l * frame[y1:y2, x1:x2, c]
                    )
            else:
                frame[y1:y2, x1:x2] = sticker_resized[:, :, :3]
        except Exception as e:
            print(f"Overlay error: {e}")
            pass
        
        return frame
    
    def process_video(self, config: VideoProcessingConfig, 
                     clusters: Dict[int, List[FaceArtifact]], 
                     selected_cluster_ids: List[int]) -> VideoProcessingArtifacts:
        """Process video with sticker overlays"""
        sticker_img = cv2.imread(config.sticker_path, cv2.IMREAD_UNCHANGED)
        
        if sticker_img is None:
            raise ValueError(f"Could not load sticker image: {config.sticker_path}")
        
        # Create frame mapping
        frame_map = {}
        for cid in selected_cluster_ids:
            for f in clusters.get(cid, []):
                frame_map.setdefault(f.frame, []).append(f)
        
        cap = cv2.VideoCapture(config.input_video_path)
        frames = []
        idx = 0
        overlay_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if idx in frame_map:
                    for f in frame_map[idx]:
                        frame = self.overlay_sticker(frame, f.bbox, sticker_img)
                        overlay_count += 1
                frames.append(frame)
                idx += 1
        finally:
            cap.release()
        
        if not frames:
            raise ValueError("No frames processed from video")
        
        # Write video
        h, w = frames[0].shape[:2]
        out = cv2.VideoWriter(config.output_path, cv2.VideoWriter_fourcc(*config.codec), config.fps, (w, h))
        
        try:
            for f in frames:
                out.write(f)
        finally:
            out.release()
        
        return VideoProcessingArtifacts(
            output_video_path=config.output_path,
            processed_frames=len(frames),
            overlay_count=overlay_count
        )

