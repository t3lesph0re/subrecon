#!/usr/bin/env bash
set -euo pipefail

# Minimal example: run subrecon against a single domain.
# Assumes subrecon is installed (pipx install . / pip install .).
#
# Usage: ./examples/quickstart.sh <domain>

domain="${1:-}"
if [[ -z "$domain" ]]; then
  echo "Usage: $0 <domain>"
  exit 1
fi

subrecon "$domain" -o "outputs/$domain" -v
