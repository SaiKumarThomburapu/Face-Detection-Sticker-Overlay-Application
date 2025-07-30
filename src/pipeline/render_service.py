import cv2
import sys
from src.utils.video_utils import create_frame_map, process_video_frames, write_video
from src.components.audio_merger import merge_audio
from src.logger import logging_logger as logging
from src.exceptions import CustomException
from src.constants import FRAME_RATE

def render_service(session_id, cluster_ids, session_data):
    try:
        if session_id not in session_data:
            raise CustomException("Session not found", sys)

        data = session_data[session_id]
        video_path = data["video_path"]
        sticker_img = cv2.imread(data["sticker_path"], cv2.IMREAD_UNCHANGED)
        clusters = data["clusters"]

        selected = [int(cid) for cid in cluster_ids.split(",") if cid.strip().isdigit()]

        frame_map = create_frame_map(selected, clusters)

        frames = process_video_frames(video_path, frame_map, sticker_img)

        h, w = frames[0].shape[:2]
        output_path = f"artifacts/{session_id}/output.mp4"
        write_video(frames, output_path, FRAME_RATE, (w, h))

        final_output_path = f"artifacts/{session_id}/output_with_audio.mp4"
        merge_audio(video_path, output_path, final_output_path)

        logging.info(f"Rendered session {session_id}")
        return final_output_path
    except Exception as e:
        raise CustomException(e, sys)



