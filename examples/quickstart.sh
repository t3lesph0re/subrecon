#!/usr/bin/env bash
set -euo pipefail

# Usage: ./examples/quickstart.sh <domain>

domain="${1:-}"
if [[ -z "$domain" ]]; then
  echo "Usage: $0 <domain>"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ROOT_DIR/src/recon_chain.py" "$domain" --outdir "outputs/$domain"
python3 "$ROOT_DIR/src/filter_200.py" -i "outputs/$domain/live.txt" -o "outputs/$domain/live-200.txt"

echo ""
echo "[✓] Results in outputs/$domain/"
