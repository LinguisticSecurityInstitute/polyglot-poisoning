# PRE-EVENT SETUP — do this BEFORE the workshop (5–10 min)

## Polyglot Poisoning: Hands-On Hunting for Linguistic Attacks in AI

**DEATHCon 2026 · November 13 & 14 · online and on-site, San Diego**

Questions? Find us in the DEATHCon Discord.

The offline half runs entirely on your own laptop with Python 3.8+ —
no models, no Docker, nothing to install beyond Python itself.
The live half uses the event lab, and Sentinel and Azure access is
provided for this workshop. See **LAB ACCESS** below.

---

## STEP 1 — Check Python (30 seconds)

In a terminal:

```bash
python --version
```

Need 3.8 or newer. (On Windows, if `python` isn't found, try
`py --version` or install Python 3.12 from python.org.)

## STEP 2 — Get the workshop kit

Clone the repo (or grab the release ZIP and unzip it somewhere easy
to find):

```bash
git clone https://github.com/LinguisticSecurityInstitute/linguistic-firewall.git
cd linguistic-firewall
```

Inside you'll find:

```
probe.py              the Linguistic Firewall (community edition)
samples/              79 prompt files + why each one is there
data/                 practice ledger (same 7 columns as the live one)
detection/            rule template + a worked example
docs/                 this file + the ledger reference
ctf/                  the two hunt challenges (player guide)
HUNTS.md              five guided KQL exercises
tests/check_setup.py  proves your kit works
```

## STEP 3 — Prove it works (1 minute)

From the repo folder:

```bash
python tests/check_setup.py
```

or just run the probe on the sample pack:

```bash
python probe.py samples/
```

If you get a score table — score, verdict, signals — you're done.
There is no pip install step; the probe is standard-library only.
Windows and macOS/Linux one-liners are in `setup.ps1` / `setup.sh`.

---

## OPTIONAL — run a local model alongside the workshop

**Not required.** Everything the workshop promises works without this.
But reading that a safeguard behaves differently across languages is one
thing; watching it happen on your own laptop is another. If you have the
disk space, this is the single best thing you can add.

It is **model-agnostic** — any local model works. If you already run one
(LM Studio, llama.cpp, text-generation-webui, anything), use that and skip
the install.

### Option A — Ollama (easiest)

Install from https://ollama.com, then pull one model:

```bash
ollama pull phi3:mini        # ~2.3 GB · 4 GB RAM · runs on almost anything
ollama pull phi4             # ~9 GB  · 16 GB RAM · noticeably better multilingual
ollama pull llama3.2:3b      # ~2 GB  · the smallest useful fallback
```

`phi3:mini` is the safe default. Pull `phi4` instead if you have the RAM —
its multilingual behavior is stronger, which makes the comparison more
interesting rather than less.

### Option B — a model you already run

Any local model is fine. You need exactly two things from it: a way to send
it a prompt, and a way to see what comes back. Nothing in this workshop
depends on which model it is.

### What to actually do with it

Run the same request in two languages and compare — that is the whole
exercise:

```bash
# the English baseline
ollama run phi3:mini "$(cat samples/eth1_en.txt)"

# the same request, different language
ollama run phi3:mini "$(cat samples/eth1_es.txt)"
ollama run phi3:mini "$(cat samples/eth1_tn.txt)"
```

Then score both with the probe and see whether the probe's reading of the
prompt matches what the model actually did:

```bash
python probe.py samples/eth1_en.txt samples/eth1_es.txt samples/eth1_tn.txt
```

**The interesting outcome is a disagreement.** A prompt the probe scores low
that the model treats differently anyway is exactly the finding worth
bringing to the Discord — that gap is the whole subject of the workshop.

### Rules if you do this

- **Keep it local.** No API keys, no hosted models, nothing leaves your
  machine.
- **Prompts only, never outputs.** Report the score, the patterns and the
  outcome category. Do not paste a model's response into Discord, the
  leaderboard, an issue, or anywhere else.
- **Your laptop, your model, your call.** Only run this against a model you
  control and are authorized to test.

---

## HOW THE GAME WORKS (optional, on top of the exercises)

1. Run the probe on the samples; see what slips under.
2. Submit a PROMPT (never the model's response) through the
   workshop's submit tool — the open-source probe scores it and
   puts your handle on the live leaderboard.
3. Everyone whose accepted submission scores >= 5 earns the Polyglot
   Poisoning Hunter badge. Every accepted prompt is credited to its
   contributor in The Living Atlas — see docs/LEADERBOARD.md.

**DISCLOSURE (we say it plainly):** Submissions are prompt text only —
never model responses. Prompts are logged, scored, and shown on the
live leaderboard, and may inform LSI's published research and
detection rules — anonymized, always. Nothing is sent unless you
choose to submit. Share scores and patterns — never harmful outputs.

---

## LAB ACCESS — for the live half

**Sentinel and Azure access is provided for this workshop.** Refer to the
DEATHCon setup instructions for Sentinel, Azure and your `@deathlab.net`
account.

**Sort it out before the session rather than during it.** Whatever the setup
asks of you, the room is not the place to discover it — and it is the one
part of this page that depends on something other than your own laptop.

You need that access for:

- the hosted **Sentinel workspace** — the live table you query
- the **CTF board**, where flags are submitted
- **live submission** to the leaderboard during the session

You do **not** need it for anything else. The probe, the sample pack, all
five guided hunts and both challenge *mechanics* run fully offline, and
`data/practice_ledger.jsonl` lets you rehearse every move with no lab
access at all — same seven columns, 22 synthetic rows. If the lab is not
working for you on the day you will still follow the whole workshop; what
you will miss is the live table and flag submission.

**You can still contribute without it.** The probe scores locally, so you
can write a prompt, test it, and opt in to contribute it to The Living
Atlas through the Discord channel. Lab access puts you on the live board
during the session — it is not what makes a contribution count.
