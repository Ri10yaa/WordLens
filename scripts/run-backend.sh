#!/usr/bin/env bash
set -euo pipefail

pushd "$(dirname "$0")/../apps/backend" >/dev/null
if [ ! -d .venv ]; then
  python -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt >/dev/null
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
