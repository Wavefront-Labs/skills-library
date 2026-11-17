---
id: computing-software.software-engineering.cobol.occurs-clause
name: occurs-clause
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, occurs-clause, cobol-data-description, occurs-depending-on, variable-length-table, indexed-by]
level: practitioner
status: docs-checked
description: "Declare fixed and variable-length tables with OCCURS, including DEPENDING ON, ASCENDING KEY and INDEXED BY."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OCCURS, DEPENDING ON, INDEXED BY and KEY
**Goal:** size tables correctly and ready them for SEARCH (Enterprise COBOL for z/OS 6.4 wording).

```cobol
01 PRICE-TABLE.
   05 PRICE-COUNT PIC 9(4) COMP.
   05 PRICE-ENTRY OCCURS 1 TO 500 TIMES DEPENDING ON PRICE-COUNT
        ASCENDING KEY IS PRICE-SKU
        INDEXED BY PX.
      10 PRICE-SKU PIC X(10).
      10 PRICE-AMT PIC 9(5)V99 COMP-3.
```
- Fixed: `OCCURS integer TIMES`, integer greater than zero. Variable: `OCCURS min TO max TIMES DEPENDING ON counter`; max must exceed min and min can be zero. If min is omitted, 1 is assumed (and TO is omitted); IBM warns about that omission under RULES(NOOMITODOMIN).
- The element length is fixed; only the number of repetitions varies. The ODO object must be an integer item and must not lie inside the table. The behaviour is undefined when its value is outside min..max when the item is referenced.
- OCCURS cannot be on level 01, 66, 77 or 88 items, nor on a redefined item.
- Seven subscripts or indexes are allowed, so a table has up to seven dimensions (one outermost and six nested OCCURS).
- INDEXED BY names the indexes for the table (up to 12 per entry). They are not data items and have no separate description.
- KEY IS: keys in decreasing order of significance; at most 12 per table element; total length at most 256; the data must really be in that order under the collating sequence in use. Allowed key usages include DISPLAY, NATIONAL, PACKED-DECIMAL, BINARY and the COMPUTATIONAL family; the key must be the entry itself or subordinate to it.
- `UNBOUNDED` can replace the maximum; unbounded groups are allowed only in the LINKAGE SECTION.

## Gotchas
- Unsorted keys make SEARCH ALL results unpredictable.
- In the LOCAL-STORAGE SECTION, and in WORKING-STORAGE of an IS INITIAL or class-definition program, indexes are allocated per invocation, so SET them on every entry. Otherwise indexes keep their last state when a program is reentered.
- A group with ODO used as a receiver (MOVE, READ INTO, STRING INTO and so on) uses the maximum length when the ODO object is in the same group; as a sender it uses the current count.
- Contents of occurrences beyond the ODO object value are undefined.
- Range checking of subscripts is a compiler option; look it up in the compiler documentation for your release.

## Self-check
Set the ODO counter to 3, then MOVE the group to another area: only 3 entries are sent (the ODO object is outside the group).

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted) the OCCURS clause section in full (fixed-length tables, KEY phrases, INDEXED BY phrase, variable-length tables, OCCURS DEPENDING ON clause with the maximum length rule). Confirmed all claims above. Removed: "7 in older standards, more in 2002+" (the 6.4 manual says seven), "storage is allocated for the maximum" (not stated as such), the GnuCOBOL `-debug` range checking claim, "counter must be set before use" as phrased (replaced by IBM's range rule), and the unread ISO, ibm.com/docs root and GnuCOBOL sources. Removed the SSRANGE claims (documented in the Programming Guide, not read).
Method: documentation only; no commands were run.
