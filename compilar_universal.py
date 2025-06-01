#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compilador Universal Simple - Windows + Linux
Autor: rodrigoangeloni
Fecha: 2025-06-01

INSTRUCCIONES:
1. En Windows: python compilar_universal.py
2. Se compilará para Windows automáticamente
3. Si tienes WSL, también compilará para Linux
4. Los ejecutables estarán en dist/
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

def print_header():
    """Imprime encabezado del compilador"""
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "COMPILADOR UNIVERSAL" + " " * 22 + "║")
    print("║" + " " * 8 + "Renombrador de Carpetas - Windows + Linux" + " " * 8 + "║")
    print("╚" + "═" * 58 + "╝")
    print()

def check_requirements():
    """Verifica requisitos básicos"""
    print("Verificando requisitos...")
    
    # Verificar Python
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Python OK: {result.stdout.strip()}")
        else:
            print("Error: Python no encontrado")
            return False
    except:
        print("Error: Python no encontrado")
        return False
    
    # Verificar archivo fuente
    if not os.path.exists("rename_folders.py"):
        print("Error: No se encuentra 'rename_folders.py'")
        return False
    
    print("OK: Archivo fuente encontrado")
    
    # Verificar/instalar PyInstaller
    try:
        subprocess.run([sys.executable, "-c", "import PyInstaller"], 
                      check=True, capture_output=True)
        print("OK: PyInstaller disponible")
    except subprocess.CalledProcessError:
        print("Instalando PyInstaller...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                          check=True, capture_output=True)
            print("OK: PyInstaller instalado")
        except subprocess.CalledProcessError:
            print("Error: No se pudo instalar PyInstaller")
            return False
    
    return True

def clean_previous_builds():
    """Limpia compilaciones anteriores"""
    print("\nLimpiando builds anteriores...")
    for folder in ["dist", "build"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"   Eliminado: {folder}/")

def compile_windows():
    """Compila para Windows"""
    print("\nCompilando para Windows...")
    
    os.makedirs("dist", exist_ok=True)
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console", 
        "--name=renombrador-universal-windows",
        "--distpath=dist",
        "--workpath=build/windows",
        "--clean",
        "--noconfirm",
        "rename_folders.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        exe_path = "dist/renombrador-universal-windows.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"OK: Windows ejecutable creado - {exe_path} ({size_mb:.1f} MB)")
            return True
        else:
            print("Error: Windows ejecutable no generado")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error: Windows compilacion fallida")
        return False

def check_wsl():
    """Verifica si WSL está disponible"""
    try:
        subprocess.run(['wsl', '--version'], check=True, capture_output=True)
        return True
    except:
        return False

