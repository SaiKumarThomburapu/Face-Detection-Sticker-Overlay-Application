import os
import subprocess
import ffmpeg
from src.entity.config_entity import AudioProcessingConfig
from src.entity.artifacts import AudioProcessingArtifacts

class AudioProcessingComponent:
    def __init__(self):
        pass
    
    def merge_audio(self, config: AudioProcessingConfig) -> AudioProcessingArtifacts:
        """Merge audio from original video to processed video"""
        try:
            probe = ffmpeg.probe(config.original_video_path)
            has_audio = any(stream['codec_type'] == 'audio' for stream in probe['streams'])
            
            if not has_audio:
                os.rename(config.video_no_audio_path, config.output_video_path)
                return AudioProcessingArtifacts(
                    final_output_path=config.output_video_path,
                    has_audio=False,
                    audio_merged=False
                )
            
            # Extract audio - FIXED COMMAND
            extract_cmd = [
                "ffmpeg", "-y", "-i", config.original_video_path, 
                "-vn", "-acodec", "copy", config.temp_audio_path
            ]
            subprocess.run(extract_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            
            # Merge audio and video - FIXED COMMAND  
            merge_cmd = [
                "ffmpeg", "-y", 
                "-i", config.video_no_audio_path,
                "-i", config.temp_audio_path,  # FIXED: Added missing -i flag
                "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", 
                config.output_video_path
            ]
            subprocess.run(merge_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            
            # Cleanup
            if os.path.exists(config.temp_audio_path):
                os.remove(config.temp_audio_path)
            
            return AudioProcessingArtifacts(
                final_output_path=config.output_video_path,
                has_audio=True,
                audio_merged=True
            )
            
        except Exception as e:
            print(f"Audio merge failed: {str(e)}")
            # Fallback: just rename the video without audio
            if os.path.exists(config.video_no_audio_path):
                os.rename(config.video_no_audio_path, config.output_video_path)
            return AudioProcessingArtifacts(
                final_output_path=config.output_video_path,
                has_audio=True,
                audio_merged=False
            )


