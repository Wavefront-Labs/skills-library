---
id: computing-software.software-engineering.cobol.sign-clause-sync
name: sign-clause-sync
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, sign-clause-sync, sign-separate, synchronized, justified-right, blank-when-zero, data-layout]
level: advanced
status: docs-checked
description: "Use SIGN, SYNC, JUSTIFIED RIGHT and BLANK WHEN ZERO clauses and understand their byte-layout side effects."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SIGN, SYNCHRONIZED, JUSTIFIED and BLANK WHEN ZERO
**Goal:** control the physical layout of a field. Rules below are from the Enterprise COBOL for z/OS 6.4 Language Reference; other compilers differ in detail.

- `SIGN IS LEADING|TRAILING [SEPARATE CHARACTER]` applies to signed numeric items (an `S` in the PICTURE) of USAGE DISPLAY or NATIONAL, or to a group containing such items (a subordinate SIGN clause overrides the group's). Without SEPARATE, the sign is associated with the leading or trailing digit position (the `S` is not counted in the item size). With SEPARATE, the sign is its own character position holding `+` or `-` (the `S` is counted in the size). SIGN without SEPARATE needs USAGE DISPLAY; SEPARATE also allows NATIONAL.
- If an FD has a CODE-SET clause, signed numeric items in that file must use SIGN IS SEPARATE.
- `SYNCHRONIZED` (SYNC), also written with LEFT or RIGHT (syntax checked, no effect on execution): never required, but can improve performance for binary items used in arithmetic. It can be given on an elementary item or a level-01 group (every elementary item inside is then synchronized). It aligns USAGE BINARY/COMPUTATIONAL items on their natural boundary; COMP-1 goes on a fullword and COMP-2 on a doubleword boundary. For USAGE DISPLAY, PACKED-DECIMAL, NATIONAL and UTF-8 items it has no effect. The item's own length is unchanged; the compiler inserts slack bytes within records before synchronized items where needed, so the group length can grow. Without SYNC, no slack bytes are reserved for binary items.
- `JUSTIFIED RIGHT` (JUST) is elementary-level only and for alphabetic, alphanumeric, DBCS or national receiving items (not numeric or edited items, nor level 66 or 88). Data is aligned at the rightmost position; a longer sender is truncated on the left and a shorter one leaves spaces on the left. It does not affect VALUE.
- `BLANK WHEN ZERO` makes an item contain only spaces when its value is zero. It is allowed on numeric or numeric-edited elementary items without the picture symbol `S` or `*`, with USAGE DISPLAY or NATIONAL; on a numeric picture it makes the item numeric-edited.
```cobol
05 AMT-OUT PIC S9(5).99 SIGN IS TRAILING SEPARATE.
05 LBL     PIC X(10) JUSTIFIED RIGHT.
05 QTY-ED  PIC ZZZ9 BLANK WHEN ZERO.
```

## Gotchas
- Slack bytes from SYNC change group sizes and file record layouts; do not SYNC fields in a record that maps to an external layout.
- A REDEFINES of a synchronized item needs the redefined item to be correctly aligned for it.
- BLANK WHEN ZERO cannot be combined with a signed picture (`S`) item.

## Self-check
DISPLAY a negative `S9(3)` without SEPARATE and with it; the second shows a literal `-`.

## Checked
2026-11-08. Confirmed in full against the Enterprise COBOL for z/OS 6.4 Language Reference PDF: SIGN clause, SYNCHRONIZED clause (table of effects, slack bytes), JUSTIFIED clause and BLANK WHEN ZERO clause sections. Removed: the claim about EBCDIC overpunch characters, the advice to verify slack bytes with the compiler map, and the claim that the sign overpunches a digit "without SEPARATE" was reworded to the documented "associated with the leading or trailing digit position".
Method: documentation only; no commands were run.
