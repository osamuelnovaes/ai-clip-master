import os
import json
import requests
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
        print("Using Universal Gemini API Call...")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response_json = response.json()
            
            if 'candidates' in response_json:
                text = response_json['candidates'][0]['content']['parts'][0]['text']
                return _parse_json(text)
            else:
                print(f"❌ Erro na API do Gemini: {response_json}")
                return []
        except Exception as e:
            print(f"❌ Falha na requisição Gemini: {e}")
            return []

    elif provider == "claude":
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
        try:
            response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
            return _parse_json(response.json()['content'][0]['text'])
        except Exception as e:
            print(f"❌ Erro na API do Claude: {e}")
            return []

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
