import asyncio
from app.pipeline import run_pipeline
import os
import glob

async def test():
    files = glob.glob("downloads/*.mp4")
    if not files:
        print("No local video files found in downloads.")
        return
    
    local_file = files[0]
    try:
        print(f"Starting manual test with local file: {local_file}...")
        result = await run_pipeline(None, "ta", input_file=local_file)
        print("Test completed successfully!")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
