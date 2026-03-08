import os
import yt_dlp

def download_video(url, output_path='temp/input.mp4', cookies_path=None):
    print(f"Downloading video from: {url}")
    
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
    }
    
    # Se houver cookies, utiliza para evitar o erro de "Bot"
    if cookies_path and os.path.exists(cookies_path):
        print(f"Using YouTube cookies from: {cookies_path}")
        ydl_opts['cookiefile'] = cookies_path
    else:
        # Fallback para tentar evitar detecção sem cookies
        ydl_opts['user_agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        download_video(sys.argv[1])
