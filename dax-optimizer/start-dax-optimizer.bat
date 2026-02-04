@echo off
title DAX Optimizer
echo.
echo ========================================
echo    Iniciando DAX Optimizer
echo ========================================
echo.
echo El navegador se abrira automaticamente
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

cd /d "%~dp0"
npm run dev

pause
