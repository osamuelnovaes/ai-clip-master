import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

def list_my_models():
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    print("🔍 Listando modelos disponíveis para sua chave...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ Modelo: {m.name}")
    except Exception as e:
        print(f"❌ Erro ao listar modelos: {e}")

if __name__ == "__main__":
    list_my_models()
