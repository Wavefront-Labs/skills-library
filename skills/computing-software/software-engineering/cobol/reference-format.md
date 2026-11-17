---
id: computing-software.software-engineering.cobol.reference-format
name: reference-format
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, reference-format, cobol-structure, fixed-format, free-format, area-a-area-b, column-72]
level: practitioner
status: docs-checked
description: "Place COBOL source correctly in fixed (columns 1-72) or free format: sequence area, indicator column, Area A and Area B."
sources:
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
  - https://gnucobol.sourceforge.io/doc/gnucobol.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fixed and free reference formats (GnuCOBOL)
**Goal:** avoid the classic column errors.
Fixed format (the default):
- Columns 1-6 sequence number area (ignored). Column 7 indicator: space, `*` comment, `-` continuation (needed only when a literal, reserved word or user-defined word is split), `/` comment (GnuCOBOL does not form-feed a listing), `D` or `d` debugging line.
- Area A is columns 8-11: division, section and paragraph headers, level numbers 01 and 77, FD and SD. Area B is columns 12-72: everything else.
- Columns 73-80 are ignored by the compiler, so text past column 72 disappears from the program.
Free format: `-free` (or `-F`, `-fformat=free`) starts the compiler in free format; the program text area starts in column 1 and runs to the end of the line (255 characters). `>>SOURCE FORMAT IS FREE` and `FIXED` switch formats inside the source; `-fixed` selects fixed format.
- Without a switch the compiler autodetects the format from the indicator on the first line: fixed for correct indicators, free for incorrect ones.
- Comments: full-line `*` in column 7 (fixed) or `*>` as first non-blank text (free); `*>` also starts a partial-line comment (column 7 or later in fixed format, any column in free).
- Debugging lines: `D` in column 7 (fixed) or `>>D` first on the line (free), compiled when `-fdebugging-line` is given or `WITH DEBUGGING MODE` is in SOURCE-COMPUTER.

## Gotchas
- Code past column 72 is not an error; it silently becomes part of the ignored area.
- Convert tabs to spaces before committing.

## Self-check
Compile with `cobc -Wall`; a statement lost past column 72 usually shows as an undefined-name or missing-period diagnostic.
## Checked
2026-11-02. Checked against the GnuCOBOL Programmer's Guide (source formats, comments, Fixed Format areas) and the manual (Source format). Corrected: `/` in column 7 is a comment that GnuCOBOL does not honour with a form-feed. Removed: IBM Enterprise COBOL statements and the ISO 2002 attribution, long-literal continuation steps, and the claim that tabs expand differently across editors.

Method: documentation only; no commands were run.
