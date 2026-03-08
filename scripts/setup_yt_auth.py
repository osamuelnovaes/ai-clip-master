import os
import subprocess
import sys

def setup_youtube_secrets():
    print("🚀 Iniciando Configuração Automática de Autenticação do YouTube...")
    
    # 1. Verificar se o GitHub CLI está instalado
    try:
        subprocess.run(["gh", "auth", "status"], check=True, capture_output=True)
    except:
        print("❌ Erro: GitHub CLI (gh) não encontrado ou não autenticado.")
        return

    print("🔎 Tentando extrair cookies do navegador local...")
    
    # Criar um arquivo temporário para os cookies
    cookie_file = "temp/yt_cookies_local.txt"
    os.makedirs("temp", exist_ok=True)

    # Comando para o yt-dlp extrair cookies do Chrome (padrão no Mac)
    try:
        # Tenta extrair do Chrome ou Safari
        result = subprocess.run(
            ["yt-dlp", "--cookies-from-browser", "chrome", "--extract-audio", "--limit-rate", "1K", "https://www.youtube.com/watch?v=4HyNQe6UI_c", "--cookies", cookie_file, "--skip-download"],
            capture_output=True, text=True
        )
        
        if os.path.exists(cookie_file):
            with open(cookie_file, 'r') as f:
                cookies_content = f.read()
            
            print("✅ Cookies extraídos com sucesso!")
            
            # Enviar para o GitHub Secrets
            print("📤 Enviando para o GitHub Secrets (osamuelnovaes/ai-clip-master)...")
            subprocess.run(["gh", "secret", "set", "YOUTUBE_COOKIES_CONTENT", "--body", cookies_content], check=True)
            
            print("\n✨ TUDO PRONTO! O robô agora tem permissão para baixar vídeos como se fosse você.")
            os.remove(cookie_file)
        else:
            print("❌ Não foi possível extrair os cookies automaticamente.")
            print("DICA: Certifique-se de que o Chrome está fechado ou dê permissão de 'Acesso Total ao Disco' para o Terminal se solicitado.")
            
    except Exception as e:
        print(f"❌ Erro durante o processo: {e}")

if __name__ == "__main__":
    setup_youtube_secrets()
