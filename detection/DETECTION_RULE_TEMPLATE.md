# DETECTION RULE TEMPLATE — turn a pattern into a rule
## Polyglot Poisoning workshop · fill the blanks, keep the rule

THE ANATOMY (every detection rule here has three parts):
  ANCHOR    — a root or keyword that survives translation.
              Dialects change the cells around it; the anchor stays.
  CONTEXT   — a framing/register signal that kills false positives
              (the museum label is WHY this part exists).
  THRESHOLD — how much signal before a human looks.

SPOTTER CARD (starter anchors — no fluency required):
  Arabic (ALL dialects): قفل = "lock" · مفتاح = "key"
  Swahili:  kufuli = "lock" · bila = "without"
  Spanish:  cerradura = "lock" · sin = "without"
  French:   serrure = "lock" · sans = "without"
  Framing words (any language mix): manual, novel, history,
  step by step, 1920

────────────────────────────────────────
PART 1 — KQL TEMPLATE (for the DEATHCon Sentinel workspace)
────────────────────────────────────────
// Fill the blanks:
PolyglotPoisoning_CL
| where PromptPreview contains "<ANCHOR>"
// | where Language == "<TAG>"        // optional: tighten
// | where RiskScore > <N>            // optional: tighten
| project TimeGenerated, UserPrincipal, Language, RiskScore, PromptPreview

// Worked example — one root catches EVERY Arabic dialect:
PolyglotPoisoning_CL
| where PromptPreview contains "قفل"
| project TimeGenerated, UserPrincipal, Language, RiskScore, PromptPreview

// With context (anchor AND a framing signal, either language):
PolyglotPoisoning_CL
| where PromptPreview contains "قفل"
| where PromptPreview has_any ("manual", "novel", "step")
| project TimeGenerated, UserPrincipal, Language, RiskScore, PromptPreview

────────────────────────────────────────
PART 2 — PYTHON TEMPLATE (scan any log/CSV/JSONL of prompts)
────────────────────────────────────────
import sys

ANCHORS = ["قفل", "مفتاح"]            # <- your roots
CONTEXT = ["manual", "novel", "step"] # <- framing signals
NEED_A, NEED_C = 1, 1                 # <- thresholds

for line in sys.stdin:
    a = sum(1 for x in ANCHORS if x in line)
    c = sum(1 for x in CONTEXT if x.lower() in line.lower())
    if a >= NEED_A and c >= NEED_C:
        print("REVIEW:", line.strip()[:120])

# Run it:  python my_rule.py < prompts.jsonl
# Exercise (Active Time 2): pick a language from the spotter card,
# fill ANCHORS, tune the thresholds, run it on the samples folder:
#     type samples\v2_ar_egyptian_dialect.txt | python my_rule.py

────────────────────────────────────────
PART 3 — BONUS: THE CORRELATION SKELETON (feeds the hard CTF)
────────────────────────────────────────
// When a prompt becomes a process: join the AI log to endpoint
// telemetry on WHO + WHEN. Fill the blanks:
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
// Encoded payload? KQL decodes in-query:
// | extend decoded = base64_decode_tostring("<blob>")

────────────────────────────────────────
TUNING NOTES
────────────────────────────────────────
- Anchors alone = false positives. The museum-label sample contains
  "lock" and "open" and is completely benign — that's why CONTEXT
  exists. Anchor + context beats anchor alone, every time.
- Roots beat phrases: "قفل" catches MSA, Egyptian AND Tunisian;
  a full phrase catches one sentence once.
- A rule you can explain in one sentence is a rule you can defend
  in a report. Keep it that small.
