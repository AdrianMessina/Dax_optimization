@echo off
title DAX Optimizer
echo.
echo ========================================
echo    Iniciando DAX Optimizer
echo ========================================
echo.

cd /d "%~dp0"

REM Usar el venv de powerbi_analyzer
call "C:\Users\SE46958\1 - Claude - Proyecto viz\powerbi_analyzer\venv\Scripts\activate"

echo Iniciando aplicacion...
echo.
cd streamlit_app
streamlit run app.py

pause
