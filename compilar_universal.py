#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compilador Universal Simple - Windows + Linux
Autor: rodrigoangeloni
Fecha: 2025-06-01

INSTRUCCIONES:
1. En Windows: python compilar_universal.py
2. Se compilará para Windows automáticamente (terminal + GUI)
3. Si tienes WSL, también compilará para Linux (terminal + GUI)
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
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 15 + "COMPILADOR UNIVERSAL v2.0" + " " * 27 + "║")
    print("║" + " " * 8 + "Renombrador de Carpetas - Terminal + GUI" + " " * 19 + "║")
    print("║" + " " * 13 + "Windows + Linux (WSL)" + " " * 33 + "║")
    print("╚" + "═" * 68 + "╝")
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
    """Compila para Windows - Terminal y GUI"""
    print("\nCompilando para Windows...")
    
    os.makedirs("dist", exist_ok=True)
    
    # Compilar versión terminal
    cmd_terminal = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console", 
        "--name=renombrador-terminal-windows",
        "--distpath=dist",
        "--workpath=build/windows-terminal",
        "--clean",
        "--noconfirm",
        "rename_folders.py"
    ]
    
    # Compilar versión GUI
    cmd_gui = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",  # Sin consola para GUI
        "--name=renombrador-gui-windows",
        "--distpath=dist",
        "--workpath=build/windows-gui",
        "--clean",
        "--noconfirm",
        "rename_folders_gui.py"
    ]
    
    success_count = 0
    
    try:
        # Compilar terminal
        print("  → Compilando versión terminal...")
        subprocess.run(cmd_terminal, check=True, capture_output=True, text=True)
        exe_path = "dist/renombrador-terminal-windows.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"    ✅ Terminal: {exe_path} ({size_mb:.1f} MB)")
            success_count += 1
        
        # Compilar GUI
        print("  → Compilando versión GUI...")
        subprocess.run(cmd_gui, check=True, capture_output=True, text=True)
        exe_path = "dist/renombrador-gui-windows.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"    ✅ GUI: {exe_path} ({size_mb:.1f} MB)")
            success_count += 1
            
    except subprocess.CalledProcessError as e:
        print(f"    ❌ Error en compilación Windows")
        return False
    
    if success_count == 2:
        print(f"OK: Windows compilación completa ({success_count}/2 versiones)")
        return True
    else:
        print(f"Parcial: Windows compilación ({success_count}/2 versiones)")
        return success_count > 0

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

echo "=== COMPILANDO VERSIONES ==="
mkdir -p dist

echo "Compilando versión terminal..."
python3 -m PyInstaller \\
    --onefile \\
    --console \\
    --name="renombrador-terminal-linux" \\
    --distpath="dist" \\
    --workpath="build/linux-terminal" \\
    --clean \\
    --noconfirm \\
    rename_folders.py

echo "Compilando versión GUI..."
python3 -m PyInstaller \\
    --onefile \\
    --windowed \\
    --name="renombrador-gui-linux" \\
    --distpath="dist" \\
    --workpath="build/linux-gui" \\
    --clean \\
    --noconfirm \\
    rename_folders_gui.py

if [ -f "dist/renombrador-universal-linux" ]; then
    chmod +x "dist/renombrador-universal-linux"
    echo "OK: Linux compilado exitosamente"
    ls -la "dist/renombrador-universal-linux"
else
    echo "Error: Linux compilacion fallida"
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
"""
      # Escribir script con finales de línea Unix y codificación UTF-8
    script_path = "compile_linux.sh"
    with open(script_path, 'w', newline='\n', encoding='utf-8') as f:
        f.write(wsl_script)
    
    success_count = 0
    
    try:
        # Ejecutar con output en tiempo real
        print("Ejecutando WSL...")
        result = subprocess.run(['wsl', 'bash', script_path], 
                              check=True, capture_output=True, text=True, encoding='utf-8')
        
        # Mostrar output del proceso
        if result.stdout:
            print("Output WSL:")
            print(result.stdout)
        
        # Verificar archivos generados
        terminal_path = "dist/renombrador-terminal-linux"
        gui_path = "dist/renombrador-gui-linux"
        
        if os.path.exists(terminal_path):
            size_mb = os.path.getsize(terminal_path) / (1024 * 1024)
            print(f"    ✅ Terminal: {terminal_path} ({size_mb:.1f} MB)")
            success_count += 1
            
        if os.path.exists(gui_path):
            size_mb = os.path.getsize(gui_path) / (1024 * 1024)
            print(f"    ✅ GUI: {gui_path} ({size_mb:.1f} MB)")
            success_count += 1
        
        if success_count == 2:
            print(f"OK: Linux compilación completa ({success_count}/2 versiones)")
            return True
        else:
            print(f"Parcial: Linux compilación ({success_count}/2 versiones)")
            return success_count > 0
            
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
    readme_content = """# Renombrador Universal v2.0 - Ejecutables Multiplataforma

