#!/usr/bin/env python3
"""
probe.py — Linguistic Firewall (community edition, workshop build)
Scores text files for polyglot-poisoning signals. Stdlib only.

Usage:  python probe.py samples/          (scan a folder)
        python probe.py one_file.txt      (scan one file)
Exit code: 1 if any file scores >= 5 (BLOCK), else 0
"""
import os, re, sys, unicodedata

ARABIZI_DIGITS = "23579"
FRAMING = ["for a chapter", "history of", "in my novel", "my novel",
           "museum", "exhibit", "training manual", "case study",
           "for a study", "academic", "hypothetical", "fiction",
           "children's book", "simple words", "novel", "for a history"]

def script_family(ch):
    try:    name = unicodedata.name(ch)
    except ValueError: return None
    for fam in ("LATIN","ARABIC","CYRILLIC","GREEK","CJK","HIRAGANA",
                "KATAKANA","HANGUL","DEVANAGARI","BENGALI","THAI",
                "HEBREW","ARMENIAN","GEORGIAN","ETHIOPIC","TAMIL"):
        if name.startswith(fam): return fam
    return None

def analyze(text):
    fams = {script_family(c) for c in text if c.isalpha()} - {None}
    hits, score = [], 0
    if fams - {"LATIN"}:                      # L1 script diversity
        hits.append("L1 script_diversity(+2)"); score += 2
    if len(fams) >= 2:                        # L2 code-switching
        hits.append("L2 code_switch(+2)"); score += 2
    az = (r"(?<![0-9])(?:[A-Za-z][" + ARABIZI_DIGITS + r"](?![0-9])"
          r"|[" + ARABIZI_DIGITS + r"](?![0-9]|nd|st|rd|th)[A-Za-z])")
    if re.search(az, text):                   # L3 arabizi (digits-as-letters,
        hits.append("L3 arabizi(+2)"); score += 2   # not numbers/ordinals)
    low = text.lower()
    if any(p in low for p in FRAMING):        # L4 Clever Hans framing
        hits.append("L4 framing(+1)"); score += 1
    return min(score, 10), hits

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "samples"
    files = ([target] if os.path.isfile(target)
             else sorted(os.path.join(target, f) for f in os.listdir(target)
                         if f.endswith(".txt")))
    print(f"{'file':38s} {'score':>5s}  verdict  signals")
    print("-" * 78)
    blocked = 0
    for path in files:
        text = open(path, encoding="utf-8").read()
        score, hits = analyze(text)
        verdict = "BLOCK" if score >= 5 else ("flag" if score >= 2 else "pass")
        blocked += verdict == "BLOCK"
        print(f"{os.path.basename(path):38s} {score:>5d}  {verdict:7s} {', '.join(hits) or '-'}")
    print("-" * 78)
    print(f"{len(files)} files scanned, {blocked} would be blocked (score >= 5)")
    sys.exit(1 if blocked else 0)

if __name__ == "__main__":
    main()
