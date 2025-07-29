from typing import List
from src.constants import *
from src.entity.config_entity import *
from src.entity.artifacts import *
from src.components.video_processing import VideoProcessingComponent
from src.components.audio_processing import AudioProcessingComponent

class RenderPipeline:
    def __init__(self):
        self.video_processing = VideoProcessingComponent()
        self.audio_processing = AudioProcessingComponent()
    
    def run_pipeline(self, session_artifacts: SessionArtifacts, cluster_ids: List[int]) -> RenderArtifacts:
        """Execute render pipeline"""
        try:
            session_id = session_artifacts.session_id
            print(f"Starting render for session: {session_id}")
            print(f"Selected clusters: {cluster_ids}")
            
            # Step 1: Setup paths
            output_path = f"{DATA_FOLDER}/{session_id}/{OUTPUT_VIDEO_NAME}"
            final_output_path = f"{DATA_FOLDER}/{session_id}/{OUTPUT_WITH_AUDIO_NAME}"
            temp_audio_path = f"{final_output_path}_audio{TEMP_AUDIO_EXTENSION}"
            
            # Step 2: Process video with overlays
            video_config = VideoProcessingConfig(
                input_video_path=session_artifacts.video_path,
                sticker_path=session_artifacts.sticker_path,
                output_path=output_path,
                fps=DEFAULT_FPS,
                codec=VIDEO_CODEC
            )
            
            print("Processing video with overlays...")
            video_artifacts = self.video_processing.process_video(
                video_config, 
                session_artifacts.clusters, 
                cluster_ids
            )
            print(f"   - Processed frames: {video_artifacts.processed_frames}")
            print(f"   - Overlays applied: {video_artifacts.overlay_count}")
            
            # Step 3: Merge audio
            audio_config = AudioProcessingConfig(
                original_video_path=session_artifacts.video_path,
                video_no_audio_path=output_path,
                output_video_path=final_output_path,
                temp_audio_path=temp_audio_path
            )
            
            print("Merging audio...")
            audio_artifacts = self.audio_processing.merge_audio(audio_config)
            print(f"   - Audio merged: {audio_artifacts.audio_merged}")
            
            return RenderArtifacts(
                final_video_path=audio_artifacts.final_output_path,
                session_id=session_id,
                processed_clusters=cluster_ids,
                message="Render successful"
            )
        except Exception as e:
            print(f"Render pipeline error: {str(e)}")
            raise e

