# Licensing — the whole map on one page

Two licenses: MIT for code and every runnable query, and CC BY-NC 4.0 for
everything else. This page is the authority on which is which.

| Bucket | License | File |
|---|---|---|
| Code, scripts, and **every runnable query or detection rule** | MIT | [`LICENSE`](LICENSE) |
| The prompt corpus and the practice data | CC BY-NC 4.0 | [`LICENSE-PROMPTS`](LICENSE-PROMPTS) |
| The teaching material | CC BY-NC 4.0 | [`LICENSE-CONTENT`](LICENSE-CONTENT) |

## Path by path

| Path | License |
|---|---|
| `probe.py`, `setup.sh`, `setup.ps1`, `tests/**` | MIT |
| `leaderboard/*.py`, `leaderboard/*.kql` | MIT |
| `detection/*.kql` | MIT |
| **Any KQL, rule or shell command quoted inside a document** | MIT |
| `samples/**` | CC BY-NC 4.0 |
| `data/practice_ledger.jsonl` | CC BY-NC 4.0 |
| `README.md`, `WORKSHOP.md`, `HUNTS.md`, `docs/**`, `ctf/**`, `season-1/**` | CC BY-NC 4.0 |
| `detection/DETECTION_RULE_TEMPLATE.md` (the prose) | CC BY-NC 4.0 |
| Slides, handout PDFs, seals, brand sheet | CC BY-NC 4.0 |
| `leaderboard/badges/*.png`, `*.svg` | CC BY-NC 4.0 |

**Why the queries are MIT even inside NonCommercial documents.** The
detection rules exist to be deployed at work, and most workplaces are
commercial. A NonCommercial or ShareAlike query would make this workshop
unusable in exactly the environments it was written for. So take the
queries to work — no permission, no attribution required, nothing to ask.

## What "NonCommercial" means here

This is guidance on how we read it, not a change to the legal text.

**No permission needed:**

- Running the workshop, or parts of it, for your own team
- Teaching it in a university or community course
- A conference talk, a blog post, a write-up, a lab exercise
- Forking the kit and adapting it for internal use
- Research that cites it — commercial employer or not
- Deploying any query or detection rule from it, anywhere, forever

**Ask first — one email, usually a quick yes:**

- Paid training, a paid course, or a paid workshop
- Bundling it into a product or a paid service
- Consulting deliverables sold to a client
- Anything where someone is charged for access to this material

<linguisticsecurityinstitute@gmail.com>

## A note on wording

The **code is open source**. The **content is not** — CC BY-NC is not an
OSI-approved open source license, because it
restricts commercial use, and Creative Commons advises against using CC
licenses for software.

Please describe the kit that way rather than calling the whole thing
"open source": *the tools are open source; the curriculum and corpus are
free to use and teach from, with commercial use by permission.*

## Names and marks — not covered by any license above

The licenses cover copyright. They do not grant any right to use the
names or marks:

> "Linguistic Security Institute", "LSI", "Polyglot Poisoning",
> "The Living Atlas", "The Living Atlas Leaderboard", "The Phoenix Corpus",
> "The Mithridate Project", and the LSI serpent-and-L mark.

You may say your work is **based on** or **adapted from** the Polyglot
Poisoning workshop by Sahara Al-Madi / Linguistic Security Institute —
that is the attribution we ask for. You may not name a fork, a course, a
product or an event in a way that suggests it is ours, endorsed by us, or
affiliated with us, without written permission.

In practice this clause does more work than either CC license. Copyright
cannot stop someone adapting openly licensed material; the name can stop
them passing the adaptation off as yours.

## If you want the legal code stored offline

The two CC files carry the official notice and the canonical link, which
is how Creative Commons says to apply a license. To keep a full copy in
the repository as well, download it unmodified rather than retyping it:

```bash
curl -L -o LICENSE-PROMPTS.legalcode.txt \
  https://creativecommons.org/licenses/by-nc/4.0/legalcode.txt
curl -L -o LICENSE-CONTENT.legalcode.txt \
  https://creativecommons.org/licenses/by-nc/4.0/legalcode.txt
```
