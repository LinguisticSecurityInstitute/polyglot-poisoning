# Contributing

Thank you for helping improve The Living Atlas. This repository is the public
participant kit, so every change has to stay safe to hand to a room of
strangers.

## What helps most

- **Corrections** — a wrong count, a broken link, a command that does not run
  as written, a query that returns nothing it should.
- **Clearer explanations** of a hunt, a field or a step that confused you.
- **New prompt samples** in a language or variety the pack does not cover yet,
  following the rules below.
- **Detection rules** you derived from the hunts and can explain in one sentence.

## Rules for prompt samples

- Prompts only, never model responses.
- Gray-zone, benchmark-register requests: nothing that names or targets a real
  person, company, system or place.
- One change per sample. A sample changes the language, *or* the dialect, *or*
  the framing — not several at once — so its score teaches something.
- `V1` is a standard or direct form; `V2` is a regional variety or dialect.
  Register, framing, code-switching and transliteration are recorded in
  `Patterns`, never as a new Variant.
- Say in `samples/README.md` why the sample is there.

## Before you open a pull request

```bash
python3 tests/check_setup.py         # SETUP OK
python3 tests/check_repository.py    # REPOSITORY OK
python3 probe.py samples/
```

The same checks run automatically on every pull request.

## Never commit

Flags, challenge solutions, planting scripts, the event receiver, ingestion
endpoints, DCR or stream settings, tokens, keys, or `.env` files. The
`.gitignore` blocks the common names, but it is a seatbelt, not a guarantee —
check `git status` before you commit.

## License of contributions

Code and queries you contribute are MIT; prompts, data and documentation are
CC BY-NC 4.0, as described in [`LICENSES.md`](LICENSES.md). By contributing you
agree your contribution is released under those terms and credited by the
handle you choose.
