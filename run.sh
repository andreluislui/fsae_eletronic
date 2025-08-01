#!/bin/bash

set -e  # Encerra o script se algo der errado

# Caminho do virtualenv correto
VENV_DIR=".venv"

echo "🔍 Verificando ambiente virtual..."

# Cria o virtualenv se não existir
if [ ! -d "$VENV_DIR" ]; then
  echo "📦 Virtualenv não encontrado. Criando em $VENV_DIR..."
  python3 -m venv "$VENV_DIR"
fi

# Ativa o ambiente virtual
echo "🐍 Ativando virtualenv ($VENV_DIR)..."
source "$VENV_DIR/bin/activate"

# Atualiza os pacotes
echo "⬇️ Instalando dependências do requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Executa o script principal
echo "🚀 Rodando o projeto (run.py)..."
python3 run.py