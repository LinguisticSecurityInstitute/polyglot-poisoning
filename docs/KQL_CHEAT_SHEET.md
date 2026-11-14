# KQL cheat sheet — Polyglot Poisoning

Everything you need to run the workshop in Microsoft Sentinel, on one sheet.
Every query here runs against `PolyglotPoisoning_CL`; the full pack, ready to
paste, is [`detection/WORKSHOP_QUERIES.kql`](../detection/WORKSHOP_QUERIES.kql).
Queries are MIT — take them to work.

---

## 1 · Get to the query pane

1. Sign in to the **Azure portal** with your own authorized **DEATHLab** account.
2. **Microsoft Sentinel** → select **`deathcon2026-sentinel`** → **Logs**.
3. Set the **time range to Last 30 days** before you type anything.
4. Find the table yourself: filter the **Tables** pane for `Polyglot` — it is under **Custom Logs**.

A shared link grants no permissions; access comes from your account. You need
read access to one table — never DCE, DCR, stream or ingestion permissions.
The DCE is an ingestion endpoint, not the table: you never query it.

## 2 · First queries

```kql
PolyglotPoisoning_CL
| take 20
```

```kql
PolyglotPoisoning_CL
| where UserPrincipal !endswith "@lb"      // drop leaderboard rows — do this first, every hunt
| take 20
```

```kql
PolyglotPoisoning_CL
| getschema
| project ColumnName, ColumnType           // expect exactly the seven columns below
```

## 3 · The seven columns

| Column | Type | What it is |
|---|---|---|
| `TimeGenerated` | datetime | when it landed |
| `UserPrincipal` | string | who — a handle ending in `@lb` is a leaderboard row |
| `Language` | string | language or regional code (`es-ES`, `ar-EG`, `mul` …) |
| `Variant` | string | `V1` standard or direct · `V2` regional variety or dialect |
| `RiskScore` | real | the probe's number; the alert fires at **5** |
| `Patterns` | string | shaping stamps, comma separated, no spaces |
| `PromptPreview` | string | first 200 characters — **read last** |

Hunt the six metadata columns. Read the seventh only after they have cut the
table down to a handful of rows.

## 4 · How KQL reads

A table goes in at the top; each `|` hands the current result to the next
line. It runs top to bottom, and it is **read-only** — nothing you type can
change the table. Press **Run** (Enter only adds a new line).

After every pipe, ask two questions: **what rows remain**, and **what does
one row represent now?**

**The five beats, in order:** inspect → reduce → count → reshape → explain.
Stuck? Ask which beat you are on.

## 5 · The seven operators

| Operator | What it does | Example |
|---|---|---|
| `where` | keep rows that match | `\| where Variant == "V2"` |
| `summarize` | group and aggregate — a row becomes a summary | `\| summarize Rows = count() by Language` |
| `count` | how many rows | `\| count` |
| `sort by` | order rows | `\| sort by RiskScore asc` |
| `project` | choose and order columns | `\| project Language, RiskScore, Patterns` |
| `mv-expand` + `split` | one row per item in a packed column | `\| mv-expand stamp = split(Patterns, ",") to typeof(string)` |
| `extract` | pull a piece out of text with a pattern | `\| extend part = extract("<PATTERN>", 1, PromptPreview)` |

Also useful: `dcount(Language)` counts **distinct** values; `count()` counts
rows. `has` matches whole terms; `contains` matches any substring.

## 6 · The four metadata moves

**Move 1 — reduce, one condition at a time.** Read the row count after each.

```kql
PolyglotPoisoning_CL
| where UserPrincipal !endswith "@lb"
| where Variant == "V2"
| count
```

**Move 2 — count.** After `summarize`, a row is a language summary, not a prompt.

```kql
PolyglotPoisoning_CL
| where UserPrincipal !endswith "@lb"
| summarize Rows = count() by Language
| sort by Rows desc
```

