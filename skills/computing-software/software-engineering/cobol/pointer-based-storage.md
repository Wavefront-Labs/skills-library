---
id: computing-software.software-engineering.cobol.pointer-based-storage
name: pointer-based-storage
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, pointer-based-storage, cobol-pointers-memory, usage-pointer, set-address-of, based-storage, allocate-free]
level: advanced
status: docs-checked
description: "Address storage dynamically with pointers, linkage overlays, BASED items and ALLOCATE/FREE."
sources:
  - https://gnucobol.sourceforge.io/HTML/gnucobpg.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# USAGE POINTER, BASED items, SET ADDRESS OF and ALLOCATE (GnuCOBOL)
**Goal:** safe use of dynamic structures.
```cobol
01 WS-PTR  USAGE POINTER.
LINKAGE SECTION.
01 LK-REC.  05 LK-ID PIC 9(6).
...
ALLOCATE 1000 CHARACTERS INITIALIZED RETURNING WS-PTR
SET ADDRESS OF LK-REC TO WS-PTR
FREE WS-PTR
```
- `USAGE POINTER` holds an address (32 or 64 bits); it has no PICTURE and stores a native binary integer.
- `ALLOCATE My-01-Item` allocates storage for a BASED 01 item and makes that the item's base address. `ALLOCATE n CHARACTERS [INITIALIZED] RETURNING pointer` allocates by size (INITIALIZED sets the block to binary zeros), then `SET ADDRESS OF item TO pointer` overlays an item. A LINKAGE item can be used this way without BASED.
- With `RETURNING`, the program remembers the requested size for a later `FREE`.
- `ALLOCATE` accepts either an item or `expression CHARACTERS`, not both in one statement.

## Gotchas
- Referencing a BASED item before `ALLOCATE` or after `FREE` gives unpredictable results; in practice the program aborts.

## Self-check
Allocate, write, free, and make sure no later statement touches the item.

## Checked
2026-11-02. Checked against the GnuCOBOL Programmer's Guide (ALLOCATE, FREE, USAGE POINTER). Removed: IBM Enterprise COBOL and LE (CEEGTST/CEEFRST) statements, pointer arithmetic claims (`SET ptr UP BY`), the `IF ptr = NULL` comparison, the dangling-pointer and z/OS addressing-mode remarks, and the ISO 2002 attribution.

Method: documentation only; no commands were run.
