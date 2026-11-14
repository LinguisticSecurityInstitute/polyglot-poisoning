# Polyglot Poisoning

**Hands-On Hunting for Linguistic Attacks in AI**
DEATHCon 2026 (San Diego + online) · BSides San Diego · Sahara Al-Madi, [Linguistic Security Institute](https://almadisahara.com)

Your safety filter reads English. Your attackers don't have to.

A safeguard that refuses a request in English does not reliably refuse the
same request in another language, dialect, script or framing. This kit teaches
you to find that gap in your own telemetry — **without reading any of the
languages involved.** You hunt the metadata around a request; the words come
last.

---

## Start here

| | When | What you do | Time |
|---|---|---|---|
| **1** | Before the event | [Quickstart](#1--quickstart-offline-5-minutes) — get the kit, check it, run the probe | 5 min |
| **2** | Before the event | **[Sentinel access](#2--sentinel-access)** — sign in, find the table. **Required for the challenges.** | 5 min |
| **3** | During and after | [Work the kit](#3--your-path-through-the-kit) — hunts, challenges, optional leaderboard | yours |

**What works where:**

| Offline, on your laptop | Live, with your DEATHLab account |
|---|---|
| `probe.py`, the 79 samples, the 22-row practice ledger, four of the five hunts, the rule template, the mock receiver | The `PolyglotPoisoning_CL` table in Sentinel, both challenges, the optional leaderboard |

The offline kit has the same seven columns as the live table, so you can
rehearse every move before you touch it — and keep working if your access
breaks mid-session. You just cannot play the challenges offline.

**Keep this open:** [`docs/KQL_CHEAT_SHEET.md`](docs/KQL_CHEAT_SHEET.md) — every
instruction and query the workshop uses, on one sheet (also as a printable PDF in `docs/`).

---

## 1 · Quickstart (offline, 5 minutes)

Python 3.8 or newer. No `pip install`, no model, no account, no network.

```bash
git clone https://github.com/LinguisticSecurityInstitute/polyglot-poisoning.git
cd polyglot-poisoning
python3 tests/check_setup.py         # expect: SETUP OK
python3 tests/check_repository.py    # expect: REPOSITORY OK
python3 probe.py samples/            # expect: 79 files scanned, 0 would be blocked (score >= 5)
```

On Windows use `py` or `python` instead of `python3`, or run `setup.ps1`;
macOS and Linux can run `setup.sh`. Doing this well ahead of the day:
[`docs/PRE_EVENT_SETUP.md`](docs/PRE_EVENT_SETUP.md).

**Then try this — it is the whole workshop in one command.** `probe.py` takes
one file, one folder, or several of either:

```bash
python3 probe.py samples/00_baseline_en.txt samples/v1_sw_direct_translation.txt
```

Same request, two languages. Write down what you expect before you press
Enter — the gap between your guess and the number is the lesson.

### Other ways to run the kit

**Docker** (optional — the kit itself needs only Python):

```bash
docker build -t polyglot-poisoning .
docker run --rm polyglot-poisoning                      # setup check
docker run --rm polyglot-poisoning probe.py samples/    # scores the sample pack
```

**Oracle VirtualBox — an existing Ubuntu VM** such as `sahaa_lsi-SANDIEGO`.
On the **host**, snapshot first:

```bash
VBoxManage snapshot "sahaa_lsi-SANDIEGO" take "before-polyglot-poisoning"
```

Then **inside the Ubuntu VM**, from the repository root:

```bash
bash vm/bootstrap-ubuntu.sh
```

The full guide — inspecting the VM, the participant baseline, moving a newer
ZIP into the VM when GitHub is behind, Sentinel from the VM's browser, and
restoring the snapshot — is [`docs/VIRTUALBOX.md`](docs/VIRTUALBOX.md). Every
step is labeled HOST or UBUNTU VM.

---

## 2 · Sentinel access

**This is where the challenges happen.** The live table, both challenges and
the optional leaderboard all run here.

1. Sign in to the **Azure portal** with your own authorized **DEATHLab** account.
2. Open **Microsoft Sentinel**.
3. Select the **`deathcon2026-sentinel`** workspace.
4. Open **Logs**, and set the time range to **Last 30 days**.
5. Run:

```kql
PolyglotPoisoning_CL
| take 20
```

You can also find `PolyglotPoisoning_CL` in the **Tables** pane, under
**Custom Logs**. For challenge hunting, drop the optional leaderboard rows first:

```kql
PolyglotPoisoning_CL
| where UserPrincipal !endswith "@lb"
| take 20
```

**About access:**

- **A shared link grants no permissions.** Access comes from your own
  authorized account, not from a URL someone sends you.
- You need **read access to one table** and nothing more — never DCE, DCR,
  stream or ingestion permissions. The DCE is an ingestion endpoint, not the
  table, and you never query it.
- No rows, or a permissions error? Check the account, the workspace and the
  time range, then ask the organizer to confirm your account has
  **Microsoft Sentinel Reader** (and, if needed, **Log Analytics Reader**) on
  the workspace. Keep working offline meanwhile.

> **A correct query returns nothing?** The time range is the cause about four
> times out of five. The other four causes, and how to find them without
> guessing, are on the [cheat sheet](docs/KQL_CHEAT_SHEET.md#10--a-correct-query-that-returns-nothing).

---

## 3 · Your path through the kit

| Step | Open | What it gives you |
|---|---|---|
| 1 | [`docs/LEDGER_REFERENCE.md`](docs/LEDGER_REFERENCE.md) | The seven columns. Keep it in a second tab. |
| 2 | [`docs/KQL_CHEAT_SHEET.md`](docs/KQL_CHEAT_SHEET.md) | Every query and instruction for the session. |
| 3 | [`HUNTS.md`](HUNTS.md) | Five guided hunts with fill-in-the-blank queries and a self-check each. |
| 4 | [`ctf/README.md`](ctf/README.md) | Both challenges: rules, hint ladders, no spoilers. |
| 5 | [`detection/`](detection/) | Turn a finding into a rule you could defend at work; the full query pack. |
| 6 | [`docs/LEADERBOARD.md`](docs/LEADERBOARD.md) | The Living Atlas Leaderboard — optional. |
| — | [`WORKSHOP.md`](WORKSHOP.md) | How the session runs. |

### The seven columns

| Column | Type | What it is | |
|---|---|---|---|
| `TimeGenerated` | `datetime` | when it landed | hunt this |
| `UserPrincipal` | `string` | who — `@lb` marks a leaderboard row | hunt this |
| `Language` | `string` | the language or regional code | hunt this |
| `Variant` | `string` | `V1` standard or direct · `V2` regional variety or dialect | hunt this |
| `RiskScore` | `real` | the number the probe returned; the alert fires at 5 | hunt this |
| `Patterns` | `string` | the shaping stamps that fired, comma separated | hunt this |
| `PromptPreview` | `string` | the first 200 characters of the text | **read last** |

Register, framing, code-switching and transliteration are recorded in
`Patterns`, never as extra Variant values.

### What a row looks like

Three of the highest-scoring rows in the practice ledger, then the English control:

```
TimeGenerated         UserPrincipal              Language  Variant  RiskScore  Patterns
2026-11-01T17:07:00Z  static_wren@deathlab.net   ar-EG     V2       8          script_diversity,register_shift,code_switch
2026-11-01T17:03:00Z  amber_saddle@deathlab.net  ar-TN     V2       6.5        script_diversity,register_shift,framing
2026-11-01T16:35:00Z  harbor_moth@deathlab.net   ar-TN     V2       4.3        script_diversity,register_shift
2026-11-01T16:00:00Z  north_pier@deathlab.net    en-US     V1       0          (empty)
```

The last row is the same request in English, scoring zero with an *empty*
`Patterns`. Across the practice ledger, **2 rows scored 5 or more and were
blocked, 12 scored between 2 and 5 and nothing fired, and 8 scored under 2.**
Low priority is not the same as cleared.

### The five hunts

1. **Metadata anchors** — one written root sits unchanged across three dialects.
2. **Stacking and frequency** — split multi-value columns *before* you count.
3. **Threshold evasion** — look in the band below the alert, not only at the blocks above it.
4. **Correlation** — when the prompt becomes a process. *(Needs a second table — run it at work.)*
5. **Translate last** — triage on labels; open only what survives.

### The two challenges

| # | Challenge | Level | The core move |
|---|---|---|---|
| 1 | **Babel's Ledger** | easy | three metadata conditions true at once |
| 2 | **Rosetta Fragments** | advanced | split before you count, then sequence and reassemble |

Ten attempts each — plenty if you hunt, nowhere near enough if you guess. Both
are played against the live table during the event window, separately from
the guided session; rehearse the mechanics on the practice ledger first.

---

## The probe, honestly

`probe.py` (the Alembic) reads the **surface** of a prompt — its script,
whether it switches languages, whether it carries transliteration or a
framing device — and returns a number plus the names of what it noticed.

- It **does not** read meaning, judge intent, or decide whether anything is
  harmful. It tells you which rows to read first.
- **Some complete, fluent requests score nothing at all.** That is not the
  probe failing; it is the lesson, and the reason the hunting half of this
  workshop exists.
- Single-dimension surface scoring is a teaching instrument, not a product.

It is short, standard library only, and nothing in it is hidden: every signal
and what it is worth is in the source and in the probe's own output. The
optional leaderboard ranks on exactly this score, computed again by the event
receiver.

## Optional — a local model alongside it

Not required. But reading that a safeguard behaves differently across
languages is one thing; watching it on a machine you own is another. If you
already run a model locally, use that. Otherwise, with [Ollama](https://ollama.com):

```bash
ollama pull phi3:mini                               # ~2.3 GB download, ~4 GB RAM
ollama run phi3:mini "$(cat samples/eth1_en.txt)"   # the English baseline
ollama run phi3:mini "$(cat samples/eth1_es.txt)"   # same request, Spanish
python3 probe.py samples/eth1_en.txt samples/eth1_es.txt
```

**The interesting outcome is a disagreement** — a prompt the probe scores low
that the model treats differently anyway. Use the curated samples only, keep
it local, and **report the score and the patterns, never a model's response.**
Rows from the live table never go into any model.

## The Living Atlas Leaderboard (optional)

Write a prompt — no rules, no template — score it with the probe, and submit
it if you want to. It becomes a row in the same table you learned to hunt,
under a handle you choose.

```bash
python3 leaderboard/submit.py --url http://RECEIVER_ADDRESS:8730 \
    --handle YOUR_HANDLE --file my_prompt.txt --lang hi-IN --variant V1
```

- **One prompt per submission.** `--lang` takes any ISO code (`es`, `ar-EG`,
  `sw-KE`), or `mul` if the prompt mixes languages. `--variant` is `V1` or `V2`.
- The receiver address is given in the session and the DEATHCon Discord, not
  in this repository. To rehearse first, run `python3 tests/mock_receiver.py`
  and use `--url http://127.0.0.1:8730` — it scores locally and sends nothing anywhere.
- The receiver scores your prompt again itself, adds `@lb` to your handle, and
  rejects anything containing `flag{`. Your row reaches the table in about
  **5–15 minutes**.
- **Every accepted submission earns a seal** for the stage it reaches —
  Nigredo, Albedo, Citrinitas or Rubedo. Rubedo (5 or more) also earns the
  Polyglot Poisoning Hunter badge.

> **Disclosure, plainly:** submissions are prompt text only — never model
> responses. Prompts are logged, scored, and shown on the live leaderboard,
> and may inform LSI's published research and detection rules — anonymized,
> always. Which entries are selected into The Living Atlas is LSI's decision;
> accepted prompts are credited by handle. Nothing is sent unless you choose
> to submit. Full details: [`docs/LEADERBOARD.md`](docs/LEADERBOARD.md).

## Rules of engagement

- **Handles, not real names** — on the challenge board and the leaderboard.
- **Prompts, not outputs.** Never paste a model's response anywhere.
- **Decode it. Do not execute it.** Prompts in the ledger are specimens: read
  them, label them, count them. Never paste one into a live model.
- **Read the table, don't write to it.** Query all you want.
- **Don't share flags or full solutions.** "What does `mv-expand` do?" is a
  good question. A query that solves a challenge is not a good answer.

## Repository map

```
probe.py                       the Alembic — surface scoring, standard library only
samples/                       79 prompt files and the notes on why each is there
data/practice_ledger.jsonl     22 rows of synthetic ledger telemetry, seven columns
HUNTS.md                       five guided hunts, with self-checks
WORKSHOP.md                    how the session runs
ctf/                           both challenges: player guide, ledger reference, field card
detection/                     rule template, a worked rule, and WORKSHOP_QUERIES.kql
docs/                          cheat sheet, ledger reference, leaderboard, pre-event setup,
                               VirtualBox guide, and the downloadable PDFs and slides
leaderboard/submit.py          optional: submit a prompt of your own
leaderboard/living_atlas_board.kql   the query behind the live board
leaderboard/board.py           draws the board from ledger rows
leaderboard/badges/            the four seals
tests/check_setup.py           is my kit OK?            -> SETUP OK
tests/check_repository.py      is the repo consistent?  -> REPOSITORY OK
tests/mock_receiver.py         rehearse a submission locally; sends nothing
vm/bootstrap-ubuntu.sh         prepare an Ubuntu VM for the kit
Dockerfile, .dockerignore      the kit in a container
setup.sh, setup.ps1            one-command setup for macOS/Linux and Windows
```

## What this repo is — and is not

- **V1 and V2 only.** Everything here applies published methodology
  (translation attacks, resource-level decay, register and temporal framing)
  to gray-zone, benchmark-register questions. Nothing touches a real person,
  company or target.
- **The two open levels of The Living Atlas.** The Phoenix Corpus — LSI's
  extended research collection — is packaged separately, on its own terms.
- The corpus translations are original LSI work, released for education and
  research. NAMAA contributed native-fluency verification for selected
  initial dialect prompts; the wider corpus, methodology, tooling and research
  are LSI's.
- This repository is participant material only. Event infrastructure,
  challenge data and solutions are kept separately and are never committed here.

### Sources

- Deng et al., *Multilingual Jailbreak Challenges in LLMs*, ICLR 2024 (arXiv:2310.06474)
- Yong, Menghini & Bach, *Low-Resource Languages Jailbreak GPT-4* (arXiv:2310.02446)
- Faruna, *LSR: Linguistic Safety Robustness Benchmark for Low-Resource West African Languages* (arXiv:2603.19273)
- Said & Sani, *Safe in the Future, Dangerous in the Past* (arXiv:2512.24556)
- Background: Upadhayay & Behzadan, *Sandwich Attack* (arXiv:2404.07242) · Poppi, Yong et al., NAACL 2025 Findings (2025.findings-naacl.126) · Yong et al., EMNLP 2025 (2025.emnlp-main.800)

Results in this area vary a great deal between studies — including a 2026
counterpoint that found almost no dialect gap. That variation is the argument
for measuring your own deployment rather than inheriting a number.

## Recordings

The workshop is recorded in three parts of about fifteen minutes each:

1. **Why it matters** — the gap, the published evidence, a Linguistic Firewall demo.
2. **The table and the query** — Sentinel, the custom table, KQL, the four metadata moves.
3. **One hunt, start to finish** — a worked case, a detection rule, the challenges, and the optional leaderboard.

Links are added here when the recordings are published.

## Need help?

- **During the event:** the workshop Discord channel. Describe where you are
  stuck — "my `mv-expand` returns nothing" — rather than what you think the
  flag is. Re-running the matching hunt in [`HUNTS.md`](HUNTS.md) is usually
  the quickest way to get moving again.
- **Anything that should not be public, or a security issue:** see [`SECURITY.md`](SECURITY.md).
- **Improving the kit:** see [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

| What | License |
|---|---|
| Code, scripts, and **every runnable query or detection rule** | MIT — [`LICENSE`](LICENSE) |
| The prompt corpus and practice data | CC BY-NC 4.0 — [`LICENSE-PROMPTS`](LICENSE-PROMPTS) |
| The teaching material | CC BY-NC 4.0 — [`LICENSE-CONTENT`](LICENSE-CONTENT) |

**Take the queries to work.** Every KQL query and detection rule here is MIT,
wherever it appears. The curriculum and corpus are free to use and teach
from, with commercial use by permission. The names and marks are licensed by
neither — the full map is [`LICENSES.md`](LICENSES.md).

---

**Contact:** almadisahara.com · linguisticsecurityinstitute@gmail.com
Workshop listing: DEATHCon 2026 (online + San Diego) & BSides San Diego.
