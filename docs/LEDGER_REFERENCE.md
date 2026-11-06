# LEDGER REFERENCE — Polyglot Poisoning (DEATHCon 2026)

Shared across all challenges in this category.
Workshop: **"Polyglot Poisoning: Hands-On Hunting for Linguistic Attacks in AI"** — Sahara Al-Madi, Linguistic Security Institute

> **Offline?** Every exercise in this reference also works against
> [`data/practice_ledger.jsonl`](../data/practice_ledger.jsonl) in this
> repo — same seven columns, no lab required.

---

## CONNECT

1. **Sentinel and Azure access is provided for this workshop.** Refer to the
   DEATHCon setup instructions for Sentinel, Azure and your `@deathlab.net`
   account — and do it before the session rather than during it.
2. Open the **deathcon2026-sentinel** workspace → Logs blade.
3. Every participant has Reader access. Queries are KQL.

Start here to see what you are working with:

```kql
PolyglotPoisoning_CL
| take 20
```

---

## THE INTAKE LEDGER

Every AI submission to this workspace is logged as one row in one
custom table: `PolyglotPoisoning_CL`.

| Column | Meaning |
|---|---|
| `TimeGenerated` | when it arrived |
| `UserPrincipal` | who sent it |
| `Language` | which tongue, at dialect level — or `mul` for a mix |
| `Variant` | how the request was shaped |
| `RiskScore` | scored risk — a real number; the wire trips at 5 |
| `Patterns` | detections it tripped (CSV string, several per row) |
| `PromptPreview` | first 200 characters of the request |

---

## LANGUAGE CODES

You do not need to speak any of these. You need to read the labels.

| Code | Language |
|---|---|
| `ar-MSA` | Modern Standard Arabic — the formal written register |
| `ar-EG` | Egyptian Arabic |
| `ar-TN` | Tunisian Arabic |
| `es-ES` | Spanish |
| `fr-FR` | French |
| `de-DE` | German |
| `it-IT` | Italian |
| `pt-PT` | Portuguese |
| `bn-IN` | Bengali |
| `hi-IN` | Hindi |
| `sw-KE` | Swahili |
| `th-TH` | Thai |
| `en-US` | English |

(Codes carry region suffixes in this ledger — filter on the full
code, e.g. `Language == "ar-TN"`, or use `startswith` for a family.)

**Submitting your own?** Any ISO code is accepted, with or without a region
suffix — and **`mul`** is the code for *multiple languages*. Use it whenever
you are mixing, matching or experimenting and no single code would be true.
It counts exactly the same as any other.


**Arabic is not one language in this ledger.** Egyptian and Tunisian
differ about as much as variations of Spanish — different words,
different grammar. A filter that handles one may not handle the
other at all, which is exactly why they are separate codes.

---

## VARIANT — HOW THE REQUEST WAS SHAPED

The column is coded:

| Code | Meaning |
|---|---|
| `V1` | asked plainly — a standard, direct request |
| `V2` | asked in a regional variety or dialect |

Only those two codes ever appear in `Variant`. Everything else about
how a request was shaped — the register it borrowed, the framing it
wore, the script it was typed in — is recorded in `Patterns`, not here.

Query the codes, not the glosses: `Variant == "V2"`, not `"dialect"`.

Language says **WHERE** a request was asked. Variant says **WHAT** was
done to it. They vary independently — any dialect can carry any
handling method — so they are two columns, not one.

That independence is the point. A crew that changes both at once is
not four incidents. It is one campaign wearing four coats.

Register and framing are not dialects: a request that is only
framed (an old manual, a museum label, a novel) stays V1, and the
shaping shows up in `Patterns`, not `Variant`.

---

## PATTERNS — WHAT THE DETECTIONS FLAGGED

Deliberately not listed here. Finding out what lives in this column,
and which values are rare, is part of the work.

One thing you do get for free: `Patterns` packs several values into a
single comma-separated string. Counting the column directly counts
combinations, not individual detections. **Split before you count.**

```kql
PolyglotPoisoning_CL
| mv-expand stamp = split(Patterns, ",") to typeof(string)
| summarize rows = count() by stamp
| sort by rows asc
```

---

## WHY THIS TABLE LOOKS LIKE THIS

At DETECTION time, the language is where the attack hides — a filter
trained on English stops recognizing a request the moment it arrives
in Tunisian. At HUNT time you cannot read every language, so you hunt
the labels the detection left behind instead.

That only works if the telemetry carries dialect and technique as
columns. Most telemetry does not. This ledger does, which is the
whole reason these hunts are possible.

---

## TAKE THIS BACK TO WORK

These seven columns are not CTF scaffolding. They are close to the
minimum an AI gateway should log if you ever want to hunt it: who
asked, in which dialect, shaped how, scored what, flagged by which
detections, and a preview you can pivot on.

Why it matters: in a 48-prompt pilot against two public safety
classifiers, both caught every English attempt and missed a third of
the same requests in Egyptian Arabic — while wrongly refusing 60% of
ordinary transliterated requests that English never had a problem
with. Attacks got through AND real users got blocked, at the same
time, in the same language. Neither is visible in telemetry that
logs only `blocked: true`.

- Linguistic Firewall — the open-source probe behind this workshop:
  **https://github.com/LinguisticSecurityInstitute/linguistic-firewall**
- Method, the Report Card format, and the full market scan:
  **almadisahara.com** · linguisticsecurityinstitute@gmail.com

If your logs cannot answer "which dialect is failing", these hunts
are ones you cannot run at home. That is the gap.

---

Flag format for this CTF: `flag{...}`
