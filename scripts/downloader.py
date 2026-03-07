import os
import yt_dlp

def download_video(url, output_path='temp/input.mp4'):
    print(f"Downloading video from: {url}")
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        download_video(sys.argv[1])