## 🎯 Contenido Compilado

### Windows:
- renombrador-terminal-windows.exe - Versión terminal para Windows
- renombrador-gui-windows.exe - Versión gráfica para Windows

### Linux:
- renombrador-terminal-linux - Versión terminal para Linux
- renombrador-gui-linux - Versión gráfica para Linux

## 🚀 Uso

### Windows Terminal:
1. Copia renombrador-terminal-windows.exe a la carpeta con carpetas a renombrar
2. Doble clic para ejecutar
3. Sigue las instrucciones en pantalla

### Windows GUI:
1. Copia renombrador-gui-windows.exe donde quieras
2. Doble clic para ejecutar
3. Interfaz gráfica moderna con todas las opciones

### Linux Terminal:
1. Copia el ejecutable a la carpeta con carpetas a renombrar
2. Dar permisos: chmod +x renombrador-terminal-linux
3. Ejecutar: ./renombrador-terminal-linux

### Linux GUI:
1. Dar permisos: chmod +x renombrador-gui-linux
2. Ejecutar: ./renombrador-gui-linux
3. Requiere X11/Wayland para la interfaz gráfica

## ✨ Funciones v2.0
- ✅ Interfaz terminal (v1) + Interfaz gráfica moderna (v2)
- ✅ Elimina espacios, acentos y caracteres especiales
- ✅ Opciones configurables (minúsculas, puntos, números)
- ✅ Vista previa antes de realizar cambios
- ✅ Solo renombra carpetas (preserva archivos)
- ✅ Detección de conflictos
- ✅ Log detallado de resultados
- ✅ Ejemplos interactivos

## 📋 Compilado con
- Python 3.11+ y PyInstaller
- tkinter para la interfaz gráfica
- Sistema dual Windows + WSL para máxima compatibilidad
- Generado automáticamente desde Windows usando WSL

## 🎮 Perfecto para
- Skins de Assetto Corsa
- Organización de archivos multimedia
- Normalización de nombres de directorios
- Proyectos web (nombres compatibles con servidores)
- Cualquier carpeta que necesite nombres limpios
"""
    
    with open("dist/README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)

def main():
    """Función principal"""
    print_header()
    
    if not check_requirements():
        return 1
    
    clean_previous_builds()
    
    # Compilar    windows_ok = compile_windows()
    linux_ok = compile_linux()
    
    if windows_ok or linux_ok:
        create_package()
        
        print("\n" + "╔" + "═" * 68 + "╗")
        print("║" + " " * 17 + "COMPILACION v2.0 COMPLETADA" + " " * 23 + "║")
        print("╚" + "═" * 68 + "╝")
        print("\n🎯 Resultados de Compilación:")
        
        if windows_ok:
            print("  ✅ Windows:")
            if os.path.exists("dist/renombrador-terminal-windows.exe"):
                size = os.path.getsize("dist/renombrador-terminal-windows.exe") / (1024 * 1024)
                print(f"     • Terminal: renombrador-terminal-windows.exe ({size:.1f} MB)")
            if os.path.exists("dist/renombrador-gui-windows.exe"):
                size = os.path.getsize("dist/renombrador-gui-windows.exe") / (1024 * 1024)
                print(f"     • GUI: renombrador-gui-windows.exe ({size:.1f} MB)")
        else:
            print("  ❌ Windows: Compilación fallida")
            
        if linux_ok:
            print("  ✅ Linux:")
            if os.path.exists("dist/renombrador-terminal-linux"):
                size = os.path.getsize("dist/renombrador-terminal-linux") / (1024 * 1024)
                print(f"     • Terminal: renombrador-terminal-linux ({size:.1f} MB)")
            if os.path.exists("dist/renombrador-gui-linux"):
                size = os.path.getsize("dist/renombrador-gui-linux") / (1024 * 1024)
                print(f"     • GUI: renombrador-gui-linux ({size:.1f} MB)")
        else:
            print("  ❌ Linux: Compilación fallida (verifica WSL)")
            
        # Contar archivos generados
        exe_files = [f for f in os.listdir("dist") if f.startswith("renombrador-") and not f.endswith(".txt")]
        print(f"\n📦 Total: {len(exe_files)} ejecutables generados en dist/")
        print("📖 Ver dist/README.txt para instrucciones completas")
        
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
