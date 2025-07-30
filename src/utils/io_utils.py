import cv2

async def save_uploaded_file(upload_file, path):
    with open(path, "wb") as f:
        f.write(await upload_file.read())

def save_preview(crop, session_path, cid):
    preview_path = f"{session_path}/cluster_{cid}.jpg"
    cv2.imwrite(preview_path, crop)
    return preview_path
