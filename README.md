# Polyglot Poisoning

**Hands-On Hunting for Linguistic Attacks in AI**
DEATHCon 2026 (San Diego) · BSides San Diego · Sahara Al-Madi, [Linguistic Security Institute](https://almadisahara.com)

Your safety filter reads English. Your attackers don't have to.
This repo is the complete hands-on kit for learning to **hunt**
multilingual and dialect-level attacks against AI systems — no
fluency in any language required. You hunt the metadata, not the
words.

---

## The gap, in one paragraph

Published work keeps finding the same crack: guardrails that refuse
harmful requests in English answer the *same request* in another
language (Deng et al., ICLR 2024), especially low-resource ones
(~79% bypass on GPT-4 — Yong et al., 2023; refusal rates collapsing
from ~90% to 35–55% in West African languages — LSR benchmark Faruna, 2026),
and even *in English* when the register shifts to historical/academic
framing (15.6% vs 57.2% safe — Said & Sani, 2026). Detection tools
mostly answer `blocked: true`, and one boolean is hard to hunt. This kit
shows the seven columns you actually need, and how to hunt them.

## Quickstart (5 minutes, offline, Python 3.8+)

```bash
git clone https://github.com/LinguisticSecurityInstitute/linguistic-firewall.git && cd linguistic-firewall
python tests/check_setup.py     # proves the kit works
python probe.py samples/        # scores the 79-prompt pack
```

No `pip install`. No models, accounts, or network required for the
core exercises. (Windows: see `setup.ps1`. macOS/Linux: `setup.sh`.
Doing this before the event: `docs/PRE_EVENT_SETUP.md`.)

**Want to watch a live model fail?** Optional: install
[Ollama](https://ollama.com), `ollama pull llama3.2:3b`, then
`ollama run llama3.2:3b "$(cat samples/v1_ar_direct_translation.txt)"`
and compare with the English baseline.

## What's inside

```
probe.py                 the Linguistic Firewall (community edition) —
                         reads the surface, returns a number
samples/                 79 prompt files: baseline, the V1 ladder
                         (one request × 10 languages), the V2 dialect
                         set (Egyptian, Tunisian) plus English
                         register/framing samples, and a 12×5
                         category matrix, with a guide to why each
                         sample is there (samples/README.md)
data/practice_ledger.jsonl   22 rows of synthetic ledger telemetry —
                         rehearse every hunt mechanic with no lab at all
docs/LEDGER_REFERENCE.md the shared field reference for the hunt data
docs/LEADERBOARD.md      The Great Work: submit a prompt, become a
                         row, watch yourself get hunted
docs/PRE_EVENT_SETUP.md  5-minute pre-event checklist
leaderboard/             receiver.py (organizer: validate → score →
                         vault → push to the DCE) + submit.py (you)
detection/               fill-in-the-blank rule template + one worked,
                         explainable rule (qufl_lock_anchor.kql)
HUNTS.md                 five guided hunt exercises (KQL, with blanks
                         to fill — answers emerge from the data)
ctf/README.md            the three DEATHCon CTF challenges
                         (player guide — no spoilers)
WORKSHOP.md              how the 90-minute live session runs
tests/check_setup.py     the deterministic "is my kit OK" gate
```

## The probe, honestly

`probe.py` reads the **surface** of a prompt and returns a number, together
with the names of whatever it noticed. It does not read meaning, and it does
not decide whether anything is harmful — it tells you which rows to read
first.

Run it on the sample pack and read the output. Every sample changes exactly
one thing, so the output tells you what this probe is and is not sensitive to.
Some complete, fluent requests score nothing at all. That is not the probe
failing; it is the lesson, and it is the reason the hunting half of this
workshop exists. Single-dimension surface scoring is a teaching instrument,
not a product.

The source is 62 lines of standard-library Python and nothing in it is hidden.
Read it if you want to know exactly how it decides. What we do not do is print
the scoring table in the documentation, because the Season 1 submission round
is a blind test — see [docs/LEADERBOARD.md](docs/LEADERBOARD.md) — and a
handed-out rubric turns prompt-writing into number-maximising.

## The five hunts

1. **Metadata anchors** — one Arabic root catches three dialects.
2. **Stacking & frequency** — split multi-value columns before you count.
3. **Threshold evasion** — the prey lives in the 2–5 band under the wire.
4. **Correlation** — when the prompt becomes a process (join to endpoint telemetry).
5. **Translate last** — triage on labels; read only what survives the filters.

Full walkthroughs with fill-in-the-blank queries: **[HUNTS.md](HUNTS.md)**.

## The CTF

Two challenges, both playable with zero language knowledge — you hunt
the ledger, not the words:

| # | Challenge | Difficulty | Core move |
|---|---|---|---|
| 1 | Babel's Ledger | easy | filter on metadata triple |
| 2 | Rosetta Fragments (CTF2 Advanced) | advanced | split, sequence, reassemble |

A third contest, **The Great Work**, runs live on the leaderboard during
the session — see below.

Player guide (rules, hint ladders, no spoilers): **[ctf/README.md](ctf/README.md)**.
Field reference you'll want open in a second tab: **[docs/LEDGER_REFERENCE.md](docs/LEDGER_REFERENCE.md)**.

## The Great Work — the leaderboard (live session only)

Submit a **prompt** (never a model's response); the open-source probe
scores it; your handle climbs the board through the four stages of the
magnum opus — **nigredo** (0–1, nothing stirs), **albedo** (2–3, first
signal), **citrinitas** (4, at the wire) and **rubedo** (5+, the phoenix
rises). Reaching rubedo earns the Polyglot Poisoning Hunter badge. Your row lands in the *same ledger table* you
just learned to hunt — submit a prompt, become a row, watch yourself
get hunted. The board itself is just a KQL query you can audit.

**How to play, the disclosure, and the board query:
[docs/LEADERBOARD.md](docs/LEADERBOARD.md).**

> **Disclosure, plainly:** Submissions are prompt text only — never
> model responses. Prompts are logged, scored, and shown on the live
> leaderboard, and may inform LSI's published research and detection
> rules — anonymized, always. Nothing is sent unless you choose to
> submit. Share scores and patterns — never harmful outputs.

## What this repo is — and is not

- **V1 and V2 only.** Everything here is a direct application of
  published methodology (translation attacks, resource-level decay,
  register/temporal framing) against gray-zone, benchmark-register
  questions (locksport, everyday ethics, generic scenarios). Nothing
  touches a real person, company, or target.
- **Nothing beyond the two open levels is in this pack.** The extended
  research collection is packaged separately and described openly —
  hybrid language forms, stacked signals, tuned composition. Ask us
  about any of it; it is not a secret, just a different distribution.
- The corpus translations are original LSI work, released for
  education and research.

### Sources (the samples' ancestry — cite them, it's good practice)

- Deng et al., *Multilingual Jailbreak Challenges in LLMs*, ICLR 2024 (arXiv:2310.06474)
- Yong, Menghini & Bach, *Low-Resource Languages Jailbreak GPT-4* (arXiv:2310.02446)
- Faruna, *LSR: Linguistic Safety Robustness Benchmark for Low-Resource West African Languages* (arXiv:2603.19273)
- Said & Sani, *Safe in the Future, Dangerous in the Past* (arXiv:2512.24556)
- Background: Upadhayay & Behzadan, *Sandwich Attack* (arXiv:2404.07242) · Poppi, Yong et al., NAACL 2025 Findings (2025.findings-naacl.126) · Yong et al., EMNLP 2025 (2025.emnlp-main.800)

## License

- **Code** (probe.py, scripts, tests): MIT
- **Content** (sample texts, corpus, docs): CC BY-NC 4.0 — free to
  learn from and remix for research/education; commercial reuse
  requires an LSI license.

See [LICENSE](LICENSE).

---

**Contact:** almadisahara.com · linguisticsecurityinstitute@gmail.com
Workshop listing: DEATHCon 2026 (online + San Diego) & BSides San Diego.
