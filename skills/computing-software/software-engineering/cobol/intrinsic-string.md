---
id: computing-software.software-engineering.cobol.intrinsic-string
name: intrinsic-string
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, intrinsic-string, cobol-intrinsic, function-upper-case, function-trim, function-reverse, function-length]
level: practitioner
status: docs-checked
description: "Manipulate text with UPPER-CASE, LOWER-CASE, REVERSE, LENGTH and TRIM in modern COBOL."
sources:
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# String intrinsic functions (UPPER-CASE, TRIM, REVERSE, LENGTH)
**Goal:** replace INSPECT loops with one call.
```cobol
MOVE FUNCTION UPPER-CASE(WS-IN) TO WS-OUT
MOVE FUNCTION REVERSE(WS-IN)    TO WS-REV
COMPUTE WS-LEN = FUNCTION LENGTH(WS-IN)
MOVE FUNCTION TRIM(WS-IN) TO WS-OUT          *> both ends
MOVE FUNCTION TRIM(WS-IN TRAILING) TO WS-OUT
```
- `TRIM(string [, LEADING|TRAILING])` removes spaces; the second argument is a keyword, not a quoted string, and with none both ends are trimmed.
- `UPPER-CASE`, `LOWER-CASE` convert case; what counts as a letter can be affected by CHARACTER CLASSIFICATION in OBJECT-COMPUTER.
- `REVERSE` reverses byte by byte.
- `LENGTH` returns characters, not bytes; contrast `BYTE-LENGTH` and `LENGTH-AN`.
- `ORD(char)` returns the ordinal position in the program character set (ORD('!') is 34 in ASCII), so subtract one for the numeric code; `CHAR(integer)` is the inverse (add 1 to its argument).
- `CONCATENATE`, `SUBSTITUTE` and `SUBSTITUTE-CASE` are also provided.

## Gotchas
- ORD and CHAR are 1-based.

## Self-check
`FUNCTION LENGTH('ABC')` is 3; `FUNCTION REVERSE('ABC')` is `CBA`.

## Checked
2026-11-02. Checked against the GnuCOBOL Programmer's Guide function entries TRIM, UPPER-CASE, REVERSE, LENGTH, ORD, CHAR, and the intrinsic function index. Removed: standard-version and IBM release attributions, the `LENGTH OF` bytes claim, and the claim about TRIM of an all-space argument.

Method: documentation only; no commands were run.
