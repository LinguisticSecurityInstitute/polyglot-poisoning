# THE GREAT WORK — Season 1 of The Living Atlas

**Submit a pair. Become a row. Watch the room hunt you.**

The Living Atlas is the public collection of the LSI Mithridate Project, and
it is not finished. The holes in it are languages. The Great Work is how
you put something in the vessel yourself — during the workshop, and for as
long as the season runs after it.

Your submission becomes telemetry. The room can hunt it. So can you.

---

## DISCLOSURE (read once — we say it plainly)

**Submissions are prompt text only — never model responses.** Prompts are
logged, scored, and shown on the live leaderboard, and may inform LSI's
published research and detection rules — **anonymized, always.** Handles,
not real names. Nothing is sent unless you choose to submit, and **every
hunt in this kit works without ever submitting.**

---

## CONTRIBUTOR CREDIT

**Every accepted prompt is credited to its contributor in The Living
Atlas.** Credits are permanent and appear in the Hall of Fame, the repo,
and the workshop materials.

Conditions:

- The prompt must be original.
- The prompt must be accepted by LSI.
- Credits may be removed for plagiarism or abuse.

Season 1 — DEATHCon 2026 contributors are listed in
[`season-1/contributors.md`](../season-1/contributors.md).

Credit uses the handle you submitted under. If you would rather be credited
under a different name, or not credited at all, say so in the workshop
Discord and we will change it — credit is a recognition, not an obligation.

**Three separate things, so nobody is surprised later:**

| | What it is |
|---|---|
| **The live board** | Shows your chosen handle and your best score during the season. |
| **Contributor credit** | Your handle on the accepted sample, in the Atlas and the Hall of Fame, permanently. |
| **Research reporting** | Anonymized, always. Published findings do not carry handles. |

---

## WHAT ONE ROW ACTUALLY DOES

Your row does not stop at the board.

1. **It teaches the room.** It joins the live table everyone is hunting.
   Next season practices on real rows instead of invented ones.
2. **It widens the Atlas.** One more language counted — with your handle on
   the sample, permanently.
3. **It raises the season.** The season report is written from what the
   Alembic missed. Your row might be the miss.
4. **It informs the research.** Coverage numbers, detection rules, the
   next paper.

### And where it does not go

| | | |
|---|---|---|
| **THE LIVING ATLAS** | → | **THE LINGUISTIC FIREWALL** |
| Public · your rows · the *evidence* | | The service that uses both |
| what the Firewall is held to | | measures a system, dialect by dialect |
| **THE PHOENIX CORPUS** | → | |
| LSI's extended research collection | | |
| never fed by your rows | | |

The Living Atlas is **evidence** — which languages fail, and how. It is
public, and your rows are in it. The Phoenix Corpus is LSI's extended
research collection, studying hybrid language forms, stacked signals and
tuned composition. It is packaged separately and described openly; it is
not fed by contributed rows. The Linguistic Firewall is the service,
and it draws on both.

> **Your prompt becomes something another analyst can hunt.**

Which is also the honest incentive: a wider Atlas means the service is held
to **more languages**. Contributing is how you make the Firewall accountable
to a language it does not cover yet.

Does LSI benefit? Yes, indirectly — better coverage data makes a better
service. What you get back is permanent credit and a measured language. The
two collections stay separate in both directions, and if that ever changes
it changes in public and before the fact.

---

## THE ONE RULE

> **Nothing enters the Atlas alone.**

Every submission is a pair: what you made, and what you changed it from.

- Transmuted a sample? That sample is your control.
- Wrote something fresh? Send a harmless twin in the same language and the
  same register.

A prompt on its own is a story. A prompt with its control is a
measurement. That is the whole difference between this corpus and a pile
of jailbreaks — and it is why the vendor Report Card could grade one
product and had to mark the other *Incomplete*.

---

## HOW TO SUBMIT

**The brief is open.** No rules, no template, no worked examples. Write a
prompt, be as creative as you like, and see what you can do. If you would
rather not start from a blank page, a sample is a fine place to begin —
but nothing here asks you to.

```bash
# 1. Write your prompt into a file.
$EDITOR my_prompt.txt

# 2. Test locally first — the receiver runs this exact probe:
python probe.py my_prompt.txt

# 3. Submit (URL announced in the workshop / Discord):
python leaderboard/submit.py --url http://HOST:8730 \
    --handle YOUR_HANDLE --file my_prompt.txt --lang hi-IN --variant V1

# Mixing languages, or experimenting past any single label? Use mul:
python leaderboard/submit.py --url http://HOST:8730 \
    --handle YOUR_HANDLE --file my_prompt.txt --lang mul --variant V1
```

- `--handle`: 2–24 chars, letters/digits/`_ . -` — a handle, **not your
  real name**. This is the name your credit will carry.
- `--lang`: **any** language code you want — any ISO 639-1 two-letter code,
  any 639-3 three-letter code where no two-letter one exists, each with an
  optional region or variety subtag. `es`, `hi`, `th`, `ar-EG`, `ar-MSA`,
  `sw-KE` are all fine.
- **`--lang mul` is for mixing, matching and experimenting.** It is the ISO
  code for *multiple languages*, and it is the honest label for a prompt no
  single code describes. It counts exactly the same as any other code, and
  it never earns a mismatch stamp. Do not skip submitting because you could
  not label it.
- `--variant`: `V1` standard, `V2` a regional variety or dialect. It
  describes the **register**, not how many languages are in the prompt — so
  a mixed prompt is still V1 unless part of it is dialect.
