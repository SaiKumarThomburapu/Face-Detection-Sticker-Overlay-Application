import os
import uuid
import cv2
from fastapi import UploadFile
from src.constants import *
from src.entity.config_entity import *
from src.entity.artifacts import *
from src.components.face_extraction import FaceExtractionComponent
from src.components.face_clustering import FaceClusteringComponent

class UploadPipeline:
    def __init__(self):
        self.face_extraction = FaceExtractionComponent()
        self.face_clustering = FaceClusteringComponent()
    
    async def run_pipeline(self, video: UploadFile, sticker: UploadFile) -> UploadArtifacts:
        """Execute upload pipeline"""
        try:
            # Step 1: Setup session
            session_id = uuid.uuid4().hex
            print(f"Generated session_id: '{session_id}'")
            
            session_path = f"{DATA_FOLDER}/{session_id}"
            os.makedirs(session_path, exist_ok=True)
            
            video_path = f"{session_path}/{INPUT_VIDEO_NAME}"
            sticker_path = f"{session_path}/{STICKER_NAME}"
            
            # Step 2: Save files (FIXED)
            with open(video_path, "wb") as f:
                f.write(await video.read())
            with open(sticker_path, "wb") as f:
                f.write(await sticker.read())
            
            print(f"Files saved:")
            print(f"   - Video: {video_path} (exists: {os.path.exists(video_path)})")
            print(f"   - Sticker: {sticker_path} (exists: {os.path.exists(sticker_path)})")
            
            # Step 3: Extract faces
            face_config = FaceExtractionConfig(
                video_path=video_path,
                model_name=FACE_MODEL_NAME,
                providers=FACE_PROVIDERS
            )
            print("Extracting faces...")
            face_artifacts = self.face_extraction.extract_faces_and_embeddings(face_config)
            print(f"   - Total faces found: {face_artifacts.total_faces}")
            
            # Step 4: Cluster faces
            cluster_config = ClusteringConfig(
                eps=DEFAULT_EPS,
                min_samples=DEFAULT_MIN_SAMPLES,
                metric=COSINE_METRIC
            )
            print("Clustering faces...")
            cluster_artifacts = self.face_clustering.cluster_embeddings(face_artifacts.faces, cluster_config)
            print(f"   - Clusters found: {cluster_artifacts.cluster_count}")
            
            # Step 5: Generate previews
            preview_paths = {}
            print("Generating previews...")
            for cid, face_list in cluster_artifacts.clusters.items():
                preview_path = f"{session_path}/cluster_{cid}{PREVIEW_EXTENSION}"
                cv2.imwrite(preview_path, face_list[0].crop)
                preview_paths[cid] = preview_path
            
            # Step 6: Create session artifacts with validation
            session_artifacts = SessionArtifacts(
                session_id=session_id,
                video_path=video_path,
                sticker_path=sticker_path,
                clusters=cluster_artifacts.clusters,
                preview_paths=preview_paths
            )
            
            # Validate session artifacts before returning
            print(f"Session artifacts created:")
            print(f"   - Session ID: '{session_artifacts.session_id}'")
            print(f"   - Clusters: {len(session_artifacts.clusters)}")
            print(f"   - Video path exists: {os.path.exists(session_artifacts.video_path)}")
            print(f"   - Sticker path exists: {os.path.exists(session_artifacts.sticker_path)}")
            
            cluster_ids = list(cluster_artifacts.clusters.keys())
            
            return UploadArtifacts(
                session_artifacts=session_artifacts,
                cluster_ids=cluster_ids,
                message="Upload successful"
            )
        except Exception as e:
            print(f"Upload pipeline error: {str(e)}")
            raise e

