import asyncio
import os
import sys

# Add the current directory to sys.path so we can import app
sys.path.append(os.getcwd())

from app.pipeline import run_pipeline

async def test():
    # Test a short YouTube video
    url = "https://www.youtube.com/shorts/a1ZiLZA3v0I"
    lang = "ta"
    voice = "ta-IN-ValluvarNeural"
    
    try:
        print("Starting test pipeline...")
        result = await run_pipeline(url, lang, voice_id=voice)
        print("Pipeline Result:", result)
    except Exception as e:
        import traceback
        print("Pipeline Failed!")
        print(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(test())
