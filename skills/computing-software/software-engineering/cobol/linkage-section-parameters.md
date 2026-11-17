---
id: computing-software.software-engineering.cobol.linkage-section-parameters
name: linkage-section-parameters
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, linkage-section-parameters, cobol-subprograms, procedure-division-using, entry-statement, omitted-parameter]
level: practitioner
status: draft
description: "Declare callee parameters in LINKAGE and expose alternate entry points."
sources:
  - https://www.iso.org/
  - https://www.ibm.com/docs/en/cobol-zos
  - https://gnucobol.sourceforge.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PROCEDURE DIVISION USING, RETURNING, ENTRY and OMITTED
**Goal:** a subprogram interface that matches its callers.

```cobol
LINKAGE SECTION.
01 LS-AMOUNT PIC S9(7)V99 COMP-3.
01 LS-RATE   PIC 9V9999.
PROCEDURE DIVISION USING LS-AMOUNT LS-RATE.
...
GOBACK.
ENTRY 'CALCTAX2' USING LS-AMOUNT.
```
- The USING list is positional; there is no automatic length check, so put a length field first for variable data.
- `ENTRY 'name' USING ...` defines extra callable names (obsolete in 2002+ but widely used).
- `OMITTED` can be passed by the caller; the callee tests `ADDRESS OF item = NULL`.
- Keep parameter blocks in a shared copybook used by both sides.

## Gotchas
- Passing fewer parameters than declared leaves later items pointing at garbage.
- A group passed from a caller that was reorganized without recompiling the callee breaks silently.

## Self-check
Compile caller and callee with a shared copybook and assert the same record length via `LENGTH OF` on both sides.
