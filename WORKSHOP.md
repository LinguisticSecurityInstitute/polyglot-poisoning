# WORKSHOP — how the 90-minute live session runs

## Polyglot Poisoning: Hands-On Hunting for Linguistic Attacks in AI

**Format:** hands-on keyboard session. Bring a laptop. Everything
works offline; the DEATHCon lab adds the live telemetry and the CTF.
**You need zero fluency in any language.** Every exercise is won by
reading metadata, not words.

**Before you arrive (5–10 min):** [docs/PRE_EVENT_SETUP.md](docs/PRE_EVENT_SETUP.md)
— check Python, clone this repo, run `python tests/check_setup.py`.

---

## THE RUN OF SHOW (90 minutes)

| Time | Block | What you do |
|---|---|---|
| 0:00–0:10 | **Setup + the gap** | Kit check (`tests/check_setup.py`). One story: the same request, blocked in English, answered in Tunisian. |
| 0:10–0:25 | **Meet the probe** | Run `python probe.py samples/`. Watch the baseline score 0 and single-dimension attacks score 1–2 — *under* the wire. Why that's a feature: stacked signals are what the threshold exists for. |
| 0:25–0:50 | **Ledger hunts** | First three hunts from [HUNTS.md](HUNTS.md): metadata anchors (one root, three dialects), split-before-count, the under-the-wire band. Live table if you're on the lab VPN; `data/practice_ledger.jsonl` if you're not. |
| 0:50–1:10 | **Build a rule + leaderboard** | Fill [detection/DETECTION_RULE_TEMPLATE.md](detection/DETECTION_RULE_TEMPLATE.md) for one language on the spotter card. Optional: submit a prompt (never a model response) to the live leaderboard — [docs/LEADERBOARD.md](docs/LEADERBOARD.md); disclosure below. |
| 1:10–1:25 | **CTF on-ramp** | Open **Babel's Ledger** (the easy challenge) together: the ledger reference, the metadata triple, the first filter. You leave knowing exactly how to finish all three. |
| 1:25–1:30 | **Close** | The take-it-to-work slide: the seven columns your own AI gateway should log. Badge announcements. |

**Async?** The recorded lecture (~1 hour) covers the same ground as
the first four blocks; do the hunts at your own pace and bring your
scores to the Discord.

---

## WHAT YOU WALK AWAY WITH

1. **Working muscle memory** for hunting AI telemetry you cannot
   read — anchors, frequencies, thresholds, joins.
2. **A detection rule you wrote** and can explain in one sentence.
3. **The ledger reference** — the seven-column minimum to demand
   from any AI gateway you defend.
4. **A CTF on-ramp** — two challenges, solvable at your own pace
   during the event window.
5. Optionally, the **Polyglot Poisoning Hunter badge** (probe
   score ≥5 on a submitted prompt).

## THE EXERCISE LOOP (used in every block)

```
predict  →  run  →  record  →  modify ONE thing  →  run again
```

`samples/WORKSHEET.md` has the copy-and-fill block for each sample.
The modification step is where the learning happens: change the
language OR the register, never both, and watch the score move.

---

## LEADERBOARD DISCLOSURE (read once, it's short)

Submissions are prompt text only — never model responses. Prompts
are logged, scored, and shown on the live leaderboard, and may
inform LSI's published research and detection rules — anonymized,
always. Nothing is sent unless you choose to submit. Share scores
and patterns — never harmful outputs.

## HOUSE RULES

- Handles, not real names — on the leaderboard and the CTF board.
- Prompts, not outputs. Never paste a model's harmful completion
  into any tool, chat, or screenshot.
- Gray-zone material stays in the room's context: this is a
  defensive hunting workshop.
