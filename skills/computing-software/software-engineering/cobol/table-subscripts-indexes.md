---
id: computing-software.software-engineering.cobol.table-subscripts-indexes
name: table-subscripts-indexes
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, table-subscripts-indexes, cobol-tables, subscript-vs-index, index-name, table-handling]
level: practitioner
status: docs-checked
description: "Choose subscripts (numeric data items) or indexes (index-names) and avoid mixing them wrongly."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subscripts versus indexes
**Goal:** address table entries legibly and correctly (Enterprise COBOL for z/OS 6.4 wording).

```cobol
01 WS-I PIC 9(4) COMP.
01 TBL.  05 ENT OCCURS 100 INDEXED BY IX PIC X(8).
MOVE 'A' TO ENT(WS-I)
SET IX TO 5
MOVE 'B' TO ENT(IX)
MOVE 'C' TO ENT(IX + 1)
```
- A subscript is a positive integer giving the occurrence number: an integer literal or a numeric elementary integer data-name (which can be qualified, not subscripted or indexed). The lowest occurrence is 1 and the highest is the OCCURS maximum.
- The number of subscripts must equal the number of dimensions, written major to minor left to right, for example `ELEMENT-THREE (2 2 1)`.
- An index-name comes from INDEXED BY; its value corresponds to an occurrence number for that dimension. Its initial value is undefined; initialise it with SET, PERFORM VARYING or SEARCH ALL.
- Using an integer or data-name subscript does not change any index of the table.
- Relative subscripting: `ENT(WS-I + 1)` or `ENT(IX + 1)`; the + or - must have a space on each side and be followed by an unsigned integer literal. It does not change the index or data-name.
- A data-name subscript works with different tables whatever their element size. An index-name can reference any table, but the element lengths of the two tables should match.

## Gotchas
- A table element must be subscripted or indexed everywhere except: the subject of SEARCH, in REDEFINES, in the KEY IS phrase, in a format 2 SORT, and in USE FOR DEBUGGING.
- Subscript `ALL` is only for intrinsic function arguments and table SORT.
- An index is valid only for values from 1 to the highest occurrence.
- To get an ordinal number from an index use `SET WS-N TO IX` (index-name to integer item is a valid SET).
- Index data items (USAGE INDEX) cannot be used as subscripts.

## Self-check
SET WS-N TO IX after SET IX TO 5; WS-N must equal 5.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted) the Subscripting section (subscripting using data-names, subscripting using index-names, relative subscripting), the SET statement format 1 (Table 52) and the SEARCH considerations. Confirmed all claims above. Removed: "the compiler multiplies by entry size every time", "an index is stored as a byte displacement (IBM)", "fastest" and "an index cannot be MOVEd to or DISPLAYed directly" (none stated in the Language Reference), "different indexes for different tables" as an absolute rule (IBM says an index-name can reference any table when element lengths match), and the unread ISO, ibm.com/docs root and GnuCOBOL sources.
Method: documentation only; no commands were run.
