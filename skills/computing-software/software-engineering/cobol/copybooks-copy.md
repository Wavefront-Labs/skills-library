---
id: computing-software.software-engineering.cobol.copybooks-copy
name: copybooks-copy
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, copybooks-copy, cobol-storage-sections, copybook, copy-replacing, copy-library]
level: practitioner
status: docs-checked
description: "Share record layouts and constants through COPY members and adjust them with REPLACING."
sources:
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
  - https://gnucobol.sourceforge.io/doc/gnucobol.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# COPY statement and REPLACING (GnuCOBOL)
**Goal:** one definition of each record, reused everywhere.
```cobol
COPY CUSTREC.
COPY CUSTREC REPLACING ==:PFX:== BY ==IN==.
COPY CUSTREC REPLACING LEADING ==CUST== BY ==OLD==.
```
- A period is mandatory at the end of every COPY statement.
- `==...==` is pseudo-text. A phrase clause replaces whole words, identifiers or literals (not part of a word); `LEADING` or `TRAILING` replace the start or end of words. A null replacement `====` deletes the match.
- COPY statements are resolved before compilation, and a COPY inside a copybook is resolved repeatedly until none remain. Recent releases check for recursive copy files.
- Search order: the program's folder, folders named by `-I`, folders in the `COBCPY` environment variable, then the folder in `COB_COPY_DIR`.
- For `COPY XXXXXXXX.` the compiler tries `XXXXXXXX.CPY`, `.CBL`, `.COB`, the lower-case forms, then the bare name; `-ext` adds another extension. The name is case-sensitive on Unix.
- `SUPPRESS PRINTING` is accepted but does nothing.

## Gotchas
- Prefix placeholders such as `:PFX:` let the same layout appear twice in one program.
- Recompile every dependent program after a copybook change.

## Self-check
Compile with a listing (`-t listing.lst`) and check that the COPY expansions show the expected names after REPLACING.

## Checked
2026-11-02. Checked against the GnuCOBOL Programmer's Guide (COPY, REPLACE, Locating Copybooks, compile-time environment variables) and the cobc option list. Removed: z/OS SYSLIB statements, `COB_COPY_EXT` (not in the docs), and the requirement that a copybook starts at level 01 or 05.

Method: documentation only; no commands were run.
