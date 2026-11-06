#!/usr/bin/env bash
# setup.sh — Polyglot Poisoning workshop kit check (macOS / Linux)
# Stdlib Python only; nothing to install.
set -e
cd "$(dirname "$0")"

echo "== Polyglot Poisoning kit setup =="

PY=""
for cand in python3 python py; do
  if command -v "$cand" >/dev/null 2>&1; then PY="$cand"; break; fi
done
if [ -z "$PY" ]; then
  echo "ERROR: Python 3.8+ not found. Install from https://python.org"
  exit 1
fi

VER=$("$PY" -c 'import sys; print("%d.%d" % sys.version_info[:2])')
echo "Python: $VER ($PY)"
"$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' \
  || { echo "ERROR: need Python 3.8+"; exit 1; }

echo
echo "== Running setup check =="
"$PY" tests/check_setup.py || exit 1

echo
echo "== Probe demo on the sample pack =="
"$PY" probe.py samples/ || true   # exit 1 just means >=1 sample scores BLOCK-level

echo
echo "DONE. Next stops:"
echo "  - docs/PRE_EVENT_SETUP.md   (if you are prepping for the event)"
echo "  - HUNTS.md                  (five guided hunts)"
echo "  - ctf/README.md             (the three challenges)"
