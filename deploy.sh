#!/bin/bash

# Configurações
PI_USER="andre"
PI_HOST="raspberrypi.local"             # Substitua pelo IP da sua Raspberry Pi
PI_PATH="/home/andre/fsae_eletronic"    # Caminho do projeto na Raspberry Pi
LOCAL_PATH="."                          # Diretório local do projeto

# ==== DEPLOY ====
echo "🚀 Iniciando deploy para $PI_USER@$PI_HOST:$PI_PATH..."

rsync -avz --delete \
  --exclude '__pycache__' \
  --exclude '.git' \
  --exclude '.vscode' \
  --exclude '.venv' \
  --exclude '*.pyc' \
  "$LOCAL_PATH/" "$PI_USER@$PI_HOST:$PI_PATH"

echo "✅ Deploy concluído com sucesso!"