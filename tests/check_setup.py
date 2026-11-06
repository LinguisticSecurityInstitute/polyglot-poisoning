#!/usr/bin/env python3
"""
check_setup.py — prove the workshop kit works, in under a second.

Run from anywhere:  python tests/check_setup.py
Exit code 0 = everything green. Stdlib only, no network, no models.

Checks:
  1. probe.py scores the three canonical samples exactly as documented
     (baseline 0 / V1 Arabic 2 / V2 register-shift 1).
  2. The DCE corpus (samples/corpus_v1v2_dce.json) parses and every row
     carries exactly the 7 ledger columns.
  3. data/practice_ledger.jsonl parses, same schema, and contains no
     CTF answer material (no "flag{" strings anywhere).
"""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DCE_KEYS = {"TimeGenerated", "UserPrincipal", "Language", "Variant",
            "RiskScore", "Patterns", "PromptPreview"}

failures = []


def check(label, ok, detail=""):
    mark = "PASS" if ok else "FAIL"
    print(f"  [{mark}] {label}" + (f" — {detail}" if detail else ""))
    if not ok:
        failures.append(label)


# --- 0. Load probe.py without installing anything -------------------------
probe_path = ROOT / "probe.py"
spec = importlib.util.spec_from_file_location("probe", probe_path)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

# --- 1. Canonical probe scores --------------------------------------------
print("Probe — canonical scores (the ladder's first rungs):")
CANONICAL = [
    ("samples/00_baseline_en.txt", 0),
    ("samples/v1_ar_direct_translation.txt", 2),
    ("samples/v1_en_register_shift.txt", 1),
]
for rel, expected in CANONICAL:
    path = ROOT / rel
    if not path.exists():
        check(rel, False, "file missing")
        continue
    score, hits = probe.analyze(path.read_text(encoding="utf-8"))
    check(rel, score == expected,
          f"score {score} (expected {expected}); signals: {', '.join(hits) or '-'}")

# Spanish V1 must stay LOW (Latin script is invisible to layer 1 by design)
score_es, _ = probe.analyze(
    (ROOT / "samples/v1_es_direct_translation.txt").read_text(encoding="utf-8"))
check("samples/v1_es_direct_translation.txt stays low (<=1)",
      score_es <= 1, f"score {score_es}")

# --- 2. DCE corpus shape ----------------------------------------------------
# Organizer-only. This is the corpus planted into the live table, so it is not
# in the public repository and its absence is NOT a failure. If you are a
# participant, you are not supposed to have this file.
corpus_path = ROOT / "samples/corpus_v1v2_dce.json"
if not corpus_path.exists():
    print("DCE corpus: not present — organizer-only, skipped (normal for participants)")
else:
    print("DCE corpus (samples/corpus_v1v2_dce.json):")
    try:
        data = json.loads(corpus_path.read_text(encoding="utf-8"))
        # top level is a wrapper: {schema, convention, count, corpus: [...]}
        entries = data["corpus"] if isinstance(data, dict) else data
        if isinstance(data, dict) and "count" in data:
            check("declared count matches entries",
                  data["count"] == len(entries),
                  f"count={data['count']}, entries={len(entries)}")
        rows = [e["row"] for e in entries]
        check("parses; corpus is a list of entries", isinstance(entries, list),
              f"{len(entries)} entries")
        check("every row has exactly the 7 ledger columns",
              all(set(r.keys()) == DCE_KEYS for r in rows))
        check("every entry carries row + meta",
              all(set(e.keys()) >= {"row", "meta"} for e in entries))
        previews_ok = all(len(r["PromptPreview"]) <= 200 for r in rows)
        check("every PromptPreview <= 200 chars", previews_ok)
    except Exception as exc:  # noqa: BLE001
        check("parses; corpus is a list of entries", False, str(exc))

# --- 3. Practice ledger shape + hygiene -------------------------------------
print("Practice ledger (data/practice_ledger.jsonl):")
pl_path = ROOT / "data/practice_ledger.jsonl"
if not pl_path.exists():
    check("exists", False, "file missing")
else:
    raw = pl_path.read_text(encoding="utf-8")
    try:
        lines = [json.loads(ln) for ln in raw.splitlines() if ln.strip()]
        check("parses as JSONL", True, f"{len(lines)} rows")
        check("every row has exactly the 7 ledger columns",
              all(set(r.keys()) == DCE_KEYS for r in lines))
    except Exception as exc:  # noqa: BLE001
        check("parses as JSONL", False, str(exc))
    check("contains no flag material", "flag{" not in raw.lower())

# --- verdict ----------------------------------------------------------------
print("-" * 60)
if failures:
    print(f"SETUP CHECK FAILED ({len(failures)} problem(s)). Fix and re-run.")
    sys.exit(1)
print("SETUP OK — everything this kit needs is green. You are ready.")
sys.exit(0)
