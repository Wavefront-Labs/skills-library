---
id: computing-software.software-engineering.cobol.literals-figurative
name: literals-figurative
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, literals-figurative, cobol-lexical, figurative-constants, hex-literal, nonnumeric-literal]
level: intro
status: docs-checked
description: "Write correct literals and use ZERO, SPACE, HIGH-VALUES, LOW-VALUES, QUOTE and ALL literal."
sources:
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Literals and figurative constants (GnuCOBOL)
**Goal:** initialize and compare fields with the right literal forms.
- Numeric: integers (`56`, `-54`), fixed point (`-2.95`) and floating point with `E` notation (`9.92E25`, `5.7E-14`, with optional `+`/`-` on mantissa and exponent). Hexadecimal numeric forms include `H#` / `X#`; also binary `B#` and octal `O#`.
- Alphanumeric literals are not valid in arithmetic until converted with `NUMVAL`, `NUMVAL-C` or `NUMVAL-F`. National literals are `N"..."` / `NC"..."` and hex `NX"..."`; Boolean literals `B"..."` and `BX"..."`.
- Figurative constants: `ZERO`/`ZEROS`/`ZEROES` (numeric 0), `SPACE`/`SPACES`, `QUOTE`/`QUOTES` (double quote), `LOW-VALUE(S)` (lowest character in the collating sequence), `HIGH-VALUE(S)` (highest), and `NULL` (all zero bits regardless of collating sequence).
- A figurative constant fills as long a sequence as needed; where a specific length is required (such as a CALL argument) it may not be used: `CALL "SUBPGM" USING SPACES` is invalid.
```cobol
MOVE SPACES TO WS-NAME
MOVE HIGH-VALUES TO WS-KEY-MAX
05 FILLER PIC 9(10) VALUE ZEROS.
```
- Create your own with the `SYMBOLIC CHARACTERS` clause of SPECIAL-NAMES.

## Gotchas
- LOW-VALUES is the ASCII NUL only when no collating sequence changes apply; use `NULL` if you need zero bits.

## Self-check
Hex dump a field after `MOVE LOW-VALUES` and after `MOVE NULL`; compare them under your collating sequence.

## Checked
2026-11-02. Checked against the GnuCOBOL Programmer's Guide (Literals, Figurative Constants). Removed: the doubling of the delimiter, `X'..'` alphanumeric hex, `ALL 'ab'`, the EBCDIC HIGH-VALUES discussion, the claim that `MOVE ZERO TO alpha-field` writes '0', and the SPACE-to-numeric claim.

Method: documentation only; no commands were run.
