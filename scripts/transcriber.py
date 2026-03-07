import whisper
import os

def transcribe_video(video_path, model_name="tiny"):
    print(f"Transcribing video: {video_path}")
    model = whisper.load_model(model_name)
    result = model.transcribe(video_path, verbose=False)
    
    # Save transcription with timestamps
    transcription = []
    for segment in result['segments']:
        transcription.append({
            'start': segment['start'],
            'end': segment['end'],
            'text': segment['text']
        })
    return transcription

if __name__ == "__main__":
    # Test path
    path = "temp/input.mp4"
    if os.path.exists(path):
        print(transcribe_video(path))
