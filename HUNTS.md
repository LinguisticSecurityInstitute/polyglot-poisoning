# HUNTS.md — five guided hunts

The complete exercise set for the workshop. Each hunt teaches one
move, gives you a query with **blanks to fill**, and works **twice**:
on the live `PolyglotPoisoning_CL` table (DEATHCon lab VPN) and
offline against [`data/practice_ledger.jsonl`](data/practice_ledger.jsonl)
(22 synthetic rows, same seven columns, no lab needed).

Self-check numbers are given for the practice data so you can verify
you did it right. Answers emerge from the data — no peeking at
previews until a hunt tells you to.

**The only schema you need:**

```
TimeGenerated · UserPrincipal · Language · Variant · RiskScore · Patterns · PromptPreview
```

Language codes, Variant codes, and doctrine: [docs/LEDGER_REFERENCE.md](docs/LEDGER_REFERENCE.md)

---

## HUNT 1 — Metadata anchors (one root, three dialects)

**The idea.** Arabic dialects differ in vocabulary and grammar, but
a trilateral root does not move. قفل (*lock*) appears identically in
MSA, Egyptian, and Tunisian. One string catches three "languages" —
and you never had to read a sentence.

**Spotter card (starter anchors — no fluency required):**

| Language | "lock" | "without" |
|---|---|---|
| Arabic (ALL dialects) | قفل | بلا / دون / من غير |
| Swahili | kufuli | bila |
| Spanish | cerradura | sin |
| French | serrure | sans |

Framing words (any language mix): `manual`, `novel`, `history`,
`step by step`, `1920`.

**Fill the blank and run:**

```kql
PolyglotPoisoning_CL
| where PromptPreview contains "<ANCHOR>"
| project TimeGenerated, UserPrincipal, Language, Variant, RiskScore, PromptPreview
```

Now tighten: keep only rows where the anchor fired **and** the
request was asked in a dialect (`Variant == "<CODE>"`).

**Offline equivalent:**

```bash
python -c "import sys,json; [print(r['Language'], r['RiskScore'], r['PromptPreview'][:50]) for r in map(json.loads, open('data/practice_ledger.jsonl', encoding='utf-8')) if 'قفل' in r['PromptPreview']]"
```

**Self-check (practice data):** قفل returns exactly **2 rows** —
`ar-MSA` (2.0) and `ar-EG` (4.0). One query, two dialects, zero
fluency. On the live table the same anchor spans all three Arabic
codes.

**You just learned:** roots beat phrases. A full translated phrase
catches one sentence once; a root catches a language family forever.

---

## HUNT 2 — Stacking & frequency (split before you count)

**The idea.** `Patterns` packs several stamps into one CSV string.
Count the column raw and you count *combinations* — a path that stops short, where
everything looks rare. Split first.

**Watch it stop short:**

```kql
PolyglotPoisoning_CL
| summarize rows = count() by Patterns
| sort by rows asc
```

**Now do it right — fill the blanks:**

```kql
PolyglotPoisoning_CL
| mv-expand stamp = <SPLIT>(Patterns, ",") to typeof(string)
| summarize rows = count() by <COLUMN>
| sort by rows asc
```

**Offline equivalent:**

```bash
python -c "import json; from collections import Counter; rows=[json.loads(l) for l in open('data/practice_ledger.jsonl', encoding='utf-8')]; print('combos:', len(Counter(r['Patterns'] for r in rows))); print(sorted(Counter(s for r in rows for s in r['Patterns'].split(',') if s).items(), key=lambda x: x[1]))"
```

**Self-check (practice data):** raw counting shows **12 unique
combos** (everything looks rare, so nothing stands out). After splitting:
`transliteration` 1, `code_switch` 3, `courier` 4, `register_shift` 5,
`framing` 7, `script_diversity` 11.

**The question that matters:** which stamps are rare *and
interesting*? Rare is not automatically forged — transliteration is
rare here and completely legitimate. A stamp that recurs a suspicious
number of times across different languages and different combos is
the one worth a second look.

**You just learned:** frequency analysis on a packed column is a
two-step move — expand, then count. Whoever skips step one sees
noise; whoever does both sees signatures.

---

## HUNT 3 — Threshold evasion (the prey lives under the wire)

**The idea.** The wire trips at 5. Anything scoring 4.9 sailed
straight through. Attackers calibrate against your threshold — so
hunt the band *under* it, not just the blocks above it.

**Fill the blanks:**

```kql
PolyglotPoisoning_CL
| where RiskScore >= <LOW> and RiskScore < <HIGH>
| summarize band_rows = count() by Language
| sort by band_rows desc
```

