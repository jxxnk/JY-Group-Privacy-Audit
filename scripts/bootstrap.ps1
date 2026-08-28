$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "[1/6] Checking required commands"
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is not installed or is not available in PATH."
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python is not installed or is not available in PATH."
}

Write-Host "[2/6] Initializing Git repository"
if (-not (Test-Path ".git")) {
    git init -b main
} else {
    Write-Host "Git repository already exists. Skipping initialization."
}

Write-Host "[3/6] Creating local environment file"
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
} else {
    Write-Host ".env already exists. Preserving it."
}

Write-Host "[4/6] Creating Python virtual environment"
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

Write-Host "[5/6] Installing development dependencies"
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements-dev.txt

Write-Host "[6/6] Running basic checks"
$env:PYTHONPATH = $ProjectRoot
& ".\.venv\Scripts\python.exe" -c "from collector.src import __version__; print('collector version:', __version__)"
& ".\.venv\Scripts\python.exe" -m pytest -q
& ".\.venv\Scripts\ruff.exe" check collector
& ".\.venv\Scripts\ruff.exe" format --check collector

Write-Host ""
Write-Host "Basic setup is complete."
Write-Host "Review git status, then create the initial commit and connect the GitHub remote."
Write-Host "See START_HERE_NEW_CHAT.md for the exact next commands."
