# THE HUNT CHALLENGES — player guide

Two challenges, one category: **Polyglot Poisoning** — plus the live
leaderboard, **The Great Work**, which runs during the session.
You do not need to know any language to solve any of them —
**hunt the metadata, not the words.**

Play them on the event CTFd board (link in the DEATHCon Discord).
The queries run in the **deathcon2026-sentinel** workspace —
Sentinel and Azure access is provided for this workshop — refer to
the DEATHCon setup instructions for Sentinel, Azure and your
`@deathlab.net` account.

**No lab / practicing at home?** Every mechanic below can be
rehearsed offline against [`../data/practice_ledger.jsonl`](../data/practice_ledger.jsonl)
— same seven columns, 22 synthetic rows. The hunts in
[`../HUNTS.md`](../HUNTS.md) are the training montage for both
challenges.

---

## THE BOARD

| # | Challenge | Difficulty | The core move |
|---|---|---|---|
| 1 | **Babel's Ledger** | easy | filter on a metadata triple |
| 2 | **Rosetta Fragments** | advanced | split → sequence → reassemble |

Running alongside them, live during the session: **The Great Work** — the
leaderboard round, scored by the open-source probe. Four stages, from
nigredo to rubedo. See [`../docs/LEADERBOARD.md`](../docs/LEADERBOARD.md).

Each challenge unlocks the next. Max **10 attempts** per challenge —
more than enough if you hunt, nowhere near enough if you guess
(there are far more plausible-looking strings than attempts).

**Flag format:** `flag{...}` — submit the whole string including
the wrapper, unless a challenge tells you to add the wrapper
yourself.

---

## RULES OF ENGAGEMENT

- **Handles, not real names** — on the board and the leaderboard.
- **Don't share flags or full solutions** in Discord. Asking "what
  does mv-expand do" is fine; posting a query that solves a
  challenge is not.
- **Prompts, not outputs.** If you detonate something, report the
  score and the patterns — never paste a harmful completion.
- The telemetry is the game. Query all you want; don't try to
  modify the table.

---

## THE SHARED ATTACHMENT

**LEDGER_REFERENCE_POLYGLOT_POISONING.txt** (attached to every
challenge, mirrored in this repo at
[`../docs/LEDGER_REFERENCE.md`](../docs/LEDGER_REFERENCE.md)):
the schema, the language codes, the Variant codes, and the one free
hint about the Patterns column. Open it in a second tab and leave it
there.

---

## CHALLENGE 1 — Babel's Ledger (easy)

*Twenty-five rows in the intake ledger. Somewhere in the haystack is
one row that isn't like the others. You don't have to know the
language — just hunt the metadata.*

**Hint ladder:**

1. Three columns matter. One row survives when all three are true.
2. Look at the rare combinations first: which dialect shows up
   shaped, and hot? Frequency tables (`count() by Language, Variant`)
   are your friend.
3. Filter `Language`, `Variant` and `RiskScore` — all three at once.
   Exactly one row survives. Read *that* preview.

---

## CHALLENGE 2 — Rosetta Fragments (Advanced)

*A supply-chain crew stamps its cargo with an inspection mark that
was never issued. The manifest column looks different on every row —
four languages, four combinations. Find the stamp that doesn't
belong, line its carriers up, and reassemble what they smuggled in.*

**Extra attachment:** `CTF2_ADVANCED_FIELD_CARD.txt` — the four
hunting moves, pocket-sized.

**Hint ladder:**

1. **Split before you count** (`mv-expand`). One stamp recurs across
   languages and combinations; counting raw combinations is a dead
   end by design.
2. **Rare is not forged.** Don't sort ascending and grab the bottom —
   check which stamp keeps company with too many different languages
   and too many different combos. Then line its rows up.
3. Brackets fence the pieces; **risk is the sequence**; you add the
   `flag{ }` wrapper yourself.

---

## STUCK?

- Re-run the matching hunt in [`../HUNTS.md`](../HUNTS.md) — each
  challenge is one hunt wearing a trench coat. Hunts 4 and 5 are not
  tied to a challenge this year; run them anyway, they are the two that
  change how you work.
- Ask in the workshop Discord channel. Describe where you're stuck
  ("my join returns nothing"), not what you think the flag is.
- The organizers can nudge; they will not hand you a query.
