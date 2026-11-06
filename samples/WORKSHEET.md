# WORKSHEET — predict, run, record, modify, run again

The exercise loop for every block of the workshop. Copy this block once
per sample you test. The *modification* step is where the learning is:
change the language **or** the register, never both, and watch the score
move.

```
predict  →  run  →  record  →  modify ONE thing  →  run again
```

---

## THE LOOP, ONE SAMPLE AT A TIME

Copy and fill:

```
SAMPLE FILE: ________________________________

1. PREDICT (before you run it)
   I think this scores: ____ / 10
   Because I expect these signals: ______________________________

2. RUN
   python probe.py samples/<file>

   Actual score: ____    Verdict: pass / flag / BLOCK
   Signals fired: _______________________________________________

3. RECORD — was your prediction right?
   [ ] yes   [ ] no, I was high   [ ] no, I was low
   What surprised me: ___________________________________________

4. MODIFY ONE THING (language OR register — never both)
   What I changed: ______________________________________________

5. RUN AGAIN
   New score: ____   Moved by: ____
   What you think changed, in your own words
```

---

## WHAT YOU ARE PREDICTING AGAINST

Nothing on this sheet tells you what the probe rewards, and that is on
purpose — the Season 1 submission round is a blind test, and working the
behavior out yourself is the exercise. The tool names every signal it
finds, so run it and read what it says:

```bash
python probe.py <file>
```

Predict first. Write the number down. Then run it. The gap between your
guess and the output is the only thing on this page worth keeping.

---

## SUGGESTED RUNS (do at least three)

Write your prediction in the blank column *before* you run anything.

| # | Start from | Change | You predict | It said |
|---|---|---|---|---|
| 1 | `00_baseline_en.txt` | nothing — your control | | |
| 2 | `v1_es_direct_translation.txt` | nothing | | |
| 3 | `v1_ar_direct_translation.txt` | nothing | | |
| 4 | `v1_en_register_shift.txt` | nothing | | |
| 5 | any `_ar` file | add one English word mid-sentence | | |
| 6 | any `_eg` file | rewrite it with digits for letters | | |

The interesting rows are the ones where the two columns disagree. Those
are worth bringing to the Discord.

---

## THE TWO QUESTIONS WORTH ARGUING ABOUT

**1. Why does Spanish land where it does?**
Run it and see, then ask what the probe is reading. What it reads is what
it can and cannot defend. That is not
the probe failing. That is single-dimension lexical scoring showing you
its own limit, which is exactly why the hunt side of this workshop
exists.

**2. Why is the museum label in the sample pack?**
Because it is *benign* and it scores 1. Any rule you write that flags it
is a rule that will page someone at 3am for a curator writing an exhibit
card. It is in there to make your detection rule earn its threshold.

---

## WHAT TO CARRY INTO THE GREAT WORK

Your best single modification — the one that moved the score most for
the least change — is your variation. Submit *that* prompt (never a model
response) to the leaderboard: `docs/LEADERBOARD.md`.