Then compare with what's above the wire:

```kql
PolyglotPoisoning_CL
| where RiskScore >= <WIRE>
| summarize blocked = count() by Language
```

**Offline equivalent:**

```bash
python -c "import json; from collections import Counter; rows=[json.loads(l) for l in open('data/practice_ledger.jsonl', encoding='utf-8')]; print('band 2-5:', dict(Counter(r['Language'] for r in rows if 2 <= r['RiskScore'] < 5))); print('over wire:', [(r['Language'], r['RiskScore']) for r in rows if r['RiskScore'] >= 5])"
```

**Self-check (practice data):** the 2–5 band holds **12 rows**
(ar-EG 4, hi-IN 2, ar-MSA / th-TH / bn-IN / ar-TN / es-ES / sw-KE 1
each); only **2 rows** sit at or above the wire (`ar-TN` 6.5,
`ar-EG` 8.0). The action is *under* the threshold — six times more
traffic, none of it blocked.

**You just learned:** a threshold is a line an attacker can see.
Your detection fires above it; your *hunting* lives below it.

---

## HUNT 4 — Correlation (when the prompt becomes a process)

**The idea.** A chat log row is a *request*. The damage, if any,
happens on an endpoint afterwards. Join the two on **who** and
**when** and you turn "someone asked something risky" into "this
machine ran this command minutes later."

*This hunt needs the live lab — the practice ledger has no endpoint
telemetry. Offline, read the query and answer the three questions
below.*

```kql
PolyglotPoisoning_CL
| where RiskScore >= <N>
| extend UserShort = tostring(split(UserPrincipal, "@")[0])
| join kind=inner (
    Event
    | where Source == "Microsoft-Windows-Sysmon" and EventID == 1
    | extend SysmonUser = tostring(split(User, "\\")[1])
    | project ExecTime=TimeGenerated, SysmonUser, Computer, CommandLine
  ) on $left.UserShort == $right.SysmonUser
| where abs(datetime_diff("second", ExecTime, TimeGenerated)) <= <SECONDS>
| project TimeGenerated, ExecTime, Computer, CommandLine
```

**Three questions to answer (any data, even on paper):**

1. What are the two join keys, and why can't you join the raw
   columns directly? *(Look at the formats: `user@domain` vs
   `MACHINE\user`.)*
2. What does the `<SECONDS>` window do — and what happens to your
   false-positive rate if you double it?
3. Encoded payload in `CommandLine`? KQL decodes in-query:
   `| extend decoded = base64_decode_tostring("<blob>")`.
   Why does the *workshop* insist you only ever decode — never
   execute — what you find?

**You just learned:** cross-source correlation is the difference
between a scary chat log and an incident timeline. WHO + WHEN is
usually enough — you rarely need to read WHAT was asked.

---

## HUNT 5 — Translate last (triage on labels, read the survivors)

**The idea.** Reading prompts does not scale and does not respect
your time. Metadata gets you from thousands of rows to a shortlist;
*then* you open a translator for the handful that survive.

**The drill (offline-friendly):** start from the 22 practice rows
(or `| take 500` live). Using **only metadata filters** — Language,
Variant, RiskScore, Patterns — get to **3 rows or fewer** *without
reading a single PromptPreview*. Then, and only then, translate the
survivors.

One path (fill the blanks):

```kql
PolyglotPoisoning_CL
| where Variant == "<CODE>"
| where RiskScore >= <N>
| project TimeGenerated, UserPrincipal, Language, RiskScore, Patterns, PromptPreview
```

**Offline equivalent:**

```bash
python -c "import json; rows=[json.loads(l) for l in open('data/practice_ledger.jsonl', encoding='utf-8')]; short=[r for r in rows if r['Variant']=='V2' and r['RiskScore']>=6]; [print(r['UserPrincipal'], r['Language'], r['RiskScore']) for r in short]"
```

**Self-check (practice data):** `Variant == "V2"` + `RiskScore >= 6`
shortlists exactly **2 rows** — `amber_saddle` (ar-TN, 6.5) and
`static_wren` (ar-EG, 8.0). Now translate those two previews. That's
the whole job: 22 rows → 2 reads.

**You just learned:** the language is the last thing you read, not
the first. Defenders who translate first drown; defenders who filter
first hunt.

---

## DONE ALL FIVE?

You have the complete moveset: anchors, frequency, thresholds,
correlation, triage. The [two CTF challenges](ctf/README.md) are
these five moves in trench coats. Start with Babel's Ledger.
