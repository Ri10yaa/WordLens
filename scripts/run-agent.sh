#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: scripts/run-agent.sh 'Explain the meaning of bank'"
  exit 1
fi

PROMPT="$1"

pushd "$(dirname "$0")/../apps/agent" >/dev/null
if [ ! -d .venv ]; then
  python -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt >/dev/null
python -m agent.cli "$PROMPT"
