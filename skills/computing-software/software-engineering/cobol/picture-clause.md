---
id: computing-software.software-engineering.cobol.picture-clause
name: picture-clause
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, picture-clause, pic, pic-9, pic-x, implied-decimal, scaling-position, signed-display]
level: intro
status: docs-checked
description: "Write PICTURE strings correctly: digits, characters, sign, implied decimal point and scaling positions."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PICTURE symbols 9, X, A, S, V, P
**Goal:** size and type fields so values neither truncate nor waste storage. Limits below are for Enterprise COBOL for z/OS 6.4; check your compiler.

| Symbol | Meaning |
|---|---|
| `9` | one decimal digit (one character position for DISPLAY and NATIONAL) |
| `X` | any allowable character of the computer's alphanumeric set |
| `A` | a letter of the Latin alphabet or a space |
| `S` | presence of an operational sign; not counted in the size unless SIGN ... SEPARATE CHARACTER applies |
| `V` | location of the assumed decimal point; not a character position |
| `P` | assumed decimal scaling position; not counted in the size of the item |
- The PICTURE character-string can hold at most 50 characters.
- Digit limits: an external decimal (zoned) item or PACKED-DECIMAL item has at most 18 digits with ARITH(COMPAT) and 31 with ARITH(EXTEND). Other computational items are limited to 18 digits.
- `PIC S9(4)V99 COMP-3` has 6 digits plus a sign; packed decimal stores two digits per byte with the sign sharing the last byte, so it occupies 4 bytes. IBM notes that an odd number of digits uses all the bits.
- Binary items take 2 bytes for 1-4 digits, 4 bytes for 5-9 digits and 8 bytes for 10-18 digits.
- `P` may appear only as a continuous string at the leftmost or rightmost digit positions. `PIC 9(3)PP` stores three digits and has the assumed decimal point to the right of the Ps, so the stored `123` has the value 12300 in numeric operations (the P digits count as zeros). In other operations the P positions are ignored and not counted in the operand size.
- `DECIMAL-POINT IS COMMA` in SPECIAL-NAMES swaps the roles of period and comma in PICTURE strings and numeric literals.

## Gotchas
- `V` is not stored, so DISPLAY of a PIC 9V99 item shows `150` with no point; use an edited picture for display.
- For zoned decimal (USAGE DISPLAY) items each digit takes one byte and the sign lives in the 4 high-order bits of the low-order byte, so a signed item's last byte differs from the plain digit byte in a hex dump.
- A numeric MOVE aligns the data on the assumed decimal point and truncates or zero-pads as needed, so a value too large for the receiver loses high-order digits. Arithmetic with ON SIZE ERROR is the way to detect overflow; without it, truncation rules apply.

## Self-check
Move 1234.56 to `PIC 9(3)V99` and DISPLAY; expect 23456 (high digit lost), confirming the alignment and truncation rule.

## Checked
2026-11-08. Confirmed against the Enterprise COBOL for z/OS 6.4 Language Reference PDF: PICTURE clause (50-character limit, symbol table, P symbol rules), computational items and USAGE (18/31 digit limits, binary sizes, PACKED-DECIMAL layout, zoned decimal sign position), Alignment rules (numeric receiving items) and SIZE ERROR phrases. Corrected: the old text said the packed example held 7 digits; the picture has 6 digits plus sign. Removed: the ISO 85 digit limit and the specific EBCDIC hex bytes.
Method: documentation only; no commands were run.
