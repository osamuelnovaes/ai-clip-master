#!/bin/bash

# Script de Execução Simplificada - AI Clip Master
# Desenvolvido por AIOS God Mode

echo "🚀 Iniciando o AI Clip Master Local..."

# 1. Entrar na pasta correta
cd "$(dirname "$0")"

# 2. Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual (primeira vez)..."
    python3 -m venv venv
fi

# 3. Ativar e instalar dependências silenciosamente
source venv/bin/activate
echo "🛠️ Verificando dependências..."
pip install -q -r requirements.txt
playwright install chromium -q 2>/dev/null

# 4. Tentar resolver cookies do YouTube automaticamente
echo "🔎 Configurando acesso ao YouTube..."
python3 scripts/setup_yt_auth.py > /dev/null 2>&1

# 5. Pedir o link do vídeo ao usuário
echo ""
read -p "🔗 Cole o link do vídeo do YouTube: " VIDEO_URL

if [ -z "$VIDEO_URL" ]; then
    echo "❌ Erro: Você precisa colar um link!"
    exit 1
fi

# 6. Rodar o motor
echo "🎬 Processando vídeo... (Aguarde alguns minutos)"
python3 main.py "$VIDEO_URL" "gemini"

echo ""
echo "✅ CONCLUÍDO! Verifique os cortes na pasta: output/"
open output/
