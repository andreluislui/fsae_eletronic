#!/bin/bash
set -e

echo "🔧 Verificando status da interface SPI..."

# Verifica se o SPI já está habilitado
if ls /dev/spi* 1> /dev/null 2>&1; then
    echo "✅ SPI já está habilitado!"
    ls /dev/spi*
    echo "👍 Nenhuma ação necessária. Encerrando script."
    exit 0
else
    echo "⚠️  SPI não está habilitado. Tentando habilitar..."
fi

# Habilita SPI sem menu interativo
sudo raspi-config nonint do_spi 0

echo "✅ SPI habilitado via raspi-config."

# Espera alguns segundos antes de reiniciar
echo "🔁 Reiniciando o sistema em 5 segundos..."
sleep 5

sudo reboot
