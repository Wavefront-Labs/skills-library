---
id: computing-software.software-engineering.cobol.value-clause-init
name: value-clause-init
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, value-clause-init, cobol-storage-sections, initialize-statement, value-clause, default-initialization]
level: practitioner
status: docs-checked
description: "Initialize items once with VALUE and repeatedly with INITIALIZE (REPLACING by category, WITH FILLER, TO VALUE) in Enterprise COBOL."
sources:
  - https://publibfp.dhe.ibm.com/epubs/pdf/igy6lr40.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VALUE clause and INITIALIZE statement
**Goal:** reset data reliably (Enterprise COBOL for z/OS 6.4).

```cobol
INITIALIZE WS-REC
INITIALIZE WS-REC REPLACING NUMERIC DATA BY 0
                            ALPHANUMERIC DATA BY SPACES
INITIALIZE WS-TABLE WITH FILLER ALL TO VALUE
```
- Plain `INITIALIZE` (no REPLACING or VALUE phrase) behaves like implicit MOVEs: SPACE to alphabetic, alphanumeric, alphanumeric-edited, DBCS, national, national-edited and UTF-8 items, ZERO to numeric and numeric-edited items.
- Elementary FILLER items are skipped unless `WITH FILLER` is given. Items with REDEFINES or RENAMES (and items under a REDEFINES) are never receivers.
- `REPLACING category DATA BY value` overrides the value for that category; a category cannot repeat. `TO VALUE` sets items that have a VALUE clause to it (`ALL TO VALUE` covers every category); `THEN TO DEFAULT` sets the rest to the default.
- You cannot INITIALIZE a variably-located or variable-length item (one involving OCCURS DEPENDING ON). A whole table is initialized only by naming a group that contains it; identifier-1 cannot be a RENAMES item or a dynamic-length elementary item.
- `VALUE` sets the initial content when the program enters its initial state (first call, after CANCEL, every call if INITIAL; every invocation for LOCAL-STORAGE). Without VALUE the initial content is undefined (unpredictable).
- A VALUE on an item with or under OCCURS applies to every occurrence; a group-level VALUE fills the group without regard to subordinates and then forbids VALUE on them.
- Editing characters in a PICTURE do not change how the VALUE literal is read: for `PIC +999.99` the literal is `"+012.34"`.

## Gotchas
- `MOVE SPACES TO group` (a group move, no conversion) leaves invalid data in numeric subfields; INITIALIZE respects each elementary category (see packed-decimal-layout).
- A numeric VALUE must fit the PICTURE range (exceptions for COMP-5 and TRUNC(BIN) binary items).

## Self-check
After INITIALIZE, every numeric field in the record passes an `IS NUMERIC` test.

## Checked
2026-11-08. Confirmed against the Enterprise COBOL for z/OS 6.4 Language Reference (INITIALIZE statement and INITIALIZE statement rules; VALUE clause; group moves). Removed: "OCCURS DEPENDING ON counters are normally left alone" (the manual instead forbids initializing variable-length items), "hot loop expense" performance claim, and the ISO and GnuCOBOL sources.
Method: documentation only; no commands were run.
