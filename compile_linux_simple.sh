#!/bin/bash
set -e

echo "=== CONFIGURANDO ENTORNO LINUX ==="
echo "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "Instalando Python..."
    sudo apt update && sudo apt install -y python3 python3-pip python3-dev python3-tk
else
    echo "Python3 encontrado: $(python3 --version)"
fi

echo "Verificando pip..."
if ! python3 -m pip --version &> /dev/null; then
    echo "Instalando pip..."
    sudo apt install -y python3-pip
fi

echo "Verificando PyInstaller..."
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo "Instalando PyInstaller..."
    if python3 -m pip install --user PyInstaller 2>/dev/null; then
        echo "PyInstaller instalado con --user"
        export PATH="$HOME/.local/bin:$PATH"
    elif python3 -m pip install --break-system-packages PyInstaller 2>/dev/null; then
        echo "PyInstaller instalado con --break-system-packages"
    else
        echo "Error: No se pudo instalar PyInstaller"
        exit 1
    fi
    
    if ! python3 -c "import PyInstaller" &> /dev/null; then
        echo "Error: PyInstaller no se instalo correctamente"
        exit 1
    fi
else
    echo "PyInstaller encontrado"
fi

echo "=== COMPILANDO VERSIONES ==="
mkdir -p dist

echo "Compilando version terminal..."
python3 -m PyInstaller \
    --onefile \
    --console \
    --name="renombrador-terminal-linux" \
    --distpath="dist" \
    --workpath="build/linux-terminal" \
    --clean \
    --noconfirm \
    rename_folders.py

echo "Compilando version GUI..."
python3 -m PyInstaller \
    --onefile \
    --windowed \
    --name="renombrador-gui-linux" \
    --distpath="dist" \
    --workpath="build/linux-gui" \
    --clean \
    --noconfirm \
    rename_folders_gui.py

echo "Verificando resultados..."
if [ -f "dist/renombrador-terminal-linux" ] && [ -f "dist/renombrador-gui-linux" ]; then
    echo "OK: Ambas versiones compiladas exitosamente"
    echo "Archivos generados:"
    ls -la dist/renombrador-*-linux
else
    echo "ERROR: No se generaron todos los ejecutables"
    echo "Contenido de dist/:"
    ls -la dist/ || echo "Carpeta dist no existe"
    exit 1
fi
