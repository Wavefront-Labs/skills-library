---
id: computing-software.software-engineering.cobol.inspect-tally-replace
name: inspect-tally-replace
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, inspect-tally-replace, cobol-strings, inspect-tallying, inspect-replacing, inspect-converting]
level: practitioner
status: docs-checked
description: "Count, replace and translate characters with INSPECT, including BEFORE/AFTER INITIAL limits."
sources:
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# INSPECT TALLYING, REPLACING and CONVERTING
**Goal:** scrub and count text in place.
```cobol
MOVE ZERO TO WS-N
INSPECT WS-TEXT TALLYING WS-N FOR ALL ','
INSPECT WS-TEXT REPLACING ALL ',' BY ';'
INSPECT WS-TEXT CONVERTING 'abcdefghijklmnopqrstuvwxyz'
                        TO 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
INSPECT WS-TEXT REPLACING LEADING ZEROS BY SPACES
```
- INSPECT does not zero the tally counter: initialize it first.
- TALLYING phrases: `ALL`, `LEADING`, `TRAILING`, `CHARACTERS`. REPLACING phrases: `ALL`, `FIRST`, `LEADING`, `TRAILING`, `CHARACTERS`. Range limits: `BEFORE INITIAL x`, `AFTER INITIAL x`, both allowed in either order.
- CONVERTING cannot be combined with TALLYING or REPLACING; when TALLYING and REPLACING are both coded, TALLYING comes first.
- REPLACING swaps a substring for an equally sized one. To replace with a different length use `FUNCTION SUBSTITUTE` or `SUBSTITUTE-CASE`.
- The inspect subject may be a literal or intrinsic function result only with TALLYING.
- For case conversion `FUNCTION UPPER-CASE(...)` is an alternative.

## Gotchas
- `REPLACING` changes the data item, so inspect a copy if you need the original.

## Self-check
Tally commas in `a,b,,c`; expect 3.

## Checked
2026-11-02. Checked against the GnuCOBOL Programmer's Guide INSPECT statement and the UPPER-CASE and SUBSTITUTE function entries. Removed: the claim that CONVERTING strings must be the same length (the Guide does not state it).

Method: documentation only; no commands were run.
