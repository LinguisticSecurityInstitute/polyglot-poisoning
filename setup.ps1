# setup.ps1 — Polyglot Poisoning workshop kit check (Windows)
# Stdlib Python only; nothing to install.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "== Polyglot Poisoning kit setup =="

$py = $null
foreach ($cand in @("python", "py", "python3")) {
    if (Get-Command $cand -ErrorAction SilentlyContinue) { $py = $cand; break }
}
if (-not $py) {
    Write-Host "ERROR: Python 3.8+ not found. Install from https://python.org"
    exit 1
}

& $py -c "import sys; print('Python: %d.%d' % sys.version_info[:2])"
& $py -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"
if ($LASTEXITCODE -ne 0) { Write-Host "ERROR: need Python 3.8+"; exit 1 }

Write-Host ""
Write-Host "== Running setup check =="
& $py tests/check_setup.py
if ($LASTEXITCODE -ne 0) { exit 1 }

Write-Host ""
Write-Host "== Probe demo on the sample pack =="
& $py probe.py samples/   # exit code 1 just means >=1 sample scores BLOCK-level

Write-Host ""
Write-Host "DONE. Next stops:"
Write-Host "  - docs/PRE_EVENT_SETUP.md   (if you are prepping for the event)"
Write-Host "  - HUNTS.md                  (five guided hunts)"
Write-Host "  - ctf/README.md             (the three challenges)"
