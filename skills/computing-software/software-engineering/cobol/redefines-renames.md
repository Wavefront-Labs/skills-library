---
id: computing-software.software-engineering.cobol.redefines-renames
name: redefines-renames
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, redefines-renames, redefines, renames, level-66, data-overlay, alternate-view]
level: practitioner
status: docs-checked
description: "Overlay storage with REDEFINES for alternate record views and group a range of fields with RENAMES."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# REDEFINES and RENAMES
**Goal:** view the same bytes two ways safely. Rules below are from the Enterprise COBOL for z/OS 6.4 Language Reference.

```cobol
01 WS-DATE-NUM PIC 9(8).
01 WS-DATE-PARTS REDEFINES WS-DATE-NUM.
   05 WS-YYYY PIC 9(4).
   05 WS-MM   PIC 99.
   05 WS-DD   PIC 99.
```
- `REDEFINES data-name-2` must be the first entry after the redefining item's name (or FILLER, or the level number). Both items must be at the same level in the hierarchy (the level numbers need not match). Neither can be level 66 or 88, and neither can have OCCURS DEPENDING ON; the redefined item cannot have OCCURS itself, though it may sit under an OCCURS item (then do not subscript the name in REDEFINES).
- Redefinitions must immediately follow the redefined area, with no intervening entries that define new character positions. One area can have several redefinitions, each naming either the original or the preceding item.
- The redefining item and its subordinates cannot contain a VALUE clause. EXTERNAL cannot be combined with REDEFINES.
- The redefining item may be larger than the redefined one, with one exception: if the redefined item is an external data record, the redefining item must not be larger.
- When several 01 entries follow one FD, they implicitly redefine each other; do not write REDEFINES on those.
- All descriptions stay in effect together: a `MOVE` into either name writes the same storage. A redefining item with a different usage does not convert the data, so `ADD B TO A` and `ADD C TO A` give different results when B is DISPLAY and C (its redefinition) is COMP-4.
- `66 NEW-NAME RENAMES FIELD-A THRU FIELD-C.` defines an alphanumeric group spanning from the first elementary item of FIELD-A to the last of FIELD-C (or aliases one item when THRU is omitted). Level-66 entries must follow the last data description entry of the record. A 66 cannot rename a 01, 66, 77 or 88 item, and no OCCURS may apply to the items renamed (or between them). FIELD-C must not end before FIELD-A, and cannot be wholly inside it.

## Gotchas
- Never use REDEFINES to reinterpret binary or packed fields as text without understanding their encoding.
- Writing through one view changes the other; stale data is the usual bug.
- Prefer separate working-storage items and MOVE when performance is not critical.

## Self-check
Set the numeric field to 20251102 and DISPLAY the parts; expect 2025, 11, 02.

## Checked
2026-11-08. Confirmed against the Enterprise COBOL for z/OS 6.4 Language Reference PDF: REDEFINES clause, REDEFINES clause considerations and examples, RENAMES clause. Corrected: the old text said the redefining item should not be larger; the manual allows it except for external data records. Removed: the exception for 88 levels under VALUE, and the ASCII/EBCDIC remark, which the sections do not state.
Method: documentation only; no commands were run.
