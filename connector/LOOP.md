# How the library improves itself

The library gets better from use, but it never edits itself. Every change goes through a normal pull request and a
human review. The loop is: **observe, propose, gate, merge.**

## What is observed

- `report(id, outcome)` calls (`used`, `not_useful`, `wrong`, `gap`) written to a local log by whoever uses the library.
- Research that had to happen anyway (the agent searched the web or read docs because the library had nothing).
- Edits people make to a skill's output: a correction is the strongest signal there is.

All of it is local. Nothing is sent anywhere unless a person copies it into an issue or a pull request.

## What is proposed

`python tools/harvest.py` turns a log into four lists:

| List | Meaning | Action |
|---|---|---|
| GAPS | tasks nobody found coverage for, most frequent first | write the skill, from verified behaviour |
| FIX FIRST | skills reported `wrong` | re-check against the source before anything else |
| WEAK | skills reported `not_useful` more than `used` | improve the description, tags or body; often the content is fine and only the words are wrong |
| WORKING | most used skills | do not break these |

A contributor, a maintainer or an agent working through a normal branch drafts the change. Updates are **small and
incremental** (add the missing gotcha, fix the wrong flag), never a wholesale rewrite of a skill: rewriting loses the
accumulated detail, and the research on evolving contexts calls this failure "context collapse".

## What gates a change

- **Content**: the evidence rule in `CONTRIBUTING.md`. A skill reaches `verified` only if every claim was fetched from an
  official source, run, or computed. A report, however many, never promotes a status.
- **Retrieval**: any change to descriptions, tags, the silence rule or the ranking must not make held-out retrieval
  worse (`tools/retrieval_eval.py` on queries that were not used to tune it). Tune on one set, judge on another, or
  you only measure your own vocabulary.
- **Behaviour**: changes to the protocol are checked with the end-to-end harness in `connector/eval/` (agent with and
  without the library, blind grading). If a change does not help there, it does not ship.
- **Review**: a maintainer reads the diff. Nothing merges itself.

## Where it comes from

The structure borrows two ideas. From *Interpretable Context Methodology* (Van Clief and McDermott, 2026): files and
folders as the architecture, with each step loading only the context its contract names, and every output an edit
surface a human can correct. From *Agentic Context Engineering* (arXiv 2510.04618): improve a context by a
generate, reflect, curate loop that applies small deltas. A method in this library is the same shape as an ICM
workspace: its phases are the stages, its ingredient table is each stage's reference layer, and its gates are the
review points.

## Limits

Reports are only as honest as whoever files them, so the end-to-end test is the arbiter, not the reports. The loop is
aimed at what a library can do that a strong model cannot: the non-obvious traps people actually hit. Find them,
write them down once, and keep them correct.
