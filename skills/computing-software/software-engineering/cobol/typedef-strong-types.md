---
id: computing-software.software-engineering.cobol.typedef-strong-types
name: typedef-strong-types
category: computing-software
field: software-engineering
product: cobol
tags: [cobol, typedef-strong-types, cobol-modern-features, typedef-clause, constant-entry, strong-types]
level: advanced
status: draft
description: "Reuse data definitions with TYPEDEF and define named constants (ISO 2002+)."
sources:
  - https://www.iso.org/
  - https://www.ibm.com/docs/en/cobol-zos
  - https://gnucobol.sourceforge.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# TYPEDEF, strongly typed data and CONSTANT
**Goal:** one definition, many uses.

```cobol
01 MONEY-T  PIC S9(9)V99 COMP-3 TYPEDEF.
01 WS-A     USAGE MONEY-T.
01 WS-B     USAGE MONEY-T.
01 MAX-ROWS CONSTANT 100.
```
- `TYPEDEF` names a type; `USAGE type-name` instantiates. `TYPEDEF STRONG` forbids implicit mixing (IBM and the standard; unconfirmed on GnuCOBOL).
- `01 name CONSTANT value` (ISO 2002; IBM 6.x; GnuCOBOL 3.x) replaces VALUE-bearing magic items.
- `CONSTANT RECORD` (GnuCOBOL) is an extension.

## Gotchas
- Older compilers (IBM 4.x, many legacy shops) do not accept TYPEDEF/CONSTANT.
- A constant cannot be a MOVE or CALL BY REFERENCE receiver.

## Self-check
Compile with `cobc -std=cobol2014` or the IBM equivalent and confirm the entries parse.
