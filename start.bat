@echo off
chcp 65001 >nul
echo Iniciando o Radar Concursos...
powershell -ExecutionPolicy Bypass -File "%~dp0iniciar.ps1"
pause
