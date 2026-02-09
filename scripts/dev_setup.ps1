# Development setup script for hivi_speaker
# Installs hivico from sibling directory ../hivico
# Run from project root: .\scripts\dev_setup.ps1

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$HivicoPath = Join-Path (Split-Path -Parent $ProjectRoot) "hivico"

if (-not (Test-Path $HivicoPath)) {
    Write-Error "hivico not found at: $HivicoPath. Clone hivico as sibling: projects/hivico"
    exit 1
}

Write-Host "Installing hivico from: $HivicoPath"
pip install -e $HivicoPath

Write-Host "Verifying..."
python -c "from hivico import HivicoClient; print('hivico OK')"
