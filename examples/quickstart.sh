#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   ./examples/quickstart.sh example.com

domain="${1:-}"
if [[ -z "$domain" ]]; then
  echo "Usage: $0 <domain>"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "[*] Running recon_chain.py for $domain..."
python "$ROOT_DIR/src/recon_chain.py" "$domain"

echo "[*] Filtering for 200s..."
python "$ROOT_DIR/src/filter_200.py"

# Uncomment to auto-clean:
# echo "[*] Cleaning up..."
# python "$ROOT_DIR/src/cleanup_recon.py"

echo "[✔] Done. See: subs.txt, resolved.txt, live.txt, live-200.txt"