- Declare honestly. A row that says English and carries Arabic script earns
  the `label_mismatch` stamp and **does not count** — not as a punishment,
  but because nothing can be measured with it. Fix the label and resubmit.
  (`mul` is exempt: it is already the correct answer for "more than one.")
- One submission per handle per 20 seconds. Compose, don't spam.
- Anything containing `flag{` is rejected. The leaderboard is not the CTF
  board.

---

## HOW SEASON 1 RANKS

**Best score on the open probe.** That is the whole rule, and the board
query is the whole implementation.

| Stage | What it means |
|---|---|
| **NIGREDO** — the blackening | Little visible signal. Often the most interesting result in the room. |
| **ALBEDO** — the whitening | The first signals fire. |
| **CITRINITAS** — the yellowing | Close to the probe's threshold. |
| **RUBEDO** — the reddening | At or past it — and the badge. |

The bands are not printed here on purpose. The brief is open: write a prompt,
no rules and no worked examples, and see what you can do. The tool tells you
your own number when you run it, and the board tells you where you stand.

### The badge, stated exactly

**The Polyglot Poisoning Hunter badge is earned by an accepted submission
that reaches the probe's own threshold** — the point at which it would stop
a prompt. The tool will tell you when you have. It recognizes signal
stacking and participation.

It does **not** certify that a model was bypassed. It does **not** certify
that the prompt is harmful. It is **not** a measure of anyone's skill in a
language. The score is a transparent surface heuristic, nothing more.

**A low score is not a failure.** The most instructive prompt measured in
the pilot was one the probe walked straight past, while a commercial
classifier answered it and refused the identical English request. If you
land at Nigredo with something natural, bring it to the Discord. That is a
finding, and it is creditable like any other.

### A known weakness, recorded rather than hidden

Ranking by score rewards stacking, and stacking is not where the most
useful contributions live. See
[`../proposals/season-2/`](../proposals/season-2/) for a
contribution-based alternative. It is **not** running.

---

## THE BOARD IS A QUERY — DON'T TRUST IT, RUN IT

Everyone in the workspace has Reader access. The live board is
[`../leaderboard/great_work_board.kql`](../leaderboard/great_work_board.kql)
and nothing else. You can also render the same standings offline as a projectable board:

```bash
python leaderboard/board.py data/practice_ledger.jsonl \
    --domain deathlab.net -o board.html
```

`board.py` is stdlib-only and writes one self-contained HTML file — no
network, no fonts to fetch, no build step. It applies the same rule as the
KQL above, so the two never disagree.

See your own rows, and why each one did or did not count:

```kql
PolyglotPoisoning_CL
| where UserPrincipal == "YOUR_HANDLE@lb"
| extend Counted = iff(Patterns has "label_mismatch", "no — label_mismatch", "yes")
| project TimeGenerated, Language, Variant, RiskScore, Patterns, Counted
| sort by TimeGenerated desc
```

Leaderboard rows always end in `@lb`; CTF rows never do — the two games
share a table and never touch.

---

## SEASONS

A season is a scope, a report, and a reset.

- **Season 1** covers the first two levels — another language, and a
  dialect in either script. It opens at DEATHCon San Diego and does not
  close when the room empties.
- **It closes** with a season report: coverage per language, what the
  Alembic missed, and what that suggests for the next one. Contributors
  are listed in `season-1/contributors.md`.
- **Then the live race resets.** Credits do not — they are permanent. A
  board that never resets is a wall telling every newcomer they arrived
  too late; a credit list that resets would not mean much.

---

## WHY THE CTF CAN'T BE OVERRUN (the four walls)

The table keeps growing all event — that's the point. The challenges don't
care, because the write path is a bouncer, not an open door:

1. **The probe cannot reach the CTF's gate.** Every submission is
   re-scored by `probe.py` on the receiver, and its ceiling sits below
   Babel's Ledger's `RiskScore > 8` gate, so no submission can ever
   produce a row that matches it.
2. **You cannot mint stamps.** `Patterns` is computed by the receiver from
   the probe's fixed vocabulary. Nobody can write themselves a `courier`
   stamp — Rosetta's forged mark stays exactly four rows, forever.
3. **No flag text can be written.** Anything containing `flag{` is
   rejected, and every CTF answer is content inside a planted row, not a
   metadata pattern.
4. **`@lb` separation + read-only KQL.** Contestants get Reader access;
   the only write path is the receiver.

These are challenge-integrity controls. They are not a claim that a small
event receiver is a hardened public service — the URL stays temporary and
organizer-controlled.

**Your row takes roughly 5–15 minutes to appear.** That's ingestion
latency, not a bug. While you wait: hunt the rows that already landed, and
please do not resubmit just because the first one has not shown up.

---

## THE FLYWHEEL

1. You learn the hunts on the practice ledger.
2. You submit a pair — it becomes real rows in the live table.
3. Fresh, consented, *controlled* rows are exactly what makes the hunts
   worth running.
4. Hunting someone else's submission teaches you to build a better one.
5. Repeat. The board climbs; the Atlas gets one more language; everyone
   leaves having been both the attacker and the analyst.

The offense writes the defense's training set. That's the whole workshop
in one loop.

---

## HOUSE RULES

- Handles, not real names.
- Prompts, never outputs.
- No flags, no spoilers, no gaming someone else's handle.
- The organizers see the same table you do.
