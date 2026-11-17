---
id: computing-software.software-engineering.cobol.set-index-statement
name: set-index-statement
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, set-index-statement, cobol-tables, set-up-by, set-down-by, index-arithmetic]
level: practitioner
status: docs-checked
description: "Manipulate indexes with SET TO, UP BY and DOWN BY, and convert between indexes and integers."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SET for indexes
**Goal:** do index arithmetic legally (Enterprise COBOL for z/OS 6.4 wording).

```cobol
SET IX TO 1
SET IX UP BY 1
SET IX DOWN BY 2
SET WS-NUM TO IX
SET IX TO WS-NUM
SET IX2 TO IX
```
- Format 1 `SET receiver TO sender`: receiver is an index-name, an index data item (USAGE INDEX) or an elementary integer item; sender is an index-name, index data item, integer item or a positive integer literal.
- Valid combinations (Table 52): an index-name can be sent to an index-name, an index data item or an integer item; an index data item can be sent to an index-name or an index data item (no conversion), not to an integer item; an integer item or literal can be sent only to an index-name.
- Format 2 `SET index UP BY | DOWN BY n`: n is an elementary integer item or a nonzero integer literal. The index value before and after must correspond to an occurrence number of the table.
- Index values can be given initially by SET, PERFORM VARYING, or SEARCH ALL.

## Gotchas
- An index must be initialised before it is used as a subscript; its initial value is undefined.
- A valid index value is from 1 to the table's highest occurrence number.
- After SEARCH or PERFORM the index can be undefined, so re-SET it before other table handling.
- A table subscripted by an index of another table needs equal element lengths, or the reference is not to the same element.
- Index data items cannot be used as subscripts.
- The sending value is taken at the start of the statement; overlapping sender and receiver gives an undefined result.

## Self-check
Loop IX from 1 to table size with PERFORM VARYING IX FROM 1 BY 1 and confirm each entry is visited once; after SET IX TO 5, SET WS-NUM TO IX leaves 5.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted) the SET statement formats 1 and 2 (Table 52), the Subscripting section (indexing and relative subscripting) and the INDEXED BY phrase. Confirmed all claims above. Removed: "only SET, PERFORM VARYING and SEARCH may change an index; ADD/MOVE invalid on index names" (not stated in these sections), "setting IX to 0 or above max is caught only with range checking" (IBM says only that the value must be valid), "index values are displacements" (not stated in the Language Reference), and the unread ISO, ibm.com/docs root and GnuCOBOL sources.
Method: documentation only; no commands were run.
