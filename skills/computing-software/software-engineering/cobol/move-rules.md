---
id: computing-software.software-engineering.cobol.move-rules
name: move-rules
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, move-rules, cobol-data-movement, move-statement, move-corresponding, truncation-padding]
level: intro
status: docs-checked
description: "Predict MOVE results between categories: alignment, padding, truncation and CORRESPONDING group moves."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MOVE rules, truncation and MOVE CORRESPONDING
**Goal:** know exactly what a MOVE does (Enterprise COBOL for z/OS 6.4 wording).

- Alphanumeric, alphabetic, alphanumeric-edited and DBCS receivers: data is aligned at the leftmost character and padded with spaces on the right or truncated on the right (JUSTIFIED modifies this).
- Numeric receivers: aligned on the assumed decimal point and truncated or zero-padded at either end; there is no rounding. A numeric-edited receiver is edited per its PICTURE or BLANK WHEN ZERO.
- A signed receiver gets the sender's sign (an unsigned sender gives a positive sign); an unsigned receiver gets the absolute value.
- Numeric to alphanumeric: an integer or ZERO sender is valid, a noninteger sender is not (Table 47). An operational sign is dropped (the unsigned value is moved).
- Alphanumeric to numeric: moved as if the sender were an unsigned integer; a literal or figurative constant sender must consist only of numeric characters.
- Group moves: if an alphanumeric group is sender or receiver the move is treated as alphanumeric to alphanumeric with no conversion, filling the receiver without regard to the elementary items inside. Dynamic-length groups cannot be moved.
- Receiving items are filled in the order written; the sender is unchanged. Overlapping operands give unpredictable results. INDEX, POINTER, FUNCTION-POINTER, PROCEDURE-POINTER and OBJECT REFERENCE items cannot be used in MOVE.
```cobol
MOVE CORRESPONDING IN-REC TO OUT-REC   *> matches same-named items
MOVE 'AB' TO WS-X10                    *> 'AB        '
```
- `MOVE CORRESPONDING` (CORR): both operands must be groups. Two subordinate items correspond when they have the same name and qualifiers, are not FILLER, at least one is elementary and the move is allowed, and neither has REDEFINES, RENAMES, OCCURS or USAGE INDEX/POINTER/PROCEDURE-POINTER/FUNCTION-POINTER/OBJECT REFERENCE. The result is as if each pair had its own MOVE.

## Gotchas
- A subscript or reference modifier on the sender is evaluated once, before the first receiver; on a receiver, just before that receiver is filled. So `MOVE A(B) TO B, C(B)` uses the new B for C(B).
- Data in a file record area can be moved only while the file is open.

## Self-check
Move 123.456 into `9(2)V9` and `9(4)V999`; by the alignment rules expect 23.4 and 0123.456.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted) the MOVE statement section (elementary move rules, Table 47, moves involving file record areas, group moves), Alignment rules and CORRESPONDING phrase. Confirmed all claims above. Removed: "moving a negative number to an unsigned field drops the sign silently" (reworded as IBM's absolute-value rule), "an alphanumeric literal to a numeric field is lax in some compilers" (replaced by IBM's numeric-characters-only rule), and the unread ISO, ibm.com/docs root and GnuCOBOL sources. The 23.4 and 0123.456 self-check results follow from the alignment rules; they were not run.
Method: documentation only; no commands were run.
