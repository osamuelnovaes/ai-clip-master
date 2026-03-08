import os
import json
import requests
from google import genai
from dotenv import load_dotenv

load_dotenv()

def find_viral_clips(transcription, provider=None, api_key=None):
    provider = provider or os.getenv("LLM_PROVIDER", "gemini")
    api_key = api_key or os.getenv(f"{provider.upper()}_API_KEY")
    
    if not api_key:
        print(f"Error: API Key for {provider} not found.")
        return []

    prompt = f"""
    Analyze the following transcription of a podcast/video. 
    Find the 3 most viral, emotional, or interesting moments (hooks).
    For each moment, provide:
    1. Start time (seconds)
    2. End time (seconds)
    3. Suggested Title/Caption
    
    Transcription:
    {json.dumps(transcription)}
    
    Return ONLY a JSON array like:
    [
      {{"start": 10.5, "end": 45.0, "caption": "The secret to success"}},
      ...
    ]
    """

    if provider == "gemini":
        try:
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt,
            )
            return _parse_json(response.text)
        except Exception as e:
            print(f"❌ Erro no Gemini GenAI: {e}")
            return []

    elif provider == "claude":
        # Anthropic API remains the same
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        data = {
            "model": "claude-3-haiku-20240307",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
        return _parse_json(response.json()['content'][0]['text'])

    return []

def _parse_json(text):
    try:
        text = text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception as e:
        print(f"Error parsing AI response: {e}")
        return []
