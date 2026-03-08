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

    # Prompt de Nível Especialista com Chain of Thought
    prompt = f"""
    Você é um Especialista em Retenção de Audiência e Algoritmos do TikTok/Reels.
    Sua missão é salvar um canal do YouTube extraindo os momentos MAIS EXPLOSIVOS da transcrição abaixo.

    FASE 1: ANÁLISE DE VALOR
    Identifique os momentos que contêm:
    - Revelações contra-intuitivas (quebras de padrão).
    - Conselhos práticos imediatos ("Como fazer X").
    - Momentos de alta carga emocional (raiva, alegria, surpresa).
    - Frases que servem como "quotes" inspiradores.

    FASE 2: CRITÉRIOS DE SELEÇÃO (DOD)
    1. O corte DEVE começar com uma frase que prenda a atenção nos primeiros 3 segundos.
    2. O corte DEVE ter entre 40 e 80 segundos para garantir contexto profundo.
    3. O corte DEVE terminar exatamente após um insight ser concluído.
    4. Adicione uma margem de segurança: se o momento importante começa em 10s, sugira o início em 8s.

    Transcrição:
    {json.dumps(transcription)}
    
    Responda APENAS um JSON puro (sem explicações fora do JSON):
    [
      {{
        "start": float, 
        "end": float, 
        "caption": "Título Viral (Ex: A verdade que ninguém te conta sobre...)",
        "reasoning": "Breve explicação do porquê esse momento vai viralizar"
      }},
      ... (exatamente 3 cortes)
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
            "temperature": 0.1, # Menor temperatura = mais foco e menos "loucura"
            "max_tokens": 2048
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
