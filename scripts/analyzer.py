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
        data = { "contents": [{ "parts": [{"text": prompt}] }] }
        try:
            response = requests.post(url, headers=headers, json=data)
            response_json = response.json()
            if 'candidates' in response_json:
                text = response_json['candidates'][0]['content']['parts'][0]['text']
                return _parse_json(text)
            print(f"❌ Erro na API do Gemini: {response_json}")
        except Exception as e:
            print(f"❌ Falha Gemini: {e}")

    elif provider == "nvidia":
        print("Using NVIDIA NIM API Call (Llama 3)...")
        url = "https://integrate.api.nvidia.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "meta/llama-3.1-405b-instruct", # Modelo top da NVIDIA
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "top_p": 0.7,
            "max_tokens": 1024
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response_json = response.json()
            if 'choices' in response_json:
                text = response_json['choices'][0]['message']['content']
                return _parse_json(text)
            print(f"❌ Erro na API da NVIDIA: {response_json}")
        except Exception as e:
            print(f"❌ Falha NVIDIA: {e}")

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
