import os

# Directory paths
DATA_FOLDER = "data"
TEMP_FOLDER = "temp"

# Face detection model
FACE_MODEL_NAME = "buffalo_l"
FACE_PROVIDERS = ["CPUExecutionProvider"]

# Clustering parameters
DEFAULT_EPS = 0.6
DEFAULT_MIN_SAMPLES = 3
COSINE_METRIC = "cosine"

# Video processing
DEFAULT_FPS = 30
VIDEO_CODEC = 'mp4v'
AUDIO_CODEC = "aac"

# File extensions
VIDEO_EXTENSION = ".mp4"
STICKER_EXTENSION = ".png"
PREVIEW_EXTENSION = ".jpg"
TEMP_AUDIO_EXTENSION = ".aac"

# File names
INPUT_VIDEO_NAME = "input.mp4"
STICKER_NAME = "sticker.png"
OUTPUT_VIDEO_NAME = "output.mp4"
OUTPUT_WITH_AUDIO_NAME = "output_with_audio.mp4"

# FFMPEG commands
FFMPEG_EXTRACT_AUDIO = ["ffmpeg", "-y", "-i"]
FFMPEG_MERGE_AUDIO = ["ffmpeg", "-y", "-i"]
FFMPEG_AUDIO_FLAGS = ["-vn", "-acodec", "copy"]
FFMPEG_MERGE_FLAGS = ["-c:v", "copy", "-c:a", "aac", "-strict", "experimental"]

# Error messages
SESSION_NOT_FOUND = "Session not found"
AUDIO_MERGE_FAILED = "Audio merge failed"

