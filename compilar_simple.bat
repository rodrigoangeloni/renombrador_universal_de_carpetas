@echo off
REM Script simple para compilar ejecutables Windows + Linux
REM Solo ejecuta este archivo y listo

title Compilador Simple: Windows + Linux

echo ========================================
echo   COMPILADOR SIMPLE: WINDOWS + LINUX
echo ========================================
echo.

echo 🚀 Iniciando compilación...
echo.

REM Verificar Python
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Python no encontrado
    echo 📦 Instala desde: https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado

REM Verificar archivo fuente
if not exist "rename_folders.py" (
    echo ❌ No se encuentra rename_folders.py
    pause
    exit /b 1
)

echo ✅ Archivo fuente encontrado
echo.

REM Ejecutar compilador
python compilar_universal.py

echo.
echo 🎉 ¡Proceso completado!
echo 📁 Revisa la carpeta dist/ para los ejecutables
echo.
pause
