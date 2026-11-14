#!/usr/bin/env python3
"""Repository integrity check for the public participant kit.

    python3 tests/check_repository.py        ->  REPOSITORY OK  (exit 0)

Checks the things that silently go wrong between edits: file counts, the
practice ledger's shape and figures, broken relative links, organizer-only
material that must never be here, and the submission client against a local
mock receiver. Standard library only. Makes no network connection beyond
127.0.0.1.
"""
import glob, json, os, re, subprocess, sys, threading, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)
fails = []


def check(ok, what):
    print(f"  [{'PASS' if ok else 'FAIL'}] {what}")
    if not ok:
        fails.append(what)


print("Required files:")
REQUIRED = ["README.md", "HUNTS.md", "WORKSHOP.md", "CONTRIBUTING.md", "SECURITY.md", "LICENSE",
            "LICENSE-CONTENT", "LICENSE-PROMPTS", "LICENSES.md", "probe.py", "setup.sh", "setup.ps1",
            "Dockerfile", ".dockerignore", ".gitignore", ".gitattributes", "vm/bootstrap-ubuntu.sh",
            "docs/VIRTUALBOX.md", "docs/LEDGER_REFERENCE.md", "docs/LEADERBOARD.md", "docs/PRE_EVENT_SETUP.md",
            "ctf/README.md", "detection/WORKSHOP_QUERIES.kql", "detection/DETECTION_RULE_TEMPLATE.md",
            "data/practice_ledger.jsonl", "leaderboard/submit.py", "leaderboard/living_atlas_board.kql",
            "tests/check_setup.py", "tests/mock_receiver.py", ".github/workflows/validate.yml"]
missing = [f for f in REQUIRED if not os.path.exists(f)]
check(not missing, "all required files present" + (f" — missing: {', '.join(missing)}" if missing else ""))

print("Organizer-only material (must be absent):")
FORBIDDEN = re.compile(r"(^|/)(receiver\.py|plant_flags\.py|plant\.py|challenges\.py|flags.*\.json|.*\.local\.json|"
                       r"\.env(\..*)?|corpus_v1v2_dce.*|.*Solution-Walkthrough.*|.*_ORGANIZER.*|CLAUDE\.md|"
                       r"LEADERBOARD_CONNECTION\.txt|dce_config\..*|.*_credentials.*|.*\.pem|.*\.key)$", re.I)
tree = [p for p in glob.glob("**/*", recursive=True) + glob.glob(".*", recursive=False)
        if os.path.isfile(p) and "/.git/" not in p and "__pycache__" not in p]
bad = [p for p in tree if FORBIDDEN.search(p)] + [p for p in ("proposals", "organizer") if os.path.exists(p)]
check(not bad, "no receiver, planting, flag, solution, credential or connection files"
      + (f" — found: {', '.join(bad)}" if bad else ""))

print("Samples:")
samples = sorted(glob.glob("samples/*.txt"))
check(len(samples) == 79, f"samples/ holds 79 prompt files ({len(samples)} found)")
empty = [s for s in samples if not open(s, encoding="utf-8").read().strip()]
check(not empty, "every sample is non-empty UTF-8")

print("Practice ledger:")
COLS = ["TimeGenerated", "UserPrincipal", "Language", "Variant", "RiskScore", "Patterns", "PromptPreview"]
rows = [json.loads(l) for l in open("data/practice_ledger.jsonl", encoding="utf-8") if l.strip()]
check(len(rows) == 22, f"22 rows ({len(rows)} found)")
check(all(list(r) == COLS for r in rows), "every row has exactly the seven columns, in order")
check({r["Variant"] for r in rows} <= {"V1", "V2"}, "Variant is only V1 or V2")
s = [r["RiskScore"] for r in rows]
bands = (sum(x >= 5 for x in s), sum(2 <= x < 5 for x in s), sum(x < 2 for x in s))
check(bands == (2, 12, 8), f"risk bands 2 blocked / 12 under the alert / 8 low ({'/'.join(map(str, bands))})")
cour = sorted((r["RiskScore"], r["Language"]) for r in rows if "courier" in r["Patterns"].split(","))
check([c[0] for c in cour] == [2.1, 2.2, 2.3, 2.4] and len({c[1] for c in cour}) == 4,
      "courier: four rows, scores 2.1 / 2.2 / 2.3 / 2.4, four languages")
