import asyncio
from app.pipeline import run_pipeline
import os

async def test():
    # URL that successfully translated according to the user's database screenshot
    url = "https://www.youtube.com/shorts/a1ZiLZA3v0I"
    try:
        print("Starting manual test with the exact URL from your screenshot...")
        result = await run_pipeline(url, "ta")
        print("\nSUCCESS! The pipeline finished correctly.")
        print(f"Original: {result['original_text'][:100]}...")
        print(f"Translated: {result['translated_text'][:100]}...")
        print(f"Output Video URL: {result['output_video_url']}")
    except Exception as e:
        print(f"\nFAILURE! Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
