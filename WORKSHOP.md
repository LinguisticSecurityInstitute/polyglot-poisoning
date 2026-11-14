# WORKSHOP — how the session runs

## Polyglot Poisoning: Hands-On Hunting for Linguistic Attacks in AI

**Format:** a hands-on session of up to two hours, plus open challenge time.
Bring a laptop. **You need no fluency in any language** — every exercise is
won by reading metadata, not words.

**Before you arrive (5–10 minutes):** [docs/PRE_EVENT_SETUP.md](docs/PRE_EVENT_SETUP.md)
— check Python, get the kit, run `python3 tests/check_setup.py`, and confirm
you can open the Sentinel workspace with your DEATHLab account.

**What needs what:**

| Works offline | Needs your DEATHLab account and the event network |
|---|---|
| `probe.py`, the 79 samples, the practice ledger, four of the five hunts, the rule template | The live `PolyglotPoisoning_CL` table in Sentinel, both challenges, the optional leaderboard |

---

## THE GUIDED SESSION (up to two hours)

The teaching is recorded in three parts of about fifteen minutes each, with
pause points where you stop and work. Live, the same three parts are
presented in the room.

| Part | Block | What you do |
|---|---|---|
| 1 | **Why it matters** (~15 min) | The gap: the same request handled differently across languages, dialects and framing. The published evidence, a short Linguistic Firewall demo, and your first prediction with `probe.py`. |
| 2 | **The table and the query** (~15 min) | Sign in to Sentinel, find `PolyglotPoisoning_CL`, run your first query, then KQL from zero and the four metadata moves: reduce, count, split before you count, look below the alert. |
| 3 | **One hunt, start to finish** (~15 min) | One case walked from raw table to named campaign, turned into a detection rule; then the hunts, the challenges, and the optional leaderboard and local model. |
| — | **Your keyboard** (the rest of the session) | The five guided hunts in [HUNTS.md](HUNTS.md), a rule from [detection/DETECTION_RULE_TEMPLATE.md](detection/DETECTION_RULE_TEMPLATE.md), and — optionally — a prompt of your own for the leaderboard. |

The pause points sit inside each part, so a fifteen-minute recording takes
longer than fifteen minutes of room time. If time runs short, the open block
at the end is what shrinks.

## THE CHALLENGES (open time, outside the guided session)

The two challenges are solved at your own pace during the event window, not
inside the guided session. They are played against the live table.

| # | Challenge | Level | The core move |
|---|---|---|---|
| 1 | **Babel's Ledger** | easy | three metadata conditions true at once |
| 2 | **Rosetta Fragments** | advanced | split before you count, then sequence and reassemble |

Ten attempts each. Rules, hint ladders and no spoilers: [ctf/README.md](ctf/README.md).

---

## WHAT YOU WALK AWAY WITH

1. **Working muscle memory** for hunting AI telemetry you cannot read —
   anchors, frequencies, thresholds, correlation.
2. **A detection rule you wrote** and can explain in one sentence.
3. **The ledger reference** — the seven-column minimum to ask of any AI
   gateway you defend.
4. **Two challenges** to finish during the event window.
5. Optionally, a **seal on The Living Atlas Leaderboard** — every accepted
   submission earns the seal for the stage it reaches; Rubedo (score 5 or
   more) also earns the Polyglot Poisoning Hunter badge.

## THE EXERCISE LOOP (used in every block)

```
predict  →  run  →  record  →  modify ONE thing  →  run again
```

[`samples/WORKSHEET.md`](samples/WORKSHEET.md) has the copy-and-fill block for
each sample. The modification step is where the learning happens: change the
language *or* the framing, never both, and watch the score move.

---

## LEADERBOARD DISCLOSURE (read once, it's short)

Submissions are prompt text only — never model responses. Prompts are logged,
scored, and shown on the live leaderboard, and may inform LSI's published
research and detection rules — anonymized, always. Nothing is sent unless you
choose to submit. Rows reach the table in about 5–15 minutes.

## HOUSE RULES

- Handles, not real names — on the leaderboard and the challenge board.
- Prompts, not outputs. Never paste a model's response into any tool, chat or
  screenshot.
- Decode it, do not execute it: ledger prompts are specimens, never inputs.
- Gray-zone material stays in the room's context: this is a defensive hunting
  workshop.
