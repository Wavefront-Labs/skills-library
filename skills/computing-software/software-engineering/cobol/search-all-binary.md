---
id: computing-software.software-engineering.cobol.search-all-binary
name: search-all-binary
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, search-all-binary, cobol-tables, search-all, binary-search, ascending-key]
level: advanced
status: docs-checked
description: "Use SEARCH ALL on a sorted table with ASCENDING/DESCENDING KEY and know its equality-only WHEN rule."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SEARCH ALL (binary search) and key order
**Goal:** efficient lookups on a sorted table (Enterprise COBOL for z/OS 6.4 wording).

```cobol
05 ENT OCCURS 500 ASCENDING KEY IS ENT-KEY INDEXED BY IX.
...
SEARCH ALL ENT
    AT END DISPLAY 'NOT FOUND'
    WHEN ENT-KEY(IX) = WS-WANTED
        MOVE ENT-VALUE(IX) TO WS-OUT
END-SEARCH
```
- The table needs an OCCURS clause with both INDEXED BY and a KEY IS phrase.
- The WHEN tests a key data-name for equality (`=`, `EQUAL TO`, or a condition-name with a single value), several tests joined by AND. The key must be subscripted by the first index-name of the table. The compared item (identifier, literal or arithmetic expression) must not be a key or subscripted by that index.
- If a later key is named in WHEN, all preceding keys for the table must also be named.
- The search index need not be set first; it is always the first index-name in the OCCURS clause.
- Keys cannot be floating-point items or groups with variable-occurrence items.
- Results are predictable only when the table is in ASCENDING/DESCENDING KEY order and the keys in WHEN identify a unique table element.
- You can sort a table with the format 2 SORT statement.

## Gotchas
- An unsorted table, or non-unique keys, makes the result unpredictable.
- On an unsuccessful search the final index setting is not predictable.
- OCCURS rules for keys: at most 12 keys per table element, total key length at most 256, in decreasing order of significance.
- Only one SEARCH ALL per dimension: for a multidimensional table SET the superordinate indexes first.

## Self-check
Binary-search every key in the table; each hit must return its own row.

## Checked
Date: 2026-11-08. Read in the Enterprise COBOL for z/OS 6.4 Language Reference PDF (text-extracted) the SEARCH statement section (format 2, binary search, WHEN phrase) and the OCCURS clause section (ASCENDING KEY and DESCENDING KEY phrases). Confirmed all claims above. Removed: "O(log n)" (not stated by IBM), "duplicate keys: which match is returned is unspecified" (replaced with IBM's wording that results are predictable only when keys give a unique reference), "SORT on table is a 2002+ feature" (replaced with IBM's statement that format 2 SORT sorts a table), "the active DEPENDING ON count is searched" (not stated), and the unread ISO, ibm.com/docs root and GnuCOBOL sources.
Method: documentation only; no commands were run.
