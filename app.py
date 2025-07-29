from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
import os
from src.constants import DATA_FOLDER, SESSION_NOT_FOUND
from src.pipeline.upload_pipeline import UploadPipeline
from src.pipeline.render_pipeline import RenderPipeline

app = FastAPI(title="Face Detection Sticker Overlay API", version="1.0.0")

# Ensure data folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)

# IMPORTANT: Initialize as module-level variable, not inside functions
session_data: dict = {}

# Initialize pipelines at module level
upload_pipeline = UploadPipeline()
render_pipeline = RenderPipeline()

# Add a debug endpoint to check session status
@app.get("/debug/sessions")
def debug_sessions():
    return {
        "total_sessions": len(session_data),
        "session_ids": list(session_data.keys()),
        "session_details": {k: {"clusters": list(v.clusters.keys())} for k, v in session_data.items()}
    }

@app.get("/")
def root():
    return {"message": "Face Detection Sticker Overlay API", "version": "1.0.0"}

@app.post("/upload/")
async def upload_files(video: UploadFile = File(...), sticker: UploadFile = File(...)):
    """Upload video and sticker files, extract and cluster faces"""
    try:
        # Run upload pipeline (FIXED - added await)
        upload_artifacts = await upload_pipeline.run_pipeline(video, sticker)
        
        # Store session data
        session_data[upload_artifacts.session_artifacts.session_id] = upload_artifacts.session_artifacts
        
        # DEBUG: Add these lines to verify storage
        print(f"Session stored: {upload_artifacts.session_artifacts.session_id}")
        print(f"Total sessions in memory: {len(session_data)}")
        print(f"Session keys: {list(session_data.keys())}")
        
        return JSONResponse(
            content={
                "session_id": upload_artifacts.session_artifacts.session_id,
                "clusters": upload_artifacts.cluster_ids,
                "message": upload_artifacts.message
            },
            status_code=200
        )
    except Exception as e:
        print(f"Upload error: {str(e)}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.post("/render/")
def render_video(session_id: str = Form(...), cluster_ids: str = Form(...)):
    """Render video with sticker overlays on selected face clusters"""
    try:
        # Clean session_id of any whitespace
        session_id = session_id.strip()
        
        # DEBUG: Add these lines to verify lookup
        print(f"Looking for session: '{session_id}' (length: {len(session_id)})")
        print(f"Available sessions: {list(session_data.keys())}")
        print(f"Session count: {len(session_data)}")
        
        if session_id not in session_data:
            # Additional debugging
            for stored_id in session_data.keys():
                print(f"Stored: '{stored_id}' (len: {len(stored_id)}) == Input: '{session_id}' (len: {len(session_id)}) ? {stored_id == session_id}")
            
            print(f"Session '{session_id}' NOT FOUND!")
            return JSONResponse(status_code=404, content={"error": SESSION_NOT_FOUND})
            
        print(f"Session '{session_id}' FOUND!")
        
        # DEBUG: Print raw cluster_ids input
        print(f"Raw cluster_ids input: '{cluster_ids}'")
        
        # Parse cluster IDs with better error handling
        try:
            selected_clusters = [int(cid.strip()) for cid in cluster_ids.split(",") if cid.strip().isdigit()]
            print(f"Parsed selected clusters: {selected_clusters}")
            
            # Verify clusters exist in session
            available_clusters = list(session_data[session_id].clusters.keys())
            print(f"Available clusters in session: {available_clusters}")
            
            # Filter only valid clusters
            valid_clusters = [cid for cid in selected_clusters if cid in available_clusters]
            print(f"Valid clusters for rendering: {valid_clusters}")
            
            if not valid_clusters:
                return JSONResponse(
                    status_code=400, 
                    content={"error": f"No valid clusters selected. Available clusters: {available_clusters}"}
                )
                
        except Exception as e:
            print(f"Cluster parsing error: {e}")
            return JSONResponse(status_code=400, content={"error": f"Invalid cluster_ids format: {cluster_ids}"})
        
        # Run render pipeline with valid clusters
        render_artifacts = render_pipeline.run_pipeline(
            session_data[session_id], 
            valid_clusters  # Use valid_clusters instead of selected_clusters
        )
        
        return FileResponse(
            render_artifacts.final_video_path, 
            media_type="video/mp4", 
            filename="output_sticker_overlay_with_audio.mp4"
        )
    except Exception as e:
        print(f"Render error: {str(e)}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )


