@echo off
title DAX Optimizer v1.1
echo.
echo ========================================
echo   DAX Optimizer v1.1
echo   Analizador de archivos PBIP
echo ========================================
echo.

cd /d "%~dp0"

REM Usar el venv de powerbi_analyzer (ya tiene todas las dependencias)
call "C:\Users\SE46958\1 - Claude - Proyecto viz\powerbi_analyzer\venv\Scripts\activate"

echo Iniciando aplicacion...
echo La aplicacion se abrira automaticamente en tu navegador
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

cd streamlit_app
streamlit run app.py

pause
