---
id: computing-software.software-engineering.cobol.search-linear
name: search-linear
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, search-linear, cobol-tables, search-statement, linear-search, at-end-search]
level: practitioner
status: docs-checked
description: "Look up entries with serial SEARCH, setting the index first and handling the not-found branch."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SEARCH (linear) with WHEN and AT END
**Goal:** a correct lookup with a defined not-found path (Enterprise COBOL for z/OS 6.4 wording).

```cobol
SET IX TO 1
SEARCH ENT
    AT END
        MOVE 'N' TO FOUND-SW
    WHEN ENT-KEY(IX) = WS-WANTED
        MOVE 'Y' TO FOUND-SW
END-SEARCH
```
- Use the serial form (format 1) for an unsorted table, or for a sorted table when you want to go through it serially or control subscripts or indexes.
- The search starts at the current value of the search index, so set it first (and set the index of each superordinate dimension of a multidimensional table).
- The WHEN conditions are tested in the order written; when one is true the search stops, its imperative runs and the index points at that element. The index is raised to the next element when none is true.
- `SEARCH ENT VARYING OTHER-IX`: if OTHER-IX is an index of another table it is increased by the same amount as the search index; if it is an index data item it is increased with it; if it is an elementary integer item it is increased by 1 each step.
- The table needs an OCCURS clause and should have INDEXED BY.
- The subject cannot be subscripted or reference-modified.

## Gotchas
- Skipping the SET makes a repeat lookup start wherever the index was left.
- If the index is already greater than the highest occurrence when the search begins, it ends at once (AT END runs if given).
- SEARCH changes only the search index (and the VARYING item): to search a table of two to seven dimensions you need one SEARCH per dimension, with indexes for all dimensions in the WHEN.
- For an OCCURS DEPENDING ON table, make sure the ODO object holds the current table length before the SEARCH.
- IBM says the index value after SEARCH or PERFORM can be undefined, so re-SET it before other table work.

## Self-check
Look up a key that exists, the first entry, the last, and one that does not; all four give the expected switch values.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted) the SEARCH statement section (formats 1 and 2, AT END and WHEN, serial search, VARYING, search statement considerations) and the SET statement format 1 note on indexes after SEARCH. Confirmed all claims above. Removed: "on AT END the index points past the table" (not stated; the PDF only says the index is raised until the end is reached), "only the active count is searched" for ODO (IBM only says the ODO object must hold the current length), and the unread ISO, ibm.com/docs root and GnuCOBOL sources.
Method: documentation only; no commands were run.
