import os
from tiktok_uploader.upload import upload_video
from dotenv import load_dotenv

load_dotenv()

def publish_to_tiktok(video_path, description="#shorts #viral #aiclip"):
    print(f"Publishing to TikTok: {video_path}")
    
    # Get cookies from environment variable (saved to temp file for the library)
    cookies_content = os.getenv("TIKTOK_COOKIES_CONTENT")
    if not cookies_content:
        print("Error: TIKTOK_COOKIES_CONTENT not found. Skipping TikTok.")
        return False

    cookie_path = 'temp/cookies.txt'
    with open(cookie_path, 'w') as f:
        f.write(cookies_content)

    try:
        # tiktok-uploader uses playwright to simulate a browser upload
        upload_video(
            video_path,
            description=description,
            cookies=cookie_path,
            browser='chromium',
            headless=True
        )
        print("Successfully posted to TikTok!")
        return True
    except Exception as e:
        print(f"Failed to post to TikTok: {e}")
        return False

def publish_to_youtube(video_path, title="Viral Clip", description="#shorts"):
    # Note: YouTube API requires OAuth2 tokens which are harder to automate 
    # fully without manual first-time auth. 
    # For now, we'll focus on TikTok which is the main target for clips.
    print(f"YouTube upload triggered for {video_path} (Stub - requires OAuth setup)")
    return True

if __name__ == "__main__":
    # Test
    pass
