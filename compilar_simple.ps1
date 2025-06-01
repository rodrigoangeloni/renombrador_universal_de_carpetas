# COMPILADOR SIMPLE DUAL: Windows + Linux
# Usa WSL para generar ambos ejecutables desde Windows
# Solo ejecuta: .\compilar_simple.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  COMPILADOR SIMPLE: WINDOWS + LINUX" -ForegroundColor Yellow  
Write-Host "========================================" -ForegroundColor Cyan
Write-Host

# Verificar Python
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python no encontrado" -ForegroundColor Red
    Write-Host "📦 Instala desde: https://python.org" -ForegroundColor Cyan
    pause
    exit 1
}

Write-Host "✅ Python encontrado" -ForegroundColor Green

# Verificar archivo fuente
if (-not (Test-Path "rename_folders.py")) {
    Write-Host "❌ No se encuentra rename_folders.py" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "✅ Archivo fuente encontrado" -ForegroundColor Green

# Ejecutar el compilador universal
Write-Host "🚀 Iniciando compilación..." -ForegroundColor Cyan
Write-Host

try {
    python compilar_universal.py
    
    Write-Host ""
    Write-Host "🎉 ¡Compilación completada!" -ForegroundColor Green
    Write-Host "📁 Revisa la carpeta dist/ para los ejecutables" -ForegroundColor Cyan
}
catch {
    Write-Host "❌ Error durante la compilación: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "Presiona cualquier tecla para cerrar..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
