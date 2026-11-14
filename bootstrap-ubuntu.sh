#!/usr/bin/env bash
# Prepare an Ubuntu VM (for example the VirtualBox VM "sahaa_lsi-SANDIEGO")
# to run the Polyglot Poisoning participant kit. Run it INSIDE the VM, from
# the repository root:
#
#     bash vm/bootstrap-ubuntu.sh
#
# It installs only what the kit needs (Python 3 and git, if missing), then
# runs the kit's own checks. It does not install Docker, open ports, or touch
# anything outside this folder. Safe to run more than once.
set -euo pipefail

cd "$(dirname "$0")/.."
echo "== Polyglot Poisoning · Ubuntu bootstrap =="

if [ -r /etc/os-release ]; then . /etc/os-release; echo "OS: ${PRETTY_NAME:-unknown}"; fi
if [ "${ID:-}" != "ubuntu" ]; then
  echo "Note: this script is written for Ubuntu; continuing, but package names may differ."
fi

need=()
command -v python3 >/dev/null 2>&1 || need+=(python3)
command -v git     >/dev/null 2>&1 || need+=(git)
if [ ${#need[@]} -gt 0 ]; then
  echo "Installing: ${need[*]}  (sudo will ask for your password)"
  sudo apt-get update -y
  sudo apt-get install -y "${need[@]}"
else
  echo "python3 and git already installed."
fi

python3 - <<'PY'
import sys
if sys.version_info < (3, 8):
    sys.exit(f"Python 3.8+ is required; this VM has {sys.version.split()[0]}")
print("Python", sys.version.split()[0], "OK")
PY

# Organizer-only material must never be in a participant VM.
for f in receiver.py leaderboard/receiver.py plant_flags.py .env; do
  if [ -e "$f" ]; then echo "STOP: $f is organizer-only and must not be in this VM."; exit 1; fi
done

echo
python3 tests/check_setup.py
echo
python3 tests/check_repository.py
echo
python3 probe.py samples/ | tail -1
echo
echo "Bootstrap complete. Next: open the Azure portal in this VM's browser with"
echo "your DEATHLab account — see README.md, section 'Sentinel access'."