check(not any("flag{" in json.dumps(r).lower() for r in rows), "no flag material in the ledger")

print("Probe:")
import probe  # noqa: E402
scored = [probe.analyze(open(f, encoding="utf-8").read())[0] for f in samples]
check(sum(x >= 5 for x in scored) == 0, f"probe.py samples/ -> 79 files scanned, 0 would be blocked")
out = subprocess.run([sys.executable, "probe.py", "samples/eth1_en.txt", "samples/eth1_es.txt"],
                     capture_output=True, text=True)
check(out.returncode == 0 and "2 files scanned" in out.stdout, "probe.py accepts several files in one command")

print("Links:")
dead = []
for md in glob.glob("**/*.md", recursive=True):
    text = open(md, encoding="utf-8").read()
    for m in re.finditer(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", text):
        u = m.group(1)
        if re.match(r"(https?|mailto):", u):
            continue
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(md), u))):
            dead.append(f"{md} -> {u}")
check(not dead, "every relative Markdown link resolves" + (f" — {'; '.join(dead)}" if dead else ""))

print("Query pack:")
kql = open("detection/WORKSHOP_QUERIES.kql", encoding="utf-8").read()
check("PolyglotPoisoning_CL\n| take 20" in kql and '| where UserPrincipal !endswith "@lb"' in kql,
      "contains the two participant access checks")

print("Submission client against the local mock receiver:")
from tests import mock_receiver  # noqa: E402
os.environ["MOCK_QUIET"] = "1"
srv = mock_receiver.serve(port=0)
port = srv.server_port
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{port}"
r = subprocess.run([sys.executable, "leaderboard/submit.py", "--url", url, "--handle", "check_one",
                    "--file", "samples/v1_ar_direct_translation.txt", "--lang", "ar", "--variant", "V1"],
                   capture_output=True, text=True)
check(r.returncode == 0 and "Score:" in r.stdout, "a valid prompt is accepted and scored server-side")
r = subprocess.run([sys.executable, "leaderboard/submit.py", "--url", url, "--handle", "check_two",
                    "--prompt", "here is flag{abc}"], capture_output=True, text=True)
check(r.returncode != 0 and "flag" in (r.stdout + r.stderr).lower(), "a flag{ submission is refused")


def post(body):
    req = urllib.request.Request(url + "/submit", data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


code, body = post({"handle": "check_three", "prompt": "x" * 4001})
check(code == 400, "a prompt over 4000 characters is rejected")
code, body = post({"handle": "a b!", "prompt": "hello"})
check(code == 400, "an invalid handle is rejected")
code, body = post({"handle": "check_four", "prompt": "hello", "score": 10, "patterns": "courier",
                   "UserPrincipal": "someone@deathlab.net"})
check(code == 200 and body["score"] == 0 and body["patterns"] == [""],
      "client-supplied score, stamps and identity are ignored")
code, body = post({"handle": "check_four", "prompt": "hello again"})
check(code == 429, "one submission per handle per 20 seconds")
row, _ = mock_receiver.classify("check_five", "hello", None, None)
check(row["UserPrincipal"] == "check_five@lb", "leaderboard identities end in @lb")
srv.shutdown()

print("-" * 60)
if fails:
    print(f"REPOSITORY CHECK FAILED — {len(fails)} item(s) above need fixing.")
    sys.exit(1)
print("REPOSITORY OK — the kit is consistent and complete.")
