#!/usr/bin/env bash
set -euo pipefail

pushd "$(dirname "$0")/../apps/extension" >/dev/null
npm install
npm run build
echo "Extension build output available at $(pwd)/dist"
