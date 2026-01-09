from fastapi import APIRouter, HTTPException, BackgroundTasks, Form, UploadFile, File
from typing import Optional
from app.pipeline import run_pipeline
from app.database import get_db_connection
import os
import time
import shutil
import uuid

router = APIRouter(
    prefix="/api",
    tags=["translation"]
)

@router.post("/translate")
async def translate_video(
    video_url: Optional[str] = Form(None),
    target_language: str = Form(...),
    voice_id: str = Form("female"),
    video_file: Optional[UploadFile] = File(None)
):
    print(f"[{time.strftime('%H:%M:%S')}] Incoming Request: URL={video_url}, Target={target_language}, Voice={voice_id}", flush=True)
    try:
        if video_file and video_file.filename:
            print(f"[{time.strftime('%H:%M:%S')}] Processing Uploaded File: {video_file.filename}", flush=True)
            # Save uploaded file
            os.makedirs("downloads", exist_ok=True)
            input_file = os.path.join("downloads", f"{uuid.uuid4()}_{video_file.filename}")
            with open(input_file, "wb") as buffer:
                shutil.copyfileobj(video_file.file, buffer)
            
            # Run the pipeline with local file
            result = await run_pipeline(None, target_language, voice_id=voice_id, input_file=input_file)
        elif video_url:
            print(f"[{time.strftime('%H:%M:%S')}] Processing YouTube URL: {video_url}", flush=True)
            # Run the pipeline with YouTube URL
            result = await run_pipeline(video_url, target_language, voice_id=voice_id)
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Error: No input provided", flush=True)
            raise HTTPException(status_code=400, detail="Either video_url or video_file must be provided")
        
        print(f"[{time.strftime('%H:%M:%S')}] Pipeline finished successfully. Result: {result.get('output_video_url')}", flush=True)
        
        # Save to database (Using URL if available, else filename)
        db_url = video_url if video_url else video_file.filename
        
        # Save to database
        db = get_db_connection()
        if db:
            cursor = db.cursor()
            sql = """INSERT INTO translations 
                     (video_url, source_language, target_language, original_text, translated_text, audio_path) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            val = (
                db_url, 
                result['source_lang'], 
                target_language, 
                result['original_text'], 
                result['translated_text'], 
                result['output_video_url']
            )
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

        return {
            "status": "completed",
            "video_url": db_url,
            "original_text": result['original_text'],
            "translated_text": result['translated_text'],
            "output_video_url": result['output_video_url']
        }
    except Exception as e:
        import traceback
        with open("error_log.txt", "a") as f:
            f.write(f"\n--- Error at {time.ctime()} ---\n")
            f.write(traceback.format_exc())
            f.write("\n")
        raise HTTPException(status_code=500, detail=str(e))
