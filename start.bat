@echo off
REM Script para levantar backend y frontend en paralelo
REM Ejecutar: start.bat

echo.
echo ========================================
echo   Retail360 Chatbot - Inicio Rapido
echo ========================================
echo.

REM Levantar backend en una nueva ventana
echo [1/2] Iniciando backend...
start "Backend - Uvicorn" cmd /k "cd backend && ..\venv\Scripts\python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000"

REM Esperar 2 segundos
timeout /t 2 /nobreak >nul

REM Levantar frontend en una nueva ventana
echo [2/2] Iniciando frontend...
start "Frontend - Vite" cmd /k "cd frontend && npm run dev -- --port 5173 --host 127.0.0.1"

echo.
echo ========================================
echo   Servicios iniciados correctamente
echo ========================================
echo.
echo   Backend:  http://127.0.0.1:8000
echo   Frontend: http://127.0.0.1:5173
echo.
echo Cierra las ventanas de terminal para detener los servicios.
echo.
pause
