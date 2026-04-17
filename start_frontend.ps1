# Script PowerShell para iniciar Frontend
# Uso: .\start_frontend.ps1

Write-Host "`n╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║  ⚡ Energy & Fuel Control Center - Frontend Next.js          ║" -ForegroundColor Magenta
Write-Host "╚════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Magenta

# Cambiar directorio
Set-Location "c:\Users\USER\Documents\gasolina-nextjs"

Write-Host "📍 Directorio: $(Get-Location)" -ForegroundColor Yellow
Write-Host "🔍 Verificando Node.js..." -ForegroundColor Yellow

# Verificar Node.js
if (!(node --version)) {
    Write-Host "❌ Node.js no está instalado" -ForegroundColor Red
    exit 1
}

$nodeVersion = node --version
Write-Host "✅ Node.js $nodeVersion" -ForegroundColor Green

Write-Host "`n⚙️  Verificando dependencias..." -ForegroundColor Yellow
if (!(Test-Path "node_modules")) {
    Write-Host "📦 Instalando npm packages..." -ForegroundColor Yellow
    npm install
}

Write-Host "`n🚀 Iniciando Frontend en puerto 3000..." -ForegroundColor Magenta
Write-Host "🌐 Abre: http://localhost:3000" -ForegroundColor Magenta
Write-Host "❌ Para detener: Presiona Ctrl+C" -ForegroundColor Yellow
Write-Host "`n" -ForegroundColor White

npm run dev
