from src.constants import EPS, MIN_SAMPLES, FRAME_RATE, OUTPUT_DIR
import os

class ConfigEntity:
    def __init__(self):
        self.eps = EPS
        self.min_samples = MIN_SAMPLES
        self.frame_rate = FRAME_RATE
        self.output_dir = OUTPUT_DIR

class VideoStickerConfig:
    def __init__(self, config: ConfigEntity, session_id: str):
        self.eps = config.eps
        self.min_samples = config.min_samples
        self.frame_rate = config.frame_rate
        self.output_dir = config.output_dir
        self.session_id = session_id
        self.session_path = os.path.join(self.output_dir, session_id)
        self.video_path = os.path.join(self.session_path, "input.mp4")
        self.sticker_path = os.path.join(self.session_path, "sticker.png")
        self.output_path = os.path.join(self.session_path, "output.mp4")
        self.final_output_path = os.path.join(self.session_path, "output_with_audio.mp4")


