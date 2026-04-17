# Script PowerShell para iniciar Backend
# Uso: .\start_backend.ps1

Write-Host "`n╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🚀 Energy & Fuel Control Center - Backend FastAPI           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Cambiar directorio
Set-Location "c:\Users\USER\Documents\gasolina-app"

Write-Host "📍 Directorio: $(Get-Location)" -ForegroundColor Yellow
Write-Host "🔍 Verificando Python..." -ForegroundColor Yellow

# Verificar Python
if (!(python --version)) {
    Write-Host "❌ Python no está instalado" -ForegroundColor Red
    exit 1
}

$pythonVersion = python --version
Write-Host "✅ $pythonVersion" -ForegroundColor Green

Write-Host "`n⚙️  Verificando dependencias..." -ForegroundColor Yellow
python -c "import fastapi; print('✅ FastAPI instalado')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ FastAPI no está instalado" -ForegroundColor Red
    Write-Host "🔧 Instalando: pip install -r requirements.txt" -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host "`n🚀 Iniciando Backend en puerto 5000..." -ForegroundColor Cyan
Write-Host "📚 Documentación: http://localhost:5000/docs" -ForegroundColor Cyan
Write-Host "❌ Para detener: Presiona Ctrl+C" -ForegroundColor Yellow
Write-Host "`n" -ForegroundColor White

python backend/main.py
