#!/bin/bash

# Script de Execução Simplificada - AI Clip Master (Versão Compatível Python 3.14+)
echo "🚀 Iniciando o AI Clip Master Local..."

# 1. Entrar na pasta correta
cd "$(dirname "$0")"

# 2. Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# 3. Ativar e instalar dependências
source venv/bin/activate
echo "🛠️ Verificando dependências e compatibilidade..."
python3 -m pip install -q --upgrade pip
python3 -m pip install -q setuptools wheel # Necessário para Python 3.14+
pip install -q -r requirements.txt
playwright install chromium -q 2>/dev/null

# 4. Tentar resolver cookies do YouTube
echo "🔎 Configurando acesso ao YouTube..."
python3 scripts/setup_yt_auth.py > /dev/null 2>&1

# 5. Pedir o link do vídeo
echo ""
read -p "🔗 Cole o link do vídeo do YouTube: " VIDEO_URL

if [ -z "$VIDEO_URL" ]; then
    echo "❌ Erro: Link vazio!"
    exit 1
fi

# 6. Rodar o motor
echo "🎬 Processando vídeo... (Isso pode levar alguns minutos)"
python3 main.py "$VIDEO_URL" "gemini"

echo ""
echo "🚚 Movendo cortes para a sua pasta de Downloads..."
mkdir -p ~/Downloads/AI-CLIPS
mv output/*.mp4 ~/Downloads/AI-CLIPS/ 2>/dev/null

echo "✅ CONCLUÍDO! Verifique os cortes em: Downloads/AI-CLIPS"
open ~/Downloads/AI-CLIPS
