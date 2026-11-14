#!/usr/bin/env python3
"""
submit.py — submit a PROMPT (never a model's response) to the
Polyglot Poisoning leaderboard. Stdlib only.

  python leaderboard/submit.py --url http://HOST:8730 --handle r3d_f0x \
      --lang ar-EG --variant V2 --file myprompt.txt

  python leaderboard/submit.py --url http://HOST:8730 --handle r3d_f0x \
      --file samples/v2_ar_egyptian_dialect.txt

--lang / --variant are optional self-declarations (default: guessed
from script, V1). The receiver scores with the same open-source
probe.py you run locally — so test locally first:

  python probe.py myprompt.txt

DISCLOSURE (you see this every time): submissions are prompt text
only — never model responses. Prompts are logged, scored, and shown
on the live leaderboard, and may inform LSI's published research and
detection rules — anonymized, always. Nothing is sent unless you
choose to submit.
"""
import argparse
import json
import re
import sys
import urllib.request

# Any ISO 639-1 (2-letter) or 639-3 (3-letter) code, with an optional region
# or variety subtag: es, sw, ar-EG, ar-MSA, sw-KE. Plus `mul` (ISO 639-3,
# "multiple languages") for a prompt that mixes, matches or experiments and
# would be a lie under any single code.
LANG = re.compile(r"^[a-z]{2,3}(-[A-Za-z]{2,8})?$")

print("Submitting prompt text only — never model responses. Prompts are")
print("logged, scored, and shown on the live leaderboard, and may inform")
print("LSI's published research and detection rules — anonymized, always.")
print("Nothing is sent unless you choose to submit. You are choosing now.")
print()

ap = argparse.ArgumentParser()
ap.add_argument("--url", required=True, help="receiver URL, e.g. http://HOST:8730")
ap.add_argument("--handle", required=True, help="your board handle (not your real name)")
src = ap.add_mutually_exclusive_group(required=True)
src.add_argument("--file", help="text file containing your prompt")
src.add_argument("--prompt", help="the prompt as a literal string")
ap.add_argument("--lang", default=None,
                help="any ISO code, with an optional region: es, hi, ar-EG, "
                     "sw-KE. Use mul if the prompt mixes languages")
ap.add_argument("--variant", default=None, choices=["V1", "V2"],
                help="V1 standard / V2 dialect (default V1)")
args = ap.parse_args()

prompt = open(args.file, encoding="utf-8").read() if args.file else args.prompt
if "flag{" in prompt.lower():
    sys.exit("That's a CTF flag, not a prompt. The leaderboard rejects these.")
if not (1 <= len(prompt) <= 4000):
    sys.exit("Prompt must be 1-4000 characters.")
if args.lang is not None and not LANG.match(args.lang):
    sys.exit(
        f"--lang {args.lang!r} is not a language code.\n"
        "Use an ISO code, with an optional region: es, hi, th, ar-EG, sw-KE.\n"
        "Mixing, matching or experimenting, so no single code is true?\n"
        "Use  --lang mul  — it means 'multiple languages' and it counts\n"
        "exactly the same. Do not skip submitting over a label.")

body = json.dumps({"handle": args.handle, "prompt": prompt,
                   "lang": args.lang, "variant": args.variant}).encode("utf-8")
req = urllib.request.Request(args.url.rstrip("/") + "/submit", data=body,
                             headers={"Content-Type": "application/json"},
                             method="POST")
try:
    with urllib.request.urlopen(req, timeout=20) as resp:
        out = json.loads(resp.read().decode("utf-8"))
except urllib.error.HTTPError as exc:
    out = json.loads(exc.read().decode("utf-8"))
    sys.exit(f"Rejected: {out.get('error', exc)}")
except Exception as exc:
    sys.exit(f"Could not reach the receiver: {exc}")

print(f"Score:    {out['score']:.0f} / 10")
print(f"Patterns: {', '.join(out['patterns']) or '-'}")
print("Badge:    Polyglot Poisoning Hunter EARNED" if out["badge"]
      else "Badge:    not yet — try something else and resubmit")
print(out.get("note", ""))
