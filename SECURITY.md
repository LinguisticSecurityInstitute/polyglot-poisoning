# Security

## Reporting a problem

If you find something in this repository that should not be public — a
credential, an endpoint, a flag, a challenge solution, or personal data — or a
weakness in the kit's code, **do not open a public issue**. Email
**linguisticsecurityinstitute@gmail.com** with the file path and what you found.
We acknowledge reports within three working days.

## What this kit does and does not do

- `probe.py` reads text you give it and prints a score. It makes no network
  connections and runs no prompt through any model.
- `tests/check_setup.py`, `tests/check_repository.py` and
  `tests/mock_receiver.py` make no network connection beyond `127.0.0.1`.
- `leaderboard/submit.py` sends exactly one thing — your handle, your prompt,
  and an optional language and variant — to the receiver address you give it,
  and only when you run it. Use `--url http://127.0.0.1:8730` with the mock
  receiver to rehearse without sending anything off your machine.

## Safe handling of the material

- **Decode it. Do not execute it.** Prompts in the samples and the ledger are
  specimens: read, label and count them. Never paste one into a live model.
- **Prompts, not outputs.** Never share or submit a model's response.
- **Handles, not real names.**
- Workshop accounts are read-only on one table. If an account can write to the
  table or see ingestion configuration, report it to an organizer — that is a
  misconfiguration, not a feature.
