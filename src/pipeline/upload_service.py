import uuid
import os
import sys
from src.entity.config_entity import ConfigEntity, VideoStickerConfig
from src.components.face_extractor import extract_faces_and_embeddings
from src.components.clusterer import cluster_embeddings
from src.utils.io_utils import save_uploaded_file, save_preview
from src.logger import logging_logger as logging
from src.exceptions import CustomException

async def upload_service(video, sticker, session_data, face_app):
    try:
        base_config = ConfigEntity()
        session_id = uuid.uuid4().hex
        config = VideoStickerConfig(base_config, session_id)
        os.makedirs(config.session_path, exist_ok=True)

        # Save files
        await save_uploaded_file(video, config.video_path)
        await save_uploaded_file(sticker, config.sticker_path)

        # Extract and cluster
        faces = extract_faces_and_embeddings(config.video_path, face_app)
        clusters = cluster_embeddings(faces, config.eps, config.min_samples)

        # Clean clusters (as in original code)
        cleaned_clusters = {}
        for cid, face_list in clusters.items():
            native_cid = int(cid)
            cleaned_clusters[native_cid] = face_list

        session_data[session_id] = {
            "video_path": config.video_path,
            "sticker_path": config.sticker_path,
            "clusters": cleaned_clusters
        }

        # Generate previews
        previews = {}
        for cid, face_list in cleaned_clusters.items():
            preview_path = save_preview(face_list[0]["crop"], config.session_path, cid)
            previews[cid] = preview_path

        cluster_ids = [int(k) for k in previews.keys()]
        logging.info(f"Uploaded session {session_id} with clusters {cluster_ids}")
        return {
            "session_id": session_id,
            "clusters": cluster_ids
        }
    except Exception as e:
        raise CustomException(e, sys)



