# Script para levantar backend y frontend en paralelo
# Ejecutar: .\start.ps1

Write-Host "🚀 Iniciando Retail360 Chatbot..." -ForegroundColor Cyan
Write-Host ""

# Backend job
$backendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    Set-Location backend
    & "..\venv\Scripts\python.exe" -m uvicorn app:app --host 127.0.0.1 --port 8000
}

Write-Host "✅ Backend iniciado en http://127.0.0.1:8000" -ForegroundColor Green

# Frontend job
$frontendJob = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    Set-Location frontend
    npm run dev -- --port 5173 --host 127.0.0.1
}

Write-Host "✅ Frontend iniciado en http://127.0.0.1:5173" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Presiona Ctrl+C para detener ambos servicios" -ForegroundColor Yellow
Write-Host ""

# Esperar y mostrar salida de ambos jobs
try {
    while ($true) {
        Receive-Job -Job $backendJob
        Receive-Job -Job $frontendJob
        Start-Sleep -Milliseconds 100
        
        # Verificar si algún job falló
        if ($backendJob.State -eq "Failed" -or $frontendJob.State -eq "Failed") {
            Write-Host "❌ Error: uno de los servicios falló" -ForegroundColor Red
            break
        }
    }
} finally {
    # Limpiar jobs al salir
    Write-Host ""
    Write-Host "🛑 Deteniendo servicios..." -ForegroundColor Yellow
    Stop-Job -Job $backendJob, $frontendJob
    Remove-Job -Job $backendJob, $frontendJob
    Write-Host "✅ Servicios detenidos" -ForegroundColor Green
}