def compile_linux():
    """Compila para Linux usando WSL"""
    print("\nCompilando para Linux (WSL)...")
    
    if not check_wsl():
        print("Aviso: WSL no disponible - saltando Linux")
        print("Info: Para instalar WSL: wsl --install")
        return False
    
    # Script para WSL con mejor manejo de errores
    wsl_script = """#!/bin/bash
set -e

echo "=== CONFIGURANDO ENTORNO LINUX ==="
echo "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "Instalando Python..."
    sudo apt update && sudo apt install -y python3 python3-pip python3-dev
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
    
    # Intentar diferentes métodos de instalación
    if python3 -m pip install --user PyInstaller 2>/dev/null; then
        echo "PyInstaller instalado con --user"
        export PATH="$HOME/.local/bin:$PATH"
    elif python3 -m pip install --break-system-packages PyInstaller 2>/dev/null; then
        echo "PyInstaller instalado con --break-system-packages"
    else
        echo "Error: No se pudo instalar PyInstaller"
        echo "Intentando con pipx..."
        if command -v pipx &> /dev/null || (apt update && apt install -y pipx); then
            pipx install pyinstaller
            export PATH="$HOME/.local/bin:$PATH"
        else
            echo "Error: Todas las instalaciones fallaron"
            exit 1
        fi
    fi
    
    # Verificar instalación
    if ! python3 -c "import PyInstaller" &> /dev/null && ! command -v pyinstaller &> /dev/null; then
        echo "Error: PyInstaller no se instaló correctamente"
        exit 1
    fi
else
    echo "PyInstaller encontrado"
fi

echo "=== COMPILANDO ==="
mkdir -p dist
python3 -m PyInstaller \\
    --onefile \\
    --console \\
    --name="renombrador-universal-linux" \\
    --distpath="dist" \\
    --workpath="build/linux" \\
    --clean \\
    --noconfirm \\
    rename_folders.py

if [ -f "dist/renombrador-universal-linux" ]; then
    chmod +x "dist/renombrador-universal-linux"
    echo "OK: Linux compilado exitosamente"
    ls -la "dist/renombrador-universal-linux"
else
    echo "Error: Linux compilacion fallida"
    echo "Contenido de dist/:"
    ls -la dist/ || echo "Carpeta dist no existe"
    exit 1
fi
"""
      # Escribir script con finales de línea Unix
    script_path = "compile_linux.sh"
    with open(script_path, 'w', newline='\n') as f:
        f.write(wsl_script)
    
    try:
        # Ejecutar con output en tiempo real
        print("Ejecutando WSL...")
        result = subprocess.run(['wsl', 'bash', script_path], 
                              check=True, capture_output=True, text=True)
        
        # Mostrar output del proceso
        if result.stdout:
            print("Output WSL:")
            print(result.stdout)
        
        exe_path = "dist/renombrador-universal-linux"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"OK: Linux ejecutable creado - {exe_path} ({size_mb:.1f} MB)")
            return True
        else:
            print("Error: Linux ejecutable no generado")
            return False
    except subprocess.CalledProcessError as e:
        print("Error: Linux compilacion fallida")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False
    finally:
        if os.path.exists(script_path):
            os.unlink(script_path)

def create_package():
    """Crea documentación para el paquete"""
    readme_content = """# Renombrador Universal - Ejecutables Multiplataforma

## 🎯 Contenido Compilado
- renombrador-universal-windows.exe - Para Windows (6.7 MB)
- renombrador-universal-linux - Para Linux (6.8 MB)

## 🚀 Uso

### Windows:
1. Copia el .exe a la carpeta con carpetas a renombrar
2. Doble clic para ejecutar
3. Sigue las instrucciones en pantalla

### Linux:
1. Copia el ejecutable a la carpeta con carpetas a renombrar
2. Dar permisos: chmod +x renombrador-universal-linux
3. Ejecutar: ./renombrador-universal-linux

## ✨ Funciones
- Elimina espacios, acentos y caracteres especiales
- Convierte a minúsculas automáticamente  
- Vista previa antes de realizar cambios
- Solo renombra carpetas (preserva archivos)
- Interfaz moderna con colores y emojis

## 📋 Compilado con
- Python 3.11+ y PyInstaller
- Sistema dual Windows + WSL para máxima compatibilidad
- Generado automáticamente desde Windows usando WSL

## 🎮 Perfecto para
- Skins de Assetto Corsa
- Organización de archivos
- Normalización de nombres de directorios
"""
    
    with open("dist/README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)

def main():
    """Función principal"""
    print_header()
    
    if not check_requirements():
        return 1
    
    clean_previous_builds()
    
    # Compilar
    windows_ok = compile_windows()
    linux_ok = compile_linux()
    
    if windows_ok or linux_ok:
        create_package()
        
        print("\n" + "╔" + "═" * 58 + "╗")
        print("║" + " " * 17 + "COMPILACION COMPLETADA" + " " * 18 + "║")
        print("╚" + "═" * 58 + "╝")
        print("\nResultados:")
        
        if windows_ok:
            print("OK: Windows ejecutable creado - dist/renombrador-universal-windows.exe")
        else:
            print("Error: Windows no compilado")
            
        if linux_ok:
            print("OK: Linux ejecutable creado - dist/renombrador-universal-linux")
        else:
            print("Error: Linux no compilado")
        
        print(f"\nTodos los archivos estan en: dist/")
        print("Instrucciones incluidas en: dist/README.txt")
        
        return 0
    else:
        print("\nERROR: No se pudo compilar ningun ejecutable")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        if platform.system().lower() == "windows":
            input("\nPresiona Enter para cerrar...")
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nCompilacion cancelada")
        sys.exit(1)
    except Exception as e:
        print(f"\nError inesperado: {e}")
        sys.exit(1)
