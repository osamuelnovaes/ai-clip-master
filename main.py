import os
import sys
from dotenv import load_dotenv
from scripts.downloader import download_video
from scripts.transcriber import transcribe_video
from scripts.analyzer import find_viral_clips
from scripts.clipper import create_clips
from scripts.publisher import publish_to_tiktok, publish_to_youtube

load_dotenv()

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <YOUTUBE_URL> [PROVIDER] [API_KEY]")
        return

    url = sys.argv[1]
    provider = sys.argv[2] if len(sys.argv) > 2 else os.getenv("LLM_PROVIDER", "gemini")
    api_key = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Ensure directories exist
    os.makedirs('temp', exist_ok=True)
    os.makedirs('output', exist_ok=True)

    # 1. Download
    video_path = download_video(url, 'temp/input.mp4')

    # 2. Transcribe
    transcription = transcribe_video(video_path, os.getenv("MODEL_SIZE", "tiny"))

    # 3. Analyze (Using Multi-Provider Logic)
    clips_data = find_viral_clips(transcription, provider=provider, api_key=api_key)
    print(f"Viral Clips Found via {provider}: {clips_data}")

    # 4. Create Clips
    create_clips(video_path, clips_data, 'output')

    # 5. Publish Clips
    print("Starting publishing phase...")
    for i, clip_info in enumerate(clips_data):
        clip_path = f"output/clip_{i+1}.mp4"
        caption = clip_info.get('caption', 'Check this viral moment! #shorts #podcast')
        
        # Publish to TikTok
        publish_to_tiktok(clip_path, description=caption)
        
        # Publish to YouTube (Stub for now)
        publish_to_youtube(clip_path, title=caption)

    print("Pipeline and Publishing Complete!")

if __name__ == "__main__":
    main()
