---
id: computing-software.software-engineering.cobol.edited-pictures
name: edited-pictures
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, edited-pictures, cobol-edited-pictures, numeric-edited, zero-suppression, floating-currency, cr-db]
level: practitioner
status: docs-checked
description: "Format numbers and dates for reports with edited PICTURE strings."
sources:
  - https://www.iso.org/
  - https://www.ibm.com/docs/en/cobol-zos
  - https://gnucobol.sourceforge.io/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Editing symbols Z, *, $, comma, period, CR, DB, +, -, B, 0, /
**Goal:** print-ready fields.

| Picture | Value | Result | Note |
|---|---|---|---|
| `999.99` | 1.234 | `001.23` | special insertion: the period is the decimal point |
| `$9999.99CR` | -123.45 | `$0123.45CR` | fixed insertion; CR/DB must be the rightmost two positions |
| `$9999.99CR` | +123.45 | `$0123.45` | CR becomes two spaces when positive or zero |
| `$,$$$,999.99` | -1234.56 | `$1,234.56` | floating currency; sign lost without a sign symbol |
| `+,+++,999.99` | -123456.789 | `-123,456.78` | floating sign |
| `****.99` | 0 | `****.00` | `*` replacement |
| `ZZZZ.99` | 0 | `.00` shown after spaces | `Z` suppression stops at the decimal point |
| `ZZZZ.ZZ` | 0 | all spaces | all positions are Z, so a zero value gives spaces |
| `*,***.**+` | -123.45 | `**123.45-` | trailing sign |

- Sign control symbols: `+` shows + or -; `-` shows a space or -; `CR` and `DB` show two spaces for positive or zero values and the letters for negative. Only one currency symbol and one editing-sign symbol may appear in a fixed insertion picture; `+` or `-` must be the first or last character.
- Simple insertion characters are `B` (space), `0`, `/` and `,`; each counts in the item's size (`99,999` with 12345 gives `12,345`).
- A numeric-edited item is a receiving item for editing; when it is the sending item of a MOVE to a numeric or numeric-edited item the compiler de-edits it to its numeric value, so a plain MOVE converts back (NUMVAL is for alphanumeric text).
- Floating insertion needs a string of at least two floating symbols (`cs`, `+` or `-`, mutually exclusive); the leftmost symbol is only the position for the inserted character and the remaining positions can hold digits. To avoid truncation the picture must be one position longer than the sending digits plus the non-floating insertion symbols.
- `Z` and `*` are mutually exclusive in one picture; do not combine `*` with BLANK WHEN ZERO.

## Gotchas
- Editing happens only when a value is moved into the edited item; MOVE aligns on the decimal point.
- A picture may hold the actual decimal point or the assumed `V`, not both.

## Self-check
Move 0 and -0.5 into `ZZ9.99` and `-ZZ9.99` and compare the printed strings with the rules above.

## Checked
2026-11-08: confirmed against the Enterprise COBOL for z/OS 6.4 Language Reference (data description entry, PICTURE editing sections): simple, special, fixed and floating insertion editing, zero suppression and replacement editing with their example tables, and the MOVE de-editing rule for numeric-edited senders. Replaced the earlier example table with the documented examples (the earlier `ZZZ,ZZ9.99`-style rows were not in the manual), removed the "arithmetic not allowed" and "Z right of V is an error" claims, and corrected the floating symbol digit-position wording. GnuCOBOL behaviour was not checked.
Method: documentation only; no commands were run.
