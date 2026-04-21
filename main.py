from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = FastAPI()

# Allow your website to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://toolsnova.github.io"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

def extract_video_id(url: str) -> str:
    patterns = [
        r'(?:youtube\.com\/watch\?v=)([\w-]+)',
        r'(?:youtu\.be\/)([\w-]+)',
        r'(?:youtube\.com\/embed\/)([\w-]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise HTTPException(400, "Invalid YouTube URL")

QUALITIES = ["default", "mqdefault", "hqdefault", "sddefault", "maxresdefault"]

# ... inside your main.py, replace the existing get_transcript function ...

@app.get("/api/transcript")
async def get_transcript(url: str = Query(...), language: str = "en"):
    try:
        video_id = extract_video_id(url)
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        # ... (your existing transcript fetching logic) ...

        return {
            "success": True,
            # ... (your existing success response) ...
        }
    except Exception as e:
        # THIS IS THE IMPORTANT PART - Return a clean, simple error
        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error": "TRANSCRIPT_NOT_AVAILABLE",
                "message": "This video doesn't have subtitles or captions. Please try another video."
            }
        )

@app.get("/")
async def root():
    return {"message": "ToolsNova API is running!", "endpoints": ["/api/thumbnail", "/api/transcript"]}