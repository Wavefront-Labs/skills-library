---
id: computing-software.software-engineering.cobol.structured-cobol-style
name: structured-cobol-style
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, structured-cobol-style, cobol-style, coding-standards, naming-conventions, structured-programming]
level: practitioner
status: draft
description: "Write COBOL that survives decades: numbered paragraphs, prefixes, scope terminators, one exit and clear flags."
sources:
  - https://www.iso.org/
  - https://www.ibm.com/docs/en/cobol-zos
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Structured COBOL style and naming conventions
**Goal:** a team standard that makes review and maintenance cheap.

- Name data with a prefix per origin: `WS-` working storage, `LS-` linkage, `IN-`/`OUT-` file records, `SW-` switches, `CNT-` counters.
- Paragraph names: `0000-MAIN`, `1000-INIT`, `2100-READ-NEXT`, ending with a `-EXIT` for THRU ranges.
- One entry, one exit: driver paragraph calls PERFORMs and ends with GOBACK; avoid GO TO except to a paragraph exit.
- Scope terminators on every conditional/loop; period only at the end of a paragraph.
- No ALTER, no NEXT SENTENCE, no fall-through between paragraphs; no redefining with different intent.
- Comments say why, not what; keep a change-log header with dates and ticket ids.
- Copybooks for every shared layout; single-source constants (88-levels, CONSTANT).
- Limit program size: split by function once past a few thousand lines.

## Gotchas
- Style rules need tooling to stick: use a formatter or review checklist (e.g. IDE linter or `cobc -Wall`).
- Do not mass-reformat legacy code without a regression test; diffs destroy history.

## Self-check
Pick a legacy paragraph and refactor it to the standard; run the golden-file regression.
