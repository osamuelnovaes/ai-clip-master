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
    Você é um Editor de Redes Sociais Senior especializado em viralização no TikTok, Reels e Shorts.
    Sua tarefa é analisar a transcrição abaixo e extrair os 3 momentos com maior potencial de VIRALIZAÇÃO.
    
    DIRETRIZES DE EDIÇÃO:
    1. GANCHO FORTE: O corte deve começar com uma frase impactante, uma pergunta curiosa ou uma afirmação forte.
    2. CONTEXTO COMPLETO: Não corte apenas a frase final. Inclua a explicação e o raciocínio que leva ao momento principal.
    3. DURAÇÃO IDEAL: Cada corte deve ter entre 30 a 70 segundos. Menos que isso perde o contexto, mais que isso perde a retenção.
    4. PENSAMENTO COMPLETO: Certifique-se de que o corte termine após a conclusão de uma ideia, evitando cortes abruptos no meio da fala.
    5. ESTILO: Busque momentos de "sabedoria", "polêmica", "humor" ou "emoção intensa".
    
    Transcrição:
    {json.dumps(transcription)}
    
    Retorne APENAS um array JSON com exatamente 3 objetos:
    [
      {{"start": tempo_inicio_float, "end": tempo_fim_float, "caption": "Título Viral e Chamativo"}},
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
            "model": "meta/llama-3.1-70b-instruct", 
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "top_p": 0.7,
            "max_tokens": 1024
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code != 200:
                print(f"❌ Erro HTTP NVIDIA ({response.status_code}): {response.text}")
                return []
            
            response_json = response.json()
            if 'choices' in response_json:
                text = response_json['choices'][0]['message']['content']
                return _parse_json(text)
            print(f"❌ Resposta inesperada da NVIDIA: {response_json}")
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
