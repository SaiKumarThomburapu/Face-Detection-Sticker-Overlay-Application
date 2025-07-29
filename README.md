Face Detection Sticker Overlay Application

Overview

This application automatically detects faces in videos and allows you to apply stickers to specific people throughout the entire video while preserving the original audio. It uses advanced computer vision to identify and group similar faces, then lets you selectively apply overlays.

What Does This Application Do?
Analyzes video frames and detects all faces

Groups similar faces together (identifies the same person across frames)

Lets you choose which groups of faces to apply stickers to

Automatically applies stickers to selected faces throughout the video

Preserves original audio and video quality

Use Cases
Social Media: Add fun filters to party videos or family gatherings

Privacy Protection: Blur specific people's faces in videos

Marketing: Add branded stickers to promotional videos

Entertainment: Create themed content with custom overlays

Technical Architecture
How It Works
Face Detection: Uses InsightFace's buffalo_l model for accurate face detection

Feature Extraction: Converts faces into mathematical representations (embeddings)

Face Clustering: Groups similar faces using DBSCAN clustering algorithm

Video Processing: Applies stickers to selected clusters across all frames

Audio Preservation: Uses FFmpeg to maintain original audio

System Architecture
text
┌─────────────────────────────────────────────────┐
│                 API LAYER                       │
│              (FastAPI Server)                   │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│              PIPELINE LAYER                     │
│  ┌─────────────────┐  ┌─────────────────────┐   │
│  │ Upload Pipeline │  │ Render Pipeline     │   │
│  └─────────────────┘  └─────────────────────┘   │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│            COMPONENTS LAYER                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────┐ │
│  │   Face   │ │   Face   │ │  Video   │ │Audio│ │
│  │Extraction│ │Clustering│ │Processing│ │Proc││ │
│  └──────────┘ └──────────┘ └──────────┘ └────┘ │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│        ENTITY & CONSTANTS LAYER                │
│     (Configuration & Data Management)           │
└─────────────────────────────────────────────────┘
Project Structure
text
face-detection-sticker-overlay/
├── app.py                          # Main API server
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation
├── src/                           # Source code
│   ├── constants/                 # Application settings
│   │   └── __init__.py           
│   ├── entity/                    # Data structures
│   │   ├── config_entity.py      # Configuration classes
│   │   └── artifacts.py          # Output data classes
│   ├── components/                # Core processing modules
│   │   ├── face_extraction.py    # Face detection logic
│   │   ├── face_clustering.py    # Face grouping logic
│   │   ├── video_processing.py   # Video overlay logic
│   │   └── audio_processing.py   # Audio merging logic
│   └── pipeline/                  # Workflow orchestration
│       ├── upload_pipeline.py    # Upload workflow
│       └── render_pipeline.py    # Render workflow
└── data/                          # Session storage (auto-created)
Installation Guide
Prerequisites
Python 3.10 (required)

FFmpeg for audio/video processing

4GB+ RAM recommended

System Dependencies
Ubuntu/Debian:

bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev ffmpeg
sudo apt install libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1
macOS:

bash
brew install python@3.10 ffmpeg
Windows:

Install Python 3.10 from python.org

Install FFmpeg from ffmpeg.org and add to PATH

Project Setup
bash
# Clone repository
git clone <your-repository-url>
cd face-detection-sticker-overlay

# Create virtual environment
python3.10 -m venv face_detection_env
source face_detection_env/bin/activate  # Linux/macOS
# face_detection_env\Scripts\activate   # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create data directory
mkdir data

# Verify installation
python -c "import cv2, numpy, insightface; print('Setup successful!')"
Usage Guide
Step 1: Start the Server
bash
# Activate environment
source face_detection_env/bin/activate

# Start server
uvicorn app:app --host 0.0.0.0 --port 8000
Step 2: Access Application
API Documentation: http://localhost:8000/docs

Debug Interface: http://localhost:8000/debug/sessions

Step 3: Upload Files
Web Interface (Recommended):

Go to http://localhost:8000/docs

Use POST /upload/ endpoint

Upload video file and sticker image

Note the session_id and clusters from response

Command Line:

bash
curl -X POST "http://localhost:8000/upload/" \
  -F "video=@your_video.mp4" \
  -F "sticker=@your_sticker.png"
Response:

json
{
  "session_id": "abc123...",
  "clusters": [0, 1, 2, 3],
  "message": "Upload successful"
}
Step 4: Render Video
Web Interface:

Use POST /render/ endpoint

Enter session_id and cluster_ids (e.g., "0,1,2")

Download the generated video

Command Line:

bash
curl -X POST "http://localhost:8000/render/" \
  -F "session_id=abc123..." \
  -F "cluster_ids=0,1,2" \
  --output final_video.mp4
Understanding Clusters
Clusters represent unique people in your video

Each cluster contains all appearances of the same person

Use specific cluster numbers to apply stickers selectively

Check /debug/sessions to see available clusters

File Requirements
Video Files
Formats: MP4, AVI, MOV (MP4 recommended)

Any resolution/duration (higher quality = longer processing)

Audio: Optional (preserved if present)

Sticker Files
Format: PNG with transparent background (recommended)

Any size (automatically resized to fit faces)

Content: Any image (emojis, logos, overlays, etc.)

API Reference
Upload Endpoint
URL: POST /upload/

Parameters: video (file), sticker (file)

Returns: session_id and available clusters

Render Endpoint
URL: POST /render/

Parameters: session_id, cluster_ids (comma-separated)

Returns: Processed video file

Debug Endpoint
URL: GET /debug/sessions

Returns: Current sessions and cluster information

Configuration
Modify src/constants/__init__.py for customization:

python
# Face detection settings
DEFAULT_EPS = 0.6          # Clustering sensitivity (0.1-1.0)
DEFAULT_MIN_SAMPLES = 3    # Min faces per cluster (1-10)
DEFAULT_FPS = 30          # Output video frame rate

# Model settings
FACE_MODEL_NAME = "buffalo_l"  # buffalo_l, buffalo_m, buffalo_s
VIDEO_CODEC = 'mp4v'          # mp4v, xvid, h264
