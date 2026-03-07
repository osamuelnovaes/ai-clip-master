from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip, vfx
import os

def create_clips(input_path, clips_data, output_dir='output'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Creating {len(clips_data)} clips...")
    
    for i, clip_info in enumerate(clips_data):
        start = clip_info['start']
        end = clip_info['end']
        output_name = f"{output_dir}/clip_{i+1}.mp4"
        
        print(f"Clipping {start}s to {end}s -> {output_name}")
        
        # Load clip
        video = VideoFileClip(input_path).subclip(start, end)
        
        # Resize for TikTok (Vertical 9:16)
        # Assuming original is 16:9, we crop the center
        w, h = video.size
        target_w = h * 9 / 16
        x_center = w / 2
        video = video.crop(x1=x_center - target_w / 2, y1=0, x2=x_center + target_w / 2, y2=h)
        
        # Resize to standard TikTok resolution if needed
        video = video.resize(height=1080)
        
        video.write_videofile(output_name, codec="libx264", audio_codec="aac")
        print(f"Saved: {output_name}")

if __name__ == "__main__":
    # Example usage for testing
    pass
