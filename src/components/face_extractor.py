import cv2
import numpy as np

def extract_faces_and_embeddings(video_path, face_app):
    cap = cv2.VideoCapture(video_path)
    all_faces = []
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        faces = face_app.get(frame)
        for face in faces:
            x1, y1, x2, y2 = face.bbox.astype(int)
            face_crop = frame[y1:y2, x1:x2]
            if face_crop.size > 0:
                emb = face.embedding / np.linalg.norm(face.embedding)
                all_faces.append({
                    "frame": frame_idx,
                    "embedding": emb,
                    "crop": face_crop,
                    "bbox": (x1, y1, x2, y2)
                })
        frame_idx += 1

    cap.release()
    return all_faces


