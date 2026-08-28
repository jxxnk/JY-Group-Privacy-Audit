#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_root"

echo "[1/6] Checking required commands"
command -v git >/dev/null || { echo "Git is required." >&2; exit 1; }
command -v python3 >/dev/null || { echo "Python 3 is required." >&2; exit 1; }

echo "[2/6] Initializing Git repository"
if [[ ! -d .git ]]; then
  git init -b main
else
  echo "Git repository already exists. Skipping initialization."
fi

echo "[3/6] Creating local environment file"
if [[ ! -f .env ]]; then
  cp .env.example .env
else
  echo ".env already exists. Preserving it."
fi

echo "[4/6] Creating Python virtual environment"
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

echo "[5/6] Installing development dependencies"
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements-dev.txt

echo "[6/6] Running basic checks"
PYTHONPATH="$project_root" .venv/bin/python -c "from collector.src import __version__; print('collector version:', __version__)"
.venv/bin/python -m pytest -q
.venv/bin/ruff check collector
.venv/bin/ruff format --check collector

echo
echo "Basic setup is complete."
echo "See START_HERE_NEW_CHAT.md for the initial commit and GitHub remote commands."
