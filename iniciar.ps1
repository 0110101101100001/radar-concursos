# Radar Concursos - Apenas terminal (sem n8n, sem Docker)
$ErrorActionPreference = "Continue"
chcp 65001 | Out-Null

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  RADAR CONCURSOS - APENAS TERMINAL" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

$PastaProjeto = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $PastaProjeto

# Verificar se o venv existe
$VenvPython = Join-Path $PastaProjeto "venv\Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    Write-Host "ERRO: venv nao encontrado em venv\Scripts\python.exe" -ForegroundColor Red
    Write-Host "Rode primeiro: python -m venv venv" -ForegroundColor Red
    Write-Host "               venv\Scripts\pip install -r requirements.txt" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "Escolha uma opcao:"
Write-Host " [1] Rodar o scraper uma vez agora"
Write-Host " [2] Rodar o scraper em loop (varredura automatica)"
Write-Host " [3] Sair"
$opcao = Read-Host "Opcao"

if ($opcao -eq "1") {
    Write-Host "`nExecutando varredura unica..." -ForegroundColor Cyan
    & $VenvPython scraper.py
    Write-Host "`nFim da varredura." -ForegroundColor Green
} elseif ($opcao -eq "2") {
    $intervalo = Read-Host "Intervalo entre varreduras em segundos (padrao 1800 = 30 min)"
    if ([string]::IsNullOrWhiteSpace($intervalo)) { $intervalo = 1800 }
    Write-Host "`nExecutando em loop a cada $intervalo segundos. Pressione Ctrl+C para parar.`n" -ForegroundColor Cyan
    & $VenvPython scraper.py --loop --intervalo $intervalo
    Write-Host "`nLoop encerrado." -ForegroundColor Green
} else {
    Write-Host "Saindo." -ForegroundColor Gray
}

Write-Host ""
pause