**Move 3 — split before you count.** Counting `Patterns` raw counts
*combinations*, so everything looks rare.

```kql
PolyglotPoisoning_CL
| where UserPrincipal !endswith "@lb" and isnotempty(Patterns)
| mv-expand stamp = split(Patterns, ",") to typeof(string)
| summarize Rows = count(), Langs = dcount(Language) by stamp
| sort by Rows asc
```

**Move 4 — look below the alert.** The interesting traffic scored 2 to 5 and
never fired.

```kql
PolyglotPoisoning_CL
| where UserPrincipal !endswith "@lb"
| where RiskScore >= 2 and RiskScore < 5
| summarize Rows = count() by Language, Variant
| sort by Rows desc
```

## 7 · The worked hunt, as a detection rule

The finding from Part 3: a stamp that lands in a **different language every
time** it appears. Anchor + context + threshold:

```kql
PolyglotPoisoning_CL
| where UserPrincipal !endswith "@lb" and isnotempty(Patterns)
| mv-expand stamp = split(Patterns, ",") to typeof(string)
| summarize Rows = count(), Langs = dcount(Language) by stamp
| where Rows >= 4 and Langs == Rows        // anchor: Langs == Rows · context: Rows >= 4
```

Then read the survivors last, lowest score first (threshold: under the alert):

```kql
PolyglotPoisoning_CL
| where UserPrincipal !endswith "@lb"
| where Patterns has "<STAMP>"              // the stamp the rule named
| project TimeGenerated, Language, Variant, RiskScore, Patterns, PromptPreview
| sort by RiskScore asc
```

Avoid the shortcut "a stamp in four or more languages": ordinary stamps span
almost every language on the live table, so it floods.

## 8 · The five hunts (fill the blanks — answers in [`HUNTS.md`](../HUNTS.md))

On the live table, add `| where UserPrincipal !endswith "@lb"` as the second line.

| # | Hunt | Skeleton |
|---|---|---|
| 1 | Metadata anchors | `\| where PromptPreview contains "<ANCHOR>"` then `\| where Variant == "<CODE>"` |
| 2 | Stacking & frequency | `\| mv-expand stamp = <SPLIT>(Patterns, ",") to typeof(string)` `\| summarize rows = count() by <COLUMN>` |
| 3 | Threshold evasion | `\| where RiskScore >= <LOW> and RiskScore < <HIGH>` `\| summarize band_rows = count() by Language` |
| 4 | Correlation | join on `UserPrincipal` ↔ Sysmon `User` within `<SECONDS>` — needs a second table, run at work |
| 5 | Translate last | metadata filters only until **3 rows or fewer**, then read |

## 9 · The two challenges

| # | Challenge | Level | Approach |
|---|---|---|---|
| 1 | **Babel's Ledger** | easy | Move 1: add one condition at a time; a score filter alone returns more than one row |
| 2 | **Rosetta Fragments** | advanced | Moves 3 and 4, as in section 7: split, find the stamp, order by `RiskScore` |

Drop `@lb` rows first. Open the field card, and check your answer's shape
against it before you spend one of your ten attempts. Rules and hints:
[`ctf/README.md`](../ctf/README.md).

## 10 · A correct query that returns nothing

1. **Time range** narrower than the data — set Last 30 days.
2. **Table name** misspelled — click it from the Tables pane.
3. **Rows not landed yet** — new submissions take about 5–15 minutes.
4. **Two filters that cannot both be true.**
5. **Wrong workspace** — the name is shown above the editor.

**Find it without guessing:** delete the last pipe and run again; keep
deleting until rows return, then add conditions back one at a time. The pipe
that empties the result is the bug.

## 11 · Rules

- **Decode it. Do not execute it.** Read previews inside the query; never paste
  one into a live model.
- **Prompts, not outputs.** **Handles, not real names.**
- Don't share flags or full solutions. "What does `mv-expand` do?" is a good
  question; a query that solves a challenge is not a good answer.
