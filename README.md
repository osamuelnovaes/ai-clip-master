# AI Clip Master 🎬

Sistema automatizado para criar cortes virais de vídeos e postar em redes sociais.

## 🚀 Como Configurar (GitHub Actions)

1. **Crie um Repositório Privado** no seu GitHub.
2. **Adicione os Secrets:** Vá em `Settings > Secrets and variables > Actions` e adicione:
   - `GEMINI_API_KEY`: Sua chave do Google AI Studio.
   - `TIKTOK_COOKIES_CONTENT`: O conteúdo do seu arquivo `cookies.txt` (exportado via extensão do navegador).
3. **Execute:** Vá na aba `Actions`, selecione `AI Clip Master Pipeline`, clique em `Run workflow` e insira a URL do vídeo.

## 💻 Como Rodar Localmente

1. **Instale o FFmpeg** no seu sistema.
2. **Crie um ambiente virtual e instale as dependências:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Configure o `.env`** baseado no `.env.example`.
4. **Execute:**
   ```bash
   python main.py "https://www.youtube.com/watch?v=EXEMPLO"
   ```

## 🔒 Segurança

- O arquivo `.env` e pastas temporárias estão no `.gitignore`.
- O repositório **DEVE** ser mantido como **PRIVADO**.
- Nunca compartilhe seus cookies do TikTok.

---
Desenvolvido por **AIOS God Mode**